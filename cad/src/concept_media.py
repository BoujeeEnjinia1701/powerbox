"""PowerBox concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the case length (pack slides in from the +X end, connector first toward -X),
Y front (-Y, output panel) to back (+Y), Z up. Units mm. Geometry comes from
cad/src/model.py, so the media match the STEP files and drawing PBX-DWG-001.
Flow values are printed by docs/04-calcs/sizing.py (PBX-CAL-001).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos
from concept import Part, render_all
from model import build_parts

parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# Context for scale: a table top and a phone lying next to the case
table = box(-420, 460, -340, 260, -38, -8)
phone = box(290, 365, -300, -150, -8, 1)
context = [Part("Table top", table, "#C8CDD3"), Part("phone", phone, "#6B7280")]

render_all(
    parts, project="PowerBox", title="Power station concept", dwg_no="PBX-DWG-010", date="2026-10-02", rev="P3",
    key_figures=["One SwapCell pack (interface v0.3): 419 Wh usable",
                 "Evening load 203 Wh: 1.87 evenings (R2 met, target 1.8)",
                 "Full charge: grid 2.1 h, 200 W solar 0.7 day (est.)",
                 "300 W, 230 V pure sine AC with RCD; USB-C PD, USB-A, 12 V",
                 "480 x 279 x 275 mm overall, 9.4 kg with pack (est.)",
                 "Never connects to household wiring"],
    scale_figure=False, context=context, cut_exclude=("Carry handle",),
    flow={"title": "energy per usable cycle, DC input to loads (estimates, PBX-CAL-001)", "unit": "Wh (est.)",
          "stages": [("DC input", 470), ("Charge controller out", 441), ("SwapCell pack, usable", 419),
                     ("Loads (12 V and USB)", 379)],
          "losses": [(1, "Controller", 28), (2, "Cell charge", 22),
                     (3, "Conversion, host", 41)]},
)
