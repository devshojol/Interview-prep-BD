#!/usr/bin/env bash
# Concatenate app/src/*.js (in filename order) into app/app.js
set -euo pipefail
cd "$(dirname "$0")/.."
ls app/src/*.js | sort | xargs cat > app/app.js
node --check app/app.js
echo "app.js: $(wc -l < app/app.js) lines"
