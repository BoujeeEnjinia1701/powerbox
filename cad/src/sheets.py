"""PowerBox general arrangement drawing PBX-DWG-001 (Rev P2, constructable design PBX-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/PBX-DWG-001.svg, .pdf and .png from the parametric model.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["powerbox-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="PowerBox", title="General arrangement, SwapCell station", dwg_no="PBX-DWG-001",
          rev="P2", author="Amish Chadha", date="2026-10-01", concept=True,
          material="Case, lid, door: 1.2 mm 5052 Al; shelf 2 mm, brackets 3 mm Al; runners and rail printed PETG. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA, SwapCell interface v0.3 (PBX-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Constructable design, PBX-DDR-003", "2026-10-01", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Body {P['case_l']:.0f} x {P['case_d']:.0f} x {P['case_h']:.0f}; overall 480 x 279 x 275",
    f"Sheet {P['sheet_t']} Al; lid skirt {P['lid_h']:.0f} over the walls, 6 M4 screws",
    f"Handle span {P['handle_span']:.0f} on a 2 mm doubler; 8 mm rubber feet",
    "Pack bay: SwapCell interface v0.3, pack 340 x 90 x 80,",
    "  393 overall; inserted from +X end, connector first",
    f"Printed runners and top rail, {P['guide_clear']:.0f} clearance per side",
    "Class D catch on a folded 3 mm bracket; 2 mm folded shelf",
    "Door hinged on its front edge; cam latch; padlock hasp",
    "Receptacle: floating mount, 10 kOhm INTERLOCK coding",
    "  resistor (v0.3 item W); 120 ohm CAN termination",
    "Station host type 3, mode 4 charge-discharge, 5.0 A max",
    "Front: USB-C 100 + 60 W, 2 x USB-A, 2 x 12 V, 230 V RCD",
    "+X end: DC in 12 to 60 V 200 W, charger in 54.6 V 5 A",
    "Main fuse 30 A, inverter breaker 20 A (PBX-CAL-001)",
    "Mass about 9.4 kg with pack (PBX-CAL-001 v0.2)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/PBX-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/PBX-DWG-001.svg, .pdf, .png")
