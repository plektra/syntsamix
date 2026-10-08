# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import json,os,subprocess,xml.etree.ElementTree as ET
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
subprocess.run([os.environ.get('KICAD_CLI','/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'),'sch','export','netlist','--format','kicadxml','-o',T+'cc.xml',D+os.path.basename(D.rstrip('/'))+'.kicad_sch'],capture_output=True)
import sys
_h=os.path.dirname(os.path.abspath(__file__))
_r=os.path.join(_h,'reference',sys.argv[1])
want=json.load(open(_r if os.path.exists(_r) else T+sys.argv[1]))
import re
fix=lambda r: re.sub(r'^U9(\d{3})[1-9]$',lambda m:f'U{int(m.group(1))}',r)
intended={}
for n in want['nets']:
    for p in n['pins']: intended[(fix(p['ref']),p['pin'])]=n['name']
actual={}
for net in ET.parse(T+'cc.xml').iter('net'):
    for nd in net.iter('node'):
        k=(nd.get('ref'),nd.get('pin'))
        if k in intended: actual[k]=net.get('name')
# map intended -> set of actual
from collections import defaultdict
m=defaultdict(set); inv=defaultdict(set)
for k,n in intended.items():
    a=actual.get(k,'<missing>'); m[n].add(a); inv[a].add(n)
bad=0
for n,a in m.items():
    if len(a)>1: print('SPLIT',n,a); bad+=1
for a,n in inv.items():
    if len(n)>1: print('MERGED',a,n); bad+=1
print('nets checked',len(m),'problems',bad)
import collections
refs=collections.Counter(c.get('ref') for c in ET.parse(T+'cc.xml').iter('comp'))
dup=[r for r,n in refs.items() if n>1]
print('duplicate references:',dup or 'none')
