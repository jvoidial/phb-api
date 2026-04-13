#!/data/data/com.termux/files/usr/bin/sh
set -e

cd "$(dirname "$0")/.."

echo "PHB + P2P ORCHESTRATOR"
echo "-----------------------"

# 1) Run PHB engine via Smart Mode launcher
if [ -x "./run_phb_godcode_vortex.sh" ]; then
    echo "→ Running PHB Smart Mode engine..."
    ./run_phb_godcode_vortex.sh
else
    echo "✗ PHB launcher not found (run_phb_godcode_vortex.sh missing)"
fi

echo
echo "P2P LAYER"
echo "---------"

# 2) Start P2P listener if present
if [ -f "gcs/scripts/p2p_listener.py" ]; then
    echo "→ Starting P2P listener (background)..."
    nohup python3 gcs/scripts/p2p_listener.py > gcs/p2p_listener.log 2>&1 &
    echo "   Log: gcs/p2p_listener.log"
else
    echo "✗ No P2P listener found at gcs/scripts/p2p_listener.py"
fi

# 3) Optional: send a heartbeat / evolution message if sender exists
if [ -f "gcs/scripts/p2p_send.py" ]; then
    echo "→ Sending PHB evolution heartbeat..."
    python3 gcs/scripts/p2p_send.py "PHB_EVOLUTION_HEARTBEAT"
else
    echo "✗ No P2P sender found at gcs/scripts/p2p_send.py"
fi

echo
echo "PHB + P2P orchestration complete."
