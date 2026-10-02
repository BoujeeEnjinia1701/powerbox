---
doc_id: PBX-REQ-001
title: PowerBox requirements
project: PowerBox
doc_type: Requirements
version: "0.6"
status: Draft
date: '2026-10-02'
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's decisions (PBX-DDR-001), including the 230 V AC region and a budget that excludes the pack; SwapCell interface v0.3; status from PBX-CAL-001
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: R10 and R11 status for the constructable design (PBX-DDR-003, PBX-CAL-001 v0.2); budget treated as a value-engineering target
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R2 restated as 1.8 evenings (Amish, 2026-10-02, PBX-DEC-001 item 5); met on paper"
---

# PowerBox requirements

These requirements are checked by calculation in PBX-CAL-001 (TRL 3). They are still proposals, not user-validated needs, and will be revised after co-design sessions. On paper, nine are met, including R2 as restated by Amish on 2026-10-02 (1.87 evenings against 1.8); R6 is at risk, R11 is reported against its value-engineering target (USD 32 over), and R12 cannot be verified until users try a pack swap. The Status column gives the TRL 3 result.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (PBX-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Store useful energy in one SwapCell pack | 400 Wh or more usable at the pack terminals, using 10 to 100 % state of charge | Calculation from SwapCell capacity and the host's discharge cut-off | Met, 419 Wh |
| R2 | Run a household through outage evenings | 1.8 evenings of the reference load profile (Table 1, 203 Wh at the loads) on one full pack, at the pack's 10 % cut-off (restated from 2 evenings by Amish on 2026-10-02, PBX-DEC-001 item 5) | Energy budget calculation including conversion losses and standby | Met on paper: 1.87 evenings (1.81 with minimum-capacity cells) |
| R3 | Accept four charging sources | (a) DC input 12 to 60 V, up to 200 W, with maximum power point tracking for a solar panel or another DC source; (b) grid through a certified external charger; (c) SunSpoke by swapping in a charged SwapCell pack; (d) SunSpoke's 100 W panel through the DC input | Design review against the input specification table | Met (design review) |
| R4 | Recharge quickly from the grid | 10 to 100 % in 3 h or less | Charger rating and SwapCell charge curve | Met, 2.1 h |
| R5 | Recharge from solar in a day | 10 to 100 % in one clear day (4.5 peak sun hours) with a 200 W panel | Solar yield calculation | Met, full in 0.70 day |
| R6 | Use DC and solar input efficiently at low power | DC input conversion efficiency 90 % or more from 40 to 200 W, and stable maximum power point tracking (no stall or hunting) as a panel's output changes with light and temperature | Converter efficiency data; later bench test with a solar panel or solar simulator | At risk, 90.5 % worst case in the loss model |
| R7 | Provide the outputs households use | 2 x USB-C PD (one 100 W, one 60 W), 2 x USB-A (12 W each), 2 x 12 V DC (10 A shared), 1 x AC outlet, 230 V 50 Hz, 300 W continuous pure sine (THD 3 % or less) behind a 30 mA RCD; total output limited to 400 W | Design review against the output specification table | Met (design review) |
| R8 | Waste little energy when idle | Off: 5 % or less of pack energy per month, including cell self-discharge. Ready (display on, outputs off): 1.0 W or less. Inverter switches itself off after 10 min below 5 W | Standby budget calculation; later measurement | Met, 3.2 % per month off, 0.6 W ready |
| R9 | Never back-feed household wiring | No AC input connector that can mate with an AC output; AC output only through a 30 mA RCD outlet with the inverter neutral bonded to the case; grid charging only through a certified external charger with a DC plug; DC bus 60 V or less | Design review and safety checklist | Met (design review) |
| R10 | Be carried by one adult | 10 kg (22 lb) or less with pack; 500 x 300 x 280 mm or smaller including handle; one top handle | Massing model, then weighing | Met, 9.4 kg, 480 x 279 x 275 mm (constructable design) |
| R11 | Keep to the value-engineering target | PowerBox parts against a value-engineering target of USD 450 (a hypothetical control target, not a limit; Amish, 2026-10-01), including the grid charger and excluding the SwapCell pack, which is priced once in the SwapCell BOM (decided by Amish, 2026-09-25) | Priced BOM | USD 482, USD 32 over the target |
| R12 | Swap packs and show status simply | Pack swapped by hand in 30 s or less without tools; display shows state of charge, input and output power and estimated time remaining, read from the SwapCell interface v0.3 CAN messages; a sleeping pack wakes through the INTERLOCK loop (v0.3 item W) | Design review; later timed trial with users | Not verifiable at TRL 3 |

## Assumptions

Table 1. Reference evening load profile (6 pm to 11 pm outage). Proposed for review; the real profile must come from co-design sessions.

| Load | Power | Hours | Energy at the load | Output used |
| --- | --- | --- | --- | --- |
| Three LED bulbs | 3 x 5 W | 5 | 75 Wh | 12 V DC |
| Wi-Fi router and fibre terminal | 12 W | 5 | 60 Wh | 12 V DC |
| Radio | 5 W | 4 | 20 Wh | 12 V DC |
| Four phone charges | about 12 Wh each | | 48 Wh | USB |
| **Total** | | | **203 Wh** | |

- The SwapCell pack is the reference 13S2P pack of SwapCell interface v0.3: 46.8 V nominal, 39.0 to 54.6 V, 468 Wh nameplate and 466 Wh at 0.2C (SWC-CAL-001). PowerBox is a station host (v0.3 item C) and its receptacle carries the 10 kΩ INTERLOCK coding resistor (item W).
- Solar input spends much of the day well below the panel rating (morning, evening and cloud), so the DC input often runs at 40 to 100 W.
- Refrigerators, kettles and other high-power or high-surge loads are out of scope (see PBX-PRB-001).
- Budget: the USD 450 value-engineering target in `project.yaml` covers the PowerBox itself (decided by Amish, 2026-09-25, PBX-DDR-001). A household that needs its own pack also buys a SwapCell pack, priced once in the SwapCell BOM at about $414 in prototype parts.
- R2: decided by Amish on 2026-10-02 (PBX-DEC-001, item 5): 1.8 evenings, which covers minimum-capacity cells (1.81); the 10 % cut-off is kept, since discharging to 3.5 % would shorten the shared SwapCell pack's life. The 203 Wh reference evening is not yet validated and is revisited with the first partner's users.
