#!/usr/bin/env bash
set -euo pipefail
BASE="https://www.openbookproject.net/books/StudentCSP/"
OUT="StudentCSP-offline"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains www.openbookproject.net,openbookproject.net -P "$OUT" "$BASE"
echo "Done. Open $OUT/www.openbookproject.net/books/StudentCSP/index.html in your browser."
