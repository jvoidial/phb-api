#!/bin/bash
# ================================
# HOLYENGINE-C HYBRID NGROK LAUNCHER
# ================================

# start ngrok tunnel
~/bin/ngrok http 8080 --authtoken 3C1ehatBGsnSLy9szm5vV3MAPHZ_3L85jNynuwgo39UVUFpgf &

# start Flask P2P server
python3 ~/gcs/scripts/phb_p2p_server.py &

# wait for tunnels to initialize
sleep 5

# start autonomous runtime
python3 ~/gcs/scripts/holyenginec_auto_hybrid.py
