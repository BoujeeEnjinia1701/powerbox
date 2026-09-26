---
doc_id: PBX-DDR-002
title: PowerBox recommendations accepted
project: PowerBox
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted for every item that carried a recommendation; items without one remain proposed, awaiting Amish

## Context

On 2026-09-25 Amish wrote, for every portfolio repo: "i accept all your recommendations, go with them across all repos." PBX-DDR-001 had already recorded his earlier decisions on the TRL 2 review (items 1 to 12). This record applies the new instruction to every remaining PowerBox item marked "Proposed, awaiting Amish" or "awaiting Amish" in `docs/REVIEW.md` and `docs/decisions/` that carries a recommendation. Where a recommendation offered several options, the recommended option is the decision. Items with no recommendation stay open; no choice is invented for them. TRL 4 stays on hold by Amish's instruction, and the repo stays at TRL 3.

## Decision

*Table 1. Items newly decided: "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item (source) | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | Recessed wake button (PBX-DDR-001 item 17, PBX-CAL-001 section 4) | A recessed, normally closed wake button in series with the 10 kΩ INTERLOCK coding resistor wakes a pack that fell asleep in the bay; no keep-alive cell, WAKE pin unused | Already in the design (`bom/bom.csv` line 11, `cad/src/model.py` output panel). Status wording updated in PBX-PRC-001 v0.5 and PBX-DDR-001 v0.2. No geometry, cost or calculation change |
| 2 | 48 V to 12 V buck at 30 A (PBX-DDR-001 item 17, PBX-CAL-001 section 5) | 30 A (360 W) buck for a 26.5 A worst-case demand, replacing the TRL 2 20 A unit | Already in `bom/bom.csv` line 10 ($30) and PBX-CAL-001. Status wording updated in PBX-PRC-001 v0.5. No change to numbers |
| 3 | Fuse ratings (PBX-DDR-001 item 17, PBX-CAL-001 Table 3) | 30 A main fuse and every other 48 V fuse rated 60 V DC or more with at least 1 kA breaking capacity; 20 A inverter breaker; fuse block as in PBX-CAL-001 | Already in `bom/bom.csv` line 16 and PBX-CAL-001. Ratings now listed in PBX-PRC-001 v0.5 key design choices |
| 4 | TRL 2 review list, items 1 to 8, and human-powered charging (`docs/REVIEW.md`, sessions of 2026-09-24) | As recommended; already recorded in PBX-DDR-001 items 1 to 9 | `docs/REVIEW.md` wording updated so the 2026-09-24 lists no longer read "Proposed, awaiting Amish" for these items |

The budget is unchanged: `budget_usd` stays at $450 for the PowerBox parts, excluding the SwapCell pack (PBX-DDR-001 item 8). No requirement text changes: R1 to R12 in PBX-REQ-001 v0.4 already assume the 30 A buck, the fuse ratings and the wake button. PBX-CAL-001, PBX-DWG-001 (Rev P1), the model and the BOM are unchanged because the accepted items were already designed in at TRL 3; only their status changes.

## Items still open

*Table 2. Items with no recommendation: "Proposed, awaiting Amish".*

| # | Item | Why it stays open |
| --- | --- | --- |
| 13 | R2 shortfall (1.87 evenings against 2): relax R2, discharge to 3.5 %, or revise the reference evening with users (about 189 Wh at the loads) | No recommendation was made |
| 14 | First co-design partner | No preference stated; the portfolio picks partners per area later |
| 15 | Theft resistance (lockable pack door) | No recommendation |
| 16 | Energy metering on the display for charging points | No recommendation |
| 18 | SwapCell clarification: may a pack in legacy discharge (state 5) accept a station heartbeat and move to mode 2 or 4 without opening its output? | A question for SwapCell, not a recommendation; listed as a cross-repo action in `docs/REVIEW.md` |

## Consequences

- R2 stays not met, and R6 and R11 stay at risk, because none of the accepted items changes their numbers.
- Work that the accepted items imply beyond paper (buying the fuses, buck and button, wiring the INTERLOCK loop, bench tests) is TRL 4 and is on hold by Amish's instruction.
