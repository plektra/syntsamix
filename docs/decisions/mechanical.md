# Mechanical decisions

Frame, panels, strip layout and front-panel parts.

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

55. Channel strip layout follows the signal flow top to bottom: trim, cutoff, resonance, filter bypass, AUX 1, AUX 2, SC send and compressor bus buttons, PFL, mute, then meter beside the fader
59. Mechanical format: desktop unit; one PCB plus FR4 top panel (about 35 mm) per strip; rear-panel PCB-mount jacks; aluminium rail frame cut to length with side cheeks; chain ribbons under the strips
75. Buttons: plain latching DPDT PCB switches, CW Industries GPBS850N (Electrokit 41012905, about 0.57 € each at 25+), with 3D-printed translucent caps lit from below by an 0805 LED beside each switch. Latching mechanics keep every button state through a power cut, which is a must (for example a power cut during a gig). Illuminated latching switches were rejected on cost (about 4 $ each for the cheapest suitable part, E-Switch LP4). Pressed = pins 2-3 and 5-6 closed (datasheet), so the logic line is on pin 3 and the LED on pin 6
86. Meters use small round 3 mm LEDs, on the channel cards (8 segments) and on the master (12 segments per side). Ready-made segmented bar graphs and square LED stacks were judged too bulky; the bar-graph sample is dropped from the second Electrokit order
