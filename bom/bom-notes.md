# BOM notes

Prices are indicative TRL 3 estimates with a supplier or supplier type for each line; named quotes are still needed before any purchase (TRL 4 work, on hold by Amish's instruction). Item numbers match the exploded view (`media/exploded.png`), the components table in `docs/02-concept.md` and the general arrangement PBX-DWG-001. Items 16 to 18 are in the BOM but not modelled.

**Total: $449.00 for the PowerBox parts, against the $450 budget.** The margin is $1, so R11 is at risk (PBX-CAL-001 section 11). The total is printed by `docs/04-calcs/sizing.py`, which reads this file.

**The SwapCell pack is not included.** Amish decided on 2026-09-25 that a shared SwapCell pack is priced once, in the SwapCell BOM (about $414 in prototype parts), and excluded from each dependent kit budget. Line 4 is therefore listed at $0.00. For reference only, one PowerBox with its own pack is about $863 in parts.

Changes from TRL 2:

- Line 10: the 48 V to 12 V buck is now 30 A (360 W), up from 20 A, because every DC output at its rating needs about 26.5 A (PBX-CAL-001 section 5). About $10 more.
- Line 5: adds the class D latch catch and the 10 kΩ ±1 % INTERLOCK coding resistor required by SwapCell interface v0.3 item W. About $2 more.
- Line 11: adds a recessed, normally closed wake button in the INTERLOCK loop. About $1 more.
- Line 16: fuse and breaker ratings from PBX-CAL-001 section 6, including a pre-charge relay and resistor for the inverter. About $1 more.
- Lines 9 and 12: 230 V 50 Hz with a 30 mA RCD (decided by Amish, 2026-09-25); the inverter output must be isolated so its neutral can be bonded.

The grid charger (line 17, $50) is the same class of certified 54.6 V, 5 A charger as the SwapCell dock charger. A household or charging point that already has a SwapCell dock can omit it, bringing the PowerBox parts to $399.

The largest cost drivers are the inverter ($70), the grid charger ($50), the output panel ($46) and protection and wiring ($36). The DC-only variant without the inverter and AC outlet saves about $92 and removes all mains voltage from the box.
