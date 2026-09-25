"""PowerBox parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the main envelopes.

Massing-plus detail: correct interfaces (SwapCell interface v0.3 pack envelope, plug,
handle zone, latch pawl and guide faces) and main dimensions; not fabrication detail.

Axes: X along the case length (the pack slides in from the +X end, connector first toward -X),
Y front (-Y, output panel) to back (+Y), Z up. Units mm. The SwapCell pack lies on one of its
guide faces, with its back (latch) face toward the front of the case and its lid face toward
the back wall.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Case (PBX-PRC-001 v0.4, R10)
    "case_l": 460.0, "case_d": 260.0, "case_h": 220.0,
    "sheet_t": 1.2,            # folded aluminium tub and lid
    "lid_h": 12.0,             # lid skirt height
    "handle_post_h": 30.0, "handle_r": 12.0, "handle_span": 200.0,
    # SwapCell interface v0.3 envelope (SWC-PRC-001 v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0, "grip_clear": 25.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    "guide_clear": 1.0,
    # Pack position in the case
    "pack_x0": -155.0,         # connector face
    "pack_y_lid": 116.0,       # lid face (back of the pack), 10 mm from the back wall
    "pack_z0": 10.0,           # lower guide face, on the floor runners
    # Bay
    "shelf_z": 106.0, "shelf_t": 4.0,
    "divider_t": 6.0,          # catch bracket carrying the class D latch catch
    "door_t": 6.0,
    # Electronics envelopes (L x D x H)
    "inverter": (222.0, 100.0, 70.0),   # 300 W, 48 V input
    "dcdc": (110.0, 65.0, 40.0),        # 48 V to 12 V, 30 A
    "controller": (150.0, 96.0, 38.0),  # buck-boost MPPT with heat sink
    "host": (90.0, 65.0, 20.0),
    "fan": 80.0,
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def pack_frame(p=PARAMS):
    """Return the pack's key coordinates in the case frame."""
    x0 = p["pack_x0"]; x1 = x0 + p["pack_l"]
    y1 = p["pack_y_lid"]; y0 = y1 - p["pack_d"]          # y0 is the back (latch) face
    z0 = p["pack_z0"]; z1 = z0 + p["pack_w"]
    yc = (y0 + y1) / 2 - p["plug_offset"]                 # plug 8 mm toward the back face
    zc = (z0 + z1) / 2
    return x0, x1, y0, y1, z0, z1, yc, zc


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Cylinder, Pos, Rot
    b = _box
    L, D, H, t = p["case_l"], p["case_d"], p["case_h"], p["sheet_t"]
    x0, x1, y0, y1, z0, z1, yc, zc = pack_frame(p)

    # SwapCell reference pack (v0.3 envelope): body, plug, handle, latch pawl
    pack = b(x0, x1, y0, y1, z0, z1)
    pw, pd, ph = p["plug_w"], p["plug_d"], p["plug_h"]
    plug = b(x0 - ph, x0, yc - pd / 2, yc + pd / 2, zc - pw / 2, zc + pw / 2)
    hw, hd, hh = p["handle_w"], p["handle_d"], p["handle_h"]
    handle_loop = b(x1, x1 + hh, yc - hd / 2, yc + hd / 2, zc - hw / 2, zc + hw / 2) \
        - b(x1 - 1, x1 + p["grip_clear"], yc - hd, yc + hd, zc - hw / 2 + 11, zc + hw / 2 - 11)
    xl = x1 - p["latch_from_top"]
    pawl = b(xl - p["latch_h"] / 2, xl + p["latch_h"] / 2, y0 - p["latch_proud"], y0,
             zc - p["latch_w"] / 2, zc + p["latch_w"] / 2)
    pack = pack + plug + handle_loop + pawl

    # 1 Enclosure body: open-topped folded tub, pack door opening and intake slots on +X
    body = b(-L / 2, L / 2, -D / 2, D / 2, 0, H) - b(-L / 2 + t, L / 2 - t, -D / 2 + t, D / 2 - t, t, H + 1)
    body = body - b(L / 2 - t - 1, L / 2 + 1, y0 - p["latch_proud"] - 4, y1 + 5, z0 - 2, z1 + 4)
    for i in range(6):
        z = 20 + i * 12
        body = body - b(L / 2 - t - 1, L / 2 + 1, -110, -20, z, z + 5)
    for i in range(6):                                           # exhaust slots behind the fan, -X end
        z = 116 + i * 12
        body = body - b(-L / 2 - 1, -L / 2 + t + 1, -55, 15, z, z + 5)

    # 2 Lid: folded tray over the body top, exhaust slots toward the back
    lh = p["lid_h"]
    lid = b(-L / 2, L / 2, -D / 2, D / 2, H, H + lh) - b(-L / 2 + t, L / 2 - t, -D / 2 + t, D / 2 - t, H - 1, H + lh - t)
    for i in range(7):
        x = -200 + i * 14
        lid = lid - b(x, x + 6, 30, 115, H + lh - t - 1, H + lh + 1)

    # 3 Carry handle: two posts and a round grip along X
    top = H + lh
    s = p["handle_span"] / 2
    handle = (b(-s, -s + 20, -12, 12, top, top + p["handle_post_h"])
              + b(s - 20, s, -12, 12, top, top + p["handle_post_h"])
              + Pos(0, 0, top + p["handle_post_h"] + 4) * Rot(0, 90, 0) * Cylinder(p["handle_r"], 2 * s))

    # 5 Pack bay: floor runners, top guide rail under the shelf, catch bracket with class D latch catch,
    #   blind-mate receptacle on a floating mount (10 kOhm INTERLOCK coding resistor inside)
    gc = p["guide_clear"]
    div_y1 = y0 - p["latch_proud"] - 2
    runners = b(-190, L / 2 - t, y0 + 8, y0 + 20, t, z0 - gc) + b(-190, L / 2 - t, y1 - 20, y1 - 8, t, z0 - gc)
    top_rail = b(-190, L / 2 - t, yc - 10, yc + 10, z1 + gc, p["shelf_z"])
    shelf = b(-195, L / 2 - t, div_y1 - p["divider_t"], D / 2 - t, p["shelf_z"], p["shelf_z"] + p["shelf_t"])
    divider = b(xl - 40, xl + 40, div_y1 - p["divider_t"], div_y1, t, p["shelf_z"])    # catch bracket
    catch = b(xl + p["latch_h"] / 2 + 1, xl + p["latch_h"] / 2 + 9, div_y1, y0 - 1, zc - 25, zc + 25)
    rx0 = x0 - ph - 22
    receptacle = b(rx0, x0 - 0.5, yc - pd / 2 - 7, yc + pd / 2 + 7, zc - pw / 2 - 7, zc + pw / 2 + 7) \
        - b(x0 - ph - 0.5, x0, yc - pd / 2 - 0.5, yc + pd / 2 + 0.5, zc - pw / 2 - 0.5, zc + pw / 2 + 0.5)
    bay = runners + top_rail + shelf + divider + catch + receptacle

    # 6 Pack bay door, hinged on the +X end, with pull and padlock eye
    dt = p["door_t"]
    door = b(L / 2, L / 2 + dt, y0 - p["latch_proud"] - 6, y1 + 7, z0 - 4, z1 + 6) \
        + b(L / 2 + dt, L / 2 + dt + 8, 60, 90, zc - 10, zc + 10)

    # 7 Multi-input charge controller on the shelf (heat sink up, toward the lid exhaust)
    cl, cd, ch = p["controller"]
    sz = p["shelf_z"] + p["shelf_t"]
    charger = b(-40, -40 + cl, 22, 22 + cd, sz, sz + 8) + b(-30, -50 + cl, 30, 14 + cd, sz + 8, sz + ch)
    # 8 Host controller (ESP32, CAN, relays), on the shelf near the receptacle
    hl, hd2, hh2 = p["host"]
    host = b(-180, -180 + hl, 30, 30 + hd2, sz, sz + hh2)
    # 9 Inverter on the floor at the front
    il, idp, ih = p["inverter"]
    inverter = b(-212, -212 + il, -D / 2 + 8, -D / 2 + 8 + idp, t, t + ih)
    # 10 DC-DC converter 48 V to 12 V, 30 A
    dl, dd, dh = p["dcdc"]
    dcdc = b(40, 40 + dl, -D / 2 + 18, -D / 2 + 18 + dd, t, t + dh)

    # 11 Output panel on the front face with USB-C, USB-A, 12 V sockets, main switch and wake button
    PF = -D / 2
    panel = b(-190, 200, PF - 4, PF, 40, 195)
    sockets = b(-150, -132, PF - 8, PF - 4, 145, 155) + b(-120, -102, PF - 8, PF - 4, 145, 155)
    for x in (-85, -60):
        sockets = sockets + b(x, x + 15, PF - 8, PF - 4, 145, 152)
    for x in (-140, -90):
        sockets = sockets + Pos(x, PF - 7, 85) * Rot(90, 0, 0) * Cylinder(14, 6)
    sockets = sockets + b(-20, 5, PF - 12, PF - 4, 150, 180)                         # main switch
    sockets = sockets + Pos(30, PF - 5, 165) * Rot(90, 0, 0) * (Cylinder(8, 2) - Cylinder(5, 2))  # recessed wake button bezel
    # 12 AC outlet with 30 mA RCD
    ac = b(70, 175, PF - 16, PF - 4, 70, 170)
    # 13 Display
    display = b(-175, -95, PF - 7, PF - 4, 170, 188)
    # 14 Input panel on the +X end: DC in and charger in (Anderson PP45)
    inputs = b(L / 2, L / 2 + 4, -115, -15, 120, 195)
    for y in (-100, -55):
        inputs = inputs + b(L / 2 + 4, L / 2 + 18, y, y + 30, 140, 175)
    # 15 Exhaust fan and grille on the -X end
    f = p["fan"]
    fan = b(-L / 2 + t, -L / 2 + t + 25, -60, -60 + f, 110, 110 + f) + b(-L / 2 - 4, -L / 2, -64, -56 + f, 106, 114 + f)

    return [
        ("Enclosure body", body, "#D1D5DB", 1, (0, 0, -300)),
        ("Lid with exhaust slots", lid, "#9CA3AF", 2, (0, 0, 260)),
        ("Carry handle", handle, "#374151", 3, (0, 0, 360)),
        ("SwapCell pack (reference)", pack, "#0F766E", 4, (470, 0, 0)),
        ("Pack bay and blind-mate receptacle", bay, "#6B7280", 5, (0, 0, 0)),
        ("Pack bay door", door, "#E5E7EB", 6, (680, 0, 0)),
        ("Multi-input charge controller", charger, "#D4A017", 7, (0, 0, 170)),
        ("Host controller (ESP32, CAN)", host, "#15803D", 8, (0, 0, 190)),
        ("300 W pure sine inverter", inverter, "#C2410C", 9, (70, -200, 110)),
        ("DC-DC converter, 48 V to 12 V", dcdc, "#B45309", 10, (0, -120, 80)),
        ("Output panel (USB-C PD, USB-A, 12 V)", panel, "#1F2937", 11, (0, -460, -40)),
        ("Output sockets", sockets, "#E5E7EB", None, (0, -460, -40)),
        ("AC outlet with RCD", ac, "#F3F4F6", 12, (0, -580, -40)),
        ("State-of-charge display", display, "#38BDF8", 13, (0, -560, 30)),
        ("Input panel (DC in, grid charger in)", inputs, "#991B1B", 14, (220, 0, 260)),
        ("Exhaust fan and grille", fan, "#4B5563", 15, (-120, 300, -20)),
    ]


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts if bom}
    enclosure = Compound([by[1], by[2], by[3], by[6]])
    return {
        "powerbox-assembly": Compound([s for _, s, _, _, _ in parts]),
        "powerbox-enclosure": enclosure,
        "powerbox-pack-bay": by[5],
        "swapcell-pack-reference": by[4],
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    # Clash check between main parts (volume of pairwise intersections)
    solids = [(n, s) for n, s, _, bom, _ in parts]
    worst = 0.0
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            v = (solids[i][1] & solids[j][1]).volume
            if v > 1.0:
                print(f"clash {solids[i][0]} / {solids[j][0]}: {v:.0f} mm3")
                worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
    vols = {n: s.volume for n, s, _, _, _ in parts}
    print(f"enclosure body sheet volume {vols['Enclosure body'] / 1e3:.0f} cm3, lid {vols['Lid with exhaust slots'] / 1e3:.0f} cm3")
