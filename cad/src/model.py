"""PowerBox parametric model (build123d), TRL 3, constructable design (PBX-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl, prints the
                                       envelopes and the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Every component is a part that can be made by its stated process or bought, and every part
touches and is fixed to the parts next to it. build_components() returns them by key;
build_parts() groups them by BOM line for the concept media and the drawing.

Axes: X along the case length (the pack slides in from the +X end, connector first toward -X),
Y front (-Y, output panel) to back (+Y), Z up from the underside of the case floor. Units mm.
The SwapCell pack lies on one of its guide faces, with its back (latch) face toward the front
of the case and its lid face toward the back wall.
"""
import sys
from collections import namedtuple
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Case (PBX-PRC-001, R10)
    "case_l": 460.0, "case_d": 260.0, "case_h": 220.0,
    "sheet_t": 1.2,            # folded 5052 aluminium tub, lid and door
    "lid_h": 16.0,             # lid skirt height, overlapping the outside of the walls
    "lid_clear": 1.0,          # gap between the skirt and the wall (room for the rivet nut flanges)
    "lid_screw_z": 213.0,      # height of the six lid screws
    "tab_w": 15.0, "tab_top": 200.0,       # corner tabs, folded from the end walls onto the long walls
    "foot_h": 8.0, "foot_d": 20.0,         # self-adhesive rubber feet
    "handle_post_h": 30.0, "handle_r": 12.0, "handle_span": 200.0, "handle_base_t": 3.0,
    "doubler_t": 2.0,
    # SwapCell interface v0.3 envelope (SWC-PRC-001 v0.3)
    "pack_l": 340.0, "pack_w": 90.0, "pack_d": 80.0,
    "plug_w": 56.0, "plug_d": 34.0, "plug_h": 18.0, "plug_offset": 8.0,
    "handle_w": 84.0, "handle_d": 22.0, "handle_h": 35.0, "grip_clear": 25.0,
    "latch_w": 36.0, "latch_from_top": 45.0, "latch_proud": 10.0, "latch_h": 24.0,
    "guide_clear": 1.0,
    # Pack position in the case
    "pack_x0": -155.0,         # connector face
    "pack_y_lid": 116.0,       # lid face (back of the pack), 12.8 mm from the inside of the back wall
    "pack_z0": 10.0,           # lower guide face, resting on the floor runners
    # Bay
    "runner_x0": -190.0, "runner_split": 19.4,
    "runner_base": 24.0, "runner_lip": 3.0, "runner_lip_h": 15.0,
    "shelf_z": 106.0, "shelf_t": 2.0, "shelf_y0": 0.0, "shelf_x0": -195.0,
    "shelf_flange": 20.0, "shelf_front_flange": 15.0,
    "divider_t": 3.0,          # catch bracket web (3 mm folded aluminium)
    "bracket_t": 3.0,          # receptacle bracket
    "door_t": 1.2,
    "panel_t": 2.0,            # output and input panel plates
    # Electronics envelopes (L x D x H)
    "inverter": (222.0, 100.0, 70.0),   # 300 W, 48 V input
    "dcdc": (110.0, 65.0, 40.0),        # 48 V to 12 V, 30 A
    "controller": (150.0, 96.0, 38.0),  # buck-boost MPPT with heat sink
    "host": (90.0, 65.0, 20.0), "standoff": 6.0,
    "fan": 80.0,
}

Comp = namedtuple("Comp", "name shape bom kind group color explode")

COLORS = {"body": "#D1D5DB", "lid": "#9CA3AF", "handle": "#374151", "pack": "#0F766E", "bay": "#6B7280",
          "runner": "#2563EB", "rail": "#7C3AED", "shelf": "#A8A29E", "bracket": "#57534E", "catch": "#111827",
          "receptacle": "#1F2937", "door": "#E5E7EB", "hinge": "#4B5563", "charger": "#D4A017", "host": "#15803D",
          "inverter": "#C2410C", "dcdc": "#B45309", "panel": "#1F2937", "sockets": "#E5E7EB", "ac": "#F3F4F6",
          "display": "#38BDF8", "inputs": "#991B1B", "fan": "#4B5563", "filter": "#0E7490", "protection": "#BE123C",
          "fuseblock": "#9F1239", "feet": "#111827", "fix": "#111827", "doubler": "#78716C"}


# ------------------------------------------------------------------ geometry helpers
def _b3d():
    import build123d as b
    return b


def bx(x0, x1, y0, y1, z0, z1):
    b = _b3d()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def cyl(axis, c, r, a0, a1):
    """Cylinder of radius r along axis ('x', 'y' or 'z') through point c, from a0 to a1 on that axis."""
    b = _b3d()
    h = abs(a1 - a0)
    m = (a0 + a1) / 2
    x, y, z = c
    if axis == "x":
        return b.Pos(m, y, z) * b.Rot(0, 90, 0) * b.Cylinder(r, h)
    if axis == "y":
        return b.Pos(x, m, z) * b.Rot(90, 0, 0) * b.Cylinder(r, h)
    return b.Pos(x, y, m) * b.Cylinder(r, h)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def pack_frame(p=PARAMS):
    """Return the pack's key coordinates in the case frame."""
    x0 = p["pack_x0"]; x1 = x0 + p["pack_l"]
    y1 = p["pack_y_lid"]; y0 = y1 - p["pack_d"]          # y0 is the back (latch) face
    z0 = p["pack_z0"]; z1 = z0 + p["pack_w"]
    yc = (y0 + y1) / 2 - p["plug_offset"]                 # plug 8 mm toward the back face
    zc = (z0 + z1) / 2
    return x0, x1, y0, y1, z0, z1, yc, zc


