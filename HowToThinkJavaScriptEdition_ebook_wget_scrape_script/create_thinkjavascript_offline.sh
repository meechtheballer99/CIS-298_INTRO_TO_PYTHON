#!/usr/bin/env bash
set -euo pipefail
BASE="https://matt.curinga.com/think-js/"
OUT="HowToThinkJavascript-offline"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains www.openbookproject.net,openbookproject.net -P "$OUT" "$BASE"
echo "Done. Open $OUT/https://matt.curinga.com/think-js/ in your browser."
