---
doc_id: PBX-CAL-001
title: PowerBox sizing calculations
project: PowerBox
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (energy, charging, converter efficiency, outputs, fuses, pre-charge, station mode, standby, wake, thermal, mass, cost) against SwapCell interface v0.3
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Mass, size and cost of the constructable design (PBX-DDR-003); budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R2 status from Amish's 2026-10-02 restatement (1.8 evenings, PBX-DEC-001 item 5): met on paper. Figures not rerun; sizing.py still prints the 2-evening target"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "sizing.py rerun with the R2 target restated to 1.8 evenings (R2 met); lit rocker main switch (USD 1 more) brings the cost to USD 483, USD 33 over the target; results.csv regenerated"
---

# PowerBox sizing calculations

On paper, PowerBox meets nine of its twelve requirements. One SwapCell pack runs the reference evening 1.87 times (1.81 with minimum-capacity cells), short of the two evenings first set; on 2026-10-02 Amish restated R2 as 1.8 evenings (PBX-DEC-001, item 5), so **R2 is met on paper** (the script now carries the restated target). R6 (DC input efficiency) is **at risk**, R11 (cost) is reported against a value-engineering target (USD 483 against USD 450, USD 33 over), and R12 (swap time) cannot be verified until users try it. Version 0.2 repriced and reweighs the constructable design of PBX-DDR-003: 9.42 kg with the pack (R10 still met) and 480 x 279 x 275 mm overall. Two TRL 2 figures were wrong and are corrected here: the 48 V to 12 V converter was too small for the full DC output set (26.5 A needed, 20 A fitted, now 30 A), and the mass rises from about 8.3 to 8.6 kg with the SwapCell v0.3 pack and the real sheet areas. SwapCell interface v0.3 removes both TRL 2 interface blockers: PowerBox wakes the pack through its INTERLOCK loop and runs loads while charging in station mode.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the case dimensions from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Pack | 13S2P, 46.8 V nominal, 39.0 to 54.6 V, 10 Ah, 468 Wh nameplate, 466 Wh at 0.2C (452 Wh with minimum cells), 110 mΩ, 2.85 kg, 393 mm overall | SwapCell interface v0.3, SWC-CAL-001 |
| Pack current limits | 20 A continuous, 35 A for 10 s, 15 A legacy, 5.0 A charge | SWC-PRC-001 v0.3 |
| Charge at 5 A | CC to 85 % state of charge, then 0.6 h CV | SWC-CAL-001 |
| Discharge window | 10 to 100 % state of charge | PBX-REQ-001 R1 |
| Cell charge efficiency | 95 % | SWC-CAL-001 |
| 48 V to 12 V buck | 94 % | Typical non-isolated buck |
| USB modules from 12 V | 93 % | Typical USB-C PD and USB-A modules |
| Grid charger | 90 % | Certified 54.6 V, 5 A unit |
| Charge controller loss | 1.2 W fixed, 2.5 % of power, 45 mΩ on the input path, 20 mΩ on the output path | Typical 200 W synchronous buck-boost; no datasheet yet |
| Inverter | 75 % at 20 W, 78 % at 25 W, 85 % at 60 W, 88 % at 200 to 300 W, 8 W idle, 600 W for 1 s at 85 % | Typical 48 V, 300 W pure sine units; no datasheet yet |
| Standby | Ready 0.6 W (ESP32 0.2, CAN and BMS awake 0.2, display 0.2); converters idle with outputs on 0.4 W; BMS sleep 100 µA; self-discharge 2.5 % per month | Typical parts; SwapCell v0.3 sleep limit |
| Solar | 4.5 peak sun hours, 0.75 derating for heat, dust and angle | Clear day in a sunny region |
| Evening profile | 155 Wh on 12 V, 48 Wh on USB, 5 h | PBX-REQ-001 Table 1 (203 Wh at the loads) |
| Heat loss from the case | 9 W/(m² K) | Still air, natural convection plus radiation |
| Fan | 16 L/s free air, half of that through the filter and grilles | Typical 80 mm, 12 V fan |
| Aluminium | 2,700 kg/m³, 1.2 mm sheet | Decided enclosure material |