def derived(p=PARAMS):
    """Named positions used by the model, the drawings and the build plan pictures."""
    L, D, H, t = p["case_l"], p["case_d"], p["case_h"], p["sheet_t"]
    x0, x1, y0, y1, z0, z1, yc, zc = pack_frame(p)
    xl = x1 - p["latch_from_top"]
    web_y1 = y0 - p["latch_proud"] - 2                    # front face of the pawl clearance, catch bracket web back face
    lid_in = L / 2 + p["lid_clear"]                       # inside face of the lid skirt (x); same rule in y
    return {
        "L": L, "D": D, "H": H, "t": t, "xin": L / 2 - t, "yin": D / 2 - t,
        "pack": (x0, x1, y0, y1, z0, z1, yc, zc), "xl": xl, "web_y1": web_y1,
        "door_open": (y0 - p["latch_proud"] - 4, y1 + 5, z0 - 2, z1 + 4),   # y0, y1, z0, z1 of the end opening
        "lid_xi": lid_in, "lid_yi": D / 2 + p["lid_clear"], "lid_top": H + t, "lid_skirt_z0": H + t - p["lid_h"],
        "shelf_top": p["shelf_z"] + p["shelf_t"], "rx0": x0 - p["plug_h"] - 22,
        "out_window": (-175.0, 185.0, 48.0, 188.0), "out_panel": (-192.0, 202.0, 36.0, 200.0),
        "in_window": (-102.0, -24.0, 130.0, 185.0), "in_panel": (-120.0, -10.0, 120.0, 195.0),
        "door": (18.5, 126.0, 2.0, 110.0),
    }


# ------------------------------------------------------------------ fixings
def _screw(axis, c, a_head, a_end, d, head_d, head_t, nut=None, nut_t=None):
    """Screw along axis through point c. The head sits outside a_head (beyond it, away from a_end);
    the shank runs to a_end. nut: position of the nut's inner face (nut outside it), or None."""
    s = 1 if a_end > a_head else -1
    shape = cyl(axis, c, head_d / 2, a_head - s * head_t, a_head) + cyl(axis, c, d / 2 - 0.25, a_head, a_end)
    if nut is not None:
        nt = nut_t or 0.8 * d
        shape += cyl(axis, c, head_d / 2 + 0.3, nut, nut + s * nt)
    return shape


