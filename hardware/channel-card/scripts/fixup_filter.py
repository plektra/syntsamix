# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import os
import re,uuid
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
def blocks(s,head):
    """yield (start,end) of top-level blocks starting with '\n\t(<head>'"""
    i=0
    while True:
        st=s.find('\n\t('+head,i)
        if st<0: return
        j=st+2;d=0
        while True:
            c=s[j]
            if c=='"': j=s.index('"',j+1)
            elif c=='(': d+=1
            elif c==')':
                d-=1
                if d==0: break
            j+=1
        yield st,j+1; i=j+1
p=D+'filter.kicad_sch'; s=open(p).read()
# drop leftover global labels and wires below the page (former PWR_FLAG stubs)
cut=[]
for st,en in blocks(s,'global_label'):
    b=s[st:en]
    if re.search(r'\(at [\d.]+ 444\.5 ',b): cut.append((st,en))
for st,en in blocks(s,'wire'):
    b=s[st:en]
    ys=[float(y) for y in re.findall(r'\(xy [\d.]+ ([\d.]+)\)',b)]
    if ys and max(ys)>425: cut.append((st,en))
for st,en in sorted(cut,reverse=True): s=s[:st]+s[en:]
print('removed',len(cut))
nc=[(191.77,139.7),(191.77,304.8),(265.43,377.19),(265.43,387.35),(353.06,367.03),(353.06,397.51)]
add=''.join(f'\n\t(no_connect (at {x} {y}) (uuid "{uuid.uuid4()}"))' for x,y in nc)
k=s.rfind('\n\t(sheet_instances')
if k<0: k=s.rfind('\n)')
s=s[:k]+add+s[k:]
open(p,'w').write(s)
# root: connect Input outputs to Filter inputs (once)
r=D+'channel-card.kicad_sch'; t=open(r).read()
if '(xy 55.88 40.64) (xy 76.2 40.64)' not in t:
    w=''.join(f'\n\t(wire (pts (xy 55.88 {y}) (xy 76.2 {y})) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))' for y in (40.64,43.18))
    k=t.rfind('\n\t(sheet_instances')
    t=t[:k]+w+t[k:]; open(r,'w').write(t); print('root wires added')
