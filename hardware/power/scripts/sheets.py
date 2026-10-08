# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Root sheet layout: writes build/calls_sheets.json, which creates the four sheets once (run with mcpcall.py)."""
import json,os
HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)
SHEETS=(("Input and clock","input.kicad_sch",25.4,38.1,[["VIN_SW","output"],["CLK_A","output"],["CLK_B","output"]]),
        ("+20 V buck","buck.kicad_sch",101.6,25.4,[["VIN_SW","input"],["CLK_A","input"],["+20V_RAW","output"]]),
        ("-20 V inverter","inverter.kicad_sch",101.6,76.2,[["VIN_SW","input"],["CLK_B","input"],["-20V_RAW","output"]]),
        ("Outputs","outputs.kicad_sch",177.8,38.1,[["+20V_RAW","input"],["-20V_RAW","input"]]))
calls=[["kicad_set_project",{"project_dir":CARD,"sch_file":CARD+'/power.kicad_sch'}]]
for name,fn,x,y,pins in SHEETS:
    calls.append(["sch_create_sheet",{"name":name,"filename":fn,"x_mm":x,"y_mm":y,"sheet_pins":pins}])
os.makedirs(HERE+'/build',exist_ok=True)
json.dump(calls,open(HERE+'/build/calls_sheets.json','w'))
print(len(SHEETS),"sheets")
