# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import re,uuid,subprocess,os,sys
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
p=D+'level.kicad_sch'; s=open(p).read()
s=re.sub(r'"U9(20[2-6])[1-5]"',r'"U\1"',s)
s=re.sub(r'"#PWR0*([0-9]+)"',r'"#PWR2\1"',s); s=re.sub(r'"#FLG0*([0-9]+)"',r'"#FLG2\1"',s)
s=re.sub(r'\(paper "A[0-4]"\)','(paper "A2")',s)
def blocks(s,head):
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
# remove PWR_FLAG symbols and their stub labels/wires below the page
cut=[]
for st,en in blocks(s,'symbol\n'):
    b=s[st:en]
    if '(lib_id "power:PWR_FLAG")' in b: cut.append((st,en))
    m=re.search(r'"Reference" "R206"',b)
    if m: s_r206=(st,en)
for st,en in blocks(s,'global_label'):
    ys=re.search(r'\(at [\d.]+ ([\d.]+) ',s[st:en])
    if ys and float(ys.group(1))>425: cut.append((st,en))
for st,en in blocks(s,'wire'):
    ys=[float(y) for y in re.findall(r'\(xy [\d.]+ ([\d.]+)\)',s[st:en])]
    if ys and max(ys)>425: cut.append((st,en))
st,en=s_r206; b=s[st:en].replace('(dnp no)','(dnp yes)',1); s=s[:st]+b+s[en:]
for st,en in sorted(cut,reverse=True): s=s[:st]+s[en:]
print('removed',len(cut))
nc=[tuple(map(float,a.split(','))) for a in sys.argv[1:]]
add=''.join(f'\n\t(no_connect (at {x} {y}) (uuid "{uuid.uuid4()}"))' for x,y in nc)
tb='''	(title_block
		(title "Channel card: level")
		(date "2026-10-05")
		(rev "0.1")
		(company "Syntsamix")
		(comment 1 "SSI2162 dual VCA (datasheet Rev 1.2 Fig. 1), Class AB; R206 DNP (fit for Class A)")
		(comment 2 "Fader law: 3-segment, 0 dB at 75 %, -113 dB at bottom; 10 ms smoothing")
		(comment 3 "MUTE: DG413 adds +4.5 V to VC; DUCK: SC_ENV, +1 V = 10 dB")
		(comment 4 "VCA stage inverts, U203 inverts back: POSTFADE same polarity as POSTFILT")
	)
'''
s=re.sub(r'\n\t\(title_block.*?\n\t\)\n','\n',s,flags=re.S)
k=s.find('\n\t(lib_symbols'); s=s[:k+1]+tb+s[k+1:]
k=s.rfind('\n\t(sheet_instances');  k=k if k>0 else s.rfind('\n)')
s=s[:k]+add+s[k:]
open(p,'w').write(s)
r=D+'channel-card.kicad_sch'; t=open(r).read()
if '(xy 106.68 40.64) (xy 127 40.64)' not in t:
    w=''.join(f'\n\t(wire (pts (xy 106.68 {y}) (xy 127 {y})) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))' for y in (40.64,43.18))
    k=t.rfind('\n\t(sheet_instances'); t=t[:k]+w+t[k:]; open(r,'w').write(t); print('root wires added')
