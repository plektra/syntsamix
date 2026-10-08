#!/bin/sh
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Rebuild every wired power board sheet, then run all checks (shared tools are linked from ../../channel-card/scripts).
# First run on an empty root: creates the sheets (sheets.py) before drawing them.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=${PY:-$(ls -d ~/.cache/uv/archive-v0/*/bin/python 2>/dev/null | while read p; do "$p" -c "import mcp" 2>/dev/null && echo "$p" && break; done)}
KICAD_CLI=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
SHEETS="input:1 buck:2 inverter:3 outputs:4"   # sheet file name : power-reference prefix
if ! grep -q '"Sheetfile" "input.kicad_sch"' ../power.kicad_sch; then
  python3 sheets.py >/dev/null
  "$PY" mcpcall.py build/calls_sheets.json >/dev/null 2>&1
fi
for spec in $SHEETS; do
  name=${spec%%:*}; pre=${spec##*:}
  [ -f ${name}_wired.py ] || continue
  python3 ${name}_build.py >/dev/null; python3 ${name}_wired.py >/dev/null
  "$PY" mcpcall.py build/calls_${name}_wired.json 2>/dev/null | grep -q "schematic was updated" || { echo "build failed: $name"; exit 1; }
  python3 post_wired.py ../${name}.kicad_sch $pre build/${name}_wired_extra.json reference/${name}_title.json >/dev/null
done
python3 fix_paths.py >/dev/null
python3 root_links.py >/dev/null
for spec in $SHEETS; do name=${spec%%:*}; [ -f ${name}_wired.py ] || continue; printf '%s: ' $name; python3 check_netlist.py $name.json | tr '\n' ' '; echo; done
"$KICAD_CLI" sch erc -o build/erc.rpt ../power.kicad_sch >/dev/null 2>&1 || true
grep "ERC messages" build/erc.rpt
