"""PowerBox product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted, powder-coated aluminium case with a lid
parting line, a dark lid with rounded exhaust slots and corner screws, a folding carry handle with a
ribbed rubber grip, the output panel (USB-C PD, USB-A, 12 V car socket and barrel, rocker main
switch with a lit indicator, recessed wake button, printed port marks and an accent band), the
state-of-charge display with a lit readout, the 230 V AC outlet module with RCD test and reset
buttons and a lit status light, the Anderson Powerpole input panel, the pack bay door with a clear
window onto the SwapCell pack, a pull, hinge and padlock eye, the fan grille and rubber feet.
Inside: the SwapCell reference pack, pack bay, finned charge controller, host board, inverter,
buck converter, fan and intake filter. The grid charger brick (BOM 17) is an accessory. Context is
a compact bench top with a small folding-stand solar panel wired to the DC input and a phone on
USB-C charge.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, position and interface comes from PARAMS, pack_frame() and build_parts() in
model.py (model.py has no derived(); pack_frame() plays that role). Axes as model.py: X along the
case length (pack slides in from +X), Y front (-Y, output panel) to back, Z up, case floor at Z = 0.
Differences from model.py are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import Axis, Box, Cylinder, Plane, Pos, Rot, Solid, Sphere, Vector, fillet
from model import PARAMS, pack_frame

TITLE = "PowerBox: portable power station built around a swappable SwapCell battery"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); output panel and AC "
             "outlet on the front, input panel and pack bay door with its window on the right end, a small "
             "solar panel behind wired to the DC input and a phone charging on USB-C"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): case, lid and handle; "
             "output panel, display and AC outlet; SwapCell pack and bay door; charge controller, host, "
             "inverter, buck converter, fan; grid charger brick"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 12, "az": -70,
     "note": "Detail from the front, slightly right and above (about 12 deg elevation): the output panel with "
             "USB-C, USB-A, 12 V sockets, main switch, wake button, display and the 230 V AC outlet"},
]

# Colours (restrained product palette; kit accent)
C_BODY = "#E4E6E9"
C_LID = "#30353C"
C_PANEL = "#1F242B"
C_BEZEL = "#3A4048"
C_BLACK = "#15181C"
C_ACCENT = "#0F766E"
C_PACK = "#0F766E"
C_METAL = "#B8BEC6"
C_ALU = "#C9CED4"
C_RUBBER = "#24272B"
C_INK = "#F2F3F1"
C_LABEL = "#F4F4F2"
C_LIT = "#5EEAD4"
C_LED_G = "#22C55E"
C_WINDOW = "#DCEBF5"
C_PCB = "#166534"
C_CHIP = "#111827"
C_RELAY = "#1E3A5F"
C_PP_RED = "#B91C1C"
C_PP_BLK = "#1C1F24"
C_OUTLET = "#EEEFF0"
C_WOOD = "#C8A27A"
C_CELL = "#1B2A44"
C_FRAME = "#AEB4BB"
C_CABLE = "#2A2D31"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def b(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _pipe(points, r):
    """Round cable through `points` with spherical joints."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _par(s, axis):
    return s.edges().filter_by(axis)


def _face_edges(s, axis, last):
    f = s.faces().sort_by(axis)
    return (f[-1] if last else f[0]).edges()


def _slot_y(cx, y0, y1, w, z0, z1):
    """Stadium slot along Y, through Z."""
    r = w / 2
    h = z1 - z0
    zc = (z0 + z1) / 2
    return b(cx - r, cx + r, y0 + r, y1 - r, z0, z1) + _zcyl(cx, y0 + r, zc, r, h) + _zcyl(cx, y1 - r, zc, r, h)


def _stadium_x(xc, y, zc, w, hgt, depth):
    """Stadium (rounded rectangle, long along X) cutter of `depth` along Y centred at y."""
    r = hgt / 2
    return (b(xc - w / 2 + r, xc + w / 2 - r, y - depth / 2, y + depth / 2, zc - r, zc + r)
            + _ycyl(xc - w / 2 + r, y, zc, r, depth) + _ycyl(xc + w / 2 - r, y, zc, r, depth))


