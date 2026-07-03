#!/usr/bin/env bash
set -euo pipefail
BASE="https://doc.rust-lang.org/stable/book/"
OUT="RustProgammingDocs"
rm -rf "$OUT"
mkdir -p "$OUT"
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent --restrict-file-names=windows --domains doc.rust-lang.org -P "$OUT" "$BASE"
echo "Done. Open $OUT/https://doc.rust-lang.org/stable/book/ in your browser."
