---
doc_id: PBX-BLD-001
title: PowerBox prototype build plan
project: PowerBox
doc_type: Build plan
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: First build plan, with pictures by component and step; design made constructable (PBX-DDR-003)
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "PBX-DDR-003 recorded as accepted; AC outlet stated as the national socket of the first partner's country with a bonded earth pin, never a universal socket (decided by Amish, 2026-10-02, PBX-DEC-001 item 10)"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Lit rocker main switch and its 22 x 30 mm hole in the output panel plate; pictures redrawn from the updated model"
---

# PowerBox prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept prototype, component by component. Building and testing to it is TRL 4 work. Decisions still to be made are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component pulled apart and numbered in build order. The parts that sit on the case floor are drawn below the case.*

The prototype is one PowerBox: a folded aluminium case, 460 mm long, 260 mm deep and 220 mm tall, with a SwapCell battery pack sliding into a bay through a door in its right-hand end. Inside are bought power modules (an inverter, a 48 V to 12 V converter, a solar charge controller and a small controller board) and a shelf over the pack; the sockets are on a panel across the front, and the two charging inputs are on a small panel at the door end. Figure 1 shows the 23 components in the order you make or fit them. Thirteen are made: the case body, the lid, the handle doubler plate, the shelf, two folded brackets and the protection plate (all cut and folded from aluminium sheet), the door and the two panel plates (cut from sheet), and the floor runners, top guide rail and intake filter frame (3D printed). Everything else is bought and fitted. The work is cutting, drilling and folding aluminium sheet (a local sheet metal shop can fold the case, lid and shelf), setting rivet nuts and blind rivets, three short 3D prints, and wiring bought modules together. The parts cost about USD 482 from the bill of materials, without the pack, which comes from the SwapCell project.

> **Safety:** The prototype holds a 468 Wh lithium-ion SwapCell pack that can deliver about 500 A into a short, a 48 V bus, and an inverter that makes 230 V AC. Keep the pack out of the case and the main fuse out of its holder until section 6 says otherwise. The 230 V side is wired from certified parts and checked by a qualified electrician before it is ever switched on. PowerBox is standalone only: its AC outlet must never be connected to a wall socket or household wiring. Cut aluminium edges are sharp: deburr everything and wear gloves.

## 2. What changed to make it buildable

The concept showed what PowerBox does; many of its parts could not be made or fixed as drawn. Each change below keeps what PowerBox does, and all of them are recorded in decision record PBX-DDR-003, accepted by Amish on 2026-10-02.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Lid | A tray standing on the 1.2 mm wall edges, with no fixing | A lid whose top rests on the walls and whose 16 mm skirt hangs outside them, held by six screws into rivet nuts (Figure 29) | It locates on all sides and comes off for service |
| Handle | A handle standing on the thin lid, with no fixing | Four bolts through the lid and a 2 mm doubler plate under it (Figure 27) | Spreads the carrying load |
| Floor runners | Runners 1 mm below the pack, nothing guiding its sides, too long to print | Four printed lengths with lips; the pack rests on them, the lips stand 1 mm off its sides (Figure 8) | The pack sits and is guided as intended |
| Shelf | A 4 mm slab resting on one bracket | A folded 2 mm shelf riveted to the back and end walls (Figure 17) | Fixed on three edges |
| Catch bracket and receptacle | A plate standing on its edge; the receptacle floating in the air | Two folded 3 mm brackets screwed to the floor (Figures 10 and 12) | Each part has a fixing |
| Pack bay door | A solid block with no hinge; no room for a magnetic catch | A sheet door on a piano hinge at its front edge, a cam latch and a padlock hasp (Figures 24 and 25) | The only edge with room for a hinge; the latch fits where a magnet cannot |
| Output and input panels | Blocks on solid walls; nowhere for the socket bodies | Windows in the walls covered by 2 mm panel plates; sockets in the plates (Figure 20) | Bought modules mount in a flat plate |
| Protection parts | Not placed anywhere | A protection plate on the floor between the inverter and the bay | Short path from the pack to the inverter |
| Fan end | Six slots, which the fan screws would have fallen on | One 76 mm hole behind the fan and grille | Twice the open area, and room for the screws |
| Corners, feet, filter | Not detailed | Riveted corner tabs (Figure 5), 8 mm rubber feet, a printed filter frame | Garage-buildable; screw heads clear the table |

The changes add about 0.8 kg (the prototype weighs about 9.4 kg with the pack) and leave the case within its size limit: 480 x 279 x 275 mm overall.

## 3. Making the components

Make and check each component before the assembly step that needs it. Sizes are in millimetres. "Front" is the side with the sockets; "left" and "right" are as seen standing in front of the case, so the fan is at the left end and the pack door at the right end. Workshop tolerance is 0.5 mm unless a step says otherwise; drawings do not carry tolerances before TRL 4.

### 3.1 Enclosure body

![Figure 2. Making sketch of the enclosure body](../cad/drawings/PBX-DWG-101.png)

