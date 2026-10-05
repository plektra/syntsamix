#!/bin/sh
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Post-process filter.kicad_sch after sch_build_circuit, then run ERC and the netlist check.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
KICAD_CLI=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
cd "$HERE/.."
F=filter.kicad_sch
sed -i '' -E 's/"U9(10[3-8])[1-5]"/"U\1"/g' $F
sed -i '' -E 's/"#PWR0*([0-9]+)"/"#PWR1\1"/g; s/"#FLG0*([0-9]+)"/"#FLG1\1"/g' $F
sed -i '' -E 's/\(paper "A[0-4]"\)/(paper "A2")/' $F
python3 "$HERE/rmflags.py"
python3 "$HERE/fixup_filter.py"
python3 "$HERE/title_filter.py"
"$KICAD_CLI" sch erc -o "$HERE/build/erc.rpt" channel-card.kicad_sch >/dev/null 2>&1 || true
grep "ERC messages" "$HERE/build/erc.rpt"
python3 "$HERE/check_netlist.py" filter.json
