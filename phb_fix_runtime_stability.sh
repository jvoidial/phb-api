#!/bin/bash

echo "🧠 PHB RUNTIME STABILITY PATCH (DAEMON FIX)"

cat << 'SH' > phb-api/run.sh
#!/bin/bash

echo "🧠 PHB AI OS STARTING (DAEMON MODE)..."

cd "$(dirname "$0")"

# kill only uvicorn safely
pkill -f "uvicorn main:app" || true

sleep 1

# IMPORTANT: keep process attached (no auto-exit wrapper)
exec uvicorn main:app --host 0.0.0.0 --port 8000
SH

chmod +x phb-api/run.sh

echo "✔ Runtime now set to EXEC mode (no shell exit)"
