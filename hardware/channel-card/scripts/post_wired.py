# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Post-process a wired sheet built from a schlayout script.

Usage: post_wired.py <sheet.kicad_sch> <ref digit prefix, e.g. 2> <extra.json> <title.json>
Renames temporary unit references, prefixes power references, renames the
GNDA/GNDPWR symbols' values to the project nets AGND/PGND, adds junctions,
no-connect markers, the title block and DNP flags.
"""
import json,re,sys,uuid,os
from schlayout import add_junctions
p,pre,extra,title=sys.argv[1],sys.argv[2],json.load(open(sys.argv[3])),json.load(open(sys.argv[4]))
LEFT=set(title.get('left_fields',[]))
s=open(p).read()
s=re.sub(r'"U9(\d{3})[1-5]"',lambda m:f'"U{int(m.group(1))}"',s)
s=re.sub(r'"#PWR0*([0-9]+)"',lambda m:f'"#PWR{pre}{int(m.group(1)):03d}"',s)
s=re.sub(r'\(paper "A[0-4]"\)','(paper "A2")',s)
ls=s.find('\n\t(lib_symbols'); le=s.find('\n\t)\n',ls)+4   # leave the embedded library copies untouched
body=s[le:].replace('(property "Value" "GNDA"','(property "Value" "AGND"').replace('(property "Value" "GNDPWR"','(property "Value" "PGND"')
s=s[:le]+body
for ref in title.get("dnp",[]):
    i=s.find(f'(property "Reference" "{ref}"'); st=s.rfind('\n\t(symbol\n',0,i)
    seg=s[st:i].replace('(dnp no)','(dnp yes)',1); s=s[:st]+seg+s[i:]
tb='\t(title_block\n'+''.join(f'\t\t({k} "{v}")\n' for k,v in (("title",title["title"]),("date",title["date"]),("rev",title["rev"]),("company","Syntsamix")))
tb+=''.join(f'\t\t(comment {i+1} "{c}")\n' for i,c in enumerate(title["comments"]))+'\t)\n'
s=re.sub(r'\n\t\(title_block.*?\n\t\)\n','\n',s,flags=re.S)
k=s.find('\n\t(lib_symbols'); s=s[:k+1]+tb+s[k+1:]
nc=''.join(f'\n\t(no_connect (at {x:g} {y:g}) (uuid "{uuid.uuid4()}"))' for x,y in extra.get("no_connect",[]))
k=s.rfind('\n)'); s=s[:k]+nc+s[k:]
# readable fields: upright text, reference and value beside the part
def place_fields(blk):
    m=re.search(r'\(lib_id "([^"]+)"\)\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)',blk)
    lib,x,y,rot=m.group(1),float(m.group(2)),float(m.group(3)),int(float(m.group(4)))
    def setf(b,name,fx,fy,just):
        def r(mm):
            prop=mm.group(0)
            prop=re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)',f'(at {fx:g} {fy:g} {0 if lib in ("Device:D","Device:LED") else (90 if rot in (90,270) else 0)})',prop,count=1)
            prop=re.sub(r'\s*\(justify[^)]*\)','',prop)
            if just:
                j={'left':'right','right':'left'}[just] if rot in (180,270) else just   # KiCad mirrors justification on these rotations
                prop=prop.replace('(effects','(effects (justify '+j+')',1)
            return prop
        return re.sub(r'\(property "'+name+r'" "[^"]*"\s*\(at [^)]*\).*?\(effects',r,b,count=1,flags=re.S)
    ref=re.search(r'\(property "Reference" "([^"]+)"',blk).group(1)
    if lib.startswith('power:'):
        return re.sub(r'(\(property "(?:Value|Reference)" "[^"]*"\s*\(at [-\d.]+ [-\d.]+ )180\)',r'\g<1>0)',blk)
    vertical=(lib in ('Device:R','Device:C','Device:R_Potentiometer','Device:R_Potentiometer_Trim') and rot in (0,180)) or (lib in ('Device:D','Device:LED') and rot in (90,270))
    horizontal=(lib in ('Device:R','Device:C') and rot in (90,270)) or (lib in ('Device:D','Device:LED') and rot in (0,180))
    if vertical:
        left=(ref in LEFT) or (lib=='Device:R_Potentiometer' and rot==0)
        dx=-2.54 if left else 2.54; just='right' if left else 'left'
        blk=setf(blk,'Reference',x+dx,y-1.27,just); blk=setf(blk,'Value',x+dx,y+1.27,just)
    elif horizontal:
        blk=setf(blk,'Reference',x,y-2.54,None); blk=setf(blk,'Value',x,y+2.54,None)
    else:
        blk=re.sub(r'(\(property "(?:Value|Reference)" "[^"]*"\s*\(at [-\d.]+ [-\d.]+ )180\)',r'\g<1>0)',blk)
    return blk
parts=re.split(r'(?=\n\t\(symbol\n\t\t\(lib_id)',s)
s=parts[0]+''.join(place_fields(b) for b in parts[1:])
open(p,'w').write(s)
print('junctions',add_junctions(p))
