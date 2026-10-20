#!/bin/sh
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Build the power board PCB from the scripts: placement.py --apply, route_power.py, autoroute.py, on a copy of the
# project; Freerouting differs from run to run, so take the first run with no DRC errors and nothing unconnected
# (silkscreen warnings aside, schematic parity on) and copy its board and project file in. KiCad must be closed.
# Usage: scripts/build_pcb.sh [max runs, default 5]
set -e
HERE=$(cd "$(dirname "$0")" && pwd); PROJ=$(dirname "$HERE")
KPY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3
KCLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
if pgrep -f 'KiCad.app/Contents/MacOS' >/dev/null; then echo "close KiCad first"; exit 1; fi
WORK=$(mktemp -d "${TMPDIR:-/tmp}/powerpcb.XXXXXX")
ln -s "$(dirname "$PROJ")/libs" "$WORK/libs"
n=1; max=${1:-5}
while [ "$n" -le "$max" ]; do
  R="$WORK/run$n"; mkdir -p "$R/scripts"
  cp "$PROJ"/power.kicad_pro "$PROJ"/power.kicad_pcb "$PROJ"/*.kicad_sch "$PROJ"/fp-lib-table "$R"/
  cp "$HERE"/placement.py "$HERE"/route_power.py "$HERE"/autoroute.py "$R/scripts/"
  (cd "$R/scripts" && "$KPY" placement.py --apply && "$KPY" route_power.py "$R" && "$KPY" autoroute.py "$R") >"$R/build.log" 2>&1 || { echo "run $n: script failed, see $R/build.log"; exit 1; }
  "$KCLI" pcb drc --severity-error --severity-warning --schematic-parity -o "$R/drc.rpt" "$R/power.kicad_pcb" >/dev/null 2>&1 || true
  bad=$(grep -E '^\[' "$R/drc.rpt" | grep -v -E '^\[silk_' | wc -l | tr -d ' ')
  echo "run $n: $bad problems other than silkscreen"
  if [ "$bad" = 0 ]; then
    cp "$R/power.kicad_pcb" "$R/power.kicad_pro" "$PROJ"/
    echo "board written from run $n ($R)"; exit 0
  fi
  n=$((n + 1))
done
echo "no clean run in $max; boards and reports kept in $WORK"; exit 1