def _hole(axis, c, d, a0, a1):
    return cyl(axis, c, d / 2, a0, a1)


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component as a Comp, keyed by a short name."""
    D_ = derived(p)
    L, D, H, t = D_["L"], D_["D"], D_["H"], D_["t"]
    xin, yin = D_["xin"], D_["yin"]
    x0, x1, y0, y1, z0, z1, yc, zc = D_["pack"]
    xl, wy = D_["xl"], D_["web_y1"]
    C = {}
    holes = []          # (part keys, hole solid)

    def add(key, name, shape, bom, kind, group, color, explode=(0, 0, 0)):
        C[key] = Comp(name, shape, bom, kind, group, color, explode)

    # 1 Enclosure body: one folded blank, open at the top. The end walls carry 15 mm tabs folded
    #   onto the outside of the long walls, three blind rivets each.
    body = bx(-L / 2, L / 2, -D / 2, D / 2, 0, H) - bx(-xin, xin, -yin, yin, t, H + 1)
    oy0, oy1, oz0, oz1 = D_["door_open"]
    body -= bx(xin - 1, L / 2 + 1, oy0, oy1, oz0, oz1)                                  # pack door opening, +X end
    for i in range(6):
        z = 20 + i * 12
        body -= bx(xin - 1, L / 2 + 1, -110, -20, z, z + 5)                             # intake slots, +X end
    body -= cyl("x", (0, -20, 150), 38, -L / 2 - 1, -xin + 1)                          # 76 mm exhaust hole behind the fan
    wx0, wx1, wz0, wz1 = D_["out_window"]
    body -= bx(wx0, wx1, -D / 2 - 1, -yin + 1, wz0, wz1)                               # output panel window
    iy0, iy1, iz0, iz1 = D_["in_window"]
    body -= bx(xin - 1, L / 2 + 1, iy0, iy1, iz0, iz1)                                   # input panel window
    tabs = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            xa, xb = sorted((sx * (L / 2 - p["tab_w"]), sx * L / 2))
            ya, yb = sorted((sy * D / 2, sy * (D / 2 + t)))
            tabs.append(bx(xa, xb, ya, yb, 4, p["tab_top"]))
    body += fuse(tabs)
    add("body", "Enclosure body", body, 1, "made", 1, COLORS["body"], (0, 0, -300))
    triv = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for z in (40, 100, 160):
                c = (sx * (L / 2 - p["tab_w"] / 2), 0, z)
                triv.append(_screw("y", c, sy * (D / 2 + t), sy * (yin - 2.5), 3.2, 6.4, 1.0, nut=sy * yin, nut_t=2.0))
                holes.append((("body",), _hole("y", c, 3.3, sy * (D / 2 + t + 1), sy * (yin - 1))))
    add("tab_rivets", "Corner tab rivets (12), 3.2 mm blind", fuse(triv), 18, "fixing", None, COLORS["fix"])

    # 18 rubber feet, self-adhesive, under the floor
    fh, fd = p["foot_h"], p["foot_d"]
    feet = fuse([cyl("z", (sx * 220, sy * 115, 0), fd / 2, -fh, 0) for sx in (-1, 1) for sy in (-1, 1)])
    add("feet", "Rubber feet (4)", feet, 18, "bought", 18, COLORS["feet"], (0, 0, -360))

    # 2 Lid: folded tray whose top sheet rests on the wall tops and whose 16 mm skirt hangs outside
    #   the walls with a 1 mm gap; six M4 screws through the skirt into rivet nuts in the walls.
    xo, yo = D_["lid_xi"] + t, D_["lid_yi"] + t
    lt, lz0 = D_["lid_top"], D_["lid_skirt_z0"]
    lid = bx(-xo, xo, -yo, yo, lz0, lt) - bx(-D_["lid_xi"], D_["lid_xi"], -D_["lid_yi"], D_["lid_yi"], lz0 - 1, H)
    for i in range(7):
        x = -200 + i * 14
        lid -= bx(x, x + 6, 30, 115, H - 1, lt + 1)
    add("lid", "Lid", lid, 2, "made", 2, COLORS["lid"], (0, 0, 260))
    lz = p["lid_screw_z"]
    ls = []
    for sy in (-1, 1):
        for x in (-150, 0, 150):
            yo_, yw = sy * yo, sy * D / 2
            scr = _screw("y", (x, 0, lz), yo_, sy * (yin - 8), 4.0, 7.0, 2.8)
            scr += cyl("y", (x, 0, lz), 4.5, yw, yw + sy * 0.8)                     # rivet nut flange
            scr += cyl("y", (x, 0, lz), 3.0, sy * yin, sy * (yin - 8))               # rivet nut body
            ls.append(scr)
            holes.append((("lid",), _hole("y", (x, 0, lz), 4.5, sy * (yo + 1), sy * (yo - t - 1))))
            holes.append((("body",), _hole("y", (x, 0, lz), 6.0, sy * (D / 2 + 1), sy * (yin - 1))))
    add("lid_screws", "Lid screws (6), M4 into rivet nuts", fuse(ls), 18, "fixing", None, COLORS["fix"], (0, 0, 260))

    # 3 Carry handle (bought folding handle with two base plates) and the doubler under the lid
    s = p["handle_span"] / 2
    bt = p["handle_base_t"]
    hb = bx(-s - 10, -s + 30, -12, 12, lt, lt + bt) + bx(s - 30, s + 10, -12, 12, lt, lt + bt)
    posts = bx(-s, -s + 20, -12, 12, lt + bt, lt + p["handle_post_h"]) + bx(s - 20, s, -12, 12, lt + bt, lt + p["handle_post_h"])
    gz = lt + p["handle_post_h"] + 4
    grip = cyl("x", (0, 0, gz), p["handle_r"], -s, s)
    add("handle", "Carry handle", hb + posts + grip, 3, "bought", 3, COLORS["handle"], (0, 0, 360))
    dt_ = p["doubler_t"]
    add("doubler", "Handle doubler plate", bx(-120, 120, -20, 20, H - dt_, H), 3, "made", 3, COLORS["doubler"], (0, 0, 330))
    hbolts = []
    for x in (-s - 5, -s + 25, s - 25, s + 5):
        hbolts.append(_screw("z", (x, 0, 0), lt + bt, H - dt_ - 0.5, 5.0, 9.0, 3.0, nut=H - dt_, nut_t=4.5))
        holes.append((("handle",), _hole("z", (x, 0, 0), 5.5, lt - 1, lt + bt + 1)))
        holes.append((("lid", "doubler"), _hole("z", (x, 0, 0), 5.5, H - dt_ - 1, lt + 1)))
    add("handle_bolts", "Handle bolts (4), M5 with nyloc nuts", fuse(hbolts), 18, "fixing", None, COLORS["fix"], (0, 0, 360))

    # 4 SwapCell reference pack (v0.3 envelope): body, plug, handle, latch pawl
    pack = bx(x0, x1, y0, y1, z0, z1)
    pw, pd, ph = p["plug_w"], p["plug_d"], p["plug_h"]
    plug = bx(x0 - ph, x0, yc - pd / 2, yc + pd / 2, zc - pw / 2, zc + pw / 2)
    hw, hd, hh = p["handle_w"], p["handle_d"], p["handle_h"]
    handle_loop = bx(x1, x1 + hh, yc - hd / 2, yc + hd / 2, zc - hw / 2, zc + hw / 2) \
        - bx(x1 - 1, x1 + p["grip_clear"], yc - hd, yc + hd, zc - hw / 2 + 11, zc + hw / 2 - 11)
    pawl = bx(xl - p["latch_h"] / 2, xl + p["latch_h"] / 2, y0 - p["latch_proud"], y0,
              zc - p["latch_w"] / 2, zc + p["latch_w"] / 2)
    add("pack", "SwapCell pack (reference)", pack + plug + handle_loop + pawl, 4, "reference", 4, COLORS["pack"], (470, 0, 0))

    # 5 Pack bay
    gc = p["guide_clear"]
    rb, rl, rlh = p["runner_base"], p["runner_lip"], p["runner_lip_h"]
    xr0, xs = p["runner_x0"], p["runner_split"]
    yf0 = y0 - gc - rl                     # front runner: lip outside the pack's latch face
    yb1 = y1 + gc + rl                     # back runner: lip outside the pack's lid face
    rscr = []
    for side, (ya, yb_, lipa, lipb) in (("f", (yf0, yf0 + rb, yf0, yf0 + rl)), ("b", (yb1 - rb, yb1, yb1 - rl, yb1))):
        for k, (xa, xb) in enumerate(((xr0, xs), (xs, xin))):
            r = bx(xa, xb, ya, yb_, t, z0) + bx(xa, xb, lipa, lipb, z0, z0 + rlh)
            name = ("Front" if side == "f" else "Back") + f" floor runner, {'inner' if k == 0 else 'outer'} length"
            add(f"runner_{side}{k + 1}", name, r, 5, "made", 5, COLORS["runner"], (0, 0, 0))
            ymid = (ya + yb_) / 2 + (2 if side == "f" else -2)
            for x in (xa + 25, xb - 35):
                rscr.append(_screw("z", (x, ymid, 0), 0, t + 7, 4.0, 7.6, 2.2))
                holes.append(((f"runner_{side}{k + 1}",), _hole("z", (x, ymid, 0), 5.6, t - 0.1, t + 8)))
                holes.append((("body",), _hole("z", (x, ymid, 0), 4.5, -1, t + 1)))
    add("runner_screws", "Runner screws (8), M4 from below into heat-set inserts", fuse(rscr), 18, "fixing", None, COLORS["fix"])

    # shelf: 2 mm folded sheet; rear and end flanges up, riveted to the walls; front flange down
    sz0, st = p["shelf_z"], p["shelf_t"]
    sx0, sy0, sf = p["shelf_x0"], p["shelf_y0"], p["shelf_flange"]
    sz1 = sz0 + st
    shelf = (bx(sx0, xin, sy0, yin, sz0, sz1)
             + bx(sx0, xin - st - 0.8, yin - st, yin, sz1, sz1 + sf)
             + bx(xin - st, xin, sy0, 100, sz1, sz1 + sf)
             + bx(sx0, xin, sy0, sy0 + st, sz0 - p["shelf_front_flange"], sz0))
    add("shelf", "Shelf", shelf, 5, "made", 5, COLORS["shelf"], (0, 0, 150))
    riv = []
    for x in (-150, -50, 50, 150):
        riv.append(_screw("y", (x, 0, sz1 + 10), D / 2, yin - st - 2.5, 3.2, 6.4, 1.0, nut=yin - st, nut_t=2.0))
        holes.append((("body", "shelf"), _hole("y", (x, 0, sz1 + 10), 3.3, D / 2 + 1, yin - st - 1)))
    for y in (30, 80):
        riv.append(_screw("x", (0, y, sz1 + 10), L / 2, xin - st - 2.5, 3.2, 6.4, 1.0, nut=xin - st, nut_t=2.0))
        holes.append((("body", "shelf"), _hole("x", (0, y, sz1 + 10), 3.3, L / 2 + 1, xin - st - 1)))
    add("shelf_rivets", "Shelf rivets (6), 3.2 mm blind", fuse(riv), 18, "fixing", None, COLORS["fix"])

    # top guide rail: printed, two lengths, screwed up into the shelf from above with M3 screws
    rail1 = bx(xr0, xs, yc - 10, yc + 10, z1 + gc, sz0)
    rail2 = bx(xs, xin, yc - 10, yc + 10, z1 + gc, sz0)
    add("rail_1", "Top guide rail, inner length", rail1, 5, "made", 5, COLORS["rail"])
    add("rail_2", "Top guide rail, outer length", rail2, 5, "made", 5, COLORS["rail"])
    tscr = []
    for key, xs_ in (("rail_1", (-180, -60)), ("rail_2", (140, 215))):
        for x in xs_:
            tscr.append(_screw("z", (x, yc, 0), sz1, sz0 - 3.5, 3.0, 5.6, 1.7))
            holes.append(((key,), _hole("z", (x, yc, 0), 4.0, sz0 - 4, sz0 + 0.1)))
            holes.append((("shelf",), _hole("z", (x, yc, 0), 3.4, sz0 - 1, sz1 + 1)))
    add("rail_screws", "Rail screws (4), M3 into heat-set inserts", fuse(tscr), 18, "fixing", None, COLORS["fix"])

    # catch bracket: 3 mm folded Z-section, foot screwed to the floor, top flange screwed to the shelf
    bt3 = p["divider_t"]
    cb = (bx(xl - 40, xl + 40, wy - bt3, wy, t + bt3, sz0 - bt3)
          + bx(xl - 40, xl + 40, sy0 + st, wy, t, t + bt3)
          + bx(xl - 40, xl + 40, sy0 + st, wy, sz0 - bt3, sz0))
    add("catch_bracket", "Catch bracket", cb, 5, "made", 5, COLORS["bracket"])
    catch = bx(xl + p["latch_h"] / 2 + 1, xl + p["latch_h"] / 2 + 9, wy, y0 - 1, zc - 25, zc + 25)
    add("catch", "Class D latch catch", catch, 5, "bought", 5, COLORS["catch"])
    # receptacle bracket: 3 mm folded L, foot screwed to the floor; receptacle screwed to its web
    rx0 = D_["rx0"]
    rbt = p["bracket_t"]
    rcb = bx(rx0 - rbt, rx0, yc - 31, yc + 31, t + rbt, 95) + bx(rx0 - 23, rx0, yc - 31, yc + 31, t, t + rbt)
    add("recept_bracket", "Receptacle bracket", rcb, 5, "made", 5, COLORS["bracket"])
    receptacle = bx(rx0, x0 - 0.5, yc - pd / 2 - 7, yc + pd / 2 + 7, zc - pw / 2 - 7, zc + pw / 2 + 7) \
        - bx(x0 - ph - 0.5, x0, yc - pd / 2 - 0.5, yc + pd / 2 + 0.5, zc - pw / 2 - 0.5, zc + pw / 2 + 0.5)
    add("receptacle", "SwapCell receptacle (floating mount)", receptacle, 5, "bought", 5, COLORS["receptacle"])

    # 16 protection plate (main fuse, inverter breaker, relay and pre-charge) and 6-way fuse block
    prot = (bx(-155, 55, -16, 18, t, t + 2) + bx(-140, -80, -12, 14, t + 2, 35)
            + bx(-70, -20, -12, 14, t + 2, 55) + bx(-10, 40, -12, 14, t + 2, 45))
    add("protection", "Protection plate: main fuse, breaker, relay", prot, 16, "made", 16, COLORS["protection"], (0, -40, 120))
    fb = bx(158, 216, -110, -40, t, t + 30)
    add("fuseblock", "Fuse block, 6-way", fb, 16, "bought", 16, COLORS["fuseblock"], (60, -80, 90))

    # floor fixings: M4 button head from below, nyloc nut on top (brackets, plates)
    fscr = []
    floor_fix = [("catch_bracket", xl - 25, (sy0 + st + wy - bt3) / 2, t + bt3), ("catch_bracket", xl + 25, (sy0 + st + wy - bt3) / 2, t + bt3),
                 ("recept_bracket", rx0 - 13, yc - 18, t + rbt), ("recept_bracket", rx0 - 13, yc + 18, t + rbt),
                 ("protection", -148, 1, t + 2), ("protection", 48, 1, t + 2)]
    for key, x, y, ztop in floor_fix:
        fscr.append(_screw("z", (x, y, 0), 0, ztop + 4.5, 4.0, 7.6, 2.2, nut=ztop, nut_t=4.0))
        holes.append(((key, "body"), _hole("z", (x, y, 0), 4.5, -1, ztop + 0.5)))
    for x, y in ((xl - 25, (sy0 + st + wy - bt3) / 2), (xl + 25, (sy0 + st + wy - bt3) / 2)):
        fscr.append(_screw("z", (x, y, 0), sz1, sz0 - bt3 - 4.5, 4.0, 7.6, 2.8, nut=sz0 - bt3, nut_t=4.0))
        holes.append((("catch_bracket", "shelf"), _hole("z", (x, y, 0), 4.5, sz0 - bt3 - 0.5, sz1 + 1)))
    add("floor_screws", "Bracket screws (8), M4 with nyloc nuts", fuse(fscr), 18, "fixing", None, COLORS["fix"])
    for x, y in ((163, -100), (211, -50)):                                   # fuse block screws (into its own feet)
        holes.append((("body",), _hole("z", (x, y, 0), 4.5, -1, t + 1)))
    il, idp, ih = p["inverter"]
    for x in (-200, -2):
        for y in (-D / 2 + 15, -D / 2 + 8 + idp - 7):
            holes.append((("body",), _hole("z", (x, y, 0), 4.5, -1, t + 1)))
    dl, dd, dh = p["dcdc"]
    for x in (47, 40 + dl - 7):
        for y in (-D / 2 + 25, -D / 2 + 18 + dd - 7):
            holes.append((("body",), _hole("z", (x, y, 0), 4.5, -1, t + 1)))

    # 6 Pack bay door: 1.2 mm sheet over the opening, piano hinge on its front edge, thumb-turn cam
    #   latch near its back edge, hasp tab at the top back corner over a flush staple riveted to the wall
    dy0, dy1, dz0, dz1 = D_["door"]
    dtt = p["door_t"]
    door = bx(L / 2, L / 2 + dtt, dy0, dy1, dz0, dz1) + bx(L / 2, L / 2 + dtt, 100, dy1, dz1, 142)
    door -= bx(L / 2 - 1, L / 2 + dtt + 1, 104, 122, 116, 136)          # hasp slot
    door -= cyl("x", (0, 111, 56), 9.75, L / 2 - 1, L / 2 + dtt + 1)    # latch hole
    add("door", "Pack bay door", door, 6, "made", 6, COLORS["door"], (680, 0, 0))
    kn = (L / 2 + 3.0, 15.5)
    hinge = (bx(L / 2, L / 2 + 1, 4, kn[1], dz0 + 4, dz1 - 4) + bx(L / 2 + dtt, L / 2 + dtt + 1, kn[1], 30, dz0 + 4, dz1 - 4)
             + cyl("z", (kn[0], kn[1], 0), 2.3, dz0 + 4, dz1 - 4))
    add("hinge", "Piano hinge", hinge, 6, "bought", 6, COLORS["hinge"], (680, 0, 0))
    latch = (cyl("x", (0, 111, 56), 9.5, L / 2 - 8, L / 2 + dtt) + cyl("x", (0, 111, 56), 12.0, L / 2 + dtt, L / 2 + dtt + 3)
             + bx(L / 2 + dtt + 3, L / 2 + dtt + 15, 108, 114, 46, 66) + bx(xin - 2.2, xin - 0.2, 111, 127, 51, 61)
             + cyl("x", (0, 111, 56), 4.0, xin - 2.2, L / 2 - 8))
    add("latch", "Thumb-turn cam latch", latch, 6, "bought", 6, COLORS["catch"], (680, 0, 0))
    staple = bx(L / 2, L / 2 + dtt, 106, 120, 118, 134) + (bx(L / 2 + dtt, L / 2 + 11, 110.5, 115.5, 121, 131) - bx(L / 2 + dtt + 2, L / 2 + 9, 110, 116, 123, 129))
    add("staple", "Padlock staple", staple, 6, "bought", 6, COLORS["hinge"], (680, 0, 0))
    hriv = []
    for z in (20, 56, 92):
        hriv.append(_screw("x", (0, 9.5, z), L / 2 + 1, xin - 2.5, 3.2, 6.4, 1.0, nut=xin, nut_t=2.0))
        holes.append((("hinge", "body"), _hole("x", (0, 9.5, z), 3.3, L / 2 + 1.5, xin - 1)))
        hriv.append(_screw("x", (0, 26, z), L / 2 + dtt + 1, L / 2 - 2.5, 3.2, 6.4, 1.0, nut=L / 2, nut_t=2.0))
        holes.append((("hinge", "door"), _hole("x", (0, 26, z), 3.3, L / 2 + dtt + 1.5, L / 2 - 1)))
    for y in (108, 118):
        hriv.append(_screw("x", (0, y, 126), L / 2 + dtt, xin - 2.5, 3.2, 4.4, 0.6, nut=xin, nut_t=2.0))
        holes.append((("staple", "body"), _hole("x", (0, y, 126), 3.3, L / 2 + dtt + 1, xin - 1)))
    add("door_rivets", "Hinge and staple rivets (8), 3.2 mm blind", fuse(hriv), 18, "fixing", None, COLORS["fix"], (680, 0, 0))

    # 7 charge controller on the shelf; 8 host on nylon standoffs
    cl, cd, ch = p["controller"]
    shtop = D_["shelf_top"]
    charger = bx(-40, -40 + cl, 22, 22 + cd, shtop, shtop + 8) + bx(-30, -50 + cl, 30, 14 + cd, shtop + 8, shtop + ch)
    add("charger", "Multi-input charge controller", charger, 7, "bought", 7, COLORS["charger"], (0, 0, 170))
    hl, hd2, hh2 = p["host"]
    so = p["standoff"]
    host = bx(-180, -180 + hl, 30, 30 + hd2, shtop + so, shtop + so + 1.6) + bx(-170, -110, 40, 85, shtop + so + 1.6, shtop + so + hh2)
    host += fuse([cyl("z", (x, y, 0), 3.0, shtop, shtop + so) for x in (-175, -95) for y in (35, 90)])
    add("host", "Host controller (ESP32, CAN)", host, 8, "bought", 8, COLORS["host"], (0, 0, 190))

    # 9 inverter and 10 buck converter on the floor
    add("inverter", "300 W pure sine inverter", bx(-212, -212 + il, -D / 2 + 8, -D / 2 + 8 + idp, t, t + ih), 9, "bought", 9,
        COLORS["inverter"], (70, -200, 110))
    add("dcdc", "DC-DC converter, 48 V to 12 V", bx(40, 40 + dl, -D / 2 + 18, -D / 2 + 18 + dd, t, t + dh), 10, "bought", 10,
        COLORS["dcdc"], (0, -120, 80))

    # 11 output panel: 2 mm plate over the window in the front wall, four M4 screws into rivet nuts;
    #   the bought modules sit in cut-outs in the plate, their backs through the window
    PF = -D / 2
    pt = p["panel_t"]
    PO = PF - pt
    px0, px1, pz0, pz1 = D_["out_panel"]
    plate = bx(px0, px1, PO, PF, pz0, pz1)
    mods = []          # (front shape, rear shape)

    def mod(front, rear, key):
        mods.append((key, front, rear))
    for x in (-150, -120):
        mod(bx(x, x + 18, PO - 4, PO, 145, 155), bx(x + 1, x + 17, PO, PF + 28, 146, 154), "sockets")       # USB-C PD
    for x in (-85, -60):
        mod(bx(x, x + 15, PO - 4, PO, 145, 152), bx(x + 1, x + 14, PO, PF + 25, 146, 151), "sockets")       # USB-A
    mod(cyl("y", (-140, 0, 100), 14, PO - 6, PO), cyl("y", (-140, 0, 100), 12, PO, PF + 55), "sockets")     # 12 V car socket
    mod(cyl("y", (-90, 0, 100), 8, PO - 6, PO), cyl("y", (-90, 0, 100), 6, PO, PF + 25), "sockets")         # barrel socket
    # main switch: lit rocker, snap-in, 22 x 30 mm panel hole, bezel 25 x 33 mm, body 21 mm behind the plate
    mod(bx(-20.5, 4.5, PO - 8, PO, 148.5, 181.5), bx(-19, 3, PO, PF + 21, 150, 180), "sockets")
    mod(cyl("y", (30, 0, 165), 8, PO - 2, PO) - cyl("y", (30, 0, 165), 5, PO - 3, PO + 1),
        cyl("y", (30, 0, 165), 6, PO, PF + 20), "sockets")                                                   # wake button
    mod(bx(70, 175, PO - 12, PO, 70, 170), bx(92, 152, PO, PF + 40, 90, 150), "ac")                         # AC outlet with RCD
    mod(bx(-175, -95, PO - 3, PO, 170, 188), bx(-170, -100, PO, PF + 10, 172, 186), "display")              # display
    for _, _, rear in mods:
        plate -= rear
    add("out_panel", "Output panel plate", plate, 11, "made", 11, COLORS["panel"], (0, -460, -40))
    for key, color, name, bom, ex in (("sockets", COLORS["sockets"], "Output sockets, switch and wake button", 11, (0, -460, -40)),
                                      ("ac", COLORS["ac"], "AC outlet with RCD", 12, (0, -580, -40)),
                                      ("display", COLORS["display"], "State-of-charge display", 13, (0, -560, 30))):
        add(key, name, fuse([f + r for k, f, r in mods if k == key]), bom, "bought", bom, color, ex)
    pscr = []
    for x in (-186, 196):
        for z in (80, 175):
            scr = _screw("y", (x, 0, z), PO, -yin + 8, 4.0, 7.0, 2.8)
            scr += cyl("y", (x, 0, z), 3.0, -yin, -yin + 8)
            pscr.append(scr)
            holes.append((("out_panel",), _hole("y", (x, 0, z), 4.5, PO - 1, PF + 0.1)))
            holes.append((("body",), _hole("y", (x, 0, z), 6.0, PF - 0.1, -yin + 1)))

    # 14 input panel: same construction on the +X end
    iy0p, iy1p, iz0p, iz1p = D_["in_panel"]
    XO = L / 2 + pt
    iplate = bx(L / 2, XO, iy0p, iy1p, iz0p, iz1p)
    pp = []
    for y in (-100, -55):
        front = bx(XO, XO + 14, y, y + 30, 140, 175)
        rear = bx(xin - 24, XO, y + 3, y + 27, 145, 170)
        iplate -= rear
        pp.append(front + rear)
    add("in_panel", "Input panel plate", iplate, 14, "made", 14, COLORS["panel"], (220, 0, 260))
    add("inputs", "Powerpole inputs (DC in, charger in)", fuse(pp), 14, "bought", 14, COLORS["inputs"], (220, 0, 260))
    for y in (-114, -14):
        for z in (140, 175):
            scr = _screw("x", (0, y, z), XO, xin - 8, 4.0, 7.0, 2.8)
            scr += cyl("x", (0, y, z), 3.0, xin, xin - 8)
            pscr.append(scr)
            holes.append((("in_panel",), _hole("x", (0, y, z), 4.5, XO + 1, L / 2 - 0.1)))
            holes.append((("body",), _hole("x", (0, y, z), 6.0, L / 2 + 0.1, xin - 1)))
    add("panel_screws", "Panel screws (8), M4 into rivet nuts", fuse(pscr), 18, "fixing", None, COLORS["fix"])

    # 15 fan inside the -X end and its grille outside, four M4 screws through both; printed frame
    #   holding the intake filter pad inside the +X end
    f = p["fan"]
    fan = bx(-xin, -xin + 25, -60, -60 + f, 110, 110 + f)
    grille = bx(-L / 2 - 4, -L / 2, -64, -56 + f, 106, 114 + f)
    for y in (-55.75, 15.75):
        for z in (114.25, 185.75):
            for k in ("fan", "grille"):
                holes.append(((k, "body"), _hole("x", (0, y, z), 4.5, -L / 2 - 5, -xin + 26)))
    add("fan", "Exhaust fan", fan, 15, "bought", 15, COLORS["fan"], (-120, 300, -20))
    add("grille", "Fan grille", grille, 15, "bought", 15, COLORS["fan"], (-160, 300, -20))
    ff = bx(xin - 6, xin, -118, -12, 12, 103) - bx(xin - 7, xin + 1, -110, -20, 20, 95)
    ff += bx(xin - 6, xin - 4.5, -110, -20, 20, 95) - fuse([bx(xin - 7, xin, -108 + 15 * i, -96 + 15 * i, 22, 93) for i in range(6)])
    add("filter_frame", "Intake filter frame", ff, 15, "made", 15, COLORS["filter"], (120, 0, 0))
    for y in (-114, -16):
        for z in (16, 99):
            holes.append((("filter_frame", "body"), _hole("x", (0, y, z), 3.3, xin - 7, L / 2 + 1)))

    # cut every fixing hole
    for keys, h in holes:
        for k in keys:
            c = C[k]
            C[k] = c._replace(shape=c.shape - h)
    return C


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM line with geometry,
    for the concept media and the general arrangement. Fixings are left out."""
    C = build_components(p)
    names = {1: "Enclosure body", 2: "Lid with exhaust slots", 3: "Carry handle and doubler", 4: "SwapCell pack (reference)",
             5: "Pack bay: runners, shelf, brackets, receptacle", 6: "Pack bay door, hinge and latch",
             7: "Multi-input charge controller", 8: "Host controller (ESP32, CAN)", 9: "300 W pure sine inverter",
             10: "DC-DC converter, 48 V to 12 V", 11: "Output panel (USB-C PD, USB-A, 12 V)", 12: "AC outlet with RCD",
             13: "State-of-charge display", 14: "Input panel (DC in, grid charger in)", 15: "Exhaust fan, grille and filter",
             16: "Protection plate and fuse block", 18: "Rubber feet"}
    groups, colors, ex = {}, {}, {}
    for c in C.values():
        if c.group is None:
            continue
        groups[c.group] = c.shape if c.group not in groups else groups[c.group] + c.shape
        if c.group not in colors or c.kind == "made":
            colors.setdefault(c.group, c.color)
        ex.setdefault(c.group, c.explode)
    first = {1: "body", 2: "lid", 3: "handle", 4: "pack", 5: "shelf", 6: "door", 7: "charger", 8: "host", 9: "inverter",
             10: "dcdc", 11: "out_panel", 12: "ac", 13: "display", 14: "inputs", 15: "fan", 16: "protection", 18: "feet"}
    return [(names[g], groups[g], C[first[g]].color, g, C[first[g]].explode) for g in sorted(groups)]