def _rbox(x0, x1, y0, y1, z0, z1, axis, radii):
    """Box with the edges parallel to `axis` rounded."""
    s = b(x0, x1, y0, y1, z0, z1)
    return _fillet_try(s, _par(s, axis), radii)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def product_parts(P=PARAMS):
    L, D, H, t = P["case_l"], P["case_d"], P["case_h"], P["sheet_t"]
    x0, x1, y0, y1, z0, z1, yc, zc = pack_frame(P)
    lh = P["lid_h"]
    PF = -D / 2
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ enclosure body (BOM 1)
    EB = (0, 0, -300)
    R = 10.0
    outer = b(-L / 2, L / 2, -D / 2, D / 2, 0, H)
    outer = _fillet_try(outer, _par(outer, Axis.Z), [R, 8.0, 6.0])
    outer = _fillet_try(outer, _face_edges(outer, Axis.Z, False), [4.0, 3.0, 2.0])
    inner = b(-L / 2 + t, L / 2 - t, -D / 2 + t, D / 2 - t, t, H + 1)
    inner = _fillet_try(inner, _par(inner, Axis.Z), [R - t, 7.0, 5.0])
    body = outer - inner
    body -= b(L / 2 - t - 1, L / 2 + 1, y0 - P["latch_proud"] - 4, y1 + 5, z0 - 2, z1 + 4)   # pack door opening
    for i in range(6):                                                                        # intake slots, +X end
        z = 20 + i * 12
        body -= Pos(L / 2 - t / 2, -65, z + 2.5) * Rot(0, 90, 0) * Box(5, 90, t + 4)
    for i in range(6):                                                                        # exhaust slots, -X end
        z = 116 + i * 12
        body -= b(-L / 2 - 1, -L / 2 + t + 1, -55, 15, z, z + 5)
    # parting line groove just under the lid joint
    gro = b(-L / 2 - 2, L / 2 + 2, -D / 2 - 2, D / 2 + 2, H - 1.4, H - 0.6)
    keep = b(-L / 2 + 0.5, L / 2 - 0.5, -D / 2 + 0.5, D / 2 - 0.5, H - 2, H)
    keep = _fillet_try(keep, _par(keep, Axis.Z), [R - 0.5, 7.0])
    body -= gro - keep
    add("Enclosure body (powder-coated aluminium)", body, C_BODY, "painted", 1, "shell", EB)

    feet = _union([_zcyl(sx * (L / 2 - 38), sy * (D / 2 - 32), -1.0, 13.0, 2.0)
                   for sx in (-1, 1) for sy in (-1, 1)])
    feet = _fillet_try(feet, _face_edges(feet, Axis.Z, False), [0.8, 0.5])
    add("Rubber feet", feet, C_RUBBER, "rubber", 18, "shell", (0, 0, -360))

    # name plate above the output panel (thin raised)
    npl = _rbox(-190, -120, PF - 0.4, PF, 203, 212, Axis.Y, [1.5, 1.0])
    add("PowerBox name plate", npl, C_ACCENT, "painted", 18, "shell", EB)
    ink = b(-186, -150, PF - 0.7, PF - 0.4, 206, 209) + b(-146, -124, PF - 0.7, PF - 0.4, 206.5, 208.5)
    add("Name plate print", ink, C_INK, "paper", 18, "shell", EB)

    # ------------------------------------------------------------ lid (BOM 2) and screws
    EL = (0, 0, 260)
    lo = b(-L / 2, L / 2, -D / 2, D / 2, H, H + lh)
    lo = _fillet_try(lo, _par(lo, Axis.Z), [R, 8.0, 6.0])
    lo = _fillet_try(lo, _face_edges(lo, Axis.Z, True), [3.0, 2.0, 1.0])
    li = b(-L / 2 + t, L / 2 - t, -D / 2 + t, D / 2 - t, H - 1, H + lh - t)
    li = _fillet_try(li, _par(li, Axis.Z), [R - t, 7.0])
    lid = lo - li
    for i in range(7):
        x = -200 + i * 14
        lid -= _slot_y(x + 3, 30, 115, 6, H + lh - t - 1, H + lh + 1)
    add("Lid with exhaust slots", lid, C_LID, "painted", 2, "shell", EL)
    top = H + lh
    scr = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (L / 2 - 16), sy * (D / 2 - 16)
            s = _zcyl(x, y, top + 0.6, 4.0, 1.2)
            s = _fillet_try(s, _face_edges(s, Axis.Z, True), [0.6, 0.3])
            s -= b(x - 2.5, x + 2.5, y - 0.5, y + 0.5, top + 0.8, top + 2)
            scr.append(s)
    add("Lid screws", _union(scr), C_METAL, "metal", 18, "shell", (0, 0, 300))

    # ------------------------------------------------------------ carry handle (BOM 3)
    EHd = (0, 0, 360)
    s_ = P["handle_span"] / 2
    ph_ = P["handle_post_h"]
    gz = top + ph_ + 4
    posts = []
    for x in (-s_ + 10, s_ - 10):
        p = b(x - 10, x + 10, -12, 12, top, gz) + _xcyl(x, 0, gz, 12.0, 20)
        p = _fillet_try(p, _par(p, Axis.Z), [4.0, 2.0])
        p = _fillet_try(p, _face_edges(p, Axis.Z, False), [1.5, 1.0])
        posts.append(p)
    add("Handle hinge posts", _union(posts), C_BLACK, "plastic", 3, "shell", EHd)
    ferr = _xcyl(-s_ + 21.5, 0, gz, 10.5, 3) + _xcyl(s_ - 21.5, 0, gz, 10.5, 3)
    add("Handle bar ferrules", ferr, C_METAL, "metal", 3, "shell", EHd)
    grip = _xcyl(0, 0, gz, P["handle_r"], 2 * s_ - 46)
    grip = _fillet_try(grip, grip.edges(), [3.0, 2.0])
    for k in range(-7, 8):
        grip -= _xcyl(k * 9.0, 0, gz, P["handle_r"] + 1, 2.0) - _xcyl(k * 9.0, 0, gz, P["handle_r"] - 0.8, 3.0)
    add("Handle grip sleeve", grip, C_RUBBER, "rubber", 3, "shell", EHd)

    # ------------------------------------------------------------ output panel (BOM 11)
    EP = (0, -460, -40)
    fp = b(-190, 200, PF - 4, PF, 40, 195)
    fp = _fillet_try(fp, _par(fp, Axis.Y), [8.0, 6.0])
    fp = _fillet_try(fp, _face_edges(fp, Axis.Y, False), [1.0, 0.6])
    add("Output panel faceplate", fp, C_PANEL, "plastic", 11, "shell", EP)
    band = b(-180, 60, PF - 4.3, PF - 4, 47, 50)
    add("Output panel accent band", band, C_ACCENT, "painted", 11, "shell", EP)

    # USB-C PD ports
    usbc = []
    for x in (-150, -120):
        bz = _rbox(x, x + 18, PF - 8, PF - 4, 145, 155, Axis.Y, [3.0, 2.0])
        bz = _fillet_try(bz, _face_edges(bz, Axis.Y, False), [0.6, 0.4])
        bz -= _stadium_x(x + 9, PF - 8, 150, 10, 3.6, 6)
        usbc.append(bz)
    add("USB-C PD ports (100 W, 60 W)", _union(usbc), C_BEZEL, "plastic", 11, "shell", EP)
    # USB-A ports with tongues
    usba, tongues = [], []
    for x in (-85, -60):
        bz = _rbox(x, x + 15, PF - 8, PF - 4, 145, 152, Axis.Y, [1.2, 0.8])
        bz -= b(x + 1.8, x + 13.2, PF - 9, PF - 5, 146.5, 150.5)
        usba.append(bz)
        tongues.append(b(x + 2.5, x + 12.5, PF - 7.5, PF - 5, 146.5, 148.3))
    add("USB-A ports", _union(usba), C_METAL, "metal", 11, "shell", EP)
    add("USB-A port tongues", _union(tongues), C_ACCENT, "plastic", 11, "shell", EP)
    # 12 V car socket and barrel jack, both r 14 bezels as model.py
    car = _ycyl(-140, PF - 7, 85, 14, 6)
    car = _fillet_try(car, _face_edges(car, Axis.Y, False), [1.5, 1.0])
    car -= _ycyl(-140, PF - 8, 85, 10.5, 6)
    car += _ycyl(-140, PF - 5.5, 85, 2.2, 2.0)
    brl = _ycyl(-90, PF - 7, 85, 14, 6)
    brl = _fillet_try(brl, _face_edges(brl, Axis.Y, False), [1.5, 1.0])
    brl -= _ycyl(-90, PF - 8, 85, 4.2, 6)
    add("12 V sockets (car socket, barrel)", car + brl, C_BEZEL, "plastic", 11, "shell", EP)
    pins = _ycyl(-140, PF - 8.2, 85, 1.4, 1.0) + _ycyl(-90, PF - 6.0, 85, 1.0, 2.0)
    add("12 V socket contacts", pins, C_METAL, "metal", 11, "shell", EP)
    # main rocker switch
    frame = _rbox(-20, 5, PF - 8, PF - 4, 150, 180, Axis.Y, [2.5, 1.5])
    frame -= b(-17, 2, PF - 9, PF - 5, 153, 177)
    add("Main switch bezel", frame, C_BLACK, "plastic", 11, "shell", EP)
    rock = Pos(-7.5, PF - 6, 165) * Rot(10, 0, 0) * Box(18, 8, 23)
    rock = _fillet_try(rock, rock.edges().filter_by(Axis.X), [2.0, 1.2])
    rock &= b(-17, 2, PF - 12, PF - 5, 153, 177)
    add("Main rocker switch", rock, C_BEZEL, "plastic", 11, "shell", EP)
    lit = b(-13, -2, PF - 11.8, PF - 10.2, 170.5, 172.0)
    add("Main switch indicator (lit)", lit, C_LIT, "emissive", 11, "shell", EP)
    # recessed wake button (bezel ring as model.py)
    wb = _ycyl(30, PF - 5, 165, 8, 2) - _ycyl(30, PF - 5, 165, 5, 3)
    add("Wake button bezel", wb, C_METAL, "metal", 11, "shell", EP)
    wk = _ycyl(30, PF - 4.6, 165, 4.6, 1.2)
    wk = _fillet_try(wk, _face_edges(wk, Axis.Y, False), [0.5, 0.3])
    add("Wake button (recessed)", wk, C_ACCENT, "plastic", 11, "shell", EP)
    # printed port marks
    marks = [b(-147, -135, PF - 4.3, PF - 4, 138, 140), b(-117, -105, PF - 4.3, PF - 4, 138, 140),
             b(-82, -73, PF - 4.3, PF - 4, 138, 140), b(-57, -48, PF - 4.3, PF - 4, 138, 140),
             b(-152, -128, PF - 4.3, PF - 4, 64, 67), b(-102, -78, PF - 4.3, PF - 4, 64, 67),
             b(-17, 2, PF - 4.3, PF - 4, 142, 144), b(22, 38, PF - 4.3, PF - 4, 153, 155),
             b(-180, -60, PF - 4.3, PF - 4, 128, 129), b(10, 60, PF - 4.3, PF - 4, 58, 60)]
    add("Output panel print", _union(marks), C_INK, "paper", 11, "shell", EP)

    # ------------------------------------------------------------ display (BOM 13)
    ED = (0, -560, 30)
    dsp = _rbox(-175, -95, PF - 7, PF - 4, 170, 188, Axis.Y, [2.5, 1.5])
    dsp = _fillet_try(dsp, _face_edges(dsp, Axis.Y, False), [0.6, 0.4])
    dsp -= b(-171, -99, PF - 8, PF - 6.2, 173, 185)
    add("Display bezel", dsp, C_BLACK, "plastic", 13, "shell", ED)
    add("Display glass", b(-171, -99, PF - 6.4, PF - 6.0, 173, 185), "#0E1216", "screen", 13, "shell", ED)
    yy = PF - 6.6
    ro = [b(-168 + 7 * k, -163 + 7 * k, yy - 0.2, yy, 176, 182) for k in range(4)]
    ro += [b(-130, -118, yy - 0.2, yy, 179, 183), b(-130, -113, yy - 0.2, yy, 175, 177),
           b(-110, -102, yy - 0.2, yy, 177, 183)]
    add("Display readout (lit)", _union(ro), C_LIT, "emissive", 13, "shell", ED)
    add("Display cell outline", b(-140, -139, yy - 0.2, yy, 176, 182), "#28515A", "screen", 13, "shell", ED)

    # ------------------------------------------------------------ AC outlet with RCD (BOM 12)
    EA = (0, -580, -40)
    ac = b(70, 175, PF - 16, PF - 4, 70, 170)
    ac = _fillet_try(ac, _par(ac, Axis.Y), [7.0, 5.0])
    ac = _fillet_try(ac, _face_edges(ac, Axis.Y, False), [2.0, 1.2])
    ax_, az_ = 106, 118
    ac -= _ycyl(ax_, PF - 16, az_, 19.5, 16)
    ac -= b(140, 166, PF - 17, PF - 14.8, 104, 160)
    add("AC outlet module (230 V)", ac, C_OUTLET, "plastic", 12, "shell", EA)
    face = _ycyl(ax_, PF - 8.5, az_, 19.4, 1.0) - _ycyl(ax_ - 9.5, PF - 8, az_, 2.4, 3) \
        - _ycyl(ax_ + 9.5, PF - 8, az_, 2.4, 3)
    add("AC socket face", face, "#D7DADD", "plastic", 12, "shell", EA)
    clips = b(ax_ - 3, ax_ + 3, PF - 16, PF - 9, az_ + 17.5, az_ + 19.5) + b(ax_ - 3, ax_ + 3, PF - 16, PF - 9, az_ - 19.5, az_ - 17.5)
    add("AC socket earth clips", clips, C_METAL, "metal", 12, "shell", EA)
    rcd = b(140, 166, PF - 15, PF - 14, 104, 160)
    add("RCD panel", rcd, C_BEZEL, "plastic", 12, "shell", EA)
    tb = _rbox(146, 160, PF - 18, PF - 14, 143, 153, Axis.Y, [1.5, 1.0])
    add("RCD test button", tb, C_ACCENT, "plastic", 12, "shell", EA)
    rb = _rbox(146, 160, PF - 17, PF - 14, 125, 135, Axis.Y, [1.5, 1.0])
    add("RCD reset button", rb, C_OUTLET, "plastic", 12, "shell", EA)
    led = _ycyl(153, PF - 15.2, 112, 2.2, 1.6) + Pos(153, PF - 16, 112) * Sphere(2.0)
    led &= b(148, 158, PF - 18.2, PF - 14, 106, 118)
    add("AC status light (lit)", led, C_LED_G, "emissive", 12, "shell", EA)
    acp = b(84, 128, PF - 16.3, PF - 16, 80, 83) + b(92, 120, PF - 16.3, PF - 16, 86, 88) \
        + b(143, 163, PF - 16.3, PF - 16, 97, 99) + b(143, 163, PF - 16.3, PF - 16, 162, 164)
    add("AC outlet print", acp, C_BEZEL, "paper", 12, "shell", EA)

    # ------------------------------------------------------------ input panel (BOM 14), +X end
    EI = (220, 0, 260)
    ip = b(L / 2, L / 2 + 4, -115, -15, 120, 195)
    ip = _fillet_try(ip, _par(ip, Axis.X), [6.0, 4.0])
    ip = _fillet_try(ip, _face_edges(ip, Axis.X, True), [1.0, 0.6])
    add("Input panel plate", ip, C_PANEL, "plastic", 14, "shell", EI)
    flanges, reds, blacks, caps = [], [], [], []
    for y in (-100, -55):
        f = _rbox(L / 2 + 4, L / 2 + 7, y, y + 30, 140, 175, Axis.X, [3.0, 2.0])
        flanges.append(f)
        for yy0, lst in ((y + 2, reds), (y + 15, blacks)):
            h_ = b(L / 2 + 7, L / 2 + 18, yy0, yy0 + 13, 144, 171)
            h_ = _fillet_try(h_, _par(h_, Axis.X), [1.0, 0.6])
            h_ -= b(L / 2 + 14, L / 2 + 19, yy0 + 3, yy0 + 10, 150, 165)
            lst.append(h_)
        caps.append(b(L / 2 + 4.1, L / 2 + 4.4, y + 3, y + 27, 128, 134))
    add("Powerpole mounting flanges", _union(flanges), C_BLACK, "plastic", 14, "shell", EI)
    add("Powerpole PP45 housings, red", _union(reds), C_PP_RED, "plastic", 14, "shell", EI)
    add("Powerpole PP45 housings, black", _union(blacks), C_PP_BLK, "plastic", 14, "shell", EI)
    add("Input panel print (DC IN, CHARGER)", _union(caps), C_INK, "paper", 14, "shell", EI)

    # ------------------------------------------------------------ pack bay door (BOM 6)
    EDr = (680, 0, 0)
    dt = P["door_t"]
    dy0, dy1 = y0 - P["latch_proud"] - 6, y1 + 7
    dz0, dz1 = z0 - 4, z1 + 6
    door = b(L / 2, L / 2 + dt, dy0, dy1, dz0, dz1)
    door = _fillet_try(door, _par(door, Axis.X), [6.0, 4.0])
    door = _fillet_try(door, _face_edges(door, Axis.X, True), [1.5, 1.0])
    win = _rbox(L / 2 - 1, L / 2 + dt + 1, 28, 54, 18, 94, Axis.X, [4.0, 3.0])
    door -= win
    add("Pack bay door", door, C_BODY, "painted", 6, "shell", EDr)
    pane = _rbox(L / 2 + 1.5, L / 2 + 4, 28, 54, 18, 94, Axis.X, [4.0, 3.0])
    add("Pack bay door window (clear)", pane, C_WINDOW, "clear", 6, "shell", EDr)
    pull = b(L / 2 + dt + 5, L / 2 + dt + 8, 60, 90, 49, 61)
    pull = _fillet_try(pull, _par(pull, Axis.X), [2.0, 1.0])
    pull += b(L / 2 + dt, L / 2 + dt + 5, 60, 66, 51, 59) + b(L / 2 + dt, L / 2 + dt + 5, 84, 90, 51, 59)
    add("Door pull", pull, C_METAL, "metal", 6, "shell", EDr)
    eye = b(L / 2 + dt, L / 2 + dt + 7, 100, 108, 70, 88)
    eye = _fillet_try(eye, _par(eye, Axis.Y), [3.0, 2.0])
    eye -= _ycyl(L / 2 + dt + 3.5, 104, 82, 2.5, 12)
    add("Padlock eye", eye, C_METAL, "metal", 6, "shell", EDr)
    hinge = _union([_zcyl(L / 2 + dt + 2, dy1 - 4, zz, 3.0, 18) for zz in (dz0 + 14, (dz0 + dz1) / 2, dz1 - 14)])
    add("Door hinge knuckles", hinge, C_METAL, "metal", 6, "shell", EDr)
    catch = _rbox(L / 2 + 0.2, L / 2 + dt + 0.4, 22, 26, 44, 66, Axis.X, [1.0, 0.5])
    add("Door magnetic catch strip", catch, C_BLACK, "plastic", 6, "shell", EDr)

    # ------------------------------------------------------------ fan grille (BOM 15), -X end
    EF = (-120, 300, -20)
    f = P["fan"]
    gr = b(-L / 2 - 4, -L / 2, -64, -56 + f, 106, 114 + f)
    gr = _fillet_try(gr, _par(gr, Axis.X), [6.0, 4.0])
    gcy, gcz = -60 + f / 2, 110 + f / 2
    for rr in (34, 25, 16):
        gr -= _xcyl(-L / 2 - 2, gcy, gcz, rr, 6) - _xcyl(-L / 2 - 2, gcy, gcz, rr - 4.5, 8)
    gr -= _xcyl(-L / 2 - 2, gcy, gcz, 7, 6) - _xcyl(-L / 2 - 2, gcy, gcz, 4, 8)
    add("Exhaust fan grille", gr, C_BEZEL, "plastic", 15, "shell", EF)
    fan = b(-L / 2 + t, -L / 2 + t + 25, -60, -60 + f, 110, 110 + f)
    fan = _fillet_try(fan, _par(fan, Axis.X), [4.0, 2.0])
    fan -= _xcyl(-L / 2 + t + 12.5, gcy, gcz, 37, 30)
    fan += _xcyl(-L / 2 + t + 12.5, gcy, gcz, 14, 20)
    for k in range(7):
        fan += Pos(-L / 2 + t + 12.5, gcy, gcz) * Rot(360 / 7 * k, 0, 0) * Pos(0, 0, 24) * Rot(0, 0, 30) \
            * Box(14, 2.0, 22)
    add("Exhaust fan (80 mm)", fan, C_BLACK, "plastic", 15, "internal", EF)
    filt = b(L / 2 - t - 1.2, L / 2 - t - 0.2, -114, -16, 17, 94)
    add("Intake dust filter (fabric mesh)", filt, "#4B5058", "fabric", 15, "internal", (220, 0, 0))

    # ------------------------------------------------------------ SwapCell pack (BOM 4)
    EPk = (470, 0, 0)
    pk = b(x0, x1, y0, y1, z0, z1)
    pk = _fillet_try(pk, _par(pk, Axis.X), [8.0, 6.0, 4.0])
    pk = _fillet_try(pk, _face_edges(pk, Axis.X, True), [2.0, 1.0])
    pk = _fillet_try(pk, _face_edges(pk, Axis.X, False), [2.0, 1.0])
    for k in range(1, 6):                                                    # grip ribs on the lid face
        xx = x0 + k * (P["pack_l"] / 6)
        pk -= b(xx - 1, xx + 1, y1 - 0.8, y1 + 1, z0 + 12, z1 - 12)
    add("SwapCell pack (reference)", pk, C_PACK, "painted", 4, "internal", EPk)
    pw, pd, ph = P["plug_w"], P["plug_d"], P["plug_h"]
    plug = b(x0 - ph, x0, yc - pd / 2, yc + pd / 2, zc - pw / 2, zc + pw / 2)
    plug = _fillet_try(plug, _par(plug, Axis.X), [3.0, 2.0])
    add("SwapCell plug", plug, C_BLACK, "plastic", 4, "internal", EPk)
    hw, hd, hh = P["handle_w"], P["handle_d"], P["handle_h"]
    loop = b(x1, x1 + hh, yc - hd / 2, yc + hd / 2, zc - hw / 2, zc + hw / 2) \
        - b(x1 - 1, x1 + P["grip_clear"], yc - hd, yc + hd, zc - hw / 2 + 11, zc + hw / 2 - 11)
    loop = _fillet_try(loop, _par(loop, Axis.Y), [4.0, 2.0])
    add("SwapCell pack handle", loop, C_RUBBER, "rubber", 4, "internal", EPk)
    xl = x1 - P["latch_from_top"]
    pawl = b(xl - P["latch_h"] / 2, xl + P["latch_h"] / 2, y0 - P["latch_proud"], y0,
             zc - P["latch_w"] / 2, zc + P["latch_w"] / 2)
    pawl = _fillet_try(pawl, _par(pawl, Axis.Y), [2.0, 1.0])
    add("SwapCell latch pawl", pawl, C_METAL, "metal", 4, "internal", EPk)
    plab = b(x0 + 40, x0 + 200, y0 - 0.4, y0, z0 + 22, z1 - 22)
    add("SwapCell pack label", plab, C_LABEL, "paper", 4, "internal", EPk)
    pink = b(x0 + 50, x0 + 110, y0 - 0.7, y0 - 0.4, z0 + 50, z0 + 58) + b(x0 + 50, x0 + 150, y0 - 0.7, y0 - 0.4, z0 + 36, z0 + 39)
    add("SwapCell label print", pink, C_BEZEL, "paper", 4, "internal", EPk)

    # ------------------------------------------------------------ pack bay (BOM 5), geometry as model.py
    gc = P["guide_clear"]
    div_y1 = y0 - P["latch_proud"] - 2
    runners = b(-190, L / 2 - t, y0 + 8, y0 + 20, t, z0 - gc) + b(-190, L / 2 - t, y1 - 20, y1 - 8, t, z0 - gc)
    top_rail = b(-190, L / 2 - t, yc - 10, yc + 10, z1 + gc, P["shelf_z"])
    add("Pack bay runners and guide rail", runners + top_rail, "#3F444B", "plastic", 5, "internal", (0, 0, 0))
    shelf = b(-195, L / 2 - t, div_y1 - P["divider_t"], D / 2 - t, P["shelf_z"], P["shelf_z"] + P["shelf_t"])
    divider = b(xl - 40, xl + 40, div_y1 - P["divider_t"], div_y1, t, P["shelf_z"])
    catch_ = b(xl + P["latch_h"] / 2 + 1, xl + P["latch_h"] / 2 + 9, div_y1, y0 - 1, zc - 25, zc + 25)
    add("Pack bay shelf and catch bracket", shelf + divider + catch_, C_ALU, "metal", 5, "internal", (0, 0, 0))
    rx0 = x0 - ph - 22
    rec = b(rx0, x0 - 0.5, yc - pd / 2 - 7, yc + pd / 2 + 7, zc - pw / 2 - 7, zc + pw / 2 + 7) \
        - b(x0 - ph - 0.5, x0, yc - pd / 2 - 0.5, yc + pd / 2 + 0.5, zc - pw / 2 - 0.5, zc + pw / 2 + 0.5)
    rec = _fillet_try(rec, _par(rec, Axis.X), [3.0, 2.0])
    add("Blind-mate receptacle (floating mount)", rec, C_BLACK, "plastic", 5, "internal", (0, 0, 0))

    # ------------------------------------------------------------ electronics
    sz = P["shelf_z"] + P["shelf_t"]
    cl, cd, ch = P["controller"]
    ECc = (0, 0, 170)
    add("Charge controller base board", b(-40, -40 + cl, 22, 22 + cd, sz, sz + 8), C_PCB, "plastic", 7, "internal", ECc)
    hs = b(-30, -50 + cl, 30, 14 + cd, sz + 8, sz + 14)
    for k in range(12):
        yk = 31 + k * 7.0
        hs += b(-30, -50 + cl, yk, yk + 2.2, sz + 14, sz + ch)
    add("Charge controller heat sink", hs, C_ALU, "metal", 7, "internal", ECc)

    hl, hd2, hh2 = P["host"]
    EH = (0, 0, 190)
    add("Host controller board", b(-180, -180 + hl, 30, 30 + hd2, sz, sz + 1.6), C_PCB, "plastic", 8, "internal", EH)
    add("ESP32 module shield", b(-172, -146, 38, 56, sz + 1.6, sz + 5), C_METAL, "metal", 8, "internal", EH)
    add("Host relays", b(-138, -118, 36, 60, sz + 1.6, sz + hh2) + b(-114, -94, 36, 60, sz + 1.6, sz + hh2),
        C_RELAY, "plastic", 8, "internal", EH)
    add("Host connectors", b(-175, -100, 80, 90, sz + 1.6, sz + 10), C_BLACK, "plastic", 8, "internal", EH)

    il, idp, ih = P["inverter"]
    EIv = (70, -200, 110)
    ivx0, ivy0 = -212, -D / 2 + 8
    inv = b(ivx0, ivx0 + il, ivy0, ivy0 + idp, t, t + ih - 12)
    inv = _fillet_try(inv, _par(inv, Axis.X), [4.0, 2.0])
    for k in range(14):
        yk = ivy0 + 3 + k * 7.0
        inv += b(ivx0 + 6, ivx0 + il - 6, yk, yk + 2.4, t + ih - 13, t + ih)
    add("300 W pure sine inverter", inv, "#474D56", "metal", 9, "internal", EIv)
    add("Inverter label", b(ivx0 + 30, ivx0 + 110, ivy0 - 0.4, ivy0, 15, 45), C_LABEL, "paper", 9, "internal", EIv)

    dl, dd, dh = P["dcdc"]
    EDc = (0, -120, 80)
    dc = b(40, 40 + dl, -D / 2 + 18, -D / 2 + 18 + dd, t, t + dh - 10)
    for k in range(8):
        yk = -D / 2 + 21 + k * 8.0
        dc += b(44, 36 + dl, yk, yk + 2.4, t + dh - 11, t + dh)
    add("DC-DC converter, 48 V to 12 V", dc, C_ALU, "metal", 10, "internal", EDc)

    # ------------------------------------------------------------ accessory: grid charger brick (BOM 17)
    gx0, gy0 = 330, -300
    EG = (260, -160, -190)
    brick = b(gx0, gx0 + 170, gy0, gy0 + 72, 0, 42)
    brick = _fillet_try(brick, _par(brick, Axis.X), [8.0, 5.0])
    brick = _fillet_try(brick, _face_edges(brick, Axis.X, True), [3.0, 2.0])
    brick = _fillet_try(brick, _face_edges(brick, Axis.X, False), [3.0, 2.0])
    add("Grid charger brick (54.6 V, 5 A)", brick, C_LID, "plastic", 17, "accessory", EG)
    add("Charger label", b(gx0 + 30, gx0 + 120, gy0 - 0.4, gy0, 10, 32), C_LABEL, "paper", 17, "accessory", EG)
    lead = _pipe([(gx0 + 170, gy0 + 36, 21), (gx0 + 215, gy0 + 36, 21), (gx0 + 240, gy0 + 60, 8),
                  (gx0 + 240, gy0 + 140, 8)], 3.5)
    add("Charger DC lead", lead, C_CABLE, "rubber", 17, "accessory", EG)
    ppl = b(gx0 + 226, gx0 + 254, gy0 + 140, gy0 + 160, 1, 15)
    add("Charger Powerpole plug", ppl, C_PP_RED, "plastic", 17, "accessory", EG)

    # ------------------------------------------------------------ context: bench top, solar panel, phone
    add("Bench top (oak)", _rbox(-280, 345, -290, 375, -32, -2, Axis.Z, [12.0, 8.0]), C_WOOD, "wood", None,
        "context", (0, 0, 0))
    # small 50 W panel on a folding stand behind the case, leaning back 30 deg, facing front
    tilt = 30.0
    pw_, ph2, pt_ = 380.0, 300.0, 22.0
    py_bot, pz_bot, pcx = 170.0, -2.0, 60.0
    ploc = Pos(pcx, py_bot, pz_bot) * Rot(-tilt, 0, 0)          # local: X across, Z up the slope, -Y is the face

    def pl(x0_, x1_, y0_, y1_, z0_, z1_):
        return ploc * b(x0_, x1_, y0_, y1_, z0_, z1_)

    frame = pl(-pw_ / 2, pw_ / 2, 0, pt_, 0, ph2) - pl(-pw_ / 2 + 12, pw_ / 2 - 12, -1, pt_ - 4, 12, ph2 - 12)
    add("Solar panel frame (aluminium)", frame, C_FRAME, "metal", None, "context", (0, 0, 0))
    add("Solar panel cells", pl(-pw_ / 2 + 12, pw_ / 2 - 12, 3, pt_ - 4, 12, ph2 - 12), C_CELL, "screen", None,
        "context", (0, 0, 0))
    bus = [pl(-pw_ / 2 + 12, pw_ / 2 - 12, 2.6, 3, zz - 0.6, zz + 0.6) for zz in (12 + (ph2 - 24) * k / 4 for k in range(1, 4))]
    bus += [pl(xx - 0.6, xx + 0.6, 2.6, 3, 12, ph2 - 12) for xx in (-pw_ / 2 + 12 + (pw_ - 24) * k / 6 for k in range(1, 6))]
    add("Solar panel cell gaps", _union(bus), "#C7CCD3", "metal", None, "context", (0, 0, 0))
    legs = []
    for sx in (-1, 1):
        tp = (ploc * Pos(sx * 130, pt_, ph2 * 0.62)).position
        legs.append(_pipe([(tp.X, tp.Y, tp.Z), (tp.X, 355.0, 3.0)], 5.0))
    legs = _union(legs)
    add("Solar panel stand legs", legs, C_FRAME, "metal", None, "context", (0, 0, 0))
    jb = pl(95, 145, pt_, pt_ + 16, 30, 70)
    add("Solar panel junction box", jb, C_BLACK, "plastic", None, "context", (0, 0, 0))
    # panel lead to the DC IN Powerpole on the +X end
    iy = -85.0
    plug = b(L / 2 + 18, L / 2 + 32, iy - 13, iy + 13, 146, 169)
    plug = _fillet_try(plug, _par(plug, Axis.X), [2.0, 1.0])
    add("Solar lead Powerpole plug", plug, C_PP_RED, "plastic", None, "context", (0, 0, 0))
    jv = (ploc * Pos(120, pt_ + 16, 50)).position
    jbw = (jv.X, jv.Y, jv.Z)
    cable = _pipe([(L / 2 + 32, iy, 157.5), (L / 2 + 55, iy, 157.5), (L / 2 + 72, iy, 120),
                   (L / 2 + 80, iy + 10, 4), (L / 2 + 85, 150, 4), (jbw[0] + 10, jbw[1] + 30, 4),
                   (jbw[0], jbw[1] + 8, jbw[2] - 10), jbw], 3.5)
    add("Solar panel lead", cable, C_CABLE, "rubber", None, "context", (0, 0, 0))
    # phone charging from USB-C on the bench in front of the case
    ph_x0, ph_x1, ph_y0, ph_y1 = -250, -95, -262, -187
    phone = b(ph_x0, ph_x1, ph_y0, ph_y1, -2, 6)
    phone = _fillet_try(phone, _par(phone, Axis.Z), [9.0, 6.0])
    phone = _fillet_try(phone, _face_edges(phone, Axis.Z, True), [2.0, 1.0])
    add("Phone (scale)", phone, "#2B2F36", "plastic", None, "context", (0, 0, 0))
    scr_ = b(ph_x0 + 5, ph_x1 - 5, ph_y0 + 5, ph_y1 - 5, 5.9, 6.2)
    scr_ = _fillet_try(scr_, _par(scr_, Axis.Z), [6.0, 4.0])
    add("Phone screen", scr_, "#0E1216", "screen", None, "context", (0, 0, 0))
    uplug = _rbox(-148, -134, PF - 26, PF - 8, 146.5, 153.5, Axis.Y, [3.0, 2.0])
    pplug = _rbox(ph_x1, ph_x1 + 18, -228, -221, 0, 6, Axis.X, [2.5, 1.5])
    add("USB-C cable plugs", uplug + pplug, "#E5E7EB", "plastic", None, "context", (0, 0, 0))
    ucab = _pipe([(-141, PF - 26, 150), (-141, PF - 40, 150), (-130, PF - 60, 110), (-100, PF - 75, 30),
                  (-70, -205, 4), (-60, -224.5, 3), (ph_x1 + 18, -224.5, 3)], 2.2)
    add("USB-C cable", ucab, "#E5E7EB", "rubber", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
