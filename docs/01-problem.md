---
doc_id: PBX-PRB-001
title: PowerBox problem statement
project: PowerBox
doc_type: Problem statement
version: "0.5"
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-24'
  author: Amish Chadha
  change: Removed StepGen as a charging source after StepGen became a walking vehicle (Amish, 2026-09-24)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. SwapCell interface v0.3, budget scope and AC region decided by Amish (PBX-DDR-001); open questions updated
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Open questions on the first partner, theft resistance and R2 answered by Amish's 2026-10-02 decisions"
---

# PowerBox problem statement

When the power goes out, households need a small, safe store of electricity for lights, phones, radio and internet, charged from whatever source is available: a solar panel, the grid when it is up or a charged pack brought home from an e-bike. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## The problem

Outages are routine for a large share of the world. Grids with scheduled load shedding, storm-exposed distribution lines and informal connections leave households dark for hours, often in the evening when lighting and phone charging matter most. The fallback is usually a kerosene lamp, candles, a car battery on an unsafe charger, or a petrol generator, which is noisy, costly to run and a carbon monoxide hazard indoors.

Commercial portable power stations solve part of this, but they have three gaps for these users:

- **Closed, sealed batteries.** When the cells wear out, the whole unit is usually discarded. The pack cannot be swapped, shared or repaired.
- **Charging assumes a working grid or a large solar array.** Few charge well from a small panel, and none are designed to share a battery with an e-bike or a village charging hub.
- **Overselling.** Marketing implies a box can run a fridge or kettle. A household that buys on that promise and then drains the battery in an hour loses trust in the whole category.

PowerBox is a standalone power station built around the portfolio's SwapCell pack, so the same battery can move between a PowerBox, a SunSpoke e-bike and a SwapCell dock. It charges from a solar panel, the grid or a charged pack brought home from the bike, and it is honest about scale: a 200 W panel delivers about 634 Wh to the pack on a clear day, and one pack runs lights, phones, a radio and a router through an outage, not a fridge or a kettle.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Outage-prone urban and peri-urban household | Evening light, phone charging, radio and home internet through a 2 to 6 h outage, recharged from the grid when it returns | Load shedding or storm outages; small homes and flats; indoor use |
| Off-grid rural household | A daily store for lights and phones, charged from a small solar panel; a pack that can travel on an e-bike to a charging hub | No grid, or an unreliable mini-grid; dust, heat, rough transport |
| Household in an informal settlement | Safe light and phone charging without unsafe improvised wiring or kerosene; low purchase cost; theft-resistant design | Dense housing, fire risk, shared walls, limited space |
| Community charging point operator | Charge many phones and lamps for a small fee; swap packs between boxes and a charging hub; see how much energy each pack delivered | Market stall, school, clinic waiting room, community centre |
| Local technician or repair shop | Open design, standard parts, a pack and modules that can be diagnosed and replaced | Informal electronics repair trade |
| Open hardware community | A reference design that ties SwapCell, SunSpoke and StepGen (a walking vehicle on the same pack) together | Makerspaces, university labs, NGOs |

## Constraints

- Garage-buildable prototype. Budget $450 USD for the PowerBox parts, excluding the SwapCell pack, which is priced once in the SwapCell project (decided by Amish, 2026-09-25).
- Built around SwapCell interface v0.3: 13S lithium-ion pack, 46.8 V nominal (39.0 to 54.6 V), 468 Wh nameplate, 340 x 90 x 80 mm body (393 mm overall), blind-mate connector with CAN, wake through a 10 kΩ coded INTERLOCK loop (item W), a station host type with a charge-discharge mode (item C) and latch classes (item V). PowerBox must not change the interface locally; conflicts go back to SwapCell.
- Standalone only. PowerBox must never connect to household wiring, a wall outlet or a distribution board. Back-feeding endangers line workers and is illegal almost everywhere.
- Carryable by one adult: a case with a single handle, small enough for a shelf or under a bed.
- Safe indoors: lithium cells, a mains-voltage AC outlet and hot power electronics all sit in a living space, often near children.
- Off-the-shelf modules where possible (certified charger brick, inverter, DC-DC converters), so no custom mains electronics are designed at portfolio level.
- DC bus kept below 60 V so the battery side stays in the extra-low-voltage range.
- Operating range about 0 to 40 °C ambient, with charging inhibited by the SwapCell BMS outside its limits.

## Out of scope

- Connection to household wiring in any form, including transfer switches, double-male plug cords and grid-tie inverters.
- Loads above about 300 W, or with high starting surges: refrigerators, freezers, kettles, irons, hair dryers, space heaters, pumps and power tools.
- Whole-home backup and multi-day autonomy for large loads.
- Design of the SwapCell pack, the SunSpoke bike or the StepGen walking vehicle; PowerBox uses the SwapCell interface they share.
- Design of new mains-voltage electronics. The inverter and grid charger are certified off-the-shelf units.

## Prior work

- Commercial portable power stations from several brands (lithium iron phosphate or NMC, 250 to 2,000 Wh) show the product form and output mix users expect: USB-C PD, USB-A, 12 V car socket and pure sine AC. Almost all have sealed, non-swappable batteries.
- Pay-as-you-go solar home systems, widely deployed in East and West Africa and South Asia, show that 20 to 100 Wh per day of lights, phone charging and radio transforms evening life, and that honest sizing matters.
- Battery-swap networks for two- and three-wheelers show that a shared, standard pack can be charged centrally and carried home.
- Open-source battery management and power electronics projects (for example open BMS designs used by the e-bike and solar DIY communities) provide starting points for the host controller and CAN handling.

No link is given where a specific reference has not been verified.

## Open questions

- Which users to involve first, and through which partner (an NGO running community charging points, a solar home system distributor, or a university group in an outage-prone city)? Decided by Amish, 2026-10-02: a partner in a 230 V, 50 Hz region that runs or supplies community charging or solar home systems where outages are routine; the first candidate type to approach is a solar distribution charity such as SolarAid, which works in Zambia and Malawi. Nothing is agreed.
- AC region first: 230 V 50 Hz with a 30 mA RCD. Decided by Amish, 2026-09-25 (PBX-DDR-001); 120 V 60 Hz is a later variant.
- Is theft resistance (a lockable pack door) a priority for informal settlement and community charging users? Decided by Amish, 2026-10-02: a thumb-turn cam latch with a padlock hasp for the prototype, and a keyed cam latch where the partner runs an unattended or shared charging point.
- Is one pack for 1.87 evenings enough, or should the reference evening change? R2 was restated as 1.8 evenings by Amish on 2026-10-02 (PBX-DDR-001 item 13); the reference evening is still to be checked with the first partner's users.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
