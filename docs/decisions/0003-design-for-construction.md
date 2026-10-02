---
doc_id: PBX-DDR-003
title: PowerBox design for construction
project: PowerBox
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish on 2026-10-02 (Tables 1 to 3); record stays Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Every change in Table 1 was made under Amish's 2026-09-30 instruction to make the design physically buildable. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A4), recorded in the design decisions register (PBX-DEC-001, items 1 to 4). The record stays Draft.

## Context

On 2026-09-30 Amish asked for a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of PBX-PRC-001 showed what PowerBox does and passed a clash check, but many of its parts could not be made or fixed as drawn: the lid sat on the 1.2 mm wall edges with nothing to locate or hold it, the SwapCell pack floated 1 mm above its runners with nothing guiding its sides, the shelf and catch bracket stood on edges with no fixing, the receptacle hung in the air, the door was a solid 6 mm block with no hinge, and the panels were blocks on a solid wall with nowhere for the module bodies to go.

The changes below keep what PowerBox does: the same case size, pack position and SwapCell interface v0.3 (station host, coded INTERLOCK, class D catch and door as second stop), the same electronics, outputs, inputs and safety arrangement. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 64 constructability checks (`python cad/src/model.py --check`): no two of its 45 components overlap, every part that must touch its support does, every clearance is at least the stated value, and the pack slides out through the end opening on its runners without touching anything else. All 64 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The lid was a tray sitting butt on the 1.2 mm wall edges, with no location and no fixing. | The lid top rests on the wall tops and its skirt, now 16 mm deep, hangs outside the walls with a 1 mm gap. Six M4 pan-head screws go through the front and back skirts into rivet nuts set in the walls 7 mm below their top edge. | The skirt locates the lid on all four sides and the 1 mm gap takes the rivet nut flanges. The lid is still removable for service. The case is 3 mm lower overall because the lid no longer stands on top of the walls. |
| P2 | The carry handle stood on the 1.2 mm lid with no fixing and nothing to spread the load. | A bought folding handle with two base plates, held by four M5 bolts through the lid and a 2 mm aluminium doubler plate (240 x 40 mm) underneath, nyloc nuts on the doubler. | The doubler spreads the 9.4 kg carrying load over the thin lid; the load passes through the lid screws into the walls. |
| P3 | The pack floated 1 mm above the floor runners, nothing guided its front and back faces, and the 419 mm runners were too long for a common 3D printer and had no fixing. | Four printed PETG runner lengths (209.4 mm each) with an L section: the pack rests on the 24 mm bases, and 3 mm lips stand 1 mm off its latch face and lid face. Each length is held by two M4 button-head screws from under the floor into heat-set inserts. The top guide rail is printed in two lengths and screwed up into the shelf with M3 screws. | The pack now sits on its runners and is guided on three sides with the 1 mm clearance of the concept. Two short lengths fit a 220 mm printer bed. |
| P4 | The shelf was a 4 mm slab resting only on the catch bracket, with no fixing. | A 2 mm folded aluminium shelf: a 20 mm rear flange and a 20 mm end flange folded up and riveted to the back and door end walls (six 3.2 mm blind rivets), a 15 mm front flange folded down for stiffness, and two M4 screws into the catch bracket's top flange. | Supported on three edges and fixed on all of them; folding 2 mm sheet is a sheet shop job, 4 mm is not. |
| P5 | The catch bracket was a 6 mm plate standing on its edge on the floor, with no fixing. | A 3 mm folded aluminium channel, 80 mm long: its foot is screwed to the floor with two M4 screws and its top flange to the shelf with two more. The class D catch bolts to its web. | The bracket that takes the pack's latch load is now fixed at both ends; the web stays 2 mm in front of the pawl as before. |
| P6 | The SwapCell receptacle hung in the air at the end of the bay. | A 3 mm folded aluminium angle bracket on the floor at the fan end, two M4 screws; the receptacle screws to its web through its floating mount. | Holds the receptacle where the concept put it; the floating mount still lets it meet the plug. |
| P7 | The door was a 6 mm block with a pull and no hinge. A magnetic catch has nowhere to go: there are 5 mm between the pack's lid face and the edge of the opening, and 9 mm of wall behind the opening. | A 1.2 mm aluminium door hinged on its front edge with a stainless piano hinge riveted to the wall and the door; a thumb-turn cam latch through the door whose tongue turns behind the end wall; and a hasp tab at the door's top back corner over a flush padlock staple riveted to the wall. | The front edge has 32 mm of wall for the hinge, the back edge only 9 mm. The cam latch holds the door shut where a magnet cannot fit, and the padlock eye of the concept becomes a hasp and staple. The closed door still stops the pack handle (10 mm clear). |
| P8 | The output and input panels were 4 mm blocks on solid walls; the bodies of the sockets, outlet and display had nowhere to go, and the 12 V socket body would have met the inverter. | A window in each wall (360 x 140 mm in the front wall, 78 x 55 mm in the door end) covered by a 2 mm aluminium panel plate held by four M4 screws into rivet nuts. Each module sits in a cut-out in its plate and its body passes through the window. The 12 V socket and barrel socket move up 15 mm so the socket body clears the inverter by 17 mm. | Bought modules mount in a flat plate, as they are made to; the plate can be cut and labelled before it goes on the case. |
| P9 | The inverter and buck converter had no fixings, and the main fuse, inverter breaker, relay and pre-charge resistor and the 6-way fuse block (BOM line 16) had no place in the case. | Floor holes for the inverter's and converter's feet; a 2 mm protection plate (210 x 34 mm) on the floor between the inverter and the pack bay carrying the main fuse holder, breaker and relay; the fuse block on the floor beside the converter; the host on four 6 mm nylon standoffs. | Every part has a fixing, and the protection parts sit on the short path from the receptacle to the inverter. |
| P10 | The folded tub's corners were not closed. | The end walls carry 15 mm tabs that fold onto the outside of the long walls, three blind rivets each. | A corner any sheet shop can fold and a builder can rivet, with no welding of 1.2 mm aluminium. |
| P11 | The intake filter had no holder, and the fan's four screws would have fallen on the ends of the exhaust slots. | A printed filter frame on four M3 screws inside the door end, holding a washable foam pad over the intake slots. The six exhaust slots behind the fan become one 76 mm hole, with the fan's four holes on a 71.5 mm square around it and the bought grille outside. | The frame holds and releases the pad; the round hole gives the fan about 4,500 mm² of open area, twice the slots it replaces. |
| P12 | Screws under the floor would stop the case standing flat; the rubber feet of BOM line 18 were not modelled. | Four self-adhesive rubber feet, 20 mm across and 8 mm tall, at the corners of the underside. | The screw heads (2.2 mm) sit inside the height of the feet. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 9.42 kg with the pack (was 8.61 kg), 0.58 kg under R10's 10 kg (PBX-CAL-001 v0.2, Table 4). | The shelf, brackets, runners, panel plates, door hardware and fixings drawn with real thickness. |
| Size | 480 x 279 x 275 mm overall (was 482 x 276 x 278 mm); R10 still met with 5 mm to spare in height. | Lid over the walls, 8 mm feet, panel plates. |
| Cost | Value-engineering target: USD 450. Estimated cost of the constructable design: USD 482 (USD 32 over the target); the concept was USD 449. BOM lines 1, 2, 3, 5, 6, 15, 16 and 18 repriced. | Parts added for construction. |
| Thermal | Unchanged: the same heat sources, fan and intake area; the exhaust open area behind the fan rises from about 2,100 to 4,500 mm². | |
| Drawings | PBX-DWG-001 Rev P2; making sketches PBX-DWG-101 to 113 added. | Follows the model. |
| Documents | PBX-CAL-001 v0.2, PBX-REQ-001 v0.5, PBX-PRC-001 v0.6: mass, size and cost; the budget is reported as a value-engineering target. No requirement changed status except R11, now reported against its target. | Follows the model. |

