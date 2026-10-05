# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import os
import re
p=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+'filter.kicad_sch'
s=open(p).read()
tb='''	(title_block
		(title "Channel card: filter")
		(date "2026-10-05")
		(rev "0.1")
		(company "Syntsamix")
		(comment 1 "SSI2144 x2 (datasheet Fig. 1), LM13700 Q VCA (Fig. 9)")
		(comment 2 "JP102/JP152 bass comp: 1-2 half (default), 2-3 full, open none")
		(comment 3 "JP101/JP151 open = hot drive; both fitted = medium")
		(comment 4 "Provisional: R111/R161, R120/R170 (set by breadboard)")
	)
'''
s=re.sub(r'\n\t\(title_block.*?\n\t\)\n','\n',s,flags=re.S)
if True:
    k=s.find('\n\t(lib_symbols')
    s=s[:k+1]+tb+s[k+1:]
    open(p,'w').write(s)
