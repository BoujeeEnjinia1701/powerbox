---
doc_id: PBX-DEC-001
title: PowerBox design decisions register
project: PowerBox
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for all twelve open decisions on 2026-10-02 (PBX-DDR-003 accepted); moved to decisions made"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Cost USD 483 (USD 33 over the target) with the lit rocker main switch; savings figure USD 433 without the grid charger"
---

# PowerBox design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The inverter's output is isolated from its DC input so its neutral can be bonded to the case and earth pin; its idle draw and light-load efficiency | The 30 mA RCD only works with a bonded neutral; idle draw sets the auto-off case | PBX-CAL-001 section 8; PBX-PRC-001 |
| 2 | The charge controller reaches 90 % or more at 12 V and 200 W and at 40 W, and tracks stably | R6 is at risk on the loss model | PBX-CAL-001 section 3 |
| 3 | The fuse block and its blade fuses are rated 58 V DC or more, and every 48 V fuse 60 V DC or more with at least 1 kA breaking capacity | A short at the pack could draw about 496 A | PBX-CAL-001 section 6; PBX-DDR-003 |
| 4 | The hole patterns of the class D catch, the receptacle's floating mount, and the inverter's and converter's feet | The catch bracket web, receptacle bracket web and floor holes are drilled to suit | PBX-DDR-003 |
| 5 | The cam latch grips a 1.2 mm door against a 1.2 mm wall, and its tongue reaches 15 mm | The tongue must turn behind the end wall | PBX-DDR-003, P7 |
| 6 | The cut-out sizes of every module in the output and input panel plates | The plate cut-outs are drawn from envelopes, not datasheets | PBX-DWG-110, PBX-DWG-111 |
| 7 | The rivet nut hole size (6.0 mm assumed for M4) and the heat-set insert hole sizes (5.6 mm for M4, 4.0 mm for M3) | Each maker gives its own | PBX-DDR-003 |
| 8 | The fan's flow through the filter, grille and 76 mm hole (half of 16 L/s free air assumed) | The 6 K air rise at full load depends on it | PBX-CAL-001 section 9 |

## Value engineering

Value-engineering target: USD 450 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 483 for the PowerBox parts, excluding the shared SwapCell pack (USD 33 over the target). Main cost drivers and savings worth trying:

- The largest lines are the inverter (USD 70), the grid charger brick (USD 50), the output panel modules (USD 46), the protection parts and wiring (USD 38), the enclosure body (USD 38), the pack bay (USD 40), and the charge controller and buck converter (USD 30 each).
- Making the design constructable added USD 33 over the concept's USD 449: rivet nuts and windows in the body, the deeper lid skirt, the handle doubler, the shelf, brackets, runners and rail, the door hinge, cam latch and staple, the filter frame, the protection plate and the counted fixings.
- Savings worth trying: leave out the grid charger where a SwapCell dock is on hand (USD 50, bringing the parts to USD 433); the DC-only variant without the inverter and AC outlet (about USD 92, and no mains voltage in the box); quotes for the folded sheet parts as one batch from one shop; printing the brackets in place of folding them is not worth trying, since they carry the pack's latch load.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-24 | StepGen removed as a charging source; the DC input stays for solar and other DC sources | Amish, 2026-09-24 | PBX-PRC-001 v0.3 |
| 2026-09-25 | TRL 2 items 1 to 12: removable SwapCell pack, side-loading bay, one DC input with MPPT, grid charging through a certified brick only, 300 W AC outlet with a DC-only variant, folded aluminium case, 230 V 50 Hz with a 30 mA RCD, budget for the PowerBox parts only, no human-powered input, station mode, wake by coded INTERLOCK, class D catch | Amish: go with recommendation | PBX-DDR-001 |
| 2026-09-25 | Recessed normally closed wake button, 30 A buck converter, fuse ratings of PBX-CAL-001 | Amish: "i accept all your recommendations, go with them across all repos." | PBX-DDR-002 |
| 2026-09-30 | Fix the design assumptions so the design can be built, and record the changes | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | PBX-DDR-003 (Draft; accepted on 2026-10-02, below) |
| 2026-10-01 | The budget is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register; PBX-CAL-001 v0.2 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 of PBX-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-003, A4 |
| 2026-10-02 | Door hinged on its front edge, as modelled; the renders are updated to match | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-003, A1 |
| 2026-10-02 | Thumb-turn cam latch plus padlock hasp for the prototype; a keyed cam latch (about USD 3 more) if the first partner runs an unattended or shared charging point | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-001, item 15; PBX-DDR-003, A2 |
| 2026-10-02 | R10 mass margin of 0.58 kg accepted; the prototype is weighed at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-003, A3 |
| 2026-10-02 | R2 restated as 1.8 evenings of the 203 Wh reference evening on one full pack (1.81 with minimum-capacity cells); the pack's 10 % cut-off is kept; the reference evening is revisited with the first partner's users | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-001, item 13 |
| 2026-10-02 | First partner: one in a 230 V, 50 Hz region that runs or supplies community charging or solar home systems where outages are routine. First candidate type to approach: a solar distribution charity such as SolarAid, which works in Zambia and Malawi | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-001, item 14 |
| 2026-10-02 | Energy and charge sessions counted per port in the host firmware and shown on the display, labelled as approximate and not for billing | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-001, item 16 |
| 2026-10-02 | The legacy-to-station question is kept with SwapCell as one cross-repo action shared with MotionCore, with an answer asked for before PowerBox's interface is frozen; if the answer is no, a small hold-up capacitor for the host is planned across the mode change | Amish: "i approve your recommendations for all 555 open decisions." | PBX-DDR-001, item 18 |
| 2026-10-02 | Bare 5052 aluminium case for the prototype; powder coat only for a product version, once priced, with the earth bond points masked | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 4 |
| 2026-10-02 | AC socket: the national socket of the first partner's country, with its earth pin bonded to the case; never a multi-standard universal socket | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 5 |
| 2026-10-02 | No window in the pack bay door | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 2 |
| 2026-10-02 | Lit rocker main switch | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, item 6 |
