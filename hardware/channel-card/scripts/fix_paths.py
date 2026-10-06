# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Rewrite symbol instance paths in the child sheets to /<root uuid>/<sheet uuid>.

sch_build_circuit writes each child sheet's symbol instances as /<child file uuid>,
which kicad-cli accepts but the KiCad app repairs on load ("An error was found when
loading the schematic that has been automatically fixed"). It also writes a
sheet_instances block into the child file, which only the root sheet should have.
It also leaves the instances' project name empty. Run after every rebuild.

It also renumbers the sheets' page numbers: sch_create_sheet gives every new sheet
page "2", and duplicate page numbers are the other thing the KiCad app repairs.
"""
import os,re
CARD=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
PROJ=os.path.basename(CARD.rstrip('/'))   # project name = folder name (channel-card, master, ...)
root=open(CARD+PROJ+'.kicad_sch').read()
root_uuid=re.search(r'\(uuid "([^"]+)"\)',root).group(1)
for m in re.finditer(r'\n\t\(sheet\n',root):
    i=root.find('"Sheetfile" "',m.start()); f=re.match(r'"Sheetfile" "([^"]+)"',root[i:]).group(1)
    sheet_uuid=re.findall(r'\n\t\t\(uuid "([^"]+)"\)',root[m.start():i])[0]
    p=CARD+f; s=open(p).read()
    file_uuid=re.search(r'\(uuid "([^"]+)"\)',s).group(1)
    n=s.count(f'(path "/{file_uuid}"')
    s=s.replace(f'(path "/{file_uuid}"',f'(path "/{root_uuid}/{sheet_uuid}"')
    s=s.replace('(project ""','(project "'+PROJ+'"')
    s=re.sub(r'\n\t\(sheet_instances\n\t\t\(path "/"\n\t\t\t\(page "[^"]*"\)\n\t\t\)\n\t\)','',s)
    open(p,'w').write(s); print(f,'paths fixed',n)

# unique page numbers, ordered by the sheet's position on the root (signal flow left to right, then top to bottom)
root=open(CARD+PROJ+'.kicad_sch').read()
blocks=re.split(r'(?=\n\t\(sheet\n)',root)
pos=lambda b: tuple(float(v) for v in re.search(r'\(at ([\d.]+) ([\d.]+)',b).groups())
xs=sorted(pos(b) for b in blocks[1:])   # left to right, then top to bottom
out=[blocks[0]]
for b in blocks[1:]:
    pg=2+xs.index(pos(b))
    out.append(re.sub(r'(\(instances\s*\(project "[^"]*"\s*\(path "/[^"]*"\s*)\(page "\d+"\)',lambda m:m.group(1)+f'(page "{pg}")',b,count=1))
root2=''.join(out)
if root2!=root:
    open(CARD+PROJ+'.kicad_sch','w').write(root2); print('pages renumbered')
