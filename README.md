# PowerBox

**Area:** CleanTech · **Status:** Concept · **Prototype budget:** about $450 USD · **Difficulty:** 3 of 5

Standalone multi-input power station built around a SwapCell battery pack. It charges from StepGen, a solar panel, the grid or a SunSpoke bike, and powers devices through USB, 12 V DC and a small AC outlet. It never connects to household wiring.

## Problem

When the power goes out, households need a small, safe store of electricity for lights, phones, radio and internet, charged from whatever source is available: human power, a solar panel or the grid when it is up. Design with, not for: requirements must come from co-design sessions and field trials with the intended users through a local partner.

## Concept

Standalone multi-input power station built around a SwapCell battery pack. It charges from StepGen, a solar panel, the grid or a SunSpoke bike, and powers devices through USB, 12 V DC and a small AC outlet. It never connects to household wiring.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- SwapCell 48 V pack or 12.8 V LiFePO4 pack
- Multi-input charge controller (DC human power, solar MPPT, AC charger)
- USB-A and USB-C PD outlets
- 12 V DC outlets
- 300 W pure sine inverter with its own AC outlet
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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
