# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import os
p=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+'filter.kicad_sch'
s=open(p).read()
key='(lib_id "power:PWR_FLAG")'
n=0
while True:
    k=s.find(key)
    if k<0: break
    st=s.rfind('\n\t(symbol\n',0,k)
    # balanced scan from st+1
    i=st+1;depth=0
    while True:
        c=s[i]
        if c=='"':
            i=s.index('"',i+1)
        elif c=='(':depth+=1
        elif c==')':
            depth-=1
            if depth==0: break
        i+=1
    s=s[:st]+s[i+1:];n+=1
open(p,'w').write(s);print('removed PWR_FLAG',n)
