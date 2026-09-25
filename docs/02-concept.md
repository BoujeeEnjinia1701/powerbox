---
doc_id: PBX-PRC-001
title: PowerBox design precis
project: PowerBox
doc_type: Design precis
version: "0.2"
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
  change: Populate to TRL 2 (architecture, first-order numbers, input and output specification, safety, media)
---

# PowerBox design precis

PowerBox is an aluminium carry case about the size of a small toolbox (460 x 260 x 220 mm body) with a SwapCell pack sliding into a bay through a side door. A charge controller takes DC from StepGen or a solar panel, a certified external charger takes grid power, and a charged pack from a SunSpoke bike can simply be swapped in. Power leaves through USB-C PD, USB-A, 12 V sockets and one 300 W pure sine AC outlet protected by a GFCI or RCD. It never connects to household wiring. First-order numbers suggest one pack gives about 420 Wh usable, enough for about 1.9 evenings of lights, phones, radio and a router, and the PowerBox parts cost about $435 without the pack.

![Hero render](../media/hero.png)

*Figure 1. PowerBox on a table, with a phone for scale. Output panel on the front, input panel and pack bay door on the right end. Massing model.*

## How it works

1. **Charge.** Energy comes in through one of three paths, all controlled by the host controller:
   - **DC input** (StepGen or a solar panel, 12 to 60 V, up to 200 W) goes through a buck-boost charge controller that tracks the source's maximum power point and charges the pack at up to 54.6 V.
   - **Grid** goes through a certified external 54.6 V, 5 A charger brick with a DC plug. PowerBox itself has no AC inlet, so it cannot be plugged into anything that would back-feed.
   - **SunSpoke** charges the pack while riding or at its own 100 W panel. The rider brings the charged SwapCell pack home and swaps it in, which takes about 30 s. SunSpoke's panel can also plug into the DC input directly.
2. **Store.** The SwapCell pack (13S2P lithium-ion, 46.8 V nominal, about 468 Wh) sits in a bay with guide rails and mates through the SwapCell blind-mate connector. The host controller runs the SwapCell CAN handshake: the pack enables its output only when seated, with the interlock closed and a valid host heartbeat.
3. **Convert and deliver.** The 39 to 54.6 V bus feeds a 48 V to 12 V buck converter for the 12 V sockets and the USB-C PD and USB-A modules, and a 48 V input, 300 W pure sine inverter for the single AC outlet.
4. **Inform.** A small display shows state of charge, input and output power and estimated time remaining, read from the pack's CAN messages. The host switches the inverter off after 10 min below 5 W, because its idle draw would otherwise drain the pack.
5. **Protect.** A pack fuse, a breaker on the inverter feed, per-output fuses, thermostatic fan control and the pack's own BMS limits guard against faults.

![Energy flow](../media/flow.png)

*Figure 2. Energy per usable cycle, DC input to loads. All values are estimates: controller 94 %, cell charge and wiring 96 %, output conversion about 91 % for a mixed load of 60 % DC, 25 % USB and 15 % AC.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Enclosure body | Folded 1.2 mm aluminium tub, 460 x 260 x 220 mm | Spreads heat and resists fire better than plastic. Proposed, awaiting Amish |
| 2 | Lid | Aluminium with exhaust slots at the back | Removable for service |
| 3 | Carry handle | Folding bar handle on the lid | Rated 15 kg or more |
| 4 | SwapCell pack | SwapCell interface v0.2 reference pack, 468 Wh | Not in the PowerBox cost; shared with SunSpoke and the dock |
| 5 | Pack bay | Floor, guide rails, SwapCell dock-side receptacle on a floating mount, shelf above | Mirrors the SwapCell dock cradle, horizontal |
| 6 | Pack bay door | Hinged door on the right end, magnetic catch, padlock eye | Keeps fingers and debris out of the bay |
| 7 | Multi-input charge controller | Buck-boost DC-DC, 12 to 60 V in, 200 W, CC-CV output set by the host | Maximum power point tracking in host firmware |
| 8 | Host controller | ESP32 with CAN transceiver, relays and current sensors | Runs the SwapCell handshake, charge control, auto-off and display |
| 9 | Inverter | 300 W pure sine, 48 V input, 600 W surge, certified | Regional variant (230 V or 120 V) awaiting Amish |
| 10 | DC-DC converter | 48 V to 12 V, 20 A buck | Feeds 12 V sockets and USB modules |
| 11 | Output panel | USB-C PD 100 W and 60 W, 2 x USB-A, 2 x 12 V sockets, main switch | Front face |
| 12 | AC outlet | Single outlet behind a 30 mA RCD (230 V) or 5 mA GFCI (120 V) | Only mains-voltage point on the box |
| 13 | Display | 2.4 in TFT or e-paper | State of charge, power in and out, time left |
| 14 | Input panel | 2 x Anderson Powerpole PP45: DC in, charger in | Right end, above the bay door |
| 15 | Exhaust fan | 80 mm 12 V fan, thermostatic; filtered intake slots on the right end | Pulls air front to back over the inverter |

