#!/bin/sh
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Rebuild every wired channel card sheet, then run all checks.
# PY must be a Python with the `mcp` package (the kicad-mcp-pro uv environment).
set -e
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
PY=${PY:-$(ls -d ~/.cache/uv/archive-v0/*/bin/python 2>/dev/null | while read p; do "$p" -c "import mcp" 2>/dev/null && echo "$p" && break; done)}
KICAD_CLI=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
python3 filter_build.py >/dev/null; python3 level_build.py >/dev/null; python3 routing_build.py >/dev/null; python3 meter_build.py >/dev/null
for spec in "input 0" "filter 1" "level 2" "routing 3" "meter 4"; do
  set -- $spec
  python3 ${1}_wired.py >/dev/null
  "$PY" mcpcall.py build/calls_${1}_wired.json 2>/dev/null | grep -q "schematic was updated" || { echo "build failed: $1"; exit 1; }
  python3 post_wired.py ../${1}.kicad_sch $2 build/${1}_wired_extra.json reference/${1}_title.json >/dev/null
done
python3 fix_paths.py >/dev/null
python3 root_links.py >/dev/null
for t in input filter level routing meter; do printf '%s: ' $t; python3 check_netlist.py $t.json | tr '\n' ' '; echo; done
"$KICAD_CLI" sch erc -o build/erc.rpt ../channel-card.kicad_sch >/dev/null 2>&1 || true
grep "ERC messages" build/erc.rpt
