# Review note: PowerBox

## Session 2026-09-24: remove StepGen as a charging source

### What changed

- StepGen removed as a charging source in `project.yaml`, `README.md`, `docs/01-problem.md` (v0.3), `docs/02-concept.md` (v0.3), `docs/03-requirements.md` (v0.3) and `cad/src/concept_media.py`; media and `docs/pdf/` regenerated. Why: Amish decided on 2026-09-24 that StepGen becomes a walking-treadmill vehicle driven by a hub motor on a SwapCell pack, so it no longer generates power for PowerBox. A pack can still move between PowerBox and StepGen, as with SunSpoke.
- The DC input stays, with MPPT, for a solar panel, SunSpoke's panel or any 12 to 60 V DC source. R3 now lists solar and other DC sources; R6 is now "Use DC and solar input efficiently at low power" (90 % or more from 40 to 200 W, stable tracking). The StepGen rows in Table 2 and the human-power safety bullet are gone. Budget, TRL and other design content are unchanged.

### Proposed, awaiting Amish

- **Human-powered charging in future.** Options: (a) no human-powered input for PowerBox; (b) a pedal generator as a separate future repo that plugs into the existing DC input. Recommendation: not now; stay within the current scope.

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

### Proposed, awaiting Amish

1. Removable SwapCell pack (recommended), with a fixed internal 12.8 V LiFePO4 pack (about 384 Wh, about $110) kept as a documented fallback.
2. Horizontal side-loading pack bay with an end door, rather than a tall top-loading bay.
3. One DC input with MPPT for solar and SunSpoke's panel; a second input later if users need both at once (about $30 more).
4. Grid charging only through a certified external 54.6 V, 5 A charger brick; no AC inlet on the box.
5. Include the 300 W AC outlet with auto-off, and document a DC-only variant (saves about $92, no mains voltage).
6. Folded aluminium enclosure over a rugged plastic case.
7. AC region first: 230 V 50 Hz with a 30 mA RCD.
8. Budget: keep $450 for PowerBox parts excluding the pack (recommended), or raise to about $850 to include one pack. `project.yaml` is unchanged at $450.
9. R2 shortfall: accept 1.9 evenings, allow discharge to 5 % (about 2.0 evenings, more cell wear), or revise the load profile with users.
10. First co-design partner: an NGO running community charging points, a solar home system distributor, or a university group in an outage-prone city.

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