Items 16 (protection and wiring), 17 (grid charger brick) and 18 (hardware) are in the BOM but not modelled.

![Cutaway](../media/cutaway.png)

*Figure 3. Section looking from the front: inverter (9) on the floor at the front, SwapCell pack (4) in its bay at the back, charge controller (7) and host (8) on the shelf above, fan (15) on the left end, input panel (14) and bay door (6) on the right end.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: the SwapCell reference pack (468 Wh, 39.0 to 54.6 V); the host allows 10 to 100 % state of charge; 12 V buck 94 %, USB modules 93 % from 12 V, charge controller 94 %, cell charge and wiring 96 %, grid charger 90 %; inverter efficiency and idle draw typical of 48 V, 300 W pure sine units (not yet from a datasheet).

Table 2. Energy, charge times, size and cost.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Usable energy | about 421 Wh | 90 % of 468 Wh (10 to 100 %) | R1 met (400 Wh) |
| Reference evening (Table 1 of PBX-REQ-001) | 225 Wh from the pack | 155 Wh DC at 94 %, 48 Wh USB at 87 %, 5 Wh host and display over 5 h | |
| Evenings per pack | about 1.9 | 421 / 225 | R2 **not met** (target 2) |
| Grid charge, 10 to 100 % | about 2.1 h; about 490 Wh from the wall | 439 Wh into the pack at 5 A (about 270 W) in CC, then CV; charger 90 % | R4 met (3 h) |
| Solar, 200 W panel | about 635 Wh per clear day; full in one day, or about 3 h of strong sun | 4.5 peak sun hours, 0.75 derating for heat, dust and angle, 94 % controller | R5 met |
| Solar, SunSpoke 100 W panel | about 315 Wh per clear day; one evening's use in about 0.7 day | Same basis | |
| StepGen, per hour of stepping | about 55 to 90 Wh stored | StepGen's estimate of 60 to 100 Wh at its output, times 94 % and 96 % | |
| StepGen, one evening's use | about 2.5 to 4 h of stepping | 225 Wh at 55 to 90 Wh per hour | |
| StepGen, 10 to 100 % | about 5 to 8 h of stepping; about 12 h at 40 W | 421 Wh at 55 to 90 Wh per hour | |
| SunSpoke pack swap | about 30 s | Open door, pull pack by its handle, insert charged pack, close door | R12 met, to confirm with users |
| Inverter efficiency | about 88 % at 200 to 300 W, 85 % at 60 W, 75 % at 20 W; idle draw 6 to 10 W | Typical 48 V, 300 W units | |
| Inverter idle, if left on | about 190 Wh per day, nearly half the pack | 8 W for 24 h | Auto-off after 10 min below 5 W (R8) |
| Standby, off | about 3 % per month | Li-ion self-discharge about 2 to 3 % per month; BMS sleep a few mW | R8 met (5 %) |
| Standby, ready (display on, outputs off) | about 0.6 W | ESP32 modem sleep 0.2 W, CAN and BMS awake 0.2 W, display 0.2 W | R8 met (1.0 W); still about 14 Wh per day, so the host returns to off after 30 min idle |
| Standby, DC outputs on, no load | about 1.2 W | Ready plus 12 V buck and USB module quiescent draw | |
| Peak pack current | about 12 A | 400 W output limit at 88 % and 39 V | Within SwapCell's 20 A continuous |
| Heat at full AC load | about 41 W from the inverter, plus about 12 W from the controller when charging at 200 W | 300 W at 88 %; 200 W at 94 % | Fan needed |
| Mass | about 8.3 kg (18 lb) with pack | Pack 2.8, body 1.4, lid 0.4, handle 0.2, inverter 1.2, bay 0.4, controller 0.3, DC-DC 0.3, panels 0.4, wiring and fuses 0.6, fan and host 0.3 kg | R10 met (10 kg); charger brick about 0.8 kg extra |
| Size | 460 x 260 x 220 mm body; about 482 x 276 x 278 mm overall | Pack 340 mm plus 35 mm handle zone, receptacle and walls set the length | R10 met (500 x 300 x 280 mm), tight on height |
| PowerBox parts cost | about $435 | Indicative prices, see `bom/bom.csv` | R11 met, about $15 margin |
| Cost with one SwapCell pack | about $805 | $435 plus about $370 from the SwapCell BOM | Above the $450 budget; see design choices |

