#!/usr/bin/env bash
set -euo pipefail
BASE="https://automatetheboringstuff.com/2e/" # use https://automatetheboringstuff.com/1e/ for first edition, https://automatetheboringstuff.com/2e/ for 2nd, and https://automatetheboringstuff.com for 3rd edition (latest)
OUT="Python-AutomateTheBoringStuff-2e"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains automatetheboringstuff.com -P "$OUT" "$BASE"
echo "Done. Open $OUT/https://automatetheboringstuff.com/ in your browser."