## 2. Energy (R1, R2)

The pack holds 419 Wh between 10 and 100 % state of charge (407 Wh with cells at their datasheet minimum), which meets R1.

The reference evening draws 224.8 Wh from the pack: 164.9 Wh for the 12 V loads through the buck, 54.9 Wh for phone charging through the buck and USB modules, and 5.0 Wh for the host, display and idle converters over 5 h. One pack therefore gives **1.87 evenings (1.81 with minimum cells)**: R2 at two evenings was not met, and R2 as restated on 2026-10-02 (1.8 evenings) is met on paper. Two evenings need 449.6 Wh, which means discharging to 3.5 % state of charge. The TRL 2 note said a 5 % cut-off would reach 2.0 evenings; with the SwapCell v0.3 energy of 466 Wh it reaches 1.97, so that option alone does not meet R2 either. At the 10 % cut-off the evening would have to fall to 209.7 Wh from the pack, about 189 Wh at the loads. Amish chose on 2026-10-02 to restate R2 as 1.8 evenings, keep the 10 % cut-off and revisit the reference evening with users (PBX-DEC-001, item 5).

## 3. Charging (R3 to R6)

**Sources (R3).** The DC input (12 to 60 V, 200 W, MPPT), the charger input, a pack swap and SunSpoke's panel on the DC input cover all four sources. Met by design review.

**Grid (R4).** From 10 % the CC phase takes (0.85 - 0.10) x 10 Ah / 5 A = 1.50 h, then 0.6 h of CV: **2.1 h**, against 3 h. The pack takes 441 Wh at its terminals and the charger draws about 492 Wh from the wall, peaking at 303 W. Met.

**Solar (R5).** A 200 W panel gives 200 x 4.5 x 0.75 x 0.94 = **634 Wh per clear day** at the pack terminals (603 Wh stored). A full charge from 10 % needs 441 Wh, or 3.13 peak sun hours: 0.70 of a clear day. Met. SunSpoke's 100 W panel gives 317 Wh per clear day, so one evening's energy takes 0.75 day.

**DC input efficiency (R6).** With the loss model in Table 1 the charge controller stays above 90 % over the whole range, but only just at a 12 V source and full power:

*Table 2. Charge controller efficiency, loss model.*

| Input voltage | 40 W | 100 W | 200 W |
| --- | --- | --- | --- |
| 12 V | 93.2 % | 93.1 % | 90.5 % |
| 18 V | 93.9 % | 94.8 % | 93.9 % |
| 36 V | 94.3 % | 95.9 % | 96.0 % |

At 12 V and 200 W the input current is 16.7 A, and conduction loss dominates. Typical 12 V nominal panels run at 17 to 20 V at maximum power, where the margin is about 4 points. The model parameters are assumptions, and MPPT stability (no stall or hunting) cannot be analysed without the chosen converter and firmware. **R6 is at risk** until a converter datasheet is in hand.

## 4. Station mode and wake (SwapCell interface v0.3)

**Charge-discharge mode (item C).** PowerBox is a SwapCell station host (host type 3) and requests mode 4 when a source and a load are both present. The worst net charge current is 200 W x 0.94 into a pack at 42 V with no load: **4.48 A**, inside the pack's 5.0 A limit. On a typical clear day with the router running the net current is about 2.74 A. The grid charger delivers a fixed 5 A, so when it is connected the host limits the MPPT output to the present load current; net charge then stays at or below 5.0 A. The host sends a 5.0 A charge limit in HOST_HEARTBEAT and follows the pack's PACK_LIMITS.