def assemblies(parts=None):
    from build123d import Compound
    C = build_components()
    allp = [c.shape for c in C.values()]
    enc = [c.shape for k, c in C.items() if c.group in (1, 2, 3, 6, 18) or k in ("lid_screws", "handle_bolts", "door_rivets")]
    bay = [c.shape for k, c in C.items() if c.group == 5 or k in ("runner_screws", "shelf_rivets", "rail_screws", "floor_screws")]
    return {
        "powerbox-assembly": Compound(allp),
        "powerbox-enclosure": Compound(enc),
        "powerbox-pack-bay": Compound(bay),
        "swapcell-pack-reference": Compound(C["pack"].shape.solids()),
    }


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS):
    """Pairs that must touch, or must be apart by at least a clearance (mm), plus an all-pairs
    overlap check. Returns (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda *ks: fuse([C[k].shape for k in ks])  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    # every pair of components: no overlap
    keys = list(C)
    worst = []
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            v = _vol(C[a].shape, C[b_].shape)
            if not v < 1e-2:
                worst.append((a, b_, v))
    rows.append((f"No two of the {len(keys)} components overlap" + (f" ({', '.join(f'{a}/{b}' for a, b, _ in worst)})" if worst else ""),
                 sum(v for *_, v in worst), 0.0, "touch", not worst))
    # supports and fixings: these faces must touch
    for k in ("runner_f1", "runner_f2", "runner_b1", "runner_b2", "catch_bracket", "recept_bracket", "inverter", "dcdc",
              "protection", "fuseblock"):
        chk(f"{C[k].name} on the case floor", S(k), S("body"), "touch")
    chk("Feet under the case floor", S("feet"), S("body"), "touch")
    chk("Lid top rests on the wall tops", S("lid"), S("body"), "touch")
    chk("Lid skirt clear of the walls (rivet nut flanges sit in the gap)", S("lid") - (S("lid") & bx(-300, 300, -200, 200, 219.9, 230)),
        S("body"), 0.9)
    chk("Handle base plates on the lid", S("handle"), S("lid"), "touch")
    chk("Doubler plate under the lid", S("doubler"), S("lid"), "touch")
    chk("Doubler clear of the walls", S("doubler"), S("body"), 5.0)
    chk("Pack rests on the front floor runner", S("pack"), S("runner_f1", "runner_f2"), "touch")
    chk("Pack rests on the back floor runner", S("pack"), S("runner_b1", "runner_b2"), "touch")
    chk("Pack clear of the top guide rail (1 mm)", S("pack"), S("rail_1", "rail_2"), 0.9)
    chk("Pack plug clear inside the receptacle", S("pack"), S("receptacle"), 0.4)
    chk("Pack pawl clear of the catch (seated)", S("pack"), S("catch"), 0.9)
    chk("Pack clear of the catch bracket", S("pack"), S("catch_bracket"), 1.5)
    chk("Pack handle clear of the closed door", S("pack"), S("door"), 5.0)
    chk("Pack clear of the cam latch", S("pack"), S("latch"), 5.0)
    chk("Pack clear of the shelf", S("pack"), S("shelf"), 5.0)
    # the pack slides out through the end opening (door open, the sprung catch pushed aside)
    b = _b3d()
    fixed = fuse([c.shape for k, c in C.items() if k not in ("pack", "catch", "door", "hinge", "latch", "staple", "door_rivets")
                  and not k.startswith("runner_")])
    worst = min(fixed.distance_to(b.Pos(dx, 0, 0) * C["pack"].shape) for dx in range(20, 461, 40))
    rows.append(("Pack slides out on its runners through the end opening (every 40 mm)", 0.0, worst, 0.4, worst >= 0.4 - 1e-6))
    chk("Top guide rail under the shelf", S("rail_1", "rail_2"), S("shelf"), "touch")
    chk("Shelf on the catch bracket", S("shelf"), S("catch_bracket"), "touch")
    chk("Shelf rear and end flanges against the walls", S("shelf"), S("body"), "touch")
    chk("Catch on the catch bracket web", S("catch"), S("catch_bracket"), "touch")
    chk("Receptacle on its bracket", S("receptacle"), S("recept_bracket"), "touch")
    chk("Receptacle bracket clear of the floor runners", S("recept_bracket"), S("runner_f1", "runner_b1"), 3.0)
    chk("Charge controller on the shelf", S("charger"), S("shelf"), "touch")
    chk("Host standoffs on the shelf", S("host"), S("shelf"), "touch")
    chk("Charge controller clear of the lid and doubler", S("charger"), S("lid", "doubler"), 20.0)
    chk("Host clear of the fan", S("host"), S("fan"), 10.0)
    chk("Inverter clear of the protection plate", S("inverter"), S("protection"), 3.0)
    chk("Protection plate clear of the pack and runners", S("protection"), S("pack", "runner_f1", "runner_f2"), 5.0)
    chk("Protection plate clear of the catch bracket", S("protection"), S("catch_bracket"), 5.0)
    chk("Fuse block clear of the buck converter and filter", S("fuseblock"), S("dcdc", "filter_frame"), 5.0)
    chk("Inverter clear of the buck converter", S("inverter"), S("dcdc"), 10.0)
    chk("Door on the end wall", S("door"), S("body"), "touch")
    chk("Hinge on the door and the wall", S("hinge"), S("door"), "touch")
    chk("Hinge on the wall", S("hinge"), S("body"), "touch")
    chk("Cam latch in the door", S("latch"), S("door"), "touch")
    chk("Cam latch tongue behind the wall, clear (closed)", S("latch"), S("body"), 0.1)
    chk("Padlock staple on the wall", S("staple"), S("body"), "touch")
    chk("Staple clear of the door hasp slot", S("staple"), S("door"), 0.5)
    chk("Output panel plate on the front wall", S("out_panel"), S("body"), "touch")
    chk("Output modules in the panel plate", S("sockets", "ac", "display"), S("out_panel"), "touch")
    PO_SW = -p["case_d"] / 2 - p["panel_t"]
    sw_bezel = bx(-20.5, 4.5, PO_SW - 8, PO_SW, 148.5, 181.5)
    sw_body = bx(-19, 3, PO_SW, PO_SW + 21, 150, 180)
    chk("Lit rocker switch bezel (25 x 33 mm) clear of the wake button", sw_bezel, cyl("y", (30, 0, 165), 8, PO_SW - 3, PO_SW), 10.0)
    chk("Lit rocker switch bezel clear of the display", sw_bezel, S("display"), 10.0)
    chk("Lit rocker switch body (22 x 30 mm hole) in the panel plate", sw_body, S("out_panel"), "touch")
    chk("Lit rocker switch body clear of the lid skirt and the inverter", sw_body, S("lid", "inverter"), 10.0)
    chk("Output modules clear of the front wall (through the window)", S("sockets", "ac", "display"), S("body"), 1.0)
    chk("Output module backs clear of the inverter", S("sockets", "ac", "display"), S("inverter"), 10.0)
    chk("Output module backs clear of the buck converter", S("sockets", "ac", "display"), S("dcdc"), 10.0)
    chk("Output panel clear of the lid skirt", S("out_panel", "sockets", "ac", "display"), S("lid"), 4.0)
    chk("Input panel plate on the end wall", S("in_panel"), S("body"), "touch")
    chk("Powerpole housings in the input panel plate", S("inputs"), S("in_panel"), "touch")
    chk("Powerpole housings clear of the end wall", S("inputs"), S("body"), 1.0)
    chk("Input panel clear of the door and hinge", S("in_panel", "inputs"), S("door", "hinge"), 10.0)
    chk("Fan against the end wall", S("fan"), S("body"), "touch")
    chk("Grille against the end wall", S("grille"), S("body"), "touch")
    chk("Fan clear of the shelf", S("fan"), S("shelf"), 5.0)
    chk("Filter frame against the end wall", S("filter_frame"), S("body"), "touch")
    chk("Fixings clear of the pack", S("lid_screws", "handle_bolts", "runner_screws", "shelf_rivets", "rail_screws", "floor_screws",
                                       "door_rivets", "panel_screws", "tab_rivets"), S("pack"), 1.5)
    return rows


def print_checks(p=PARAMS):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc[:70]:70s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    for name, shape in assemblies().items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:26s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    print_checks()
