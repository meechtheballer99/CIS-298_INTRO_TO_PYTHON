#!/usr/bin/env bash
set -euo pipefail
BASE="https://missing.csail.mit.edu/"
OUT="TheMissingSemesterOfYourCS-Education-html-ebook"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains missing.csail.mit.edu -P "$OUT" "$BASE"
echo "Done. Open $OUT/https://missing.csail.mit.edu/ in your browser."
