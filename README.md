# PowerBox

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** CleanTech · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** $450 USD, excluding the shared SwapCell pack · **Difficulty:** 3 of 5

Standalone multi-input power station built around a SwapCell battery pack. It charges from a solar panel, the grid or a SunSpoke bike, and powers devices through USB, 12 V DC and a small AC outlet. It never connects to household wiring.

![PowerBox concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

When the power goes out, households need a small, safe store of electricity for lights, phones, radio and internet, charged from whatever source is available: a solar panel, the grid when it is up or a charged pack brought home from an e-bike. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Standalone multi-input power station built around a SwapCell battery pack. It charges from a solar panel, the grid or a SunSpoke bike, and powers devices through USB, 12 V DC and a small AC outlet. It never connects to household wiring.

It builds to SwapCell interface v0.3 as a station host: it wakes the pack through a coded INTERLOCK loop and can run loads while charging from solar. The sizing note shows 419 Wh usable per pack, 1.87 evenings of the reference load (short of the two-evening target), a 2.1 h grid charge, 8.6 kg with the pack and $449 of PowerBox parts.

Full design precis: [docs/02-concept.md](docs/02-concept.md) · Sizing: [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md) · General arrangement: [cad/drawings/PBX-DWG-001.pdf](cad/drawings/PBX-DWG-001.pdf)

## Key components

- Removable SwapCell 48 V pack (interface v0.3), with a fixed 12.8 V LiFePO4 pack as a documented fallback
- Multi-input charge controller (12 to 60 V DC and solar input with MPPT, external certified charger)
- USB-A and USB-C PD outlets
- 12 V DC outlets from a 30 A buck converter
- 300 W, 230 V pure sine inverter with its own AC outlet behind a 30 mA RCD
- State-of-charge display
- Enclosure with ventilation and handles

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Standalone use only: never connect the AC output to a wall outlet or household wiring, because back-feeding endangers utility workers and is illegal. Contains a lithium battery pack. Use a BMS with cell-level protection, fuse the pack, and charge on a non-combustible surface.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (PBX-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `PBX-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
