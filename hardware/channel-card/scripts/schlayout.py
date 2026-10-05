# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Small layout helper for wired, human-readable sheets.

Reads pin geometry from the KiCad symbol libraries, places symbols, draws
Manhattan wires between pins and collects labels and power symbols in the
input format of kicad-mcp-pro's sch_build_circuit (no `nets`, so the builder
adds no label stubs). Junctions are written by add_junctions() afterwards.
"""
import math,os,re,json,uuid
KLIB=os.environ.get('KICAD_SYMBOLS','/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols/')
HERE=os.path.dirname(os.path.abspath(__file__))
PROJLIB=os.path.join(HERE,'..','..','libs','syntsamix.kicad_sym')
G=1.27
_cache={}
def _libtext(lib):
    if lib not in _cache:
        _cache[lib]=open(PROJLIB if lib=='syntsamix' else os.path.join(KLIB,lib+'.kicad_sym')).read()
    return _cache[lib]
def _block(text,name):
    i=text.find(f'\n\t(symbol "{name}"')
    if i<0: raise KeyError(name)
    j=text.find('\n\t(symbol "',i+5)
    return text[i:j if j>0 else len(text)]
def pins_of(lib,name,unit=1):
    """{number: (x, y, angle)} in symbol coordinates (y up) for one unit."""
    b=_block(_libtext(lib),name)
    m=re.search(r'\(extends "([^"]+)"\)',b)
    if m: return pins_of(lib,m.group(1),unit)
    out={}
    for sm in re.finditer(r'\n\t\t\(symbol "[^"]*_(\d+)_(\d+)"(.*?)(?=\n\t\t\(symbol "|\n\t\)|\Z)',b,re.S):
        u=int(sm.group(1))
        if u not in (0,unit): continue
        for pm in re.finditer(r'\(pin \w+ \w+\s*\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\).*?\(number "([^"]+)"',sm.group(3),re.S):
            out[pm.group(4)]=(float(pm.group(1)),float(pm.group(2)),float(pm.group(3)))
    return out
def snap(v): return round(round(v/G)*G,2)
class Sheet:
    def __init__(s):
        s.symbols=[];s.wires=[];s.labels=[];s.powers=[];s.pins={}
    def place(s,lib,name,ref,value,x,y,rot=0,unit=None,fp="",props=None):
        x,y=snap(x),snap(y)
        d={"library":lib,"symbol_name":name,"reference":ref,"value":value,"x_mm":x,"y_mm":y,"rotation":rot,"footprint":fp,"properties":props or {}}
        if unit: d["unit"]=unit
        s.symbols.append(d)
        a=math.radians(rot); ca,sa=round(math.cos(a)),round(math.sin(a))
        for n,(px,py,_) in pins_of(lib,name,unit or 1).items():
            rx=px*ca-py*sa; ry=px*sa+py*ca
            s.pins[(ref,n)]=(snap(x+rx),snap(y-ry))
        return lambda n: s.pins[(ref,str(n))]
    def wire(s,*pts):
        pts=[(snap(x),snap(y)) for x,y in pts]
        for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
            if (x1,y1)!=(x2,y2):
                assert x1==x2 or y1==y2, ("diagonal wire",x1,y1,x2,y2)
                s.wires.append({"x1_mm":x1,"y1_mm":y1,"x2_mm":x2,"y2_mm":y2})
    def hv(s,a,b):  # horizontal first, then vertical
        s.wire(a,(b[0],a[1]),b)
    def vh(s,a,b):
        s.wire(a,(a[0],b[1]),b)
    def label(s,name,at,rot=0,kind="local",shape=None):
        d={"name":name,"x_mm":snap(at[0]),"y_mm":snap(at[1]),"rotation":rot}
        if kind=="global": d["kind"]="global_label"
        if kind=="hierarchical": d["kind"]="hierarchical_label"; d["shape"]=shape or "input"
        s.labels.append(d)
    def power(s,name,at,rot=0):
        s.powers.append({"name":name,"x_mm":snap(at[0]),"y_mm":snap(at[1]),"rotation":rot})
    def build_args(s,paper="A2"):
        return {"symbols":s.symbols,"wires":s.wires,"labels":s.labels,"power_symbols":s.powers,"max_paper":paper,"auto_layout":False}
def add_junctions(path):
    """Add a junction wherever three or more wire ends / pins meet, or a wire end lands mid-segment."""
    txt=open(path).read()
    segs=[tuple(map(float,m.groups())) for m in re.finditer(r'\(wire\s+\(pts\s+\(xy ([-\d.]+) ([-\d.]+)\)\s+\(xy ([-\d.]+) ([-\d.]+)\)',txt)]
    from collections import Counter
    ends=Counter()
    for x1,y1,x2,y2 in segs: ends[(x1,y1)]+=1; ends[(x2,y2)]+=1
    pts=set(p for p,n in ends.items() if n>=3)
    for p in ends:
        for x1,y1,x2,y2 in segs:
            if (x1==x2==p[0] and min(y1,y2)<p[1]<max(y1,y2)) or (y1==y2==p[1] and min(x1,x2)<p[0]<max(x1,x2)):
                pts.add(p)
    add=''.join(f'\n\t(junction (at {x:g} {y:g}) (diameter 0) (color 0 0 0 0) (uuid "{uuid.uuid4()}"))' for x,y in sorted(pts))
    k=txt.rfind('\n)'); txt=txt[:k]+add+txt[k:]
    open(path,'w').write(txt); return len(pts)
