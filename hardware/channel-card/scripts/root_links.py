# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Label root sheet pins that appear on more than one sheet with their name, so they connect.

Pins that already have a wire get the label right on the pin; free pins get a short stub
(left for inputs, right for outputs) ending in the label. Idempotent: existing root labels
are removed and rewritten each run.
"""
import os,re,uuid
CARD=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
PROJ=os.path.basename(CARD.rstrip('/'))   # project name = folder name (channel-card, master, ...)
p=CARD+PROJ+'.kicad_sch'; s=open(p).read()
# drop labels written by an earlier run
MARK='c0ffee00'   # uuid prefix of items written by this script (KiCad files allow no comments)
def uid(): return MARK+str(uuid.uuid4())[8:]
# drop items written by an earlier run: one-line blocks with our uuid prefix, or KiCad's multi-line re-save of them
s=re.sub(r'\n\t\((?:label|wire)\b(?:(?!\n\t\().)*?\(uuid "'+MARK+r'[^"]*"\)\s*\)','',s,flags=re.S)
ends=set()
for m in re.finditer(r'\(xy ([-\d.]+) ([-\d.]+)\)',s): ends.add((float(m.group(1)),float(m.group(2))))
from collections import Counter
pins=list(re.finditer(r'\(pin "([^"]+)" (input|output|bidirectional|passive)\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)',s))
shared={n for n,c in Counter(m.group(1) for m in pins).items() if c>1}   # only pins that link two sheets
add=[]
for m in re.finditer(r'\(pin "([^"]+)" (input|output|bidirectional|passive)\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)',s):
    name,kind,x,y,a=m.group(1),m.group(2),float(m.group(3)),float(m.group(4)),float(m.group(5))
    if name not in shared: continue
    out=1 if int(a)==0 else -1          # pin angle 0: pin on the sheet's right edge
    if (x,y) in ends: lx,ly=x,y
    else:
        lx,ly=x+out*5.08,y
        add.append(f'\n\t(wire (pts (xy {x:g} {y:g}) (xy {lx:g} {ly:g})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
    just='left' if out>0 else 'right'
    add.append(f'\n\t(label "{name}" (at {lx:g} {ly:g} {0 if out>0 else 180}) (fields_autoplaced yes) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid "{uid()}"))')
k=s.rfind('\n\t(sheet_instances'); s=s[:k]+''.join(add)+s[k:]
open(p,'w').write(s); print(len([a for a in add if 'label' in a]),'labels')
