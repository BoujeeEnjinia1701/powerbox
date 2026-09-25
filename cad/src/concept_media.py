"""PowerBox concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the case length (pack slides in from the +X end, connector first toward -X),
Y front (-Y, output panel) to back (+Y), Z up. Units mm.
The SwapCell pack envelope (340 x 90 x 80 mm, handle zone 35 mm) follows the SwapCell
interface definition v0.2 in the swapcell-ref design precis.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

# Case envelope
L, D, H = 460.0, 260.0, 220.0    # length (X), depth (Y), body height (Z)
T = 4.0                           # wall thickness
LID_T = 12.0

def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

# SwapCell pack (reference part, 340 x 90 x 80 mm), lying along X at the back of the case
PK_Y0, PK_Y1 = 20.0, 110.0
PK_Z0, PK_Z1 = 10.0, 90.0
PK_X0 = -155.0                    # connector face
PK_X1 = PK_X0 + 340.0             # top end (handle end), 185
pack_body = box(PK_X0, PK_X1, PK_Y0, PK_Y1, PK_Z0, PK_Z1)
pack_handle = box(PK_X1, PK_X1 + 32, 23, 107, 39, 61) - box(PK_X1 + 6, PK_X1 + 26, 30, 100, 30, 70)
pack = pack_body + pack_handle

# 1 Enclosure body: open-topped tub with a pack door opening (+X end) and intake slots
body = box(-L / 2, L / 2, -D / 2, D / 2, 0, H) - box(-L / 2 + T, L / 2 - T, -D / 2 + T, D / 2 - T, T, H + 1)
body = body - box(L / 2 - T - 1, L / 2 + 1, 14, 116, 6, 102)            # pack door opening
for i in range(6):                                                          # intake slots, +X end
    z = 20 + i * 12
    body = body - box(L / 2 - T - 1, L / 2 + 1, -110, -20, z, z + 5)

# 2 Lid with exhaust slots
lid = box(-L / 2, L / 2, -D / 2, D / 2, H, H + LID_T)
for i in range(7):
    x = -200 + i * 14
    lid = lid - box(x, x + 6, 30, 115, H - 1, H + LID_T + 1)

# 3 Carry handle: two posts and a round grip along X
handle = (box(-100, -80, -12, 12, H + LID_T, H + LID_T + 30)
          + box(80, 100, -12, 12, H + LID_T, H + LID_T + 30)
          + Pos(0, 0, H + LID_T + 34) * Rot(0, 90, 0) * Cylinder(12, 200))

# 5 Pack bay: floor, two low guide rails, blind-mate receptacle, electronics shelf above
bay = (box(-190, 222, 14, 116, T, 8)
       + box(-160, 222, 14, 18, 8, 40) + box(-160, 222, 112, 116, 8, 40)
       + box(-185, -157, 30, 100, 20, 80)
       + box(-190, 222, 14, 116, 100, 104))

# 6 Pack bay door, hinged on the +X end
door = box(L / 2, L / 2 + 6, 12, 118, 6, 104) + box(L / 2 + 6, L / 2 + 14, 50, 80, 45, 65)

# 7 Multi-input charge controller board (buck-boost MPPT with heat sink), on the shelf
charger = box(-40, 110, 22, 118, 104, 112) + box(-30, 100, 30, 110, 112, 142)
# 8 Host controller (ESP32, CAN, relays)
host = box(-175, -85, 30, 95, 104, 124)
# 9 Inverter, 300 W pure sine, front half on the floor
inverter = box(-212, 10, -122, -22, T, 74)
# 10 DC-DC converter, 48 V to 12 V
dcdc = box(40, 140, -112, -52, T, 40)

# 11 Output panel on the front face with USB-C, USB-A and 12 V sockets
PF = -D / 2                                                                  # front face Y
panel = box(-190, 200, PF - 4, PF, 40, 195)
sockets = box(-150, -132, PF - 8, PF - 4, 145, 155) + box(-120, -102, PF - 8, PF - 4, 145, 155)  # USB-C PD
for x in (-85, -60):                                                                             # USB-A
    sockets = sockets + box(x, x + 15, PF - 8, PF - 4, 145, 152)
for x in (-140, -90):                                                                            # 12 V sockets
    sockets = sockets + Pos(x, PF - 7, 85) * Rot(90, 0, 0) * Cylinder(14, 6)
sockets = sockets + box(-20, 5, PF - 12, PF - 4, 150, 180)                                       # main switch

# 12 AC outlet with GFCI (RCD), right side of the panel
ac = box(70, 175, PF - 16, PF - 4, 70, 170)
# 13 State-of-charge display, top left of the panel
display = box(-175, -95, PF - 7, PF - 4, 170, 188)

# 14 Input panel on the +X end: DC input (StepGen or solar) and grid charger port
inputs = box(L / 2, L / 2 + 4, -115, -15, 120, 195)
for y in (-100, -55):
    inputs = inputs + box(L / 2 + 4, L / 2 + 18, y, y + 30, 140, 175)

# 15 Exhaust fan and grille on the -X end
fan = box(-L / 2 + T, -L / 2 + T + 25, -60, 20, 110, 190) + box(-L / 2 - 4, -L / 2, -64, 24, 106, 194)

parts = [
    Part("Enclosure body", body, "#D1D5DB", 1, (0, 0, -300)),
    Part("Lid with exhaust slots", lid, "#9CA3AF", 2, (0, 0, 260)),
    Part("Carry handle", handle, "#374151", 3, (0, 0, 360)),
    Part("SwapCell pack (reference)", pack, "#0F766E", 4, (430, 0, 0)),
    Part("Pack bay and blind-mate receptacle", bay, "#6B7280", 5),
    Part("Pack bay door", door, "#E5E7EB", 6, (640, 0, 0)),
    Part("Multi-input charge controller", charger, "#D4A017", 7, (0, 0, 170)),
    Part("Host controller (ESP32, CAN)", host, "#15803D", 8, (0, 0, 190)),
    Part("300 W pure sine inverter", inverter, "#C2410C", 9, (70, -200, 110)),
    Part("DC-DC converter, 48 V to 12 V", dcdc, "#B45309", 10, (0, -120, 80)),
    Part("Output panel (USB-C PD, USB-A, 12 V)", panel, "#1F2937", 11, (0, -460, -40)),
    Part("Output sockets", sockets, "#E5E7EB", None, (0, -460, -40)),
    Part("AC outlet with GFCI", ac, "#F3F4F6", 12, (0, -580, -40)),
    Part("State-of-charge display", display, "#38BDF8", 13, (0, -560, 30)),
    Part("Input panel (DC in, grid charger in)", inputs, "#991B1B", 14, (220, 0, 260)),
    Part("Exhaust fan and grille", fan, "#4B5563", 15, (-120, 300, -20)),
]

# Context for scale: a table top and a phone lying next to the case
table = box(-420, 460, -340, 260, -30, 0)
phone = box(290, 365, -300, -145, 0, 9)
context = [Part("Table top", table, "#C8CDD3"), Part("phone", phone, "#6B7280")]

render_all(
    parts, project="PowerBox", title="Power station concept", dwg_no="PBX-DWG-010",
    key_figures=["One SwapCell pack: about 420 Wh usable (estimate)",
                 "Evening load 203 Wh: about 1.9 evenings (estimate)",
                 "Full charge: grid 2.1 h, 200 W solar 1 day, StepGen 5 to 8 h (est.)",
                 "300 W pure sine AC with GFCI; USB-C PD, USB-A, 12 V",
                 "About 482 x 276 x 278 mm overall, 8.3 kg with pack (est.)",
                 "Never connects to household wiring"],
    scale_figure=False, context=context, cut_exclude=("Carry handle",),
    flow={"title": "energy per usable cycle, DC input to loads (all values are estimates)", "unit": "Wh",
          "stages": [("Charging input", 467), ("Charge controller", 439), ("SwapCell pack", 421),
                     ("Loads (DC, USB, AC)", 382)],
          "losses": [(1, "Controller loss (est.)", 28), (2, "Cell and wiring loss (est.)", 18),
                     (3, "Output conversion (est.)", 39)]},
)
