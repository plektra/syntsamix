# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Search the Mouser catalogue (Search API v1/v2, https://api.mouser.com; keyword and part number, at most 50 parts per call).

The API key comes from the macOS Keychain, never from a file in the repo. Store it once:
  security add-generic-password -s mouser-api -a key -w
(prompts for the value; a Search API key from mouser.com, My Account > APIs). MOUSER_API_KEY overrides the Keychain.
Mouser's API has no parametric filters: use specific keywords, then check ProductAttributes (--json) or the datasheet.

Usage:
  python3 tools/mouser.py search "alpha 9mm potentiometer 10k" [--in-stock] [--rohs] [--limit N] [--start N]
  python3 tools/mouser.py search KEYWORD --mfr "Alps Alpine"     keyword within one manufacturer (v2)
  python3 tools/mouser.py part MPN[|MPN ...] [--exact]           up to 10 part numbers, Mouser or maker's
  python3 tools/mouser.py manufacturers                          manufacturer names (v2)
Prints one line per part (Mouser no., maker, MPN, description, stock, price breaks, datasheet); --json gives the full response.
"""
import argparse,json,os,subprocess,sys,urllib.error,urllib.request
API="https://api.mouser.com/api"
def key():
    if os.environ.get("MOUSER_API_KEY"): return os.environ["MOUSER_API_KEY"]
    try: return subprocess.run(["security","find-generic-password","-s","mouser-api","-a","key","-w"],capture_output=True,text=True,check=True).stdout.strip()
    except (subprocess.CalledProcessError,FileNotFoundError): sys.exit("No Mouser key: set MOUSER_API_KEY or store it with  security add-generic-password -s mouser-api -a key -w")
def call(path,body=None):
    url=f"{API}/{path}?apiKey={key()}"
    req=urllib.request.Request(url,data=None if body is None else json.dumps(body).encode(),headers={"Content-Type":"application/json","Accept":"application/json","User-Agent":"syntsamix-mouser"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error":e.code,"path":path,"body":e.read().decode(errors="replace")[:2000]}
def brief(r):
    if r.get("Errors"): print("errors:",r["Errors"])
    s=r.get("SearchResults") or {}; print(f"{s.get('NumberOfResult','?')} results")
    for p in s.get("Parts") or []:
        pb=", ".join(f"{b['Quantity']}: {b['Price']}" for b in (p.get("PriceBreaks") or [])[:4])
        print(f"{p.get('MouserPartNumber')} | {p.get('Manufacturer')} {p.get('ManufacturerPartNumber')} | {p.get('Description')} | {p.get('Availability') or 'no stock'} | {pb} | {p.get('LifecycleStatus') or ''} | {p.get('DataSheetUrl') or ''}")
def main():
    a=argparse.ArgumentParser(description=__doc__.split("\n")[0])
    a.add_argument("command"); a.add_argument("args",nargs="*")
    a.add_argument("--in-stock",action="store_true"); a.add_argument("--rohs",action="store_true"); a.add_argument("--exact",action="store_true")
    a.add_argument("--mfr"); a.add_argument("--limit",type=int,default=20); a.add_argument("--start",type=int,default=0); a.add_argument("--json",action="store_true")
    o=a.parse_args(); kw=" ".join(o.args)
    opt={(False,False):"None",(False,True):"Rohs",(True,False):"InStock",(True,True):"RohsAndInStock"}[(o.in_stock,o.rohs)]
    if o.command=="search" and o.mfr:
        r=call("v2/search/keywordandmanufacturer",{"SearchByKeywordMfrNameRequest":{"keyword":kw,"manufacturerName":o.mfr,"records":o.limit,"pageNumber":o.start//max(o.limit,1)+1,"searchOptions":opt}})
    elif o.command=="search":
        r=call("v1/search/keyword",{"SearchByKeywordRequest":{"keyword":kw,"records":o.limit,"startingRecord":o.start,"searchOptions":opt}})
    elif o.command=="part":
        r=call("v1/search/partnumber",{"SearchByPartRequest":{"mouserPartNumber":"|".join(o.args),"partSearchOptions":"Exact" if o.exact else "None"}})
    elif o.command=="manufacturers": r=call("v2/search/manufacturerlist")
    else: sys.exit(f"unknown command {o.command}")
    if o.json or "error" in r or o.command=="manufacturers": print(json.dumps(r,indent=1,ensure_ascii=False))
    else: brief(r)
if __name__=="__main__": main()
