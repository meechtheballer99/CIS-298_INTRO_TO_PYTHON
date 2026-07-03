#!/usr/bin/env bash
set -euo pipefail
BASE="https://go.dev/doc/effective_go"
OUT="GoProgramming-html-docs"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains go.dev -P "$OUT" "$BASE"
echo "Done. Open $OUT/https://go.dev/doc/effective_go in your browser."