*Table 3. Proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Which edge the door hinges on. The product renders show a back-edge hinge (REVIEW 2026-09-26, item 3); the constructable design hinges on the front edge, so the door opens toward the back of the case. | (a) front edge, as modelled; (b) back edge, which needs the opening narrowed or the case made deeper. | (a): it is the only edge with room for the hinge. Accepted 2026-10-02; the renders are updated to the front-edge hinge. |
| A2 | The cam latch is a thumb turn. Theft resistance is still open (PBX-DDR-001 item 15). | (a) thumb turn plus the padlock hasp, as modelled; (b) a keyed cam latch, about USD 3 more. | (a) for the prototype; decide with item 15. Accepted 2026-10-02; a keyed cam latch (about USD 3) if the first partner runs an unattended or shared charging point (PBX-DEC-001, item 3). |
| A3 | The R10 mass margin is now 0.58 kg on estimated masses. | (a) accept and weigh the prototype at TRL 4; (b) look for mass now (1.5 mm panel plates, lighter runner infill). | (a). Accepted 2026-10-02; weigh at TRL 4. |
| A4 | Whether to accept the design for construction as a whole. | (a) accept P1 to P12; (b) accept with changes. | (a). Accepted 2026-10-02. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan PBX-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept lid, door, panels and fan end; they need updating on Amish's Mac, with the door hinged on its front edge (A1), no door window, a lit rocker main switch and a bare aluminium case (PBX-DEC-001, items 9, 11 and 12).
- Several bought parts must be checked against their datasheets when they are chosen at TRL 4 (the design decisions register PBX-DEC-001 lists them): hole patterns of the catch, receptacle mount, inverter and converter feet, cam latch grip, panel cut-outs, and the voltage rating of the fuse block.