**Wake (item W).** The PowerBox receptacle fits the 10 kΩ ±1 % coding resistor in the INTERLOCK loop, so the node sits at 3.3 x 10 / 110 = **0.30 V**, inside the pack's 0.24 to 0.37 V window. Inserting a pack gives the falling edge that wakes it. To wake a pack that fell asleep in the bay, a recessed, normally closed wake button in series with the coding resistor opens the loop (node 3.3 V, which re-arms the comparator); releasing it gives a new falling edge. PowerBox needs no keep-alive cell and does not use the WAKE pin.

The pack's output is dead until it hears a heartbeat, but the PowerBox host is powered from the pack. Under the v0.3 rules a valid loop with no heartbeat for 2 s puts the pack in legacy discharge (15 A limit), which boots the host (about 1 W). The host then sends a station heartbeat. Interface v0.3 does not state whether a pack in legacy discharge accepts a heartbeat and moves to mode 2 or 4 without opening its output. PowerBox depends on that, so it is raised with SwapCell as a clarification, not changed locally.

**Latch.** PowerBox is not a vehicle, so the bay uses a class D catch, with the closed bay door as a second stop behind the handle. Carrying the box gives accelerations of a few g at most: about 84 N at 3 g on a 2.85 kg pack, against the 1.72 kN proof load of the pack latch.

## 5. Outputs and pack current (R7)

With every DC output at its rating the 12 V bus must supply 120 W to the sockets plus 184 W / 0.93 = 198 W to the USB modules: **318 W, or 26.5 A**. The TRL 2 design had a 20 A (240 W) buck, which could not carry this. The buck is now **30 A (360 W)**; `bom/bom.csv` line 10 is updated.

The host limits total output to 400 W. At 300 W AC plus 100 W DC the pack supplies 341 + 106 + 1 W; at the 39.0 V minimum that is **11.5 A**, within the 20 A continuous rating, with 1.26 V of sag and 14.5 W of heat in the pack. A 600 W, 1 s inverter surge with 100 W of DC load draws 20.9 A, inside the 35 A, 10 s peak rating. R7 is met by design review; the RCD function depends on the inverter (section 8).

## 6. Protection

*Table 3. Fuse and breaker ratings.*

| Circuit | Design current | Rating |
| --- | --- | --- |
| Main fuse, pack to bus | 11.5 A continuous, 20.9 A for 1 s | 30 A, 60 V DC or higher, 1 kA breaking |
| Inverter feed | 8.7 A continuous, 18.1 A for 1 s | 20 A DC breaker |
| Buck input | 9.8 A at 360 W | 15 A |
| DC input | 16.7 A at 12 V, 200 W | 20 A |
| Charge controller output | 4.8 A | 10 A |
| USB-C 100 W, USB-C 60 W, USB-A pair (12 V side) | 9.0, 5.4, 2.2 A | 10, 7.5, 5 A |
| 12 V sockets | 10 A | 10 A |

A bolted short at the pack terminals could draw about 496 A (54.6 V over 110 mΩ), so every fuse on the 48 V side needs a DC voltage rating of 60 V or more and a breaking capacity of at least 1 kA. The 10 AWG main wiring drops 23 mV over a 0.6 m loop at 11.5 A.

**Pre-charge.** At enable the pack pre-charges only the host and buck input capacitance (about 1,000 µF), matching the SwapCell assumption of 1,000 µF through 100 Ω (99 % in 461 ms). The inverter (about 2,200 µF) is switched in later by its own relay through a 47 Ω resistor: time constant 103 ms, 99 % in 476 ms, 3.3 J in the resistor and a peak of 1.16 A.

## 7. Standby (R8)

Off, the pack sleeps at 100 µA: 3.42 Wh per month, or 0.73 %, on top of about 2.5 % self-discharge, for **3.2 % per month** against 5 %. Ready (display on, outputs off) draws 0.6 W, against 1.0 W, but that is still 14.4 Wh per day, so the host returns to off after 30 min idle. With the DC outputs on and no load the draw is 1.0 W. An inverter left idling at 8 W would use 192 Wh per day, 46 % of the usable energy; the 10 min auto-off wastes 1.3 Wh per event. R8 is met.

