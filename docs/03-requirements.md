---
doc_id: PBX-REQ-001
title: PowerBox requirements
project: PowerBox
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-24'
  author: Amish Chadha
  change: Removed StepGen as a charging source after StepGen became a walking vehicle (Amish, 2026-09-24)
---

# PowerBox requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be checked by calculation at TRL 3 and revised after co-design sessions.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Store useful energy in one SwapCell pack | 400 Wh or more usable at the pack terminals, using 10 to 100 % state of charge | Calculation from SwapCell capacity and the host's discharge cut-off |
| R2 | Run a household through outage evenings | Two evenings of the reference load profile (Table 1, 203 Wh at the loads) on one full pack | Energy budget calculation including conversion losses and standby |
| R3 | Accept four charging sources | (a) DC input 12 to 60 V, up to 200 W, with maximum power point tracking for a solar panel or another DC source; (b) grid through a certified external charger; (c) SunSpoke by swapping in a charged SwapCell pack; (d) SunSpoke's 100 W panel through the DC input | Design review against the input specification table |
| R4 | Recharge quickly from the grid | 10 to 100 % in 3 h or less | Charger rating and SwapCell charge curve |
| R5 | Recharge from solar in a day | 10 to 100 % in one clear day (4.5 peak sun hours) with a 200 W panel | Solar yield calculation |
| R6 | Use DC and solar input efficiently at low power | DC input conversion efficiency 90 % or more from 40 to 200 W, and stable maximum power point tracking (no stall or hunting) as a panel's output changes with light and temperature | Converter efficiency data; later bench test with a solar panel or solar simulator |
| R7 | Provide the outputs households use | 2 x USB-C PD (one 100 W, one 60 W), 2 x USB-A (12 W each), 2 x 12 V DC (10 A shared), 1 x AC outlet, 300 W continuous pure sine (THD 3 % or less) with GFCI or RCD; total output limited to 400 W | Design review against the output specification table |
| R8 | Waste little energy when idle | Off: 5 % or less of pack energy per month, including cell self-discharge. Ready (display on, outputs off): 1.0 W or less. Inverter switches itself off after 10 min below 5 W | Standby budget calculation; later measurement |
| R9 | Never back-feed household wiring | No AC input connector that can mate with an AC output; AC output only through a GFCI or RCD outlet; grid charging only through a certified external charger with a DC plug; DC bus 60 V or less | Design review and safety checklist |
| R10 | Be carried by one adult | 10 kg (22 lb) or less with pack; 500 x 300 x 280 mm or smaller including handle; one top handle | Massing model, then weighing |
| R11 | Stay within the concept budget | PowerBox parts $450 or less, excluding the SwapCell pack (budgeted with SwapCell) | Priced BOM |
| R12 | Swap packs and show status simply | Pack swapped by hand in 30 s or less without tools; display shows state of charge, input and output power and estimated time remaining, read from the SwapCell CAN messages | Design review; later timed trial with users |

## Assumptions

Table 1. Reference evening load profile (6 pm to 11 pm outage). Proposed for review; the real profile must come from co-design sessions.

| Load | Power | Hours | Energy at the load | Output used |
| --- | --- | --- | --- | --- |
| Three LED bulbs | 3 x 5 W | 5 | 75 Wh | 12 V DC |
| Wi-Fi router and fibre terminal | 12 W | 5 | 60 Wh | 12 V DC |
| Radio | 5 W | 4 | 20 Wh | 12 V DC |
| Four phone charges | about 12 Wh each | | 48 Wh | USB |
| **Total** | | | **203 Wh** | |

- The SwapCell pack is the reference 13S2P pack of the SwapCell interface v0.2: 46.8 V nominal, 39.0 to 54.6 V, about 468 Wh.
- Solar input spends much of the day well below the panel rating (morning, evening and cloud), so the DC input often runs at 40 to 100 W.
- Refrigerators, kettles and other high-power or high-surge loads are out of scope (see PBX-PRB-001).
- Budget: the $450 in `project.yaml` covers the PowerBox itself. A household that needs its own pack also buys a SwapCell pack (about $370 in prototype parts). Whether the budget should include one pack is proposed, awaiting Amish.
