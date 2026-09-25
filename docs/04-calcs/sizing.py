"""PowerBox sizing calculations, PBX-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles paper estimates; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P  # noqa: E402  (parameters only; build123d is not imported)

# ---------------------------------------------------------------- 1. Assumptions
# SwapCell interface v0.3 reference pack (SWC-PRC-001 v0.3, SWC-CAL-001 v0.1)
V_NOM, V_MIN, V_MAX = 46.8, 39.0, 54.6
AH_NOM = 10.0
E_NAME = V_NOM * AH_NOM          # 468 Wh nameplate
E_PACK = 466.0                   # Wh at 0.2C, nominal cells (SWC-CAL-001)
E_PACK_MIN = 452.0               # Wh at 0.2C, cells at datasheet minimum
R_PACK = 0.110                   # ohm
I_CONT, I_PEAK, I_LEGACY = 20.0, 35.0, 15.0
I_CHG = 5.0                      # A, pack allowed charge current (0.5C)
I_SLEEP = 100e-6                 # A
PACK_MASS, PACK_COST = 2.85, 414.0
PACK_OVERALL = 393.0             # mm, body 340 plus handle 35 plus plug 18
CV_TIME = 0.6                    # h, CV phase at 5 A (SWC-CAL-001)
CC_END = 0.85                    # state of charge at the end of CC

SOC_MIN = 0.10                   # host discharge cut-off (R1)
ETA_CELL_CHG = 0.95              # cell charge efficiency (SWC-CAL-001)
ETA_BUCK = 0.94                  # 48 V to 12 V buck
ETA_USB = 0.93                   # USB modules from 12 V
ETA_BRICK = 0.90                 # certified grid charger
ETA_MPPT_NOM = 0.94              # charge controller, nominal
SELF_DISCHARGE = 0.025           # per month, lithium-ion at room temperature
P_READY = 0.6                    # W: ESP32 modem sleep 0.2, CAN and BMS awake 0.2, display 0.2
P_DC_IDLE = 0.4                  # W: 12 V buck and USB module quiescent draw with outputs on
INV_IDLE = 8.0                   # W, typical 48 V 300 W pure sine
INV_CURVE = [(20, 0.75), (25, 0.78), (60, 0.85), (200, 0.88), (300, 0.88)]  # typical, no datasheet yet
PSH, SOLAR_DERATE = 4.5, 0.75    # peak sun hours, heat, dust and angle

# Buck-boost loss model for R6: fixed + proportional + conduction on the input and output paths
MPPT_FIXED, MPPT_PROP, R_IN, R_OUT = 1.2, 0.025, 0.045, 0.020

# Reference evening (PBX-REQ-001 Table 1): loads on the 12 V sockets and USB
EVE_DC, EVE_USB, EVE_HOURS = 155.0, 48.0, 5.0

rows = []


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


def inv_eta(p):
    pts = INV_CURVE
    if p <= pts[0][0]:
        return pts[0][1]
    for (p0, e0), (p1, e1) in zip(pts, pts[1:]):
        if p <= p1:
            return e0 + (e1 - e0) * (p - p0) / (p1 - p0)
    return pts[-1][1]


def mppt_eta(p_in, v_in, v_out=V_NOM):
    i_in, i_out = p_in / v_in, p_in / v_out
    loss = MPPT_FIXED + MPPT_PROP * p_in + R_IN * i_in ** 2 + R_OUT * i_out ** 2
    return (p_in - loss) / p_in


print("PBX-CAL-001 PowerBox sizing (SwapCell interface v0.3)\n")

# ---------------------------------------------------------------- 2. Energy (R1, R2)
e_use = (1 - SOC_MIN) * E_PACK
e_use_min = (1 - SOC_MIN) * E_PACK_MIN
print(f"Pack nameplate {E_NAME:.0f} Wh; {E_PACK:.0f} Wh at 0.2C; usable 10 to 100 %: {e_use:.1f} Wh "
      f"({e_use_min:.1f} Wh with minimum cells)")
res("R1", f"{e_use:.0f} Wh usable ({e_use_min:.0f} Wh with minimum cells)", "400 Wh or more", "Met")

eve_dc = EVE_DC / ETA_BUCK
eve_usb = EVE_USB / (ETA_BUCK * ETA_USB)
eve_host = (P_READY + P_DC_IDLE) * EVE_HOURS
eve = eve_dc + eve_usb + eve_host
evenings = e_use / eve
print(f"Evening: DC {eve_dc:.1f} + USB {eve_usb:.1f} + host and idle {eve_host:.1f} = {eve:.1f} Wh from the pack")
print(f"Evenings per pack: {evenings:.2f} (minimum cells {e_use_min / eve:.2f})")
soc_needed = 1 - 2 * eve / E_PACK
e5 = 0.95 * E_PACK
print(f"Two evenings need {2 * eve:.1f} Wh: cut-off {soc_needed * 100:.1f} % SoC; "
      f"at 5 % cut-off {e5:.1f} Wh gives {e5 / eve:.2f} evenings; "
      f"at 10 % cut-off the profile must fall to {e_use / 2:.1f} Wh from the pack "
      f"(about {e_use / 2 / eve * 203:.0f} Wh at the loads)")
res("R2", f"{evenings:.2f} evenings ({eve:.0f} Wh per evening from the pack)", "2 evenings", "Not met")

# ---------------------------------------------------------------- 3. Charging (R3, R4, R5, R6)
res("R3", "DC in 12 to 60 V 200 W MPPT; charger in; pack swap; SunSpoke panel on DC in", "Four sources", "Met (design review)")

cc_h = (CC_END - SOC_MIN) * AH_NOM / I_CHG
t_grid = cc_h + CV_TIME
e_term = e_use / ETA_CELL_CHG
e_wall = e_term / ETA_BRICK + P_READY * t_grid
p_wall_peak = V_MAX * I_CHG / ETA_BRICK
print(f"\nGrid, 10 to 100 %: CC {cc_h:.2f} h + CV {CV_TIME} h = {t_grid:.1f} h; {e_term:.0f} Wh at the pack terminals; "
      f"{e_wall:.0f} Wh from the wall; peak wall power {p_wall_peak:.0f} W")
res("R4", f"{t_grid:.1f} h", "3 h or less", "Met")


def solar_day(panel_w):
    return panel_w * PSH * SOLAR_DERATE * ETA_MPPT_NOM


s200, s100 = solar_day(200), solar_day(100)
psh_full = e_term / (200 * SOLAR_DERATE * ETA_MPPT_NOM)
print(f"Solar 200 W: {s200:.0f} Wh per clear day at the pack terminals ({s200 * ETA_CELL_CHG:.0f} Wh stored); "
      f"10 to 100 % needs {e_term:.0f} Wh = {psh_full:.2f} peak sun hours = {psh_full / PSH:.2f} day")
print(f"Solar 100 W (SunSpoke panel): {s100:.0f} Wh per clear day; one evening ({eve:.0f} Wh from the pack) "
      f"needs {eve / ETA_CELL_CHG / s100:.2f} day")
res("R5", f"{s200:.0f} Wh per clear day; full in {psh_full / PSH:.2f} day", "Full in one clear day", "Met")

print("\nCharge controller efficiency (loss model, no datasheet yet):")
worst = 1.0
for v in (12.0, 18.0, 36.0):
    line = []
    for pw in (40.0, 100.0, 200.0):
        e = mppt_eta(pw, v)
        worst = min(worst, e)
        line.append(f"{pw:.0f} W {e * 100:.1f} %")
    print(f"  Vin {v:4.0f} V: " + ", ".join(line))
print(f"  worst case {worst * 100:.1f} % (12 V, 200 W, {200 / 12:.1f} A input)")
res("R6", f"{worst * 100:.1f} % worst case (model); MPPT stability not analysed",
    "90 % or more from 40 to 200 W; stable MPPT", "At risk")

# ---------------------------------------------------------------- 4. Outputs and currents (R7)
usb_w = 100 + 60 + 2 * 12
bus12 = 10 * 12 + usb_w / ETA_USB
print(f"\n12 V bus full demand: sockets 120 W + USB {usb_w} W / {ETA_USB} = {bus12:.0f} W = {bus12 / 12:.1f} A "
      f"(TRL 2 buck was 20 A = 240 W; resized to 30 A = 360 W)")
p_ac = 300.0
p_dc = 100.0          # rest of the 400 W total output limit
pin_ac = p_ac / inv_eta(p_ac)
pin_dc = p_dc / ETA_BUCK
p_host = P_READY + P_DC_IDLE
i_cont = (pin_ac + pin_dc + p_host) / V_MIN
pin_surge = 600 / 0.85
i_surge = (pin_surge + pin_dc + p_host) / V_MIN
print(f"Pack current at 400 W output: AC {pin_ac:.0f} W + DC {pin_dc:.0f} W + host {p_host:.1f} W at {V_MIN} V = {i_cont:.1f} A "
      f"(limit {I_CONT:.0f} A); inverter surge 600 W for 1 s: {i_surge:.1f} A (peak limit {I_PEAK:.0f} A for 10 s)")
sag = i_cont * R_PACK
print(f"Pack sag at {i_cont:.1f} A: {sag:.2f} V; pack I2R {i_cont ** 2 * R_PACK:.1f} W")
res("R7", f"Outputs as specified; 12 V buck 30 A for {bus12 / 12:.1f} A demand; pack {i_cont:.1f} A at 400 W",
    "Output set in R7, 400 W total", "Met (design review)")

# Fuses and breaker
i_inv = pin_ac / V_MIN
i_inv_surge = pin_surge / V_MIN
i_buck_in = 360 / ETA_BUCK / V_MIN
i_dcin = 200 / 12
i_ctrl_out = 200 * ETA_MPPT_NOM / V_MIN
i_usbc1, i_usbc2, i_usba = 100 / ETA_USB / 12, 60 / ETA_USB / 12, 24 / ETA_USB / 12
print(f"\nFuses: main 30 A (continuous {i_cont:.1f} A, surge {i_surge:.1f} A); inverter breaker 20 A "
      f"(continuous {i_inv:.1f} A, surge {i_inv_surge:.1f} A); buck input 15 A ({i_buck_in:.1f} A); "
      f"DC in 20 A ({i_dcin:.1f} A at 12 V); controller output 10 A ({i_ctrl_out:.1f} A); "
      f"USB-C 10 A ({i_usbc1:.1f} A), 7.5 A ({i_usbc2:.1f} A), USB-A 5 A ({i_usba:.1f} A)")
i_short = V_MAX / R_PACK
print(f"Prospective short-circuit current from the pack: about {i_short:.0f} A, so fuses need 60 V DC and 1 kA ratings")
wire_r = 3.28e-3  # ohm per m, 10 AWG
print(f"10 AWG drop over a 0.6 m loop at {i_cont:.1f} A: {i_cont * wire_r * 0.6 * 1000:.0f} mV")

# Pre-charge
c_host, r_pack_pre = 1000e-6, 100.0
c_inv, r_pre = 2200e-6, 47.0
tau_h = c_host * r_pack_pre
tau_i = c_inv * r_pre
e_pre = 0.5 * c_inv * V_MAX ** 2
print(f"Pre-charge: host and buck {c_host * 1e6:.0f} uF through the pack's 100 ohm, 99 % in {tau_h * math.log(100) * 1000:.0f} ms; "
      f"inverter {c_inv * 1e6:.0f} uF through 47 ohm, tau {tau_i * 1000:.0f} ms, 99 % in {tau_i * math.log(100) * 1000:.0f} ms, "
      f"{e_pre:.1f} J in the resistor, peak {V_MAX / r_pre:.2f} A")

# ---------------------------------------------------------------- 5. Station mode (SwapCell v0.3 item C)
p_ctrl_max = 200 * ETA_MPPT_NOM
i_net_max = p_ctrl_max / 42.0
p_router = 12 / ETA_BUCK
i_net_typ = (200 * SOLAR_DERATE * ETA_MPPT_NOM - p_router) / V_NOM
print(f"\nStation mode 4: worst net charge (200 W, no load, 42 V pack) {i_net_max:.2f} A; "
      f"typical clear day with the router {i_net_typ:.2f} A; limit {I_CHG:.1f} A")
print("With the grid charger (5 A fixed) connected, the host limits the MPPT output to the load current, "
      "so net charge stays at or below 5.0 A")

# ---------------------------------------------------------------- 6. Standby (R8)
sleep_wh_month = I_SLEEP * V_NOM * 730
off_pct = SELF_DISCHARGE * 100 + sleep_wh_month / E_PACK * 100
ready_day = P_READY * 24
inv_idle_day = INV_IDLE * 24
autooff = INV_IDLE * 10 / 60
print(f"\nOff: self-discharge {SELF_DISCHARGE * 100:.1f} % + BMS sleep {sleep_wh_month:.2f} Wh "
      f"({sleep_wh_month / E_PACK * 100:.2f} %) = {off_pct:.1f} % per month")
print(f"Ready {P_READY} W = {ready_day:.1f} Wh per day; DC outputs on, no load {P_READY + P_DC_IDLE:.1f} W")
print(f"Inverter idle left on {inv_idle_day:.0f} Wh per day ({inv_idle_day / e_use * 100:.0f} % of usable); "
      f"auto-off after 10 min wastes {autooff:.1f} Wh per event")
res("R8", f"Off {off_pct:.1f} %/month; ready {P_READY} W; inverter auto-off", "5 %/month; 1.0 W; auto-off", "Met")

# Wake through the INTERLOCK loop (SwapCell v0.3 item W)
v_node = 3.3 * 10 / (100 + 10)
print(f"INTERLOCK node with the 10 kOhm coding resistor: {v_node:.2f} V (pack window 0.24 to 0.37 V); "
      f"wake button open: 3.30 V; release gives the falling edge below 1.0 V")

# ---------------------------------------------------------------- 7. Safety limits (R9)
res("R9", f"No AC inlet; DC bus {V_MAX} V; RCD needs bonded inverter neutral", "No back-feed path; 60 V or less",
    "Met (design review)")

# ---------------------------------------------------------------- 8. Thermal
q_inv = pin_ac - p_ac
q_buck = pin_dc - p_dc
q_ctrl = 200 * (1 - ETA_MPPT_NOM)
q_tot = q_inv + q_buck + q_ctrl + p_host
fan_eff = 16.0 * 0.5 / 1000     # m3/s: 16 L/s free air, half through filter and grilles
dt_air = q_tot / (1.2 * 1005 * fan_eff)
L, D, H = P["case_l"] / 1000, P["case_d"] / 1000, P["case_h"] / 1000
area = 2 * (L * D + L * H + D * H)
ua = 9.0 * area
q_eve = (eve - (EVE_DC + EVE_USB)) / EVE_HOURS
print(f"\nHeat at full output while charging: inverter {q_inv:.0f} W + buck {q_buck:.1f} W + controller {q_ctrl:.0f} W "
      f"+ host {p_host:.0f} W = {q_tot:.0f} W; air rise with the fan {dt_air:.1f} K")
print(f"Fan off, evening losses {q_eve:.1f} W over UA {ua:.1f} W/K (area {area:.3f} m2): rise {q_eve / ua:.1f} K")
print(f"Pack I2R at 5 A charge {I_CHG ** 2 * R_PACK:.2f} W")

# ---------------------------------------------------------------- 9. Mass and size (R10)
t_m = P["sheet_t"] / 1000
rho = 2700
m_body = (L * D + 2 * L * H + 2 * D * H) * t_m * rho
m_lid = (L * D + 2 * (L + D) * P["lid_h"] / 1000) * t_m * rho
mass = {"SwapCell pack": PACK_MASS, "Enclosure body": m_body, "Lid": m_lid, "Handle": 0.20,
        "Inverter": 1.20, "Bay, runners, receptacle": 0.40, "Charge controller": 0.30, "DC-DC 30 A": 0.35,
        "Panels, sockets, outlet": 0.40, "Wiring and fuses": 0.60, "Fan, host, display": 0.30, "Door and hardware": 0.15}
m_tot = sum(mass.values())
print("\nMass budget (kg): " + ", ".join(f"{k} {v:.2f}" for k, v in mass.items()))
print(f"Total {m_tot:.2f} kg ({m_tot * 2.2046:.1f} lb); grid charger brick about 0.8 kg extra")
ovl = P["case_l"] + 18 + 4                        # input connectors 18 mm proud on +X, fan grille 4 mm on -X
ovd = P["case_d"] + 16
ovh = P["case_h"] + P["lid_h"] + P["handle_post_h"] + 4 + P["handle_r"]
print(f"Overall {ovl:.0f} x {ovd:.0f} x {ovh:.0f} mm (model bounding box 482.0 x 276.0 x 278.0); "
      f"pack bay length needed {PACK_OVERALL:.0f} + 22 receptacle + 8 clear = {PACK_OVERALL + 30:.0f} mm "
      f"of {P['case_l'] - 2 * P['sheet_t']:.0f} mm inside")
res("R10", f"{m_tot:.1f} kg; {ovl:.0f} x {ovd:.0f} x {ovh:.0f} mm", "10 kg; 500 x 300 x 280 mm", "Met")

# ---------------------------------------------------------------- 10. Cost (R11)
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
total = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
no_brick = total - 50.0
print(f"\nBOM: {len(bom)} lines, total ${total:.2f} excluding the SwapCell pack; budget $450; margin ${450 - total:.2f}")
print(f"Without the grid charger (dock on hand) ${no_brick:.2f}; with one pack (reference only) ${total + PACK_COST:.2f}")
res("R11", f"${total:.0f} excluding the pack", "$450 or less", "At risk" if 450 - total < 20 else "Met")

# ---------------------------------------------------------------- 11. Swap and display (R12)
res("R12", "Door, runners and class D catch allow a one-hand swap; display reads PACK_STATUS and PACK_LIMITS",
    "30 s swap; status display", "Not verifiable at TRL 3")

# ---------------------------------------------------------------- Runtime table
print("\nRuntime on one full pack:")
single = [("Router", 12 / ETA_BUCK), ("Three LED bulbs", 15 / ETA_BUCK), ("Radio", 5 / ETA_BUCK),
          ("Laptop 45 W USB-C", 45 / (ETA_BUCK * ETA_USB)), ("TV 60 W AC", 60 / inv_eta(60)),
          ("Desk fan 25 W AC", 25 / inv_eta(25)), ("300 W AC", 300 / inv_eta(300))]
for name, pw in single:
    print(f"  {name:20s} {pw:6.1f} W from the pack, {e_use / pw:5.1f} h")
phone = 12 / (ETA_BUCK * ETA_USB)
print(f"  Phone charge 12 Wh: {phone:.1f} Wh from the pack, {e_use / phone:.0f} charges")

# Flow figure (per usable cycle, DC input to loads, evening profile mix)
f_in = e_term / ETA_MPPT_NOM
f_loads = e_use * (EVE_DC + EVE_USB) / eve
print(f"\nFlow: DC input {f_in:.0f} Wh, controller out {e_term:.0f} Wh, usable {e_use:.0f} Wh, loads {f_loads:.0f} Wh; "
      f"losses {f_in - e_term:.0f}, {e_term - e_use:.0f}, {e_use - f_loads:.0f} Wh")

with (Path(__file__).parent / "results.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
print("\nwrote docs/04-calcs/results.csv")
for r in rows:
    print(" | ".join(r))