## 8. Back-feed and RCD (R9)

There is no AC inlet, grid charging goes through a certified charger with a DC plug, and the DC bus peaks at 54.6 V, below 60 V. R9 is met by design review. The 30 mA RCD only trips if the inverter output neutral is bonded to the case and earth pin, which requires an inverter whose output is isolated from its DC input. This is a purchasing specification (`bom/bom.csv` line 9) to confirm from a datasheet.

## 9. Thermal

At full output while charging at 200 W, the case holds 41 W from the inverter, 6.4 W from the buck, 12 W from the charge controller and 1 W from the host: **60 W**. The fan moves about 8 L/s through the filter and grilles, so the air warms by about 6.2 K. On a typical evening the losses are 4.4 W; over the case's 0.556 m² at 9 W/(m² K) (UA 5.0 W/K) that is a 0.9 K rise, so the fan stays off. The pack sheds 2.75 W at 5 A of charge and 14.5 W at the 11.5 A maximum; the SwapCell thermal risk (R3 of SWC-REQ-001) applies at 20 A, well above what PowerBox draws.

## 10. Mass and size (R10)

*Table 4. Mass budget of the constructable design (PBX-DDR-003).*

| Part | Mass (kg) | Basis |
| --- | --- | --- |
| SwapCell pack | 2.85 | SWC-CAL-001 |
| Enclosure body | 1.22 | 1.2 mm aluminium over 0.436 m², less 0.071 m² of openings, plus 0.012 m² of corner tabs |
| Lid | 0.47 | 1.2 mm aluminium, 464.4 x 264.4 mm with a 16 mm skirt |
| Handle | 0.20 | Estimate |
| Handle doubler | 0.05 | 2 mm aluminium, 240 x 40 mm |
| Inverter | 1.20 | Typical 300 W unit |
| Shelf and brackets | 0.53 | 2 mm shelf and 3 mm brackets, aluminium, model volumes |
| Runners and top rail | 0.21 | Printed PETG, model volumes, 65 % fill |
| Receptacle and catch | 0.15 | Estimate |
| Charge controller | 0.30 | Estimate |
| DC-DC converter, 30 A | 0.35 | Estimate |
| Panel plates | 0.35 | 2 mm aluminium, model volumes |
| Sockets, outlet and display | 0.30 | Estimate |
| Wiring, fuses and protection plate | 0.64 | Estimate |
| Fan, host and filter | 0.30 | Estimate |
| Door, hinge, latch and staple | 0.14 | Estimate |
| Fixings and feet | 0.15 | Counted from the model |
| **Total** | **9.42 (20.8 lb)** | R10 limit 10 kg; concept design 8.61 kg |

The constructable design weighs 0.81 kg more than the concept, mostly in the shelf, brackets and runners that the concept drew without thickness or fixings and the 2 mm panel plates. The margin to R10 is 0.58 kg. The parametric model gives an overall envelope of **480 x 279 x 275 mm** (460 x 260 x 220 mm body; 8 mm feet; lid skirt over the walls; 46 mm handle), which meets the 500 x 300 x 280 mm limit with 5 mm to spare in height. The pack needs 393 mm plus 22 mm for the receptacle and 8 mm of clearance: 423 mm of the 458 mm inside. The charger brick adds about 0.8 kg when carried. R10 is met.

## 11. Cost (R11)

Value-engineering target: USD 450 (a hypothetical control target, not a limit; Amish, 2026-10-01). Estimated cost of the constructable design: **USD 483** for 18 BOM lines, excluding the SwapCell pack, which Amish decided on 2026-09-25 is priced once in the SwapCell BOM (about $414). That is **USD 33 over the target**; the concept design was USD 449. The lit rocker main switch decided on 2026-10-02 adds USD 1 (USD 46 to USD 47 for the output panel line). Making the design constructable added USD 33: rivet nuts and window cut-outs in the body, a deeper lid skirt, the handle doubler, the shelf, brackets, runners and rail, the door hinge, cam latch and staple, the filter frame, the protection plate and more fixings. A household or charging point with a SwapCell dock can omit the grid charger, bringing the parts to USD 433. For reference only, one PowerBox with its own pack is about USD 897. The savings worth trying are listed in the design decisions register (PBX-DEC-001).

