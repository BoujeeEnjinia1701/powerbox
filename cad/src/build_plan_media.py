"""PowerBox prototype build plan pictures (PBX-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
A sheet, joint or step can be drawn on its own: sheets:104, joints:4, steps:9.
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/PBX-DWG-101 to 113        making sketches for the made components
    docs/05-build-plan/*-holes.png         hole and cut-out layouts (floor, end wall, output panel)
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, bx, fuse  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
L, DD, H = P["case_l"], P["case_d"], P["case_h"]
REPO = "github.com/BoujeeEnjinia1701/powerbox"


def S(*ks):
    return fuse([C[k].shape for k in ks])


def part(name, keys, color=None, explode=(0, 0, 0)):
    keys = (keys,) if isinstance(keys, str) else keys
    return Part(name, S(*keys), color or C[keys[0]].color, None, tuple(explode), 1.0)


RUNNERS = ("runner_f1", "runner_f2", "runner_b1", "runner_b2")


def named():
    """The components in build order, as the plan names them."""
    return {
        "body": part("Enclosure body, with rivet nuts", ("body", "tab_rivets")),
        "runners": part("Floor runners (4 lengths)", RUNNERS + ("runner_screws",), C["runner_f1"].color),
        "catch": part("Catch bracket and latch catch", ("catch_bracket", "catch")),
        "recept": part("Receptacle bracket and receptacle", ("recept_bracket", "receptacle")),
        "inverter": part("Inverter", "inverter"),
        "dcdc": part("DC-DC converter, 48 V to 12 V", "dcdc"),
        "protection": part("Protection plate (main fuse, breaker, relay)", "protection"),
        "fuseblock": part("Fuse block", "fuseblock"),
        "fan": part("Exhaust fan and grille", ("fan", "grille")),
        "filter": part("Intake filter frame", "filter_frame"),
        "rail": part("Top guide rail (2 lengths)", ("rail_1", "rail_2", "rail_screws"), C["rail_1"].color),
        "shelf": part("Shelf", ("shelf", "shelf_rivets")),
        "charger": part("Charge controller", "charger"),
        "host": part("Host controller", "host"),
        "out_panel": part("Output panel plate", ("out_panel",)),
        "modules": part("Output sockets, AC outlet, display", ("sockets", "ac", "display"), C["ac"].color),
        "in_panel": part("Input panel plate and Powerpoles", ("in_panel", "inputs"), C["inputs"].color),
        "door": part("Pack bay door, hinge, latch, staple", ("door", "hinge", "latch", "staple", "door_rivets"), C["door"].color),
        "doubler": part("Handle doubler plate", "doubler"),
        "handle": part("Carry handle", ("handle", "handle_bolts")),
        "lid": part("Lid", ("lid", "lid_screws")),
        "feet": part("Rubber feet (4)", "feet"),
        "pack": part("SwapCell pack (from the SwapCell project)", "pack"),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = named()
    off = {"body": (0, 0, 0), "runners": (0, 0, -250), "catch": (0, 0, -250), "recept": (0, 0, -250),
           "inverter": (0, -300, -300), "dcdc": (0, -300, -300), "protection": (0, 40, -400), "fuseblock": (0, -300, -300),
           "fan": (-200, 0, 0), "filter": (170, 0, -60), "rail": (0, 0, 270), "shelf": (0, 0, 300), "charger": (0, 0, 380),
           "host": (0, 0, 380), "out_panel": (0, -230, 0), "modules": (0, -340, 0), "in_panel": (260, 0, 40),
           "door": (260, 0, 0), "doubler": (0, 0, 430), "handle": (0, 0, 680), "lid": (0, 0, 600), "feet": (0, 0, -580),
           "pack": (640, 0, -160)}
    parts = []
    for k, p in M.items():
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "PowerBox prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; floor parts are drawn below the case",
                       elev=20, azim=-52, size=(12, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = named()
    base = dict(project="PowerBox", date=DATE)
    ghost_case = [M["body"]]
    out = []

    def sheet(n, *a, **k):
        if only is None or n == only:
            out.append(bv.component_sheet(*a, **k))

    sheet(101, Part("Enclosure body", C["body"].shape, C["body"].color), [M["out_panel"], M["in_panel"], M["shelf"]],
          dwg_no="PBX-DWG-101", title="PowerBox enclosure body: making sketch",
          material="5052 aluminium sheet 1.2 mm, folded; 14 M4 rivet nuts", inset_view=(28, -55),
          notes=["One blank, about 900 x 700 mm before folding; the shop sets bend allowances.",
                 "Floor 460 x 260; walls 220 tall. End walls carry 15 mm tabs that fold onto",
                 "  the outside of the long walls: 3 blind rivets each, 40, 100, 160 up.",
                 "Front wall: window 360 x 140, 55 from the left end, 48 to 188 up.",
                 "  Rivet nuts (6.0 holes): 44 and 426 from the left end, 80 and 175 up;",
                 "  and for the lid, 80, 230 and 380 from the left end, 213 up.",
                 "Back wall: lid rivet nuts as the front; shelf rivets 3.3 mm at 80, 180,",
                 "  280 and 380 from the fan end, 118 up.",
                 "Fan end: a 76 mm hole centred 110 from the front edge and 150 up, with",
                 "  four 4.5 mm holes on a 71.5 mm square round it. Door end: see its layout.",
                 "Floor: 24 holes of 4.5 mm; see the floor layout picture.",
                 "Deburr every edge. Set the rivet nuts with a hand rivet nut tool.",
                 "Check: square within 1 mm over the diagonals; lid sits on all walls."],
          **base)

    lidv = C["lid"].shape
    sheet(102, Part("Lid", lidv, C["lid"].color), [M["body"], M["handle"]],
          dwg_no="PBX-DWG-102", title="PowerBox lid: making sketch", material="5052 aluminium sheet 1.2 mm, folded",
          view_shape=b.Pos(0, 0, -H) * lidv, inset_view=(30, -55),
          notes=["Blank: top 464.4 x 264.4 mm with a 16 mm skirt folded down on all sides;",
                 "  relieve the corners, they need not be closed.",
                 "Seven exhaust slots 6 x 85 mm, 14 mm apart, the first 32.2 from the",
                 "  left edge, from 162.2 to 247.2 back from the front edge.",
                 "Handle bolt holes 5.5 mm on the centre line, 127.2, 157.2, 307.2 and",
                 "  337.2 from the left edge.",
                 "Screw holes 4.5 mm in the front and back skirts, 82.2, 232.2 and 382.2",
                 "  from the left edge, 7.8 above the skirt's lower edge.",
                 "Fit: the top rests on the wall tops; the skirt hangs outside the walls",
                 "  with a 1 mm gap, where the rivet nut flanges sit.",
                 "Six M4 pan-head screws through the skirt into the rivet nuts.",
                 "Check: the lid drops on without forcing and every hole lines up."],
          **base)

    sheet(103, Part("Handle doubler", C["doubler"].shape, C["doubler"].color), [M["lid"], M["handle"]],
          dwg_no="PBX-DWG-103", title="PowerBox handle doubler plate: making sketch", material="5052 aluminium sheet 2 mm",
          view_shape=b.Pos(0, 0, -H) * C["doubler"].shape, inset_view=(-35, -60),
          notes=["Cut 240 x 40 mm from 2 mm sheet; round the corners and deburr.",
                 "Four 5.5 mm holes on the centre line, 15, 45, 195 and 225 from the",
                 "  left end. Drill it clamped under the lid so the holes match.",
                 "Fit: under the lid, centred, held by the four M5 handle bolts;",
                 "  the nyloc nuts sit on the doubler.",
                 "It spreads the carrying load of about 9.4 kg over the thin lid.",
                 "Check: the bolts pass through handle, lid and doubler without forcing."],
          **base)

    sh = C["shelf"].shape
    sheet(104, Part("Shelf", sh, C["shelf"].color), [M["body"], M["catch"], M["rail"], M["charger"]],
          dwg_no="PBX-DWG-104", title="PowerBox shelf: making sketch", material="5052 aluminium sheet 2 mm, folded",
          view_shape=b.Pos(0, 0, -P["shelf_z"]) * sh, inset_view=(35, -125),
          notes=["Deck 423.8 x 128.8 mm. Fold up a 20 mm rear flange (stop it 2.8 mm",
                 "  short of the right end), a 20 mm right end flange 100 long from the",
                 "  front edge, and fold down a 15 mm front flange along the front edge.",
                 "Rail screw holes 3.4 mm, 68 back from the front edge, 15, 135, 335 and",
                 "  410 from the left end.",
                 "Catch bracket holes 4.5 mm, 11.5 back from the front edge, 310 and",
                 "  360 from the left end.",
                 "Rivet holes 3.3 mm, 10 above the deck: rear flange 45, 145, 245, 345",
                 "  from the left end; end flange 30 and 80 from the front edge.",
                 "Fit: drops into the case onto the catch bracket; drill the walls through",
                 "  the flange holes and rivet. Deck top 108 above the case underside.",
                 "Check: the deck is flat within 1 mm and level side to side."],
          **base)

    cb = C["catch_bracket"].shape
    sheet(105, Part("Catch bracket", cb, C["catch_bracket"].color), [M["body"], M["shelf"], M["pack"]],
          dwg_no="PBX-DWG-105", title="PowerBox catch bracket: making sketch",
          material="5052 aluminium sheet 3 mm, folded", inset_view=(30, -120),
          notes=["A channel 80 long: web 104.8 tall, two 22 mm flanges, both folded to the",
                 "  front (toward the inverter). 3 mm sheet; inside bend radius 3 mm.",
                 "Two 4.5 mm holes in each flange, 15 and 65 from the left end, 9.5",
                 "  back from the flange's front edge.",
                 "Catch: drill the web to the catch's own holes, its centre 57 from the",
                 "  left end and 53.8 above the underside of the foot.",
                 "Fit: foot on the floor, two M4 button heads from below, nyloc nuts on",
                 "  top; top flange under the shelf, two M4 screws down through the shelf.",
                 "The web's back face is 2 mm in front of the pack's latch pawl and 12 mm",
                 "  in front of its latch face; the catch takes the pawl.",
                 "Check: the web is square to the floor and the catch springs freely."],
          **base)

    rb = C["recept_bracket"].shape
    sheet(106, Part("Receptacle bracket", rb, C["recept_bracket"].color), [M["runners"], part("Receptacle", "receptacle"), M["pack"]],
          dwg_no="PBX-DWG-106", title="PowerBox receptacle bracket: making sketch",
          material="5052 aluminium sheet 3 mm, folded", inset_view=(35, -160),
          notes=["An angle 62 wide: web 93.8 tall, foot 23 deep, folded from 3 mm sheet.",
                 "Two 4.5 mm holes in the foot, 10 from its free edge, 13 and 49",
                 "  from one side.",
                 "Web: drill to the floating-mount holes of the SwapCell receptacle",
                 "  (SwapCell dock drawing); the receptacle face is centred 55 above the",
                 "  case underside and 198 back from the outside of the front wall.",
                 "Fit: foot on the floor, foot toward the fan end, two M4 button heads",
                 "  from below with nyloc nuts on top.",
                 "The receptacle screws to the web's pack side through its rubber",
                 "  grommets, so it can float about 1 mm to meet the plug.",
                 "Check: with a pack on the runners the plug enters the receptacle",
                 "  without touching its sides."],
          **base)

    r = C["runner_f1"].shape
    sheet(107, Part("Floor runner", r, C["runner_f1"].color), [M["pack"], part("Other runners", ("runner_f2", "runner_b1", "runner_b2")), M["catch"], M["recept"]],
          dwg_no="PBX-DWG-107", title="PowerBox floor runner (make 4): making sketch",
          material="PETG, 3D printed, 4 walls, 40 % infill", inset_view=(30, -60),
          notes=["An L section: base 24 wide x 8.8 tall, lip 3 wide rising 15 above it.",
                 "Print four, each 209.4 long, lying on the base; all four are the same.",
                 "Two holes 5.6 mm, 8 deep, from below, 14 in from the lip's outer face:",
                 "  25 from one end and 35 from the other. Press in M4 heat-set inserts.",
                 "Fit: two lengths end to end along the front of the bay and two along",
                 "  the back, lips on the outside, starting 38.8 from the inside of the fan end.",
                 "  Each held by two M4 button heads from under the floor.",
                 "The pack rests on the bases; the lips stand 1 mm off its sides.",
                 "Check: the joints between lengths are flush; the pack slides from",
                 "  end to end without catching."],
          **base)

    rl = C["rail_1"].shape
    sheet(108, Part("Top guide rail", rl, C["rail_1"].color), [M["pack"], part("Outer rail", "rail_2"), M["recept"]],
          dwg_no="PBX-DWG-108", title="PowerBox top guide rail (make 2): making sketch",
          material="PETG, 3D printed, 4 walls, 40 % infill", inset_view=(30, -60),
          notes=["A bar 20 wide x 5 tall x 209.4 long; print two, lying flat.",
                 "Two holes 4.0 mm, 4 deep, in the top face on the centre line; press in",
                 "  M3 heat-set inserts. Inner length: 10 and 130 from the fan-end end.",
                 "  Outer length: 120.6 and 195.6 from the fan-end end.",
                 "Fit: under the shelf, 58 to 78 back from the front edge, held by",
                 "  M3 screws down through the shelf.",
                 "It stands 1 mm above the top of the pack and stops it lifting.",
                 "Check: the pack slides under it with light hand pressure."],
          **base)

    dr = C["door"].shape
    sheet(109, Part("Pack bay door", dr, C["door"].color), [M["body"], part("Door hardware", ("hinge", "latch", "staple")), M["pack"]],
          dwg_no="PBX-DWG-109", title="PowerBox pack bay door: making sketch", material="5052 aluminium sheet 1.2 mm",
          view_shape=b.Rot(0, 0, -90) * b.Pos(-L / 2, 0, 0) * dr, inset_view=(15, -25),
          notes=["Cut 107.5 wide x 108 tall, with a hasp tab 26 wide rising 32 above",
                 "  the top edge at the back corner.",
                 "Hasp slot 18 x 20: 85.5 to 103.5 from the front edge, 114 to 134 up.",
                 "Latch hole 19.5 mm: 92.5 from the front edge, 54 up.",
                 "Hinge rivet holes 3.3 mm: 7.5 from the front edge, 18, 54 and 90 up.",
                 "Fit: a stainless piano hinge on the front edge, riveted to the door and",
                 "  to the end wall; the door lies flat on the wall, 3.5 mm over the",
                 "  opening at the front and 5 mm at the back, 6 at top and bottom.",
                 "A thumb-turn cam latch in the 19.5 hole; its tongue turns behind the",
                 "  end wall. The tab goes over a flush padlock staple on the wall.",
                 "Check: the door shuts flat and the latch holds it shut."],
          **base)

    op = C["out_panel"].shape
    sheet(110, Part("Output panel plate", op, C["out_panel"].color), [M["body"], M["modules"]],
          dwg_no="PBX-DWG-110", title="PowerBox output panel plate: making sketch", material="5052 aluminium sheet 2 mm",
          view_shape=b.Pos(0, DD / 2, 0) * op, inset_view=(20, -60),
          notes=["Cut 394 x 164 mm. Cut-outs from the panel cut-out layout picture,",
                 "  measured from the left and bottom edges:",
                 "  USB-C 16 x 8 (2), USB-A 13 x 5 (2), 12 V socket 24 diameter,",
                 "  barrel socket 12, switch 21 x 26, wake button 12, AC outlet 60 x 60,",
                 "  display 70 x 14. Check each against the part's datasheet first.",
                 "Four 4.5 mm screw holes: 6 and 388 from the left edge, 44 and 139 up.",
                 "Fit: the modules fit their cut-outs with their own nuts or clips; the",
                 "  plate covers the front wall window, 17 over at the ends, 12 top and bottom;",
                 "  four M4 screws into the rivet nuts.",
                 "Print the port labels before fitting the modules.",
                 "Check: every module's back clears the window edges."],
          **base)

    ip = C["in_panel"].shape
    sheet(111, Part("Input panel plate", ip, C["in_panel"].color), [M["body"], part("Powerpoles", "inputs"), M["door"]],
          dwg_no="PBX-DWG-111", title="PowerBox input panel plate: making sketch", material="5052 aluminium sheet 2 mm",
          view_shape=b.Rot(0, 0, -90) * b.Pos(-L / 2, 0, 0) * ip, inset_view=(20, -20),
          notes=["Cut 110 wide x 75 tall.",
                 "Two Powerpole cut-outs 24 x 25: 23 to 47 and 68 to 92 from the front",
                 "  edge, 25 to 50 up. Size them to the panel-mount housing you buy.",
                 "Four 4.5 mm screw holes: 6 and 106 from the front edge, 20 and 55 up.",
                 "Fit: over the window in the door end wall, above the intake slots,",
                 "  four M4 screws into the rivet nuts.",
                 "DC in on the front cut-out, charger in on the back one; the housings",
                 "  are turned differently so the two plugs cannot be swapped.",
                 "Check: each plug mates with only its own socket."],
          **base)

    ff = C["filter_frame"].shape
    sheet(112, Part("Intake filter frame", ff, C["filter_frame"].color), [M["body"], M["fuseblock"]],
          dwg_no="PBX-DWG-112", title="PowerBox intake filter frame: making sketch",
          material="PETG, 3D printed, 4 walls, 40 % infill", view_shape=b.Rot(0, 0, -90) * b.Pos(-L / 2, 0, 0) * ff, inset_view=(30, -150),
          notes=["A frame 106 wide x 91 tall x 6 thick, printed lying flat.",
                 "Window 90 x 75, the same as the slotted area of the end wall.",
                 "A 4.5 mm deep pocket on the wall side holds a 5 mm foam filter pad;",
                 "  a 1.5 mm grid of six bars keeps the pad in.",
                 "Four 3.3 mm holes, 4 in from each side and 4 from top and bottom.",
                 "Fit: inside the door end wall over the intake slots, its window",
                 "  20 to 110 from the front edge and 20 to 95 up; four M3 screws from",
                 "  outside with nuts inside.",
                 "Check: the pad covers every slot and lifts out for washing."],
          **base)

    pr = C["protection"].shape
    sheet(113, Part("Protection plate", pr, C["protection"].color), [M["inverter"], M["runners"], M["catch"], M["dcdc"], M["fuseblock"]],
          dwg_no="PBX-DWG-113", title="PowerBox protection plate: making sketch",
          material="5052 aluminium sheet 2 mm, with bought fuse holder, breaker and relay", inset_view=(45, 115),
          notes=["Cut 210 x 34 mm from 2 mm sheet.",
                 "Two 4.5 mm holes for the floor screws, 7 from each end, 17 from either",
                 "  long edge.",
                 "Lay out on it, left to right: the 30 A main fuse holder, the 20 A DC",
                 "  breaker, then the inverter relay with its 47 ohm pre-charge resistor.",
                 "  Drill each to its own holes, M4 or M3 with nyloc nuts.",
                 "Fit: on the floor between the inverter and the pack bay, two M4 button",
                 "  heads from below with nyloc nuts on top.",
                 "All three parts must be rated 60 V DC or more; the fuse holder",
                 "  and fuse at least 1 kA breaking capacity.",
                 "Check: 6 mm clear of the inverter and 14 mm clear of the runners."],
          **base)
    return out


# ----------------------------------------------------------------- layouts
def _holes(face):
    out = []
    for w in face.inner_wires():
        bb = w.bounding_box()
        edges = w.edges()
        circ = len(edges) <= 2 and all("CIRCLE" in str(e.geom_type) for e in edges)
        out.append(("circle" if circ else "rect", bb.center(), bb.size))
    return out


def _fig(title, sub, size=(11, 8)):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=size, dpi=150)
    fig.text(0.03, 0.975, title, fontsize=13, fontweight="bold", color="#111827", va="top")
    fig.text(0.03, 0.94, sub, fontsize=8.4, color="#4B5563", va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    return fig, plt


def _key(fig, x, y, groups, step=0.024):
    """groups: list of (letter, colour, title, [position lines])."""
    fig.text(x, y, "Key (mm)", fontsize=9, fontweight="bold", color="#111827", va="top")
    y -= 0.035
    for letter, col, title, lines in groups:
        fig.text(x, y, letter, fontsize=8, fontweight="bold", color="white", va="top",
                 bbox=dict(boxstyle="circle,pad=0.2", fc=col, ec="none"))
        fig.text(x + 0.025, y, title, fontsize=8, fontweight="bold", color="#111827", va="top")
        y -= step
        for ln in lines:
            fig.text(x + 0.025, y, ln, fontsize=7.6, color="#111827", va="top")
            y -= step * 0.85
        y -= step * 0.3


def layouts():
    from matplotlib.patches import Rectangle
    res = []
    INK = "#111827"
    body = C["body"].shape
    # --- floor, seen from above (inside), front edge at the bottom of the page
    face = [f for f in body.faces() if abs(f.center().Z) < 0.01 and f.area > 1e5][0]
    H_ = _holes(face)
    grp = {"R": ("#2563EB", "Runner screws, 4.5"), "C": ("#57534E", "Catch bracket, 4.5"), "B": ("#78716C", "Receptacle bracket, 4.5"),
           "P": ("#BE123C", "Protection plate, 4.5"), "F": ("#9F1239", "Fuse block, 4.5"), "I": ("#C2410C", "Inverter, 4.5"),
           "D": ("#B45309", "DC-DC converter, 4.5")}

    def cls(x, y):
        if abs(y - 46) < 1 or abs(y - 106) < 1:
            return "R"
        if abs(y - 11.5) < 1:
            return "C"
        if abs(x + 208) < 1:
            return "B"
        if abs(y - 1) < 1:
            return "P"
        if (round(x), round(y)) in ((163, -100), (211, -50)):
            return "F"
        if x < 10 and y < -20:
            return "I"
        return "D"
    fig, plt = _fig("Case floor: hole positions",
                    "Seen from above, inside the case; front wall at the bottom. Distances from the outside of the left (fan) end and of the front wall, in mm, from the model.",
                    size=(12, 7.6))
    ax = fig.add_axes([0.03, 0.08, 0.62, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), L, DD, fc="#F3F4F6", ec=INK, lw=1.2))
    pos = {}
    for kind, c, sz in H_:
        g = cls(c.X, c.Y)
        X, Y = c.X + L / 2, c.Y + DD / 2
        pos.setdefault(g, []).append((X, Y))
        ax.add_patch(plt.Circle((X, Y), 4.5, fc=grp[g][0], ec="none"))
        ax.text(X + 6, Y + 4, g, fontsize=7, color=grp[g][0], fontweight="bold")
    for nm, (x0, x1, y0, y1) in (("pack bay", (-155 + L / 2, 185 + L / 2, 36 + DD / 2, 116 + DD / 2)),
                                 ("inverter", (18, 240, 8, 108)), ("DC-DC", (270, 380, 18, 83))):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#9CA3AF", lw=0.8, ls="--"))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, nm, ha="center", va="center", fontsize=8, color="#6B7280")
    ax.text(L / 2, -12, "front wall (output panel side)", ha="center", va="top", fontsize=8, color="#4B5563")
    ax.text(-10, DD / 2, "fan end", ha="right", va="center", fontsize=8, color="#4B5563", rotation=90)
    ax.text(L + 10, DD / 2, "door end", ha="left", va="center", fontsize=8, color="#4B5563", rotation=90)
    ax.set_xlim(-25, L + 25); ax.set_ylim(-30, DD + 10)
    groups = []
    for g in "RCBPFID":
        pts = sorted(pos.get(g, []))
        lines = [", ".join(f"{x:g} / {y:g}" for x, y in pts[i:i + 2]) for i in range(0, len(pts), 2)]
        groups.append((g, grp[g][0], grp[g][1] + f" ({len(pts)})", lines))
    _key(fig, 0.68, 0.89, groups, step=0.026)
    fig.text(0.68, 0.11, "Each pair: from the fan end / from the front.\nAll holes 4.5 mm for M4 screws from below.",
             fontsize=7.6, color="#4B5563", va="top")
    fig.savefig(OUT / "floor-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "floor-holes.png")

    # --- door end wall, seen from outside: front edge on the left
    face = [f for f in body.faces() if abs(f.center().X - L / 2) < 0.01 and f.area > 1e4][0]
    H_ = _holes(face)
    fig, plt = _fig("Door end wall: openings and holes",
                    "Seen from outside the door end; front wall on the left. Distances from the outside of the front wall and up from the case underside, in mm.",
                    size=(12, 8))
    ax = fig.add_axes([0.03, 0.08, 0.55, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), DD, H, fc="#F3F4F6", ec=INK, lw=1.2))
    rect, circ = [], {}
    for kind, c, sz in H_:
        Y, Z = c.Y + DD / 2, c.Z
        if kind == "rect":
            ax.add_patch(Rectangle((Y - sz.Y / 2, Z - sz.Z / 2), sz.Y, sz.Z, fc="white", ec=INK, lw=0.9))
            rect.append((Y - sz.Y / 2, Y + sz.Y / 2, Z - sz.Z / 2, Z + sz.Z / 2))
        else:
            d = round(sz.Y, 1)
            col = "#0F766E" if d > 5 else "#7C3AED"
            ax.add_patch(plt.Circle((Y, Z), d / 2 + 0.6, fc=col, ec="none"))
            circ.setdefault(d, []).append((round(Y, 1), round(Z, 1)))
    big = sorted([r for r in rect if (r[1] - r[0]) * (r[3] - r[2]) > 2000], key=lambda r: r[0])
    slots = sorted([r for r in rect if (r[1] - r[0]) * (r[3] - r[2]) <= 2000], key=lambda r: r[2])
    names = {0: "input panel window", 1: "pack door opening"}
    for i, r in enumerate(big):
        ax.text((r[0] + r[1]) / 2, (r[2] + r[3]) / 2, names.get(i, ""), ha="center", va="center", fontsize=8, color="#6B7280")
    ax.text(DD / 2, -10, "case underside", ha="center", va="top", fontsize=8, color="#4B5563")
    ax.set_xlim(-10, DD + 10); ax.set_ylim(-25, H + 10)
    def kind3(y, z):
        if abs(y - 139.5) < 1:
            return "H"
        if abs(z - 118) < 1:
            return "R"
        if abs(z - 126) < 1:
            return "P"
        return "F"
    by = {}
    for y, z in sorted(circ.get(3.3, [])):
        k = kind3(y, z)
        by.setdefault(k, []).append((y, z))
        ax.text(y + 3, z + (3 if z > 50 else -9), k, fontsize=7, color="#7C3AED", fontweight="bold")
    for y, z in circ.get(6.0, []):
        ax.text(y + 5, z + 4, "N", fontsize=7, color="#0F766E", fontweight="bold")
    ax.text(slots[0][0] - 3, (slots[0][2] + slots[-1][3]) / 2, "T", fontsize=8, color=INK, fontweight="bold", ha="right", va="center")
    fmt = lambda pts: [", ".join(f"{y:g} / {z:g}" for y, z in pts[i:i + 2]) for i in range(0, len(pts), 2)]  # noqa: E731
    groups = [("W", "#111827", "Input panel window", [f"{big[0][0]:g} to {big[0][1]:g} along, {big[0][2]:g} to {big[0][3]:g} up"]),
              ("O", "#111827", "Pack door opening", [f"{big[1][0]:g} to {big[1][1]:g} along, {big[1][2]:g} to {big[1][3]:g} up"]),
              ("T", "#111827", f"Intake slots ({len(slots)}), {slots[0][1] - slots[0][0]:g} x {slots[0][3] - slots[0][2]:g}",
               [f"{slots[0][0]:g} to {slots[0][1]:g} along; bottoms at", ", ".join(f"{s_[2]:g}" for s_ in slots) + " up"]),
              ("N", "#0F766E", "Rivet nuts, 6.0 (input panel)", fmt(sorted(circ.get(6.0, []))))]
    for k, t in (("H", "Hinge rivets, 3.3"), ("R", "Shelf rivets, 3.3"), ("P", "Padlock staple rivets, 3.3"),
                 ("F", "Filter frame screws, 3.3")):
        groups.append((k, "#7C3AED", t, fmt(by.get(k, []))))
    _key(fig, 0.62, 0.89, groups, step=0.025)
    fig.text(0.62, 0.11, "Each pair: from the front wall / up from the underside.", fontsize=7.6, color="#4B5563", va="top")
    fig.savefig(OUT / "end-wall-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "end-wall-holes.png")

    # --- output panel plate, seen from the front
    op = C["out_panel"].shape
    px0, px1, pz0, pz1 = D["out_panel"]
    face = [f for f in op.faces() if abs(f.center().Y - (-DD / 2 - P["panel_t"])) < 0.01][0]
    H_ = _holes(face)
    fig, plt = _fig("Output panel plate: cut-outs",
                    "Seen from the front. Distances from the left and bottom edges to the centre of each cut-out, sizes width x height, in mm, from the model.",
                    size=(12, 6.6))
    ax = fig.add_axes([0.03, 0.08, 0.6, 0.8]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), px1 - px0, pz1 - pz0, fc="#E5E7EB", ec=INK, lw=1.2))
    lab = {(-140, 100): "12 V socket", (-90, 100): "barrel", (30, 165): "wake button", (122, 120): "AC outlet",
           (-135, 179): "display", (-7.5, 165): "switch", (-141, 150): "USB-C 1", (-111, 150): "USB-C 2",
           (-77.5, 148.5): "USB-A 1", (-52.5, 148.5): "USB-A 2"}
    rows = []
    for kind, c, sz in H_:
        X, Z = c.X - px0, c.Z - pz0
        name = next((v for (kx, kz), v in lab.items() if abs(c.X - kx) < 3 and abs(c.Z - kz) < 3), "screw hole")
        if kind == "circle":
            ax.add_patch(plt.Circle((X, Z), sz.X / 2, fc="white", ec=INK, lw=0.9))
            size = f"{sz.X:.1f} dia"
        else:
            ax.add_patch(Rectangle((X - sz.X / 2, Z - sz.Z / 2), sz.X, sz.Z, fc="white", ec=INK, lw=0.9))
            size = f"{sz.X:g} x {sz.Z:g}"
        rows.append((name, size, X, Z))
    order = {}
    for n_, s_, X, Z in sorted(rows, key=lambda r: (r[0] != "screw hole", r[2])):
        order.setdefault(n_, []).append((s_, X, Z))
    k = 1
    lines = []
    for n_, items in order.items():
        for s_, X, Z in items:
            dx = 9 if n_ == "screw hole" and X < 200 else (-9 if n_ == "screw hole" else 0)
            ax.text(X + dx, Z, str(k), fontsize=6.5, ha="center", va="center", color="#B91C1C", fontweight="bold")
            lines.append(f"{k}  {n_}: {s_}, {X:g} along, {Z:g} up")
            k += 1
    ax.set_xlim(-5, px1 - px0 + 5); ax.set_ylim(-8, pz1 - pz0 + 5)
    fig.text(0.66, 0.86, "Cut-outs (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(lines):
        fig.text(0.66, 0.82 - i * 0.034, t, fontsize=7.6, color=INK, va="top")
    fig.savefig(OUT / "panel-cutouts.png", facecolor="white"); plt.close(fig); res.append(OUT / "panel-cutouts.png")
    return res


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & bx(x0, x1, y0, y1, z0, z1)


def joints(only=None):
    out = []
    J = []

    def jp(name, keys, box_, color=None):
        return Part(name, win(S(*((keys,) if isinstance(keys, str) else keys)), *box_),
                    color or C[keys if isinstance(keys, str) else keys[0]].color, None, (0, 0, 0), 1.0)

    # 1 lid skirt over the wall, cut through a lid screw
    b1 = (-12, 0, -140, -112, 196, 226)
    J.append(([jp("Lid (top on the wall, skirt outside)", "lid", b1, "#475569"), jp("Front wall", "body", b1, "#CBD5E1"),
               jp("M4 screw into a rivet nut", "lid_screws", b1)],
              "Joint 1: lid on the case (cut through a lid screw)",
              "Seen from the side. The lid top rests on the wall; its skirt hangs 1 mm outside it", dict(elev=0, azim=0)))
    # 2 handle on the lid with the doubler
    b2 = (-125, -60, 0, 20, 212, 232)
    J.append(([jp("Handle base and post", "handle", b2, "#64748B"), jp("Lid", "lid", b2, "#CBD5E1"), jp("Doubler plate", "doubler", b2, "#A16207"),
               jp("M5 bolts and nyloc nuts", "handle_bolts", b2)],
              "Joint 2: handle base, lid and doubler (cut on the centre line)",
              "Seen from the front. Two M5 bolts clamp the handle base, lid and doubler together", dict(elev=0, azim=-90)))
    # 3 corner tab
    b3 = (195, 236, -140, -100, 20, 185)
    tabbox = (L / 2 - P["tab_w"] - 0.01, L / 2 + 0.01, -DD / 2 - P["sheet_t"] - 0.01, -DD / 2, 0, 230)
    tab = win(win(S("body"), *b3), *tabbox)
    J.append(([Part("End wall tab, folded round the corner", tab, "#0F766E", None, (0, 0, 0), 1.0),
               Part("Front wall and end wall", win(S("body"), *b3) - tab, C["body"].color, None, (0, 0, 0), 1.0),
               jp("Blind rivets (3)", "tab_rivets", b3),
               jp("Output panel plate", "out_panel", b3)],
              "Joint 3: corner tab (front right corner)",
              "Seen from the front right. The end wall's tab lies on the outside of the front wall, three rivets", dict(elev=12, azim=-60)))
    # 4 pack on the runners, section across the bay
    b4 = (60, 100, 10 - 15, 135, -10, 112)
    J.append(([jp("SwapCell pack", "pack", b4), jp("Front floor runner", "runner_f2", b4), jp("Back floor runner", "runner_b2", b4),
               jp("Top guide rail", "rail_2", b4), jp("Shelf", "shelf", b4), jp("Case floor and back wall", "body", b4),
               jp("Runner screws from below", "runner_screws", b4)],
              "Joint 4: the pack in its bay (section across the bay)",
              "Seen from the door end. The pack rests on the runner bases; lips and rail stand 1 mm off it", dict(elev=4, azim=0)))
    # 5 catch bracket, catch and pawl, from above
    b5 = (95, 190, -5, 50, 40, 72)
    J.append(([jp("Catch bracket web", "catch_bracket", b5), jp("Class D latch catch", "catch", b5),
               jp("Pack latch pawl and latch face", "pack", b5)],
              "Joint 5: latch catch and the pack's pawl (seen from above, cut at the catch)",
              "Door end to the right. The pawl sits 1 mm behind the catch, so the catch stops the pack sliding out", dict(elev=80, azim=-90)))
    # 6 receptacle bracket and plug, cut on the plug centre line
    yc = D["pack"][6]
    b6 = (-225, -120, yc, 112, -2, 104)
    J.append(([jp("Receptacle bracket", "recept_bracket", b6), jp("SwapCell receptacle", "receptacle", b6),
               jp("Pack plug", "pack", b6), jp("Case floor", "body", b6), jp("Bracket screws", "floor_screws", b6)],
              "Joint 6: receptacle bracket and the pack plug (cut on the plug centre line)",
              "Seen from the front. The plug enters the receptacle with 0.5 mm all round; the receptacle floats on its mount",
              dict(elev=10, azim=-90)))
    # 7 shelf flanges riveted to the walls
    b7 = (140, 232, 60, 132, 92, 135)
    J.append(([jp("Shelf (rear and end flanges)", "shelf", b7), jp("Back and end walls", "body", b7),
               jp("Blind rivets", "shelf_rivets", b7), jp("Top guide rail", "rail_2", b7), jp("Rail screws", "rail_screws", b7)],
              "Joint 7: shelf flanges on the back and end walls (back right corner, inside)",
              "Seen from inside, front left. Each flange is riveted to its wall", dict(elev=30, azim=-135)))
    # 8 door from outside
    b8 = (226, 250, -5, 135, -5, 148)
    J.append(([jp("Pack bay door", "door", b8, "#93C5FD"), jp("Piano hinge", "hinge", b8), jp("Thumb-turn cam latch", "latch", b8),
               jp("Padlock staple through the hasp slot", "staple", b8), jp("End wall", "body", b8),
               jp("Rivets", ("door_rivets", "shelf_rivets"), b8)],
              "Joint 8: pack bay door, hinge, latch and hasp", "Seen from outside the door end",
              dict(elev=12, azim=-15)))
    # 9 cam latch tongue behind the wall
    b9 = (165, 250, 85, 135, 40, 56)
    J.append(([jp("Door", "door", b9, "#93C5FD"), jp("Cam latch, tongue turned to shut", "latch", b9, "#C2410C"),
               jp("End and back walls", "body", b9), jp("SwapCell pack (handle end, lid face)", "pack", b9)],
              "Joint 9: cam latch shut (cut level with the latch, seen from above)",
              "Door end to the right, back wall at the top. The tongue turns behind the end wall, 0.2 mm off it, clear of the pack", dict(elev=80, azim=-90)))
    # 10 output panel on the front wall, section through the 12 V socket
    b10 = (-165, -140, -150, -40, 40, 230)
    J.append(([jp("Output panel plate", "out_panel", b10), jp("12 V socket and USB-C module", "sockets", b10),
               jp("Front wall (window edge)", "body", b10), jp("Inverter", "inverter", b10), jp("Lid skirt", "lid", b10),
               jp("State-of-charge display", "display", b10)],
              "Joint 10: output panel on the front wall (section through the 12 V socket)",
              "Seen from the right. The plate covers the window; module backs pass through it, clear of the inverter",
              dict(elev=6, azim=0)))
    # 11 runner screw from below
    b11 = (-185, -165, 20, 70, -10, 28)
    J.append(([jp("Front floor runner", "runner_f1", b11), jp("Case floor", "body", b11),
               jp("M4 button head into a heat-set insert", "runner_screws", b11)],
              "Joint 11: floor runner fixing (cut through a runner screw)",
              "Seen from the door end. The screw head sits under the floor, inside the 8 mm height of the feet", dict(elev=6, azim=0)))
    for i, (parts, title, sub, kw) in enumerate(J, 1):
        if only is None or only == i:
            out.append(bv.joint(parts, OUT / f"joint-{i:02d}.png", title, subtitle=sub, size=(8, 6), **kw))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = named()
    out = []

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    def pn(name, keys, e, color=None):
        p = part(name, keys, color)
        p.explode = tuple(e)
        return p

    body = M["body"]
    floor = [body, M["runners"], M["catch"], M["recept"]]
    floor2 = floor + [M["inverter"], M["dcdc"], M["protection"], M["fuseblock"]]
    walls = floor2 + [M["fan"], M["filter"]]
    shelf = walls + [M["shelf"], M["rail"]]
    shelf2 = shelf + [M["charger"], M["host"]]
    front = shelf2 + [M["out_panel"], M["modules"]]
    ends = front + [M["in_panel"]]
    doors = ends + [M["door"]]
    lidded = doors + [M["lid"], M["doubler"], M["handle"]]
    ST = [
        ([body], [pn("Floor runners (4 lengths)", RUNNERS + ("runner_screws",), (0, 0, 150), C["runner_f1"].color)],
         "floor runners onto the floor", "Two M4 button heads from under the floor into each length; lips on the outside",
         dict(elev=40, azim=-60)),
        ([body, M["runners"]], [pn("Catch bracket and catch", ("catch_bracket", "catch"), (0, -60, 150)),
                                 pn("Receptacle bracket and receptacle", ("recept_bracket", "receptacle"), (0, 0, 170))],
         "catch bracket and receptacle bracket", "Feet on the floor, M4 button heads from below, nyloc nuts on top",
         dict(elev=40, azim=-60)),
        (floor, [pn("Inverter", "inverter", (0, 0, 160)), pn("DC-DC converter", "dcdc", (0, 0, 160)),
                 pn("Protection plate", "protection", (0, 0, 220)), pn("Fuse block", "fuseblock", (0, 0, 180))],
         "inverter, converter, protection plate and fuse block", "Each on its floor holes; M4 screws from below, nyloc nuts inside",
         dict(elev=40, azim=-60)),
        (floor2, [pn("Exhaust fan and grille", ("fan", "grille"), (-160, 0, 0)), pn("Intake filter frame and pad", "filter_frame", (0, 0, 150))],
         "fan, grille and intake filter frame", "Seen from the front left. Fan inside the fan end, grille outside, four M4 screws; filter frame inside the door end, four M3 screws",
         dict(elev=35, azim=-125)),
        ([M["shelf"]], [pn("Top guide rail (2 lengths)", ("rail_1", "rail_2", "rail_screws"), (0, 0, -70), C["rail_1"].color)],
         "top guide rail onto the shelf", "Seen from below. Hold both lengths under the shelf, end to end; four M3 screws down through the shelf into the inserts",
         dict(elev=-35, azim=-60)),
        (walls, [pn("Shelf with its rail", ("shelf", "rail_1", "rail_2", "rail_screws"), (0, 0, 200), C["shelf"].color)],
         "shelf into the case", "Lower it onto the catch bracket; drill the walls through the flange holes; six rivets; two M4 screws",
         dict(elev=35, azim=-60)),
        (shelf, [pn("Charge controller", "charger", (0, 0, 120)), pn("Host controller on standoffs", "host", (0, 0, 120))],
         "charge controller and host onto the shelf", "Controller on four M4 screws; host on four 6 mm nylon standoffs",
         dict(elev=35, azim=-60)),
        ([M["out_panel"]], [pn("Sockets, switch and wake button", "sockets", (0, -60, 0), "#0F766E"),
                            pn("AC outlet with RCD", "ac", (0, -60, 0), "#334155"), pn("Display", "display", (0, -60, 0))],
         "modules into the output panel plate", "Seen from the front. Each module goes in from the front and is held by its own nut or clip",
         dict(elev=15, azim=-70)),
        (shelf2, [Part("Output panel plate", S("out_panel") + win(S("panel_screws"), -300, 300, -150, -100, 0, 250), "#475569", None, (0, -120, 0), 1.0),
                  Part("Its modules (fitted in step 8)", S("sockets", "ac", "display"), "#0F766E", None, (0, -120, 0), 1.0)],
         "output panel onto the front wall", "Module backs through the window; four M4 screws into the rivet nuts",
         dict(elev=15, azim=-70)),
        (front, [Part("Input panel plate", S("in_panel") + win(S("panel_screws"), 200, 260, -150, 0, 0, 250), "#475569", None, (120, 0, 0), 1.0),
                 Part("Powerpole housings", S("inputs"), C["inputs"].color, None, (120, 0, 0), 1.0)],
         "input panel onto the door end", "Powerpole housings into the plate first; four M4 screws into the rivet nuts",
         dict(elev=20, azim=-30)),
        None,   # step 11: wiring, drawn by wiring()
        (ends, [pn("Door, hinge, latch and staple", ("door", "hinge", "latch", "staple", "door_rivets"), (100, 0, 0), "#3B82F6")],
         "pack bay door", "Rivet the hinge to the wall and door, fit the cam latch, rivet the staple to the wall",
         dict(elev=20, azim=-40)),
        ([M["lid"]], [pn("Carry handle", ("handle", "handle_bolts"), (0, 0, 80)), pn("Doubler plate", "doubler", (0, 0, -110))],
         "handle and doubler onto the lid", "Four M5 bolts down through handle, lid and doubler; nyloc nuts under the doubler",
         dict(elev=10, azim=-60)),
        (doors, [pn("Lid with handle", ("lid", "doubler", "handle", "handle_bolts", "lid_screws"), (0, 0, 160), "#475569")],
         "lid onto the case", "Lower it over the walls; six M4 screws through the skirt into the rivet nuts",
         dict(elev=25, azim=-60)),
        (lidded, [pn("Rubber feet (4)", "feet", (0, 0, -80))],
         "rubber feet", "Seen from below. One self-adhesive foot at each corner of the underside, clear of the screw heads",
         dict(elev=-30, azim=-60)),
        ([q for q in lidded if q is not M["door"]] + [M["feet"]], [pn("SwapCell pack", "pack", (360, 0, 0))],
         "the pack into its bay", "Door open (left out of the picture). Connector first, on the runners, until the catch clicks; shut the door, turn the latch",
         dict(elev=20, azim=-25)),
    ]
    for i, s_ in enumerate(ST, 1):
        if s_ is None or (only is not None and only != i):
            continue
        done, new, title, sub, kw = s_
        out.append(bv.step(done, new, OUT / f"step-{i:02d}.png", f"Step {i}: {title}", subtitle=sub, label_done=False, **kw))
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(13, 7.8), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 130); ax.set_ylim(0, 78); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 76, "PowerBox prototype: block-level wiring (step 11)", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 72.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; crimped lugs or ferrules on every terminal.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(128, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, ORG, BLU, GRY, AC = "#B91C1C", "#C2410C", "#1D4ED8", "#6B7280", "#7E22CE"
    # mains zone
    ax.add_patch(FancyBboxPatch((96, 8), 32, 22, boxstyle="round,pad=0.4", fc="#FEF2F2", ec="#B91C1C", lw=1, ls="--"))
    ax.text(97, 29.4, "230 V zone: certified parts, short leads", fontsize=7.4, color="#B91C1C", va="top", fontweight="bold")
    blk(2, 54, 15, 11, "DC in", "Powerpole, 12 to\n60 V, 200 W", "#991B1B")
    blk(2, 38, 15, 11, "Charger in", "Powerpole,\n54.6 V 5 A brick", "#991B1B")
    blk(24, 54, 17, 11, "Charge controller", "buck-boost MPPT,\nCC-CV 54.6 V", "#D4A017")
    blk(2, 14, 17, 14, "SwapCell receptacle", "pack 39 to 54.6 V;\nCAN; INTERLOCK\nwith 10 k coding", "#1F2937")
    blk(26, 14, 17, 12, "Protection plate", "30 A main fuse,\n60 V DC, 1 kA", "#BE123C")
    blk(50, 30, 20, 30, "48 V bus", "fuse block, 6-way,\n58 V DC rated:\n20 A DC in\n10 A charger\n15 A buck", "#9F1239")
    blk(76, 46, 16, 11, "DC-DC converter", "48 V to 12 V,\n30 A", "#B45309")
    blk(76, 59.5, 16, 8, "12 V outputs", "car socket, barrel,\n10 A fuse", "#1F2937")
    blk(96, 59.5, 18, 8, "USB modules", "USB-C 100 + 60 W,\n2 x USB-A, fused", "#1F2937")
    blk(76, 16, 16, 12, "Breaker and relay", "20 A DC breaker,\nrelay with 47 ohm\npre-charge", "#BE123C")
    blk(99, 16, 12, 10, "Inverter", "300 W, 48 V in,\n230 V out", "#C2410C")
    blk(114, 16, 12, 10, "AC outlet", "30 mA RCD,\nneutral bonded", "#9CA3AF")
    blk(50, 6, 20, 14, "Host controller", "ESP32, CAN,\nrelay drivers,\ncurrent sensors", "#15803D")
    blk(117, 44, 11, 11, "Fan, display", "12 V, from\nthe host", "#4B5563")
    # power
    wire([(17, 59.5), (24, 59.5)], RED); lab(20.5, 61.5, "10 AWG", RED, "center")
    wire([(41, 59.5), (50, 59.5)], RED); lab(45.5, 61.5, "10 AWG", RED, "center")
    wire([(17, 43.5), (50, 43.5)], RED); lab(30, 45.4, "14 AWG", RED, "center")
    wire([(19, 21), (26, 21)], RED, 2.6); lab(22.5, 23, "10 AWG", RED, "center")
    wire([(43, 21), (46, 21), (46, 35), (50, 35)], RED, 2.6); lab(46.6, 28, "10 AWG", RED)
    wire([(70, 51.5), (76, 51.5)], RED); lab(73, 53.4, "14 AWG", RED, "center")
    wire([(84, 57), (84, 59.5)], ORG); lab(84.6, 58.2, "12 V, 10 AWG", ORG)
    wire([(92, 52), (105, 52), (105, 59.5)], ORG); lab(105.6, 55.5, "18 AWG", ORG)
    wire([(70, 38), (73, 38), (73, 22), (76, 22)], RED, 2.6); lab(73.6, 33, "12 AWG", RED)
    wire([(92, 21), (99, 21)], RED, 2.6); lab(95.5, 23, "12 AWG", RED, "center")
    wire([(111, 21), (114, 21)], "#7F1D1D", 2.4); lab(112.5, 13.6, "1.5 mm² mains", "#7F1D1D", "center")
    # signals
    wire([(10, 14), (10, 10), (50, 10)], BLU, 1.2); lab(24, 10, "CAN, twisted pair, 24 AWG", BLU, "center")
    wire([(5, 14), (5, 4), (40, 4)], AC, 1.2); lab(22, 4, "INTERLOCK loop through the wake button (normally closed)", AC, "center")
    wire([(70, 13), (84, 13), (84, 16)], GRY, 1.2); lab(77, 11.6, "relay drive", GRY, "center")
    wire([(60, 20), (60, 30)], GRY, 1.2); lab(60.6, 28.2, "current sense", GRY)
    wire([(70, 7), (129.3, 7), (129.3, 49.5), (128.3, 49.5)], GRY, 1.2); lab(128.7, 38, "fan, display", GRY, "right")
    wire([(66, 20), (66, 26), (44, 26), (44, 54)], GRY, 1.2); lab(44.6, 46, "set point", GRY)
    ax.text(2, 70, "Safety: pack out and main fuse out until the stop points in section 6 of the plan; the 230 V side is checked by a qualified electrician.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 67.2, "Red: 48 V power. Orange: 12 V. Dark red: 230 V AC. Blue: CAN. Purple: INTERLOCK. Grey: control and sensing.",
            fontsize=7.2, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        name, _, n = w.partition(":")
        r = fns[name](int(n)) if n else fns[name]()
        print(w, "->", r)
