# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Freeze a sheet's current netlist and part fields as a reference (reference/<sheet>.json, reference/<sheet>_parts.json, committed).

Usage: make_reference.py <sheet name, e.g. Input> <file stem, e.g. input>
Use before redrawing a sheet that has no build script, so check_netlist.py can prove the new drawing is identical.
"""
import json,os,re,subprocess,sys,xml.etree.ElementTree as ET
HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'; T=os.path.join(HERE,'build')+'/'; REF=os.path.join(HERE,'reference')+'/'
os.makedirs(T,exist_ok=True)
name,stem=sys.argv[1],sys.argv[2]
subprocess.run([os.environ.get('KICAD_CLI','/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'),'sch','export','netlist','--format','kicadxml','-o',T+'ref.xml',CARD+'channel-card.kicad_sch'],capture_output=True,check=True)
x=ET.parse(T+'ref.xml')
refs={c.get('ref') for c in x.iter('comp') if c.find('sheetpath').get('names')==f'/{name}/'}
nets=[]
for n in x.iter('net'):
    pins=[{"ref":nd.get('ref'),"pin":nd.get('pin')} for nd in n.iter('node') if nd.get('ref') in refs]
    if pins: nets.append({"name":re.sub(rf'^/{name}/','',n.get('name')),"pins":pins})
os.makedirs(REF,exist_ok=True)
json.dump({"nets":nets},open(REF+stem+'.json','w'),indent=0)
# part fields from the sheet file
s=open(CARD+stem+'.kicad_sch').read()
parts={}
for m in re.finditer(r'\n\t\(symbol\n\t\t\(lib_id "([^"]+)"\)(.*?)\n\t\)',s,re.S):
    lib,b=m.group(1),m.group(2)
    if lib.startswith('power:'): continue
    props=dict(re.findall(r'\(property "([^"]+)" "([^"]*)"',b))
    unit=int(re.search(r'\(unit (\d+)\)',b).group(1))
    ref=props.pop('Reference'); parts.setdefault(ref,{"lib":lib,"value":props.pop('Value'),"footprint":props.pop('Footprint',''),
        "props":{k:v for k,v in props.items() if k not in ('Datasheet','Description','ki_keywords','ki_fp_filters') and v},"units":[]})
    parts[ref]["units"].append(unit)
json.dump(parts,open(REF+stem+'_parts.json','w'),indent=1)
tb=re.search(r'\(title_block(.*?)\n\t\)',s,re.S)
print(len(nets),'nets',len(parts),'parts'); print(tb.group(0) if tb else 'no title block')