## 12. Runtime

*Table 5. Runtime on one full pack (419 Wh usable), single loads.*

| Load | Drawn from the pack | Runtime |
| --- | --- | --- |
| Router and fibre terminal, 12 W on 12 V | 12.8 W | 32.9 h |
| Three 5 W LED bulbs on 12 V | 16.0 W | 26.3 h |
| Radio, 5 W on 12 V | 5.3 W | 78.8 h |
| Phone charge, 12 Wh on USB | 13.7 Wh | 31 charges |
| Laptop, 45 W on USB-C | 51.5 W | 8.1 h |
| Small TV, 60 W on AC | 70.6 W | 5.9 h |
| Desk fan, 25 W on AC | 32.1 W | 13.1 h |
| Maximum AC load, 300 W | 340.9 W | 1.2 h |

Energy flow per usable cycle (DC input to loads, evening mix): 470 Wh at the DC input, 441 Wh out of the controller, 419 Wh usable, 379 Wh at the loads; losses of 28, 22 and 41 Wh.

## 13. Results against requirements

*Table 6. Requirement status (not met and at risk first).*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R2 | 1.87 evenings (225 Wh per evening from the pack); 1.81 with minimum cells | 1.8 evenings (restated 2026-10-02) | Met on paper |
| R6 | 90.5 % worst case (model); MPPT stability not analysed | 90 % or more from 40 to 200 W; stable MPPT | At risk |
| R11 | USD 483 excluding the pack | Value-engineering target USD 450 | Over the target by USD 33 |
| R12 | Door, runners and class D catch; display reads PACK_STATUS and PACK_LIMITS | 30 s swap; status display | Not verifiable at TRL 3 |
| R1 | 419 Wh usable (407 Wh with minimum cells) | 400 Wh or more | Met |
| R3 | DC in 12 to 60 V 200 W MPPT; charger in; pack swap; SunSpoke panel | Four sources | Met (design review) |
| R4 | 2.1 h | 3 h or less | Met |
| R5 | 634 Wh per clear day; full in 0.70 day | Full in one clear day | Met |
| R7 | Outputs as specified; 30 A buck for 26.5 A; pack 11.5 A at 400 W | R7 output set, 400 W total | Met (design review) |
| R8 | Off 3.2 % per month; ready 0.6 W; inverter auto-off | 5 % per month; 1.0 W; auto-off | Met |
| R9 | No AC inlet; DC bus 54.6 V; RCD needs a bonded inverter neutral | No back-feed path; 60 V or less | Met (design review) |
| R10 | 9.4 kg; 480 x 279 x 275 mm | 10 kg; 500 x 300 x 280 mm | Met |

## 14. Checks against earlier documents

The TRL 2 figures in PBX-PRC-001 v0.3 were checked against this script and corrected in v0.4: usable energy 421 to 419 Wh (SwapCell v0.3 gives 466 Wh at 0.2C, not 468 Wh); evenings 1.9 to 1.87; the 5 % cut-off option 2.0 to 1.97 evenings; mass 8.3 to 8.6 kg; buck 20 A to 30 A; PowerBox parts $435 to $449; pack price $370 to $414 and with-pack cost $805 to $863; SunSpoke panel days per evening 0.7 to 0.75; router runtime 33 h and phone charges 30 to 31; wall energy for a grid charge 490 to 492 Wh.

> **Safety:** These are paper estimates for a box that holds a 468 Wh lithium-ion pack able to deliver about 500 A into a short, and a 230 V AC outlet. They do not replace protection design review, datasheet checks or testing. Nothing may be built or energized from this note; building and testing are TRL 4 work and on hold by Amish's instruction.
