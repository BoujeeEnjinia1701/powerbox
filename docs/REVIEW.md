# Review note: PowerBox

## Session 2026-09-25: recommendations accepted

### Decisions applied

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every PowerBox item marked awaiting Amish that carried a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (PBX-DDR-002 v0.1).

| Item | Before | After | Numbers |
| --- | --- | --- | --- |
| Recessed normally closed wake button in the INTERLOCK loop | Engineering proposal, awaiting Amish | Decided | No change; already in BOM line 11 and the model |
| 48 V to 12 V buck | 30 A proposed (20 A at TRL 2) | Decided at 30 A | 20 A (240 W) at TRL 2, 30 A (360 W) now, for 26.5 A demand; $30, already in the BOM |
| Fuse ratings | Proposed in PBX-CAL-001 Table 3 | Decided | 30 A main fuse, 60 V DC or more, 1 kA breaking; 20 A inverter breaker; unchanged |
| TRL 2 list items 1 to 8 and human-powered charging | Already decided in PBX-DDR-001 but still worded "Proposed, awaiting Amish" in this note | Wording updated below | None |

What changed: PBX-PRC-001 v0.4 to v0.5 (item 17 status and the fuse ratings in the key design choices); PBX-DDR-001 v0.1 to v0.2 (item 17 decided); PBX-DDR-002 v0.1 added; `project.yaml` trl_evidence lists DDR-002; README gains the concept rationale, burning platform, where it could be used and what sparked the idea sections. The budget stays at $450 (PowerBox parts, pack excluded). No requirement, calculation, BOM line, model geometry or drawing changed, because the accepted items were already designed in at TRL 3; PBX-CAL-001 stays at v0.1 and PBX-DWG-001 at Rev P1. All PDFs, drawing sheets and media were regenerated so the footer shows designmolecule.com.

### Requirement status (PBX-CAL-001, unchanged)

| ID | Result | Status |
| --- | --- | --- |
| R2 | 1.87 evenings per pack | **Not met** |
| R6 | 90.5 % worst case in the loss model | At risk |
| R11 | $449 against $450 | At risk |
| R12 | Swap time and display need users | Not verifiable at TRL 3 |
| R1, R3, R4, R5, R7, R8, R9, R10 | As in the TRL 3 session below | Met (R3, R7, R9 by design review) |

### Still awaiting Amish (no recommendation)

- R2 shortfall (PBX-DDR-001 item 13): relax R2, discharge to 3.5 %, or revise the reference evening with users.
- First co-design partner (item 14).
- Theft resistance, a lockable pack door (item 15).
- Energy metering for charging points (item 16).

### Cross-repo actions

- **SwapCell:** answer whether a pack in legacy discharge (state 5) may accept a station heartbeat and move to mode 2 or 4 without opening its output (PBX-DDR-001 item 18). PowerBox's host is powered from the pack and depends on this. Not changed locally.

### TRL 4

