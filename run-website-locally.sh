#!/usr/bin/env bash
# Build, gate and serve the site on http://localhost:8000 (the version shows as "pending": only CI numbers releases).
set -euo pipefail
cd "$(dirname "$0")"
python3 admin/build/build.py
python3 admin/build/validate.py
python3 -m http.server 8000 -d _site
