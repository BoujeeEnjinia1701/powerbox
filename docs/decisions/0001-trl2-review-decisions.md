---
doc_id: PBX-DDR-001
title: PowerBox TRL 2 review decisions
project: PowerBox
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the move to SwapCell interface v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 13 to 16 and 18 decided by Amish on 2026-10-02 (PBX-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 12; item 17 accepted by PBX-DDR-002); items 13 to 16 and 18 remained proposed at this record and were decided by Amish on 2026-10-02 as recommended in the design decisions register (PBX-DEC-001, items 3 and 5 to 8): "i approve your recommendations for all 555 open decisions."

## Context

The TRL 2 review note (`docs/REVIEW.md`, sessions of 2026-09-24) listed the PowerBox design choices as "Proposed, awaiting Amish", most with a recommendation, and raised two interface issues with SwapCell (waking the pack and pass-through charging). On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." He also approved three cross-cutting additions to the SwapCell interface (a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles), a rule that shared SwapCell packs are priced once and excluded from each dependent budget, and a rule that co-design partners are chosen per area later.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (2026-09-24) and PBX-PRC-001 v0.3. They are not repeated here.

## Decision

Each item in Table 1 is "Decided by Amish, 2026-09-25: go with recommendation" unless the row says otherwise.

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Pack | Decided by Amish, 2026-09-25: go with recommendation. Removable SwapCell pack; the fixed 12.8 V LiFePO4 pack (about 384 Wh) stays only as a documented fallback | PBX-PRC-001 v0.4, README |
| 2 | Bay layout | Decided by Amish, 2026-09-25: go with recommendation. Horizontal side-loading bay with a door on the end | PBX-PRC-001 v0.4, `cad/src/model.py`, PBX-DWG-001 |
| 3 | DC input | Decided by Amish, 2026-09-25: go with recommendation. One DC input with MPPT for a solar panel or SunSpoke's panel; a second input only if users need two sources at once | PBX-PRC-001 v0.4, PBX-REQ-001 R3 |
| 4 | Grid charging | Decided by Amish, 2026-09-25: go with recommendation. Only through a certified external 54.6 V, 5 A charger brick; no AC inlet on the box | PBX-PRC-001 v0.4, PBX-REQ-001 R9 |
| 5 | AC outlet | Decided by Amish, 2026-09-25: go with recommendation. Include the 300 W AC outlet with auto-off; document a DC-only variant (saves about $92, no mains voltage) | PBX-PRC-001 v0.4 |
| 6 | Enclosure | Decided by Amish, 2026-09-25: go with recommendation. Folded aluminium | PBX-PRC-001 v0.4, `bom/bom.csv` |
| 7 | AC region first | Decided by Amish, 2026-09-25: go with recommendation. 230 V 50 Hz with a 30 mA RCD; 120 V 60 Hz is a later variant | PBX-PRC-001 v0.4, PBX-REQ-001 R7, `bom/bom.csv` lines 9 and 12 |
| 8 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Keep `budget_usd: 450`; it covers the PowerBox parts only. The SwapCell pack is priced once in the SwapCell BOM and excluded here (cross-cutting rule) | `project.yaml` (unchanged), PBX-REQ-001 R11, `bom/bom-notes.md` |
| 9 | Human-powered charging | Decided by Amish, 2026-09-25: go with recommendation. No human-powered input for PowerBox now; a pedal generator could later be a separate repo using the DC input | PBX-PRC-001 v0.4 |
| 10 | Pass-through (station mode) | Decided by Amish, 2026-09-25 (cross-cutting approval): SwapCell adds a charge-while-discharging mode. PowerBox cites SwapCell interface v0.3 item C: host type 3 (station), requested mode 4 (charge-discharge), host charge limit in HOST_HEARTBEAT | PBX-PRC-001 v0.4, PBX-CAL-001 section 4 |
| 11 | Waking the pack | Decided by Amish, 2026-09-25 (cross-cutting approval): SwapCell adds a wake method. PowerBox cites SwapCell interface v0.3 item W: every receiver fits a 10 kΩ coding resistor in its INTERLOCK loop instead of a direct link to ground; no keep-alive cell | PBX-PRC-001 v0.4, PBX-CAL-001 section 4, `bom/bom.csv` line 5 |
| 12 | Latch class | Decided by Amish, 2026-09-25 (cross-cutting approval): SwapCell adds latch classes (item V). PowerBox is not a vehicle and uses a class D catch, with the bay door as a second stop; class V1 applies only if PowerBox is ever carried on a vehicle | PBX-PRC-001 v0.4 |

### Items that remain open

These had no recommendation, or depend on users or on SwapCell, so they stayed **Proposed, awaiting Amish** at this record. All five were decided by Amish on 2026-10-02 (PBX-DEC-001). Item 17 had a recommendation and was decided on 2026-09-25 (PBX-DDR-002).

*Table 2. Open items.*

| # | Item | Status |
| --- | --- | --- |
| 13 | R2 shortfall (1.87 evenings against 2). Options: accept 1.87 evenings and relax R2; discharge to 3.5 % (a 5 % cut-off now gives only 1.97); or revise the reference profile with users (it must fall to about 189 Wh at the loads) | Decided by Amish, 2026-10-02 (PBX-DEC-001, item 5): R2 restated as 1.8 evenings (1.81 with minimum-capacity cells), the 10 % cut-off kept, the reference evening revisited with the first partner's users. |
| 14 | First co-design partner (NGO running community charging points, solar home system distributor, or university group) | Decided by Amish, 2026-10-02 (PBX-DEC-001, item 6): a partner in a 230 V, 50 Hz region that runs or supplies community charging or solar home systems; first candidate type to approach, a solar distribution charity such as SolarAid (Zambia and Malawi). Nothing is agreed. |
| 15 | Theft resistance: is a lockable pack door a priority? The door carries a padlock eye either way | Decided by Amish, 2026-10-02 (PBX-DEC-001, item 3): thumb-turn cam latch plus padlock hasp for the prototype; a keyed cam latch if the first partner runs an unattended or shared charging point. |
| 16 | Energy metering on the display for charging points that charge per phone | Decided by Amish, 2026-10-02 (PBX-DEC-001, item 7): energy and sessions counted per port in the host firmware and shown on the display, approximate and not for billing. |
| 17 | TRL 3 engineering proposals made in this session: a recessed normally closed wake button in series with the coding resistor, the 30 A buck, and the fuse ratings in PBX-CAL-001 | Decided by Amish, 2026-09-25: go with recommendation (PBX-DDR-002) |
| 18 | Clarification requested from SwapCell: may a pack in legacy discharge (state 5) accept a station heartbeat and move to mode 2 or 4 without opening its output? PowerBox's host is powered from the pack and depends on this | Decided by Amish, 2026-10-02 (PBX-DEC-001, item 8): kept with SwapCell as one cross-repo action shared with MotionCore, answer needed before PowerBox's interface is frozen; if no, a small hold-up capacitor for the host. |

## Consequences

- PowerBox now builds to **SwapCell interface v0.3**. The receptacle must carry a 10 kΩ ±1 % INTERLOCK coding resistor; a direct link to SGND would leave the pack output dead.
- The two TRL 2 interface blockers (wake and pass-through) are closed on the SwapCell side. Item 18 is the one remaining interface question.
- The budget stays at $450 and excludes the pack; the BOM totals $449 (PBX-CAL-001), so R11 is at risk on indicative prices.
- R2 stays not met until item 13 is decided.