TRL 4 remains on hold by Amish's instruction. `trl: 3` and `trl_target: 3` are unchanged. Buying and wiring the fuses, buck and wake button, and any bench test, are TRL 4 and were not started.

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (PBX-DDR-001 v0.1): Amish's 2026-09-25 decisions (items 1 to 12) and the items still open (13 to 18).
- `docs/04-calcs/01-sizing.md` (PBX-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: energy, charging, converter efficiency, station mode and wake against SwapCell interface v0.3, outputs and pack current, fuses and pre-charge, standby, thermal, mass, cost and runtime, with a results table for R1 to R12.
- `cad/src/model.py`: parametric build123d model (case, lid, handle, SwapCell v0.3 pack envelope with plug, handle zone and latch pawl, bay with runners, top rail, class D catch and receptacle, door, electronics, panels, fan). Exports `cad/step/` and `cad/stl/` (assembly, enclosure, pack bay, reference pack) and runs a clash check (none found).
- `cad/src/sheets.py` and `cad/drawings/PBX-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, marked not for fabrication. PBX-DWG-001 was free because the concept blueprint uses PBX-DWG-010.
- `bom/bom.csv` (18 lines, every line priced with a supplier or supplier type) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from `model.py`; all media regenerated (hero, blueprint, cutaway, exploded, flow, `model.glb`, `viewer.html`) and checked by eye; temporary `media/_views*` folders deleted.
- `docs/01-problem.md`, `docs/02-concept.md` and `docs/03-requirements.md` moved to v0.4 (they were already at v0.3 after the StepGen change on 2026-09-24), with decisions recorded, SwapCell interface v0.3 and numbers from PBX-CAL-001. The requirements table now has a status column.
- `project.yaml`: trl 3, trl_target 3, trl_evidence updated. `README.md`: TRL badge, budget scope, TRL 3 summary and key components. `budget_usd` stays at 450.

### Requirements (PBX-CAL-001)

| ID | Result | Status |
| --- | --- | --- |
| R2 | 1.87 evenings per pack (225 Wh per evening from the pack, 419 Wh usable) | **Not met** |
| R6 | 90.5 % at 12 V and 200 W in a loss model; 93 % or more elsewhere; MPPT stability not analysed | At risk |
| R11 | $449 of PowerBox parts against $450 | At risk |
| R12 | 30 s swap and status display by design; needs users | Not verifiable at TRL 3 |
| R1, R4, R5, R8, R10 | 419 Wh; 2.1 h grid; full in 0.70 solar day; 3.2 % per month off and 0.6 W ready; 8.6 kg and 482 x 276 x 278 mm | Met |
| R3, R7, R9 | Sources, outputs and back-feed rules | Met (design review) |

Corrections to TRL 2 numbers: the 48 V to 12 V buck was undersized (26.5 A needed, 20 A fitted; now 30 A); usable energy 421 to 419 Wh; a 5 % cut-off gives 1.97 evenings, not 2.0; mass 8.3 to 8.6 kg; PowerBox parts $435 to $449; pack price $370 to $414.

SwapCell interface v0.3 closes both TRL 2 interface issues: PowerBox's receptacle carries the 10 kΩ INTERLOCK coding resistor (item W), so a sleeping pack wakes without a keep-alive cell, and PowerBox is a station host (type 3) that requests mode 4 to charge while running loads (item C). The worst net charge current in station mode is 4.48 A, inside the 5.0 A limit. The bay uses a class D catch (item V).

### Decisions recorded (PBX-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: removable SwapCell pack (fixed LiFePO4 pack as fallback); horizontal side-loading bay; one DC input with MPPT; grid charging only through a certified external charger; 300 W AC outlet with auto-off and a documented DC-only variant; folded aluminium enclosure; 230 V 50 Hz with a 30 mA RCD first; budget kept at $450 for the PowerBox parts, excluding the pack (priced once in SwapCell); no human-powered input now. Cross-cutting approvals cited as SwapCell interface v0.3 items W, C and V.

### Still awaiting Amish (as of this session; see the 2026-09-25 recommendations session above for the current list)

- R2 shortfall: relax R2 to 1.87 evenings, discharge to 3.5 %, or revise the reference evening with users (about 189 Wh at the loads). No recommendation was made at TRL 2, so none is recorded as decided.
- First co-design partner (portfolio rule: chosen per area later).
- Theft resistance (lockable door) and energy metering for charging points.
- For SwapCell (not changed locally): may a pack in legacy discharge accept a station heartbeat and move to mode 2 or 4 without opening its output? PowerBox's host is powered from the pack and depends on this.

### Safety concerns

- RCD function depends on an inverter with an output isolated from its DC input, so its neutral can be bonded to the case and earth pin. Not yet confirmed from a datasheet.
- A short at the pack could draw about 496 A; every 48 V fuse needs a 60 V DC rating and at least 1 kA breaking capacity.
- In station mode PowerBox is a charger: the host must hold net charge at or below 5.0 A, especially when the fixed 5 A grid charger and solar are both connected.
- The wake button opens the INTERLOCK loop; pressed while running it drops the output, so it is recessed.
- Back-feeding through improvised double-male cords remains a user risk; labels and the guide must warn.
- About 60 W of heat at full load while charging needs the fan; not for closed cupboards or bags. Not for life-support equipment.

### Other notes

- No TRL 4 material exists in the repo (`build-log/` holds only its README; `electronics/` and `firmware/` are empty). None was created.
- No unchecked citations were listed; prior work in PBX-PRB-001 carries no links.

### Recommended next step

TRL 4 is on hold by Amish's instruction, so the next step is a decision, not a build: Amish to choose how to handle R2 and confirm the engineering proposals, and SwapCell to answer the legacy-to-station question. For the record only, TRL 4 would need a bench test article of the bay and receptacle, named inverter and charge controller parts with datasheets confirming neutral bonding and 90 % efficiency at 40 W and 12 V, a lab test report (TST, environment: lab) and build log entries.

## Session 2026-09-24: remove StepGen as a charging source

### What changed

- StepGen removed as a charging source in `project.yaml`, `README.md`, `docs/01-problem.md` (v0.3), `docs/02-concept.md` (v0.3), `docs/03-requirements.md` (v0.3) and `cad/src/concept_media.py`; media and `docs/pdf/` regenerated. Why: Amish decided on 2026-09-24 that StepGen becomes a walking-treadmill vehicle driven by a hub motor on a SwapCell pack, so it no longer generates power for PowerBox. A pack can still move between PowerBox and StepGen, as with SunSpoke.
- The DC input stays, with MPPT, for a solar panel, SunSpoke's panel or any 12 to 60 V DC source. R3 now lists solar and other DC sources; R6 is now "Use DC and solar input efficiently at low power" (90 % or more from 40 to 200 W, stable tracking). The StepGen rows in Table 2 and the human-power safety bullet are gone. Budget, TRL and other design content are unchanged.

### Decided (was proposed, awaiting Amish)

- **Human-powered charging in future.** Decided by Amish, 2026-09-25: go with recommendation (no human-powered input now; PBX-DDR-001 item 9). Options: (a) no human-powered input for PowerBox; (b) a pedal generator as a separate future repo that plugs into the existing DC input. Recommendation: not now; stay within the current scope.

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (PBX-PRB-001 v0.2): the problem, users and context (outage-prone homes, off-grid households, informal settlements, community charging points, repair shops), constraints, out of scope, prior work without links, open questions; co-design checklist kept.
- `docs/03-requirements.md` (PBX-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets and planned verification, and a reference evening load profile (203 Wh at the loads).
- `docs/02-concept.md` (PBX-PRC-001 v0.2): how it works, components table numbered to the BOM and exploded view, first-order numbers with assumptions, runtime table, input and output specification, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model (aluminium case, lid, handle, SwapCell pack to the v0.2 envelope, pack bay and receptacle, bay door, charge controller, host controller, inverter, DC-DC converter, output panel, AC outlet, display, input panel, fan) with a table top and phone for scale.
- `media/`: hero, blueprint sheet (PNG and PDF), cutaway, exploded view with BOM callouts, energy flow diagram (estimates marked), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 18 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and links line added.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Usable energy, one SwapCell pack | about 421 Wh (10 to 100 %) | R1 met |
| Reference evening (203 Wh at the loads) | 225 Wh from the pack; about 1.9 evenings per pack | R2 **not met** (target 2) |
| Grid charge, 10 to 100 % | about 2.1 h | R4 met |
| Solar, 200 W panel | about 635 Wh per clear day; full in one day | R5 met |
| Inverter idle if left on | about 190 Wh per day | Auto-off needed (R8) |
| Standby, ready | about 0.6 W | R8 met |
| Mass and size | about 8.3 kg with pack; 482 x 276 x 278 mm overall | R10 met, tight on height |
| PowerBox parts cost | about $435, excluding the SwapCell pack | R11 met, about $15 margin |
| Cost with one pack | about $805 | Above the $450 budget |

Requirements not met or at risk: R2 is missed by about 5 %; R6 is at risk until a converter is chosen and its efficiency at 40 W is known; R11 is met only because the pack is excluded.

### Proposed at TRL 2; status after 2026-09-25

Items 1 to 8 are now "Decided by Amish, 2026-09-25: go with recommendation" (PBX-DDR-001 items 1 to 8). Items 9 and 10 had no recommendation and remain "Proposed, awaiting Amish".

1. Removable SwapCell pack (recommended), with a fixed internal 12.8 V LiFePO4 pack (about 384 Wh, about $110) kept as a documented fallback.
2. Horizontal side-loading pack bay with an end door, rather than a tall top-loading bay.
3. One DC input with MPPT for solar and SunSpoke's panel; a second input later if users need both at once (about $30 more).
4. Grid charging only through a certified external 54.6 V, 5 A charger brick; no AC inlet on the box.
5. Include the 300 W AC outlet with auto-off, and document a DC-only variant (saves about $92, no mains voltage).
6. Folded aluminium enclosure over a rugged plastic case.
7. AC region first: 230 V 50 Hz with a 30 mA RCD.
8. Budget: keep $450 for PowerBox parts excluding the pack (recommended), or raise to about $850 to include one pack. `project.yaml` is unchanged at $450.
9. R2 shortfall (still proposed, awaiting Amish): accept 1.9 evenings, allow discharge to 5 % (about 2.0 evenings, more cell wear), or revise the load profile with users.
10. First co-design partner (still proposed, awaiting Amish): an NGO running community charging points, a solar home system distributor, or a university group in an outage-prone city.

### Interface issues to raise with SwapCell (not changed locally)

- **Waking the pack.** WAKE needs 5 to 15 V from the host, but a battery-only host like PowerBox has no source when the pack is asleep and no charger is connected. Options: a keep-alive cell in PowerBox, wake on interlock closure, or a wake button on the pack.
- **Pass-through.** The v0.2 behavior rules allow charging only with a dock heartbeat and define no host that charges and discharges at once. PowerBox needs a "station" host type with a combined mode to run the router while charging from solar.

### Safety concerns

- Back-feeding: the box has no AC inlet and grid charging is DC only, but users can still improvise double-male cords. Labels and the user guide must warn clearly.
- GFCI or RCD on an inverter output only works if the output neutral is bonded to the case and earth; many small inverters float. This must be confirmed for the chosen inverter.
- A 468 Wh lithium-ion pack in a living space: fused, BMS-protected, charged on a non-combustible surface, with ventilation and temperature cut-offs. The charge controller sits on a shelf above the pack; its heat path needs checking.
- Inverter heat (about 41 W at full load) needs the fan; the box must not be used in a closed cupboard or bag.
- PowerBox must not be relied on for life-support equipment.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to size the converters, inverter and fuses by calculation, confirm the inverter's GFCI or RCD compatibility and idle draw, settle the SwapCell wake and pass-through questions with the SwapCell design, and produce the parametric model and drawing sheet.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal, product-style renders. It changes no requirement, calculation, BOM line, drawing or `cad/src/model.py`.

### What was added

- `cad/src/product_model.py`: `product_parts()` returns 82 parts (46 shell, 20 internal, 4 accessory, 12 context), each with a colour, a render material, a BOM line and an explode offset. It imports `PARAMS`, `pack_frame()` and the model.py geometry, so every main dimension and interface is unchanged (460 x 260 x 220 mm case, 12 mm lid, SwapCell v0.3 pack envelope, plug, handle, latch pawl, bay, receptacle and all panel and component envelopes). model.py has no `derived()`; `pack_frame()` plays that role.
- Appearance detail: filleted case and lid corners with a parting-line groove at the lid joint; stadium exhaust slots and four lid screws; folding handle with hinge posts, ferrules and a ribbed rubber grip; output panel with USB-C PD and USB-A ports, 12 V car socket and barrel jack, rocker main switch with a lit indicator, the recessed wake button, printed port marks and a teal accent band; display with a lit state-of-charge readout; AC outlet module with socket recess, earth clips, RCD test and reset buttons and a lit status light; Anderson PP45 input panel with red and black housings and printed marks; pack bay door with a clear window onto the SwapCell pack, pull, padlock eye, hinge knuckles and catch strip; ringed fan grille; rubber feet; name plate.
- Internals for the exploded view: filleted SwapCell pack with lid-face ribs, label, plug, rubber handle and latch pawl; bay runners, rail, shelf, catch bracket and receptacle; finned charge controller; host board with ESP32 shield and relays; finned inverter and buck converter; fan; intake dust filter.
- Accessory: the grid charger brick (BOM 17) with its Powerpole DC lead, shown only in the exploded view.
- Context: a compact oak bench top, a small solar panel on a folding stand behind the case wired to the DC IN Powerpole, and a phone charging from USB-C.
- `TITLE` and `RENDER_VIEWS`: hero (front right, 30 deg elevation, with context), exploded (front right, 28 deg) and detail (front, 12 deg, shell only, framing the output panel).
- README hero image now points to `media/render-hero.png` with a link to `media/render-exploded.png`. The render files are produced later by the orchestrator.

### Differences from model.py (each Proposed, awaiting Amish)

1. **Rubber feet.** Four 2 mm rubber feet (BOM 18) sit under the case floor, so the overall height becomes 280 mm and uses the 2 mm spare in R10. Recommendation: recess the feet into dimples in the folded floor so R10 keeps its margin.
2. **Window in the pack bay door.** The door (BOM 6) has a 26 x 76 mm clear polycarbonate window so the pack is visible. It is not in model.py or the BOM. Recommendation: keep it as a render option only until TRL 4; a window adds cost and a sealing detail.
3. **Door hardware.** The padlock eye is a separate tab beside the pull (model.py folds it into the pull block), and the hinge knuckles are drawn on the back edge of the door (model.py does not say which edge). Recommendation: hinge on the back edge so the door opens toward the user at the front.
4. **Finish and colour.** The case is shown powder-coated light grey with a dark lid, dark panels and a teal accent. The BOM gives bare 5052 aluminium. Recommendation: powder coat, priced within the BOM 1 and 2 lines at TRL 4.
5. **AC socket type.** The 230 V outlet is drawn with a round, earth-clip recess (CEE 7/3 style). The BOM does not name a socket type. Recommendation: choose the socket type with the first co-design partner's country.
6. **Lit main switch.** The rocker main switch carries a lit indicator; BOM 11 names a plain main switch. Recommendation: accept, since a lit switch shows the box is on and costs little.
7. **Grid charger size.** The charger brick is drawn at 170 x 72 x 42 mm, an assumption; model.py does not model BOM 17.

Powerpole housings, USB ports and sockets are drawn inside the model.py envelopes at appearance scale, not at connector-datasheet dimensions.

### Scope

This is an appearance model only, with no tolerances and no fabrication detail. `trl` stays 3, `trl_target` stays 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.