Table 3. Runtime on one full pack (421 Wh usable) for single loads. Estimates.

| Load | Output | Power at the load | Drawn from the pack | Runtime |
| --- | --- | --- | --- | --- |
| Wi-Fi router and fibre terminal | 12 V DC | 12 W | 12.8 W | about 33 h |
| Three 5 W LED bulbs | 12 V DC | 15 W | 16.0 W | about 26 h |
| Radio | 12 V DC | 5 W | 5.3 W | about 79 h |
| Phone charges | USB | 12 Wh each | 13.7 Wh each | about 30 charges |
| Laptop | USB-C PD | 45 W | 51 W | about 8 h |
| Small LED TV | AC | 60 W | 71 W | about 6 h |
| Desk fan | AC | 25 W | 32 W | about 13 h |
| Maximum AC load | AC | 300 W | 341 W | about 1.2 h |
| Refrigerator or kettle | AC | Out of scope: starting surge or power beyond the 300 W inverter | | |

Table 4. Input and output specification (proposed).

| Port | Type and connector | Voltage | Power or current | Notes |
| --- | --- | --- | --- | --- |
| DC in | Anderson PP45, red and black | 12 to 60 V DC | 200 W maximum, about 15 A at 12 V | StepGen, solar panel or SunSpoke panel; MPPT; TVS and reverse-polarity protection; one source at a time |
| Charger in | Anderson PP45, keyed differently from DC in | 54.6 V DC from the certified brick | 5 A | Grid charging only through the external charger |
| Pack | SwapCell blind-mate connector | 39.0 to 54.6 V | 20 A continuous available; PowerBox uses 12 A or less | CAN 2.0B at 250 kbit/s; 120 Ω termination in PowerBox |
| USB-C PD 1 | USB-C | 5 to 20 V | 100 W | Laptops |
| USB-C PD 2 | USB-C | 5 to 20 V | 60 W | Phones, tablets |
| USB-A 1, 2 | USB-A | 5 V | 12 W each | Phones, lamps, radios |
| 12 V DC 1 | Car socket | 12 V regulated | 10 A shared with 12 V DC 2 | Router, lights, radio |
| 12 V DC 2 | 5.5 x 2.1 mm barrel | 12 V regulated | As above | |
| AC out | One regional socket behind a GFCI or RCD | 230 V 50 Hz or 120 V 60 Hz, pure sine | 300 W continuous, 600 W for 1 s | Auto-off; never to be connected to household wiring |
| Total output | | | 400 W | Host limit to keep pack current and heat in range |

## Key design choices

All are proposed, awaiting Amish.

- **Removable SwapCell pack, with a fixed internal pack as fallback.** A removable SwapCell pack is the point of the design: one battery moves between PowerBox, SunSpoke and the SwapCell dock, and a worn pack is replaced without discarding the box. The fallback is a fixed internal 12.8 V LiFePO4 pack (about 30 Ah, 384 Wh, about $110), with a 12 V inverter and no CAN. It is safer chemistry, cheaper, fits the $450 budget with the pack included and does not depend on SwapCell's schedule, but it loses swapping and sharing. Recommendation: removable SwapCell pack, with the fixed-pack variant kept as a documented fallback.
- **Side-loading horizontal bay.** A vertical, top-loading bay would make the case about 450 mm tall. Laying the pack along the case length with a door on the end keeps the case low and stable. Recommendation: horizontal side-loading bay.
- **One DC input with maximum power point tracking.** A single buck-boost input covers StepGen, solar and SunSpoke's panel. Two independent inputs would allow solar and StepGen at the same time, for about $30 more. Recommendation: one DC input for the first build.
- **Grid charging only through a certified external charger.** Keeps mains-input electronics out of the box, reuses the SwapCell dock charger class, and means the box has no AC inlet. Recommendation: external charger brick.
- **A 300 W AC outlet with a DC-only variant.** AC is what users expect, but it brings mains voltage into the home, costs about $92 and wastes energy at idle. Recommendation: include 300 W AC with auto-off, and document a DC-only variant for lights, phones and routers.
- **Aluminium enclosure.** Aluminium spreads heat and delays a fire better than a rugged plastic case, at similar cost if folded locally. Recommendation: folded aluminium.
- **Pass-through operation.** Users will want to charge from solar while running the router. The SwapCell v0.2 behavior rules allow charge only with a dock heartbeat and do not define a host that charges and discharges at once. Recommendation: ask SwapCell for a "station" host type with a combined charge and discharge mode, rather than work around it locally.
- **Budget.** Recommendation: keep $450 for the PowerBox parts excluding the pack, and report the with-pack cost (about $805) openly. Alternative: raise the budget to about $850 to include one pack. Proposed, awaiting Amish.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers.*

