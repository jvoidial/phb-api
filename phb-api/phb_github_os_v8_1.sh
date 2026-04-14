#!/bin/bash

echo "🧠 PHB GITHUB OS v8.1 HARDENING PATCH"

cd phb-api || exit

# =========================
# CLEAN ENTRYPOINT (NO DUPLICATES)
# =========================
cat << 'SH' > run.sh
#!/bin/bash

echo "🧠 PHB OS v8.1 STARTING (GITHUB SAFE MODE)"

cd "$(dirname "$0")"

# kill only this app instance
pkill -f "uvicorn main:app" || true

sleep 1

# single process runtime
exec uvicorn main:app --host 0.0.0.0 --port 8000
SH

chmod +x run.sh

# =========================
# GITHUB STRUCTURE LOCK
# =========================
mkdir -p .github/workflows

cat << 'YML' > .github/workflows/ci.yml
name: PHB OS CI

on:
  push:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install deps
        run: pip install fastapi uvicorn
      - name: Validate import
        run: python -c "import main; print('PHB OK')"
YML

# =========================
# CLEAN IGNORE RULES
# =========================
cat << 'TXT' > .gitignore
__pycache__/
*.pyc
phb_memory.json
*.log
.venv/