*Figure 2. Enclosure body making sketch (PBX-DWG-101).*

![Figure 3. Hole positions in the case floor](05-build-plan/floor-holes.png)

*Figure 3. The 24 holes in the floor, from the outside of the left end and of the front wall.*

![Figure 4. Openings and holes in the door end wall](05-build-plan/end-wall-holes.png)

*Figure 4. The door end wall, seen from outside, with the front wall on the left.*

**What it is and what it is made from.** The open-topped case everything goes in. One blank of 5052 aluminium sheet 1.2 mm thick, about 900 x 700 mm, folded into a tub 460 long, 260 deep and 220 tall. This is a job for a sheet metal shop with a box-and-pan folder.

**How to make it.**

1. Give the shop the outside sizes and the openings below; the shop sets the bend allowances. The two end walls carry a 15 mm tab on each side edge, to be folded round the corner onto the outside of the long walls.
2. Front wall: a window 360 wide and 140 tall, from 55 to 415 from the left end and from 48 to 188 up from the underside.
3. Door end wall (Figure 4): the pack door opening, 99 wide and 96 tall; six intake slots 90 x 5; the input panel window, 78 x 55.
4. Fan end wall: a 76 mm hole centred 110 back from the front wall and 150 up, and four 4.5 mm holes on a 71.5 mm square round it for the fan screws.
5. Floor: the 24 holes of Figure 3, all 4.5 mm.
6. Rivet nut holes, 6.0 mm (check against the rivet nut maker's figure): in the front and back walls at 80, 230 and 380 from the left end, 213 up (for the lid); in the front wall at 44 and 426 from the left end, 80 and 175 up (for the output panel); in the door end as Figure 4 (for the input panel).
7. Rivet holes, 3.3 mm: in the back wall at 80, 180, 280 and 380 from the left end, 118 up (shelf); in the door end as Figure 4 (shelf, hinge, padlock staple and filter frame). Drill the shelf rivet holes through the shelf flanges at step 6 instead if you prefer.
8. Fold the walls up, then fold each end wall's tabs onto the outside of the long walls. Drill each tab and the wall behind it at 40, 100 and 160 up and set three 3.2 mm blind rivets.
9. Set the 14 M4 rivet nuts with a hand rivet nut tool, flanges outside.
10. Deburr every edge and hole.

**How it fits the parts next to it.**

![Figure 5. Joint 3: corner tab](05-build-plan/joint-03.png)

*Figure 5. Each end wall's tab lies on the outside of the long wall and is held by three blind rivets.*

The lid rests on the top edges of the walls; the floor carries the runners, brackets and power modules on screws from below; the panels and door go on the outside of the walls.

**Check before moving on.** The diagonals of the top opening agree within 1 mm; the walls are square to the floor; every rivet nut turns an M4 screw freely.

### 3.2 Floor runners (make 4)

![Figure 6. Making sketch of the floor runner](../cad/drawings/PBX-DWG-107.png)

*Figure 6. Floor runner making sketch (PBX-DWG-107).*

**What it is and what it is made from.** The pack slides on these. Each is an L section, printed in PETG with four walls and 40 % infill: a base 24 wide and 8.8 tall, with a lip 3 wide rising 15 above it along one edge. Four lengths of 209.4, all the same.

**How to make it.**

1. Print each length lying on its base, lip up.
2. In the underside, two holes 5.6 mm and 8 deep, 14 in from the outer face of the lip, one 25 from one end and one 35 from the other.
3. Press an M4 heat-set insert into each hole with a soldering iron, flush with the underside.

**How it fits the parts next to it.**

![Figure 7. Joint 11: runner fixing](05-build-plan/joint-11.png)

*Figure 7. An M4 button-head screw comes up through the floor into the insert; its head sits inside the height of the rubber feet.*

![Figure 8. Joint 4: the pack in its bay](05-build-plan/joint-04.png)

*Figure 8. Section across the bay: the pack rests on the runner bases; the lips and the top guide rail stand 1 mm off it.*

Two lengths go end to end along the front of the bay and two along the back, lips on the outside, starting 38.8 from the inside of the fan end and running to the door end wall. The pack's latch face is 1 mm inside the front lips and its lid face 1 mm inside the back lips.

**Check before moving on.** The joints between lengths are flush; a straight edge laid along the bases does not rock.

### 3.3 Catch bracket

![Figure 9. Making sketch of the catch bracket](../cad/drawings/PBX-DWG-105.png)

*Figure 9. Catch bracket making sketch (PBX-DWG-105).*

**What it is and what it is made from.** The bracket that carries the latch catch, which holds the pack in place, and supports the front of the shelf. A channel 80 long folded from 5052 aluminium sheet 3 mm thick: a web 104.8 tall with a 22 mm flange at the bottom and at the top, both folded the same way.

**How to make it.**

1. Cut a blank 80 wide and about 145 long; fold both flanges 90° the same way, inside radius 3 mm, so the overall height is 104.8.
2. Drill two 4.5 mm holes in each flange, 15 and 65 from the left end, 9.5 back from the flange's front edge.
3. Drill the web to the latch catch's own holes, its centre 57 from the left end and 53.8 above the underside of the bottom flange.
4. Bolt the class D latch catch to the web with M4 screws and nyloc nuts.

**How it fits the parts next to it.**

![Figure 10. Joint 5: latch catch and pawl](05-build-plan/joint-05.png)

*Figure 10. Seen from above: the pack's latch pawl sits 1 mm behind the catch, so the catch stops the pack sliding out.*

The flanges point to the front, toward the inverter. The bottom flange sits on the floor, held by two M4 button-head screws from below with nyloc nuts on top; the top flange sits under the shelf and two M4 screws come down through the shelf into it. The web's back face is 2 mm in front of the pack's latch pawl and 12 mm in front of its latch face.

**Check before moving on.** The web is square to the floor; the catch springs back freely when pushed.

### 3.4 Receptacle bracket

![Figure 11. Making sketch of the receptacle bracket](../cad/drawings/PBX-DWG-106.png)

*Figure 11. Receptacle bracket making sketch (PBX-DWG-106).*

**What it is and what it is made from.** The bracket that holds the SwapCell receptacle, which the pack plugs into, at the fan end of the bay. An angle 62 wide folded from 5052 aluminium sheet 3 mm thick: a web 93.8 tall and a foot 23 deep.

**How to make it.**

1. Cut a blank 62 wide and about 115 long and fold the foot 90°.
2. Drill two 4.5 mm holes in the foot, 10 from its free edge, 13 and 49 from one side.
3. Drill the web to the floating-mount holes of the SwapCell receptacle (from the SwapCell dock drawing), so the receptacle face is centred 55 above the case underside and 198 back from the outside of the front wall.

**How it fits the parts next to it.**

![Figure 12. Joint 6: receptacle and plug](05-build-plan/joint-06.png)

*Figure 12. The pack's plug enters the receptacle with 0.5 mm all round; the receptacle floats on its mount.*

The foot sits on the floor, pointing toward the fan end, on two M4 button-head screws from below with nyloc nuts on top. The receptacle screws to the pack side of the web through its rubber grommets, so it can float about 1 mm to meet the plug. The receptacle carries the 10 kilohm INTERLOCK coding resistor of SwapCell interface v0.3.

**Check before moving on.** With a pack on the runners, the plug enters the receptacle without touching its sides.

### 3.5 Protection plate

![Figure 13. Making sketch of the protection plate](../cad/drawings/PBX-DWG-113.png)

*Figure 13. Protection plate making sketch (PBX-DWG-113).*

**What it is and what it is made from.** A flat plate that carries the 30 A main fuse holder, the 20 A DC breaker for the inverter, and the inverter relay with its 47 ohm pre-charge resistor. 5052 aluminium sheet 2 mm, 210 x 34.

**How to make it.**

1. Cut the plate and deburr it. Drill two 4.5 mm holes, 7 from each end, 17 from either long edge.
2. Lay out the fuse holder, breaker and relay left to right; mark each part's holes through it, drill, and fit with M4 or M3 screws and nyloc nuts.

**How it fits the parts next to it.** The plate sits on the floor between the inverter and the pack bay, 6 clear of the inverter and 14 clear of the front runner, on two M4 button-head screws from below with nyloc nuts on top.

**Check before moving on.** Every part on the plate is rated 60 V DC or more, and the fuse holder and fuse at least 1 kA breaking capacity (read the labels and datasheets).

### 3.6 Intake filter frame

![Figure 14. Making sketch of the intake filter frame](../cad/drawings/PBX-DWG-112.png)

*Figure 14. Intake filter frame making sketch (PBX-DWG-112).*

**What it is and what it is made from.** A frame that holds a washable foam filter pad over the intake slots inside the door end. Printed PETG, 106 wide, 91 tall and 6 thick.

**How to make it.**

1. Print it lying flat, pocket side up: a window 90 x 75, a 4.5 mm deep pocket on the wall side for a 5 mm foam pad, and a 1.5 mm grid of six bars that keeps the pad in.
2. Drill or print four 3.3 mm holes, 4 in from each side and 4 from top and bottom.
3. Cut the foam pad to 90 x 75.

**How it fits the parts next to it.** The frame goes inside the door end wall with its window over the slots, 20 to 110 from the front wall and 20 to 95 up, on four M3 screws from outside with nuts inside.

**Check before moving on.** The pad covers every slot and lifts out for washing.

### 3.7 Top guide rail (make 2)

![Figure 15. Making sketch of the top guide rail](../cad/drawings/PBX-DWG-108.png)

*Figure 15. Top guide rail making sketch (PBX-DWG-108).*

**What it is and what it is made from.** A bar under the shelf that stops the pack lifting. Printed PETG, 20 wide, 5 tall, in two lengths of 209.4.

**How to make it.**

1. Print both lengths lying flat.
2. In the top face, on the centre line, two holes 4.0 mm and 4 deep in each length: in the inner length 10 and 130 from its fan-end end, in the outer length 120.6 and 195.6 from its fan-end end. Press in M3 heat-set inserts.

**How it fits the parts next to it.** Both lengths go end to end under the shelf, 58 to 78 back from its front edge, held by four M3 screws down through the shelf (step 5). The rail stands 1 mm above the top of the pack (Figure 8).

**Check before moving on.** The pack slides under the fitted rail with light hand pressure.

### 3.8 Shelf

![Figure 16. Making sketch of the shelf](../cad/drawings/PBX-DWG-104.png)

*Figure 16. Shelf making sketch (PBX-DWG-104).*

**What it is and what it is made from.** The shelf over the pack that carries the charge controller and the controller board. 5052 aluminium sheet 2 mm, folded: a deck 423.8 x 128.8 with three flanges.

**How to make it.**

1. Cut the blank with a 20 mm rear flange (stopped 2.8 mm short of the right end for the corner), a 20 mm right end flange 100 long from the front edge, and a 15 mm front flange.
2. Fold the rear and end flanges up and the front flange down.
3. Drill the rail screw holes, 3.4 mm, 68 back from the front edge at 15, 135, 335 and 410 from the left end.
4. Drill the catch bracket holes, 4.5 mm, 11.5 back from the front edge at 310 and 360 from the left end.
5. Drill the rivet holes, 3.3 mm, 10 above the deck: in the rear flange at 45, 145, 245 and 345 from the left end; in the end flange 30 and 80 from the front edge.
6. Screw the top guide rail on (step 5).

**How it fits the parts next to it.**

![Figure 17. Joint 7: shelf flanges on the walls](05-build-plan/joint-07.png)

*Figure 17. The rear and end flanges are riveted to the back and door end walls; the rail is screwed under the deck.*

The shelf drops into the case onto the catch bracket's top flange, its deck top 108 above the case underside, its left end 33.8 from the inside of the fan end. Its rear flange lies on the back wall and its end flange on the door end wall, above the door opening; six 3.2 mm blind rivets hold them, and two M4 screws hold the front to the catch bracket.

**Check before moving on.** The deck is flat within 1 mm and level side to side.

### 3.9 Output panel plate and its modules

![Figure 18. Making sketch of the output panel plate](../cad/drawings/PBX-DWG-110.png)

*Figure 18. Output panel plate making sketch (PBX-DWG-110).*

![Figure 19. Cut-outs in the output panel plate](05-build-plan/panel-cutouts.png)

*Figure 19. Every cut-out in the output panel plate, from the left and bottom edges.*

**What it is and what it is made from.** The front panel that carries the two USB-C and two USB-A ports, the 12 V car socket and barrel socket, the lit rocker main switch (a 22 x 30 mm hole), the recessed wake button, the AC outlet with its residual current device (RCD) and the display. 5052 aluminium sheet 2 mm, 394 x 164.

**How to make it.**

1. Cut the plate and mark the cut-outs of Figure 19. Before cutting, check each size against the datasheet of the module you bought.
2. Cut the rectangular openings by chain drilling and filing, the round ones with a step drill or hole saw. Drill the four 4.5 mm screw holes, 6 and 388 from the left edge, 44 and 139 up.
3. Deburr, then print or fix the port labels.
4. Fit the modules from the front, each with its own nut or clip (step 8).

**How it fits the parts next to it.**

![Figure 20. Joint 10: output panel on the front wall](05-build-plan/joint-10.png)

*Figure 20. Section through the 12 V socket: the plate covers the window and the module bodies pass through it, clear of the inverter.*

The plate covers the front wall window, overlapping it 17 at each end and 12 at top and bottom, on four M4 screws into the rivet nuts. The 12 V socket body ends 17 above the inverter.

**Check before moving on.** Every module's body clears the edges of the window.

### 3.10 Input panel plate

![Figure 21. Making sketch of the input panel plate](../cad/drawings/PBX-DWG-111.png)

*Figure 21. Input panel plate making sketch (PBX-DWG-111).*

**What it is and what it is made from.** The small panel at the door end that carries the two Anderson Powerpole inputs: DC in (solar panel or another 12 to 60 V source) and charger in (the 54.6 V grid charger brick). 5052 aluminium sheet 2 mm, 110 wide and 75 tall.

**How to make it.**

1. Cut the plate. Cut two openings 24 x 25 for the panel-mount Powerpole housings, 23 to 47 and 68 to 92 from the front edge, 25 to 50 up; size them to the housing you buy.
2. Drill four 4.5 mm screw holes, 6 and 106 from the front edge, 20 and 55 up.
3. Fit the housings: DC in at the front, charger in at the back, turned differently so the two plugs cannot be swapped. Label them.

**How it fits the parts next to it.** The plate covers the window in the door end wall, above the intake slots and in front of the door, on four M4 screws into the rivet nuts.

**Check before moving on.** Each plug mates with only its own socket.

### 3.11 Wiring

![Figure 22. Block-level wiring](05-build-plan/wiring.png)

*Figure 22. Block-level wiring with wire sizes. No circuit board is laid out at this stage; bought modules are wired together.*

Every power module is bought. Buy to these specifications, not to a brand:

*Table 2. Modules to buy.*

| Module | What to buy |
| --- | --- |
| Charge controller | Buck-boost DC-DC, 12 to 60 V in, 200 W, constant current and constant voltage to 54.6 V with the current limit set by the controller board; input surge protection and reverse-polarity protection |
| Controller board | ESP32 with a CAN transceiver and 120 ohm termination, relay drivers and current sensors on the inputs and outputs |
| Inverter | 48 V DC in (40 to 60 V), 300 W continuous, 600 W for 1 s, pure sine, 230 V 50 Hz, output isolated from the DC input so its neutral can be bonded, remote on and off, idle 10 W or less |
| Buck converter | 36 to 60 V in, 12 V 30 A out, about 94 % efficient |
| Fuse block | 6-way blade fuse block rated 58 V DC or more, with 60 V fuses: 15 A converter, 20 A DC in, 10 A charger in, 10 A 12 V sockets, and the USB modules at 10, 7.5 and 5 A |
| Protection parts | 30 A main fuse and holder rated 60 V DC or more with at least 1 kA breaking capacity; 20 A DC breaker; relay with a 47 ohm pre-charge resistor for the inverter |

Wire it like this, with stranded copper and a crimped lug or ferrule on every terminal:

1. Receptacle power pins to the main fuse on the protection plate, and on to the 48 V side of the fuse block: 10 AWG (5.3 mm²).
2. DC in housing to the charge controller input, through its 20 A fuse: 10 AWG. Charge controller output to the fuse block: 10 AWG.
3. Charger in housing to the fuse block through its 10 A fuse: 14 AWG (2.1 mm²).
4. Fuse block to the buck converter through its 15 A fuse: 14 AWG. Buck converter output to the 12 V sockets: 10 AWG to the socket fuse, 14 AWG on to the sockets; to the USB modules: 18 AWG (0.8 mm²).
5. Fuse block through the 20 A breaker and the relay with its pre-charge resistor to the inverter input: 12 AWG (3.3 mm²).
6. Receptacle CAN pins to the controller board: twisted pair, 24 AWG. The 120 ohm termination is on the board.
7. Receptacle INTERLOCK pin through the normally closed wake button and the 10 kilohm coding resistor to signal ground: 24 AWG.
8. Controller board to the relay coil, the current sensors, the charge controller's current set point, the fan and the display: 24 AWG.
9. Inverter output to the AC outlet with its RCD: 1.5 mm² mains cable with an earth, as short as possible, with the inverter's output neutral bonded to the case and to the outlet's earth pin. This step is done or checked by a qualified electrician (section 6).

Keep the 48 V and 230 V wires apart from the signal wires, tie every wire down, and label both ends.

**Check before moving on.** Every wire continues end to end; with no pack in the bay and the main fuse out, the 48 V bus reads open to the case; the polarity of each Powerpole matches the module it feeds, checked with a meter, not by wire colour.

### 3.12 Pack bay door, with its hinge, latch and hasp

![Figure 23. Making sketch of the pack bay door](../cad/drawings/PBX-DWG-109.png)

*Figure 23. Pack bay door making sketch (PBX-DWG-109), seen from outside.*

**What it is and what it is made from.** The door over the pack bay. 5052 aluminium sheet 1.2 mm, 107.5 wide and 108 tall, with a hasp tab 26 wide rising 32 above its top edge at the back corner.

**How to make it.**

1. Cut the door with its tab and deburr it.
2. Cut the hasp slot, 18 x 20: 85.5 to 103.5 from the front edge, 114 to 134 up from the bottom edge.
3. Drill the latch hole, 19.5 mm: 92.5 from the front edge, 54 up.
4. Drill the hinge rivet holes, 3.3 mm: 7.5 from the front edge, 18, 54 and 90 up.

**How it fits the parts next to it.**

![Figure 24. Joint 8: door, hinge, latch and hasp](05-build-plan/joint-08.png)

*Figure 24. Seen from outside: the piano hinge on the front edge, the cam latch, and the hasp tab over the padlock staple.*

![Figure 25. Joint 9: cam latch shut](05-build-plan/joint-09.png)

*Figure 25. Seen from above, cut level with the latch: the latch tongue turns behind the end wall and stays clear of the pack.*

The door lies flat on the outside of the end wall, overlapping the opening by 3.5 at the front, 5 at the back and 6 at top and bottom. A stainless piano hinge on its front edge is riveted to the door and to the wall (three rivets each side). A thumb-turn cam latch in the 19.5 mm hole holds it shut: its tongue turns behind the end wall, 0.2 mm off it. The hasp tab goes over a flush padlock staple riveted to the wall, so a padlock can lock the door. When shut, the door is 10 mm behind the end of the pack's handle and stops the pack if the latch catch ever lets go.

**Check before moving on.** The door shuts flat and the latch holds it; the hinge swings without binding.

### 3.13 Handle doubler plate

![Figure 26. Making sketch of the handle doubler plate](../cad/drawings/PBX-DWG-103.png)

*Figure 26. Handle doubler plate making sketch (PBX-DWG-103).*

**What it is and what it is made from.** A strip under the lid that spreads the carrying load. 5052 aluminium sheet 2 mm, 240 x 40.

**How to make it.**

1. Cut the strip, round the corners and deburr it.
2. Drill four 5.5 mm holes on the centre line, 15, 45, 195 and 225 from the left end. Best drilled clamped under the lid, through the lid's holes.

**How it fits the parts next to it.**

![Figure 27. Joint 2: handle, lid and doubler](05-build-plan/joint-02.png)

*Figure 27. Four M5 bolts clamp the handle base plates, the lid and the doubler together; the nyloc nuts sit on the doubler.*

**Check before moving on.** The four bolts pass through handle, lid and doubler without forcing.

### 3.14 Lid

![Figure 28. Making sketch of the lid](../cad/drawings/PBX-DWG-102.png)

*Figure 28. Lid making sketch (PBX-DWG-102).*

**What it is and what it is made from.** The removable top of the case, with exhaust slots and the handle. 5052 aluminium sheet 1.2 mm, folded: a top 464.4 x 264.4 with a 16 mm skirt on all four sides.

**How to make it.**

1. Cut the blank and relieve the corners; the skirt corners need not be closed. Fold the skirt down on all four sides.
2. Cut seven exhaust slots 6 x 85, 14 apart, the first 32.2 from the left edge, from 162.2 to 247.2 back from the front edge.
3. Drill the handle bolt holes, 5.5 mm, on the centre line at 127.2, 157.2, 307.2 and 337.2 from the left edge.
4. Drill the screw holes, 4.5 mm, in the front and back skirts at 82.2, 232.2 and 382.2 from the left edge, 7.8 above the skirt's lower edge.

**How it fits the parts next to it.**

![Figure 29. Joint 1: lid on the case](05-build-plan/joint-01.png)

*Figure 29. Cut through a lid screw: the lid top rests on the wall and its skirt hangs 1 mm outside it, where the rivet nut flange sits.*

The top rests on the top edges of all four walls; the skirt hangs outside them with a 1 mm gap. Six M4 pan-head screws go through the skirt into the rivet nuts.

**Check before moving on.** The lid drops on without forcing and every screw hole lines up.

### 3.15 Bought components

Buy to specification, not brand. Line numbers are those of the bill of materials.

- **Carry handle (line 3).** Folding bar handle with two base plates, 200 mm span, rated 15 kg or more.
- **SwapCell pack (line 4).** The SwapCell interface v0.3 reference pack, from the SwapCell project; it is not part of this build's parts.
- **Pack bay parts (line 5).** Class D latch catch; SwapCell receptacle on its floating mount with the 10 kilohm INTERLOCK coding resistor (the SwapCell dock part); M3 and M4 heat-set inserts.
- **Door hardware (line 6).** Stainless piano hinge about 100 long; thumb-turn cam latch for a 19 mm hole that grips 1.2 mm sheet with a tongue about 15 long; flush padlock staple.
- **Power modules (lines 7 to 10).** As Table 2.
- **Output modules (lines 11 to 13).** USB-C power delivery modules (100 W and 60 W), two USB-A modules, a 12 V car socket and a 5.5 x 2.1 mm barrel socket, a snap-in lit rocker main switch (22 x 30 mm panel hole), a recessed normally closed push button for the wake button, a single 230 V outlet with a 30 mA RCD (the national socket of the first partner's country with its earth pin bonded to the case, never a universal multi-standard socket), and a 2.4 inch display.
- **Inputs (line 14).** Two panel-mount Anderson Powerpole PP45 housings with dust caps.
- **Fan (line 15).** 80 mm 12 V fan, about 16 L/s free air, with a finger grille and a washable foam filter pad.
- **Protection and wiring (line 16).** As Table 2, with 10, 12, 14, 18 and 24 AWG stranded wire, 1.5 mm² mains cable, lugs and ferrules.
- **Grid charger (line 17).** A certified 54.6 V, 5 A lithium-ion charger brick with a Powerpole DC lead.
- **Fixings and feet (line 18).** Stainless: 14 M4 rivet nuts and 14 M4 x 10 pan-head screws; 8 M4 x 12 button-head screws for the runners; 8 M4 button-head screws with nyloc nuts for the brackets and protection plate, and 8 more for the inverter and converter; 4 M5 x 16 bolts with nyloc nuts; M3 screws and nuts; about 30 blind rivets 3.2 mm; 4 self-adhesive rubber feet 20 mm across and 8 mm tall; 6 mm nylon standoffs; labels and heat-shrink.

## 4. Putting it together

In each picture the parts already fitted are grey and the part being fitted is in colour, with an arrow showing the way it goes in.

### Step 1: floor runners onto the floor

![Step 1](05-build-plan/step-01.png)

Two M4 button-head screws from under the floor into each length's inserts, lips on the outside of the bay, snug. A drop of medium threadlocker on each.

### Step 2: catch bracket and receptacle bracket

![Step 2](05-build-plan/step-02.png)

The catch bracket with its catch, flanges to the front, and the receptacle bracket with its receptacle, foot toward the fan end. Two M4 button-head screws from below each, nyloc nuts on top. Leave the catch bracket's screws loose until step 6.

### Step 3: inverter, converter, protection plate and fuse block

![Step 3](05-build-plan/step-03.png)

Each on its floor holes with M4 screws from below and nyloc nuts inside. **Hold point:** the main fuse stays out of its holder.

### Step 4: fan, grille and intake filter frame

![Step 4](05-build-plan/step-04.png)

The fan inside the fan end, blowing out, the grille outside, four M4 screws through both. The filter frame and pad inside the door end on four M3 screws.

### Step 5: top guide rail onto the shelf

![Step 5](05-build-plan/step-05.png)

Hold both rail lengths under the shelf, end to end; four M3 screws down through the shelf into the inserts.

### Step 6: shelf into the case

![Step 6](05-build-plan/step-06.png)

Lower the shelf onto the catch bracket. Clamp the flanges to the walls, drill through any rivet holes not yet drilled, and set six blind rivets. Two M4 screws down through the shelf into the catch bracket; then tighten the catch bracket's floor screws.

### Step 7: charge controller and host onto the shelf

![Step 7](05-build-plan/step-07.png)

The charge controller on four M4 screws through the shelf, heat sink up; the controller board on four 6 mm nylon standoffs.

### Step 8: modules into the output panel plate

![Step 8](05-build-plan/step-08.png)

With the plate on a soft cloth, fit each module from the front with its own nut or clip.

### Step 9: output panel onto the front wall

![Step 9](05-build-plan/step-09.png)

Feed the module bodies through the window; four M4 screws into the rivet nuts.

### Step 10: input panel onto the door end

![Step 10](05-build-plan/step-10.png)

Four M4 screws into the rivet nuts, DC in at the front.

### Step 11: wiring

![Step 11](05-build-plan/wiring.png)

Wire the modules as section 3.11 and Figure 22. **Hold point:** the wiring checks of section 3.11 pass, and the 230 V side has been checked by a qualified electrician, before going on.

### Step 12: pack bay door

![Step 12](05-build-plan/step-12.png)

Rivet the piano hinge to the end wall and to the door, fit the cam latch through the door, and rivet the padlock staple to the wall so it comes through the hasp slot.

### Step 13: handle and doubler onto the lid

![Step 13](05-build-plan/step-13.png)

Four M5 bolts down through the handle base plates, the lid and the doubler; nyloc nuts under the doubler, tight.

### Step 14: lid onto the case

![Step 14](05-build-plan/step-14.png)

Check no wire lies across the wall tops. Lower the lid over the walls; six M4 screws through the skirt into the rivet nuts.

### Step 15: rubber feet

![Step 15](05-build-plan/step-15.png)

Clean the underside with alcohol; one foot at each corner, clear of the screw heads.

### Step 16: the pack into its bay

![Step 16](05-build-plan/step-16.png)

**Hold point:** safety stops S1 to S4 of section 6. Open the door, slide the pack in connector first on the runners until the catch clicks, shut the door and turn the latch.

## 5. First checks

These are the checks a TRL 4 test report would record; this plan only lists them. Requirement numbers are those of PBX-REQ-001.

*Table 3. First checks.*

| Check | Requirement | How | Pass when |
| --- | --- | --- | --- |
| Pack fit and swap | R12 | Slide a pack in and out ten times; time one swap | Plug enters without touching; catch clicks; door shuts; swap 30 s or less |
| Insulation and back-feed | R9 | With no pack, meter between the 48 V bus and the case, and between each AC pin and the DC side | Open circuit everywhere; no AC inlet on the case |
| Keyed inputs | R3, R9 | Try each plug in each input | Each plug mates only with its own input |
| First power | R12 | Bench supply at 48 V with a 0.5 A limit in place of the pack, through the main fuse | Controller board starts, display shows; current under the limit |
| Wake | R12 | Pack in; let it sleep; press the wake button | Pack wakes through the INTERLOCK loop and the display reads its state of charge |
| 12 V and USB outputs | R7 | Load each output to its rating in turn | 12 V within 5 %; USB-C negotiates 100 W and 60 W; no fuse opens |
| AC outlet | R7, R9 | Electrician present; switch the inverter on with a 100 W lamp, then press the RCD test button | 230 V pure sine; pre-charge relay closes without a spark; the RCD trips |
| DC input charging | R3, R5, R6 | Bench supply at 12 V, 36 V and 60 V with a current limit at the DC in | Charging starts; input and output power read for efficiency; net charge 5.0 A or less |
| Grid charging | R4 | The charger brick at the charger in | Charge current 5 A or less; charging ends at 54.6 V |
| Standby | R8 | Measure pack current with outputs off and display on, then off | Ready 1.0 W or less; inverter off after 10 min below 5 W |
| Heat | R7 | Full output while charging for 30 min | The fan starts; the case stays hand-warm; no derating message |
| Mass and size | R10 | Weigh with the pack; measure | 10 kg or less (9.4 kg estimated); 500 x 300 x 280 mm or less |

## 6. Safety stops

Stop at each point. Carry on only when everything listed is true.

- **S1. Before the pack comes into the workshop.** The pack is the SwapCell reference pack with its own battery management, undamaged, dry and not swollen, with its fuse in place. A charging spot is ready on a non-combustible surface (ceramic tile or steel tray), away from exits, with a fire extinguisher for electrical fires and a smoke alarm in the room.
- **S2. Before the main fuse goes in.** With no pack in the bay, the 48 V bus reads open to the case; every fuse and the breaker are rated 60 V DC or more (58 V for the blade fuse block); the receptacle's polarity matches the main fuse and fuse block, checked with a meter, not by wire colour.
- **S3. Before any 230 V is made.** A qualified electrician has checked the wiring from the inverter to the outlet, the neutral bond to the case and earth pin, and that the inverter's output is isolated from its input. The AC outlet is never connected to a wall socket, household wiring, a distribution board or a transfer switch, and no double-male cord is ever made.
- **S4. Before the first charge.** First power and wake checks of section 5 have passed on the bench supply. The first charge is attended the whole time, lid off and case on the charging spot; stop if any part becomes too hot to hold or smells.
- **S5. Before running the inverter at full load.** The fan runs, the intake filter is clean, and the case stands in open air, never in a cupboard or bag.
- **S6. Before the prototype leaves the bench.** The lid screws, handle bolts and door latch are tight; no sharp edge is exposed; the warning labels (standalone only, no back-feed, lithium battery) are on the case.

## 7. Tools, skills and workspace

**Tools.** Sheet metal shop for the case, lid and shelf folds (or a box-and-pan folder 500 mm wide for 1.2 mm aluminium); hand folder or vice with bending bars for the 3 mm brackets; drill press and cordless drill; drills 3.3 to 6.0 mm, step drill to 20 mm and a 19 mm and 76 mm hole saw; files and deburring tool; nibbler or jigsaw with a metal blade for the windows; hand rivet nut tool for M4; hand blind rivet tool; 3D printer with a 220 mm bed that prints PETG; soldering iron for the heat-set inserts; scriber, square, steel rule and calipers; crimp tools for lugs and ferrules; wire strippers; multimeter; bench power supply with a current limit (0 to 60 V, 0 to 5 A); clamp meter; torque screwdriver; scale to 15 kg; stopwatch.

**Skills.** Sheet metal marking, drilling, cutting and riveting; basic 3D printing; crimping and low-voltage DC wiring; safe handling of lithium-ion packs. The 230 V side (inverter output to outlet and RCD) needs a qualified electrician to do or check it; everything else is extra-low voltage (54.6 V or less).

**Workspace.** A bench about 1.5 x 0.75 m; a metalwork area kept apart from the electronics so swarf stays off the modules; the charging spot of S1; ventilation for printing PETG.

**Personal protective equipment.** Safety glasses for cutting, drilling and riveting; cut-resistant gloves for sheet metal; hearing protection for the nibbler or jigsaw; no gloves near a turning drill; insulated tools for the battery and bus work.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`python cad/src/model.py --check`, 64 checks); STEP and STL exports in `cad/step/` and `cad/stl/`.
- Pictures: `cad/src/build_plan_media.py`, using `.kit/build_views.py`; written to `docs/05-build-plan/` and `cad/drawings/PBX-DWG-101` to `PBX-DWG-113`.
- General arrangement: `cad/drawings/PBX-DWG-001.pdf`, Rev P2.
- Calculations: `docs/04-calcs/01-sizing.md` (PBX-CAL-001 v0.2) and `docs/04-calcs/sizing.py`; mass and size section 10, protection section 6, thermal section 9.
- Bill of materials: `bom/bom.csv` and `bom/bom-notes.md`.
- Decisions: `docs/decisions/0003-design-for-construction.md` (PBX-DDR-003), with PBX-DDR-001 and PBX-DDR-002; register `docs/06-design-decisions.md` (PBX-DEC-001).
- Requirements: `docs/03-requirements.md` (PBX-REQ-001 v0.5).
