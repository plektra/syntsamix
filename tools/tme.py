# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Search and look up parts in the TME catalogue (API v2, https://api.tme.eu, OAuth 2.0 client credentials).

Credentials come from the macOS Keychain, never from a file in the repo. Store them once:
  security add-generic-password -s tme-api -a token -w
  security add-generic-password -s tme-api -a secret -w
(each prompts for the value; the token and application secret come from developers.tme.eu).
Environment variables TME_TOKEN and TME_APP_SECRET override the Keychain.

Usage:
  python3 tools/tme.py search "potentiometer 10k" [--category ID (needs a phrase too)] [--param ID=VALUE[,VALUE]] [--limit N] [--sort PRICE_FIRST_QUANTITY --direction asc] [--in-stock]
  python3 tools/tme.py product SYMBOL [SYMBOL ...]      basic data (max 50 symbols)
  python3 tools/tme.py params SYMBOL [SYMBOL ...]       technical parameters
  python3 tools/tme.py stock SYMBOL [SYMBOL ...]        prices and stock (max 50 symbols); --qty N adds delivery for N of each
  python3 tools/tme.py files SYMBOL [SYMBOL ...]        datasheets, drawings, photos
  python3 tools/tme.py similar SYMBOL | related SYMBOL
  python3 tools/tme.py categories                       category tree
  python3 tools/tme.py get /products/... key=value ...  any GET endpoint (keys ending in [] may repeat)
Options for every command: --country FI --currency EUR --lang en. Output is JSON, except search, which prints one
line per product and the filters as name (id): value (id)xcount; --json gives the full response, --values N more filter values.
"""
import argparse,base64,json,os,subprocess,sys,urllib.error,urllib.parse,urllib.request
API="https://api.tme.eu"
def secret(account,env):
    if os.environ.get(env): return os.environ[env]
    try: return subprocess.run(["security","find-generic-password","-s","tme-api","-a",account,"-w"],capture_output=True,text=True,check=True).stdout.strip()
    except (subprocess.CalledProcessError,FileNotFoundError): sys.exit(f"No TME {account}: set {env} or store it with  security add-generic-password -s tme-api -a {account} -w")
def token():
    basic=base64.b64encode(f"{secret('token','TME_TOKEN')}:{secret('secret','TME_APP_SECRET')}".encode()).decode()
    req=urllib.request.Request(API+"/auth/token",data=b"grant_type=client_credentials",headers={"Authorization":"Basic "+basic,"Content-Type":"application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)["access_token"]
def get(path,query,lang):
    url=API+path+"?"+urllib.parse.urlencode(query,doseq=True)
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+token(),"Accept-Language":lang,"User-Agent":"syntsamix-tme"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
    except urllib.error.HTTPError as e: return {"error":e.code,"url":url,"body":e.read().decode(errors="replace")[:2000]}
def main():
    p=argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("command"); p.add_argument("args",nargs="*")
    p.add_argument("--country",default="FI"); p.add_argument("--currency",default="EUR"); p.add_argument("--lang",default="en")
    p.add_argument("--category"); p.add_argument("--param",action="append",default=[]); p.add_argument("--limit",type=int,default=20)
    p.add_argument("--page",type=int,default=1); p.add_argument("--sort",default="ACCURACY_IN_STOCK_FIRST"); p.add_argument("--direction",default="desc"); p.add_argument("--in-stock",action="store_true")
    p.add_argument("--json",action="store_true"); p.add_argument("--qty",type=int); p.add_argument("--values",type=int,default=12)
    a=p.parse_args(); c=a.command; q={"country":a.country}
    if c=="search":
        q.update({"scope[]":["products","parameters","counters"],"limit":a.limit,"page":a.page,"sort[property]":a.sort,"sort[direction]":a.direction})
        if a.in_stock: q["filter[in_stock]"]="true"
        if a.args: q["phrase"]=" ".join(a.args)
        if a.category: q["category_id"]=a.category
        for i,spec in enumerate(a.param):
            pid,vals=spec.split("=",1); q[f"parameters[{i}][id]"]=pid; q[f"parameters[{i}][values][]"]=vals.split(",")
        path="/products/search"
    elif c=="product": path="/products"; q["symbols[]"]=a.args
    elif c=="stock":
        path="/products/data"; q.update({"symbols[]":a.args,"currency":a.currency,"scope[]":["prices","stock"]})
        if a.qty: q["scope[]"].append("delivery"); q["amounts[]"]=[a.qty]*len(a.args)
    elif c in ("params","files","similar","related"):
        path="/products/"+{"params":"parameters"}.get(c,c)
        if c in ("params","files"): q["symbols[]"]=a.args
        else: q["symbol"]=a.args[0]
    elif c=="categories": path="/products/categories/tree"
    elif c=="get":
        path=a.args[0]
        for kv in a.args[1:]:
            k,v=kv.split("=",1); q.setdefault(k,[]).append(v) if k.endswith("[]") else q.__setitem__(k,v)
    else: sys.exit(f"unknown command {c}")
    r=get(path,q,a.lang)
    if c=="search" and not a.json and "data" in r: brief(r["data"],a.values)
    else: print(json.dumps(r,indent=1,ensure_ascii=False))
def brief(d,nvals):
    """One line per product, then the filterable parameters (use the ids with --param ID=VALUE_ID)."""
    n=d.get("counters",{}); print(f"{n.get('count','?')} products, page {n.get('page','?')} of {n.get('pages','?')}")
    for e in d.get("products",{}).get("elements",[]):
        print(f"{e['symbol']} | {e['manufacturer']['name']} {','.join(e.get('manufacturer_symbols',[]))} | {e['description']} | cat {e['category']['id']} {e['category']['name']} | min {e.get('minimal_amount')}")
    print("filters:")
    for g in d.get("parameters",{}).get("elements",[]):
        vs=sorted(g["values"],key=lambda v:-v.get("products_count",0)); more=len(vs)-nvals
        print(f"  {g['name']} ({g['id']}): "+"; ".join(f"{v['value']} ({v['id']})x{v['products_count']}" for v in vs[:nvals])+(f"; +{more} more" if more>0 else ""))
if __name__=="__main__": main()