## Safety

> **Safety:** PowerBox is standalone only. Never connect the AC outlet to a wall outlet, household wiring, a distribution board or a transfer switch. Back-feeding can kill utility workers repairing lines during an outage, can damage the box and the home's wiring, and is illegal.

> **Safety:** The SwapCell pack is a 468 Wh lithium-ion battery. Use it only with the SwapCell BMS, keep the 40 A pack fuse in place, and never charge a damaged, swollen or wet pack. Charge on a non-combustible surface, away from exits, beds and children, and do not cover the box while charging. Keep a smoke alarm in the room.

> **Safety:** The AC outlet carries mains voltage (230 V or 120 V). It must be behind a GFCI or RCD, and for the protection to work the inverter's output neutral must be bonded to the case and the protective earth pin, as in a vehicle or boat installation. Many small inverters have a floating output where a GFCI will not trip. This must be confirmed for the chosen inverter at TRL 3.

- **No back-feed by design.** There is no AC inlet on the box, and grid charging uses a certified external charger with a DC plug, so no cable can join PowerBox's AC output to a live circuit through an ordinary plug. The user guide and labels must still warn against double-male cords and improvised connections.
- **Extra-low-voltage bus.** The battery side stays at 54.6 V or less, below the 60 V DC limit for extra-low voltage, so only the inverter output and the charger brick input are at mains voltage.
- **Ventilation.** The inverter can shed about 41 W and the controller about 12 W. A thermostatic fan pulls air through filtered intake slots on the right end and out through the left end and lid. The host derates or shuts outputs down if internal temperature exceeds a limit, and the pack enforces its own temperature limits. The case must not be used in a closed cupboard or bag.
- **Cords and connectors.** Keyed Powerpole connectors prevent the charger and DC inputs from being swapped. Input and output cords must be rated for their current, kept out of walkways and never run under rugs. The 12 V car socket is fused at 10 A.
- **Pack handling.** The bay door keeps fingers away from the connector, and the SwapCell interlock keeps the pack output dead until it is fully seated.
- **Human power.** StepGen is moving machinery with its own safety section in its design; PowerBox limits input current so a generator cannot over-charge the pack.
- **Not a medical or life-safety supply.** PowerBox must not be relied on for oxygen concentrators or other life-support equipment.

## Open questions for TRL 3

- **Waking the pack from a battery-only host.** SwapCell's WAKE pin needs 5 to 15 V from the host, but with the pack asleep and no charger connected, PowerBox has no other source. Options: a small keep-alive cell in PowerBox, SwapCell waking on interlock closure, or a wake button on the pack. Raise with SwapCell; do not change the interface locally.
- **Pass-through charging** needs a SwapCell host mode that allows charge and discharge together (see design choices).
- Confirm inverter idle draw, efficiency at light load and whether its output neutral can be bonded for GFCI or RCD operation.
- Confirm that the buck-boost controller stays at or above 90 % efficiency at 40 W and tracks StepGen's varying voltage without hunting (R6, at risk).
- Choose the AC region first (230 V 50 Hz or 120 V 60 Hz). Proposed: 230 V, awaiting Amish.
- The evening profile misses R2 by about 5 %. Options: accept 1.9 evenings, lower the discharge cut-off to 5 % (about 445 Wh, 2.0 evenings but more cell wear), or revise the reference profile with users.
- Where to place the charge controller relative to the pack, so its heat does not warm the cells.
- Should the display count energy delivered, for a community charging point that charges per phone?
- Validate the load profile, pack-swap routine and price with users through a local partner.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
