# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Check every part in docs/parts.csv against the JLCPCB/LCSC catalogue (jlcsearch.tscircuit.com).

Writes docs/lcsc-check.csv: project part number, what was searched, best match
(basic parts first, then stock), LCSC code, JLC class (basic/extended), stock,
unit price, and a note. Parts meant for hand soldering are marked as such.
Usage: python3 tools/lcsc_check.py
"""
import csv,json,os,re,time,urllib.parse,urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API="https://jlcsearch.tscircuit.com"
def get(path,**q):
    url=f"{API}/{path}?"+urllib.parse.urlencode(q)
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"syntsamix-bom-check"}),timeout=30) as r: return json.load(r)
        except Exception as e: err=e; time.sleep(2)
    return {"error":str(err)}
UNITS={"p":1e-12,"n":1e-9,"u":1e-6,"µ":1e-6,"m":1e-3,"k":1e3,"M":1e6}
def val(text,unit):
    m=re.search(r'([\d.]+)\s*([pnuµkM]?)\s*'+unit,text)
    if not m: return None
    return float(m.group(1))*UNITS.get(m.group(2),1)
def best(items):
    items=[i for i in items if i.get("stock",0)>0]
    items.sort(key=lambda i:(not i.get("is_basic"),not i.get("is_preferred"),-i.get("stock",0)))
    return items[0] if items else None
# what to search for each IC / semiconductor (by part number)
# search terms per part; a result counts only if its manufacturer part number contains the term (fuzzy search guard)
MPN={"SX-IC-001":["SSI2144SS-TU","SSI2144"],"SX-IC-002":["SSI2162SS-TU","SSI2162"],"SX-IC-003":["AD8273ARZ","AD8273"],
     "SX-IC-004":["NE5532DR","NE5532D"],"SX-IC-005":["DG413DY-T1-E3","DG413DY"],"SX-IC-006":["LM13700MX/NOPB","LM13700M"],
     "SX-IC-007":["TL072IDR","TL072CDR"],"SX-IC-008":["DG412DY-T1-E3","DG412DY"],"SX-IC-009":["LM339DR","LM339DT"],
     "SX-IC-010":["LM317T"],"SX-IC-011":["LM337TG","LM337T"],"SX-IC-012":["L78L05ACUTR"],"SX-Q-001":["MMBT3904"],
     "SX-D-001":["BZT52C6V2"],"SX-D-003":["1N4148W"],"SX-D-007":["SS14"],"SX-R-021":["ERA-V33J102V","ERA-V33J102"]}
PKG={"SX-IC-003":"SOIC","SX-IC-004":"SO","SX-IC-005":"SO","SX-IC-006":"SO","SX-IC-007":"SO","SX-IC-008":"SO","SX-IC-009":"SO","SX-IC-010":"TO-220","SX-IC-011":"TO-220","SX-IC-012":"SOT-89","SX-D-001":"SOD-123","SX-D-003":"SOD-123","SX-D-007":"SMA"}
norm=lambda t: re.sub(r'[^A-Z0-9]','',t.upper())
# LCSC codes seen in successful queries on 2026-10-06, used when the flaky search returns nothing; recheck before ordering
KNOWN={"SX-IC-004":("C7426","NE5532DR","basic",91852,0.1064),"SX-IC-005":("C141600","DG413DY-T1-E3","extended",331,""),
       "SX-IC-011":("C73683","LM337TG","extended",5683,""),"SX-D-001":("C19077403","BZT52C6V2","extended",125612,"")}
HAND=("SX-POT","SX-TRIM","SX-CONN","SX-SW","SX-MECH")
rows=[]
for p in csv.DictReader(open(os.path.join(ROOT,'docs','parts.csv'))):
    pn,desc=p["ProjectPN"],p["Description"]
    out={"ProjectPN":pn,"Description":desc,"Search":"","LCSC":"","MPN":"","Class":"","Stock":"","Price":"","Note":""}
    hit=None
    if pn.startswith(HAND) or "radial" in desc or "film" in desc.lower() or "3 mm" in desc or "bipolar" in desc:
        out["Note"]="hand-solder (through-hole or mechanical)"
    elif pn in MPN:
        out["Search"]=" / ".join(MPN[pn])
        for term in MPN[pn]:
            cands=[]
            for attempt in range(3):   # the catalogue search is flaky: retry empty answers
                cands=[c for c in get("components/list.json",search=term).get("components",[]) if norm(term)[:8] in norm(c.get("mfr",""))]
                if cands: break
                time.sleep(3)
            if pn in PKG: cands=[c for c in cands if PKG[pn].upper() in (c.get("package","") or "").upper().replace("SOP","SO").replace("SOIC","SOIC SO")] or cands
            hit=best(cands)
            if hit: break
    elif pn.startswith("SX-R"):
        v=val(desc,"(?:Ohm|kOhm)") ; m=re.search(r'([\d.]+)\s*(k?)Ohm',desc); v=float(m.group(1))*(1e3 if m.group(2) else 1)
        out["Search"]=f"{v:g} Ohm 0805 1%"; r=get("resistors/list.json",resistance=v,package="0805")
        hit=best([c for c in r.get("resistors",[]) if (c.get("tolerance_fraction") or 1)<=0.01])
    elif pn.startswith("SX-C"):
        m=re.search(r'([\d.]+)\s*([pnu])F',desc); v=float(m.group(1))*UNITS[m.group(2)]
        want="C0G" if "C0G" in desc else ("X7R" if "X7R" in desc else "")
        out["Search"]=f"{desc.split(',')[0]}"
        r=get("capacitors/list.json",capacitance=v,package="0805")
        cands=r.get("capacitors",[])
        if want: cands=[c for c in cands if want in (c.get("temperature_coefficient") or "") or (want=="C0G" and "NP0" in (c.get("temperature_coefficient") or ""))]
        hit=best(cands)
    elif pn=="SX-D-002":
        out["Search"]="LED 0805"; hit=best(get("leds/list.json",package="0805").get("leds",[]))
        if hit: out["Note"]="colour to choose; any 0805 LED in this class"
    if hit:
        out.update(LCSC=f"C{hit['lcsc']}",MPN=hit.get("mfr",""),Class="basic" if hit.get("is_basic") else "extended",Stock=hit.get("stock",""),
                   Price=hit.get("price1") or str(hit.get("price","")).split(',')[0].split(':')[-1])
    elif pn in KNOWN:
        c,m,cl,st,pr=KNOWN[pn]; out.update(LCSC=c,MPN=m,Class=cl,Stock=st,Price=pr,Note="from an earlier query on 2026-10-06 (search flaky); recheck")
    elif not out["Note"]: out["Note"]="not found at LCSC: consign or hand-solder"
    rows.append(out); print(f'{pn:12} {out["Class"] or "-":9} {out["LCSC"]:10} {str(out["Stock"]):>8}  {out["MPN"][:28]:28} {out["Note"]}')
with open(os.path.join(ROOT,'docs','lcsc-check.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
