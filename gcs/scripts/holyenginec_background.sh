#!/bin/bash
LOG_DIR=~/gcs/logs
SCRIPT_DIR=~/gcs/scripts
nohup python3 -u "$SCRIPT_DIR/holyenginec_auto_hybrid_full.py" >> "$LOG_DIR/phb_runtime.log" 2>&1 &
echo "[PHB] All processes started in background. Logs: $LOG_DIR"
