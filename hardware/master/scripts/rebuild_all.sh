#!/bin/sh
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Rebuild every wired master card sheet, then run all checks (shared tools are linked from ../../channel-card/scripts).
set -e
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=${PY:-$(ls -d ~/.cache/uv/archive-v0/*/bin/python 2>/dev/null | while read p; do "$p" -c "import mcp" 2>/dev/null && echo "$p" && break; done)}
KICAD_CLI=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
SHEETS="bus:1 aux_return1:2 aux_return2:3 power:9"   # sheet file name : power-reference prefix
for f in *_build.py *_wired.py; do [ "$f" = post_wired.py ] || python3 "$f" >/dev/null; done
for spec in $SHEETS; do
  name=${spec%%:*}; pre=${spec##*:}
  "$PY" mcpcall.py build/calls_${name}_wired.json 2>/dev/null | grep -q "schematic was updated" || { echo "build failed: $name"; exit 1; }
  python3 post_wired.py ../${name}.kicad_sch $pre build/${name}_wired_extra.json reference/${name}_title.json >/dev/null
done
python3 fix_paths.py >/dev/null
python3 root_links.py >/dev/null
for spec in $SHEETS; do name=${spec%%:*}; printf '%s: ' $name; python3 check_netlist.py $name.json | tr '\n' ' '; echo; done
"$KICAD_CLI" sch erc -o build/erc.rpt ../master.kicad_sch >/dev/null 2>&1 || true
grep "ERC messages" build/erc.rpt
