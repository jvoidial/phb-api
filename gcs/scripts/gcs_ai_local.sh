#!/bin/bash

LOG_FILE="$HOME/gcs/logs/gcs_ai.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

echo "[GCS AI] Starting AI command interface..."

while true; do
  read -p "[GCS AI] > " input_line
  input_line=$(echo "$input_line" | tr '[:lower:]' '[:upper:]')

  if [[ "$input_line" == "EXIT" ]]; then
    echo "[GCS AI] Exiting..."
    break
  fi

  # Split input line into commands by spaces
  IFS=' ' read -r -a commands <<< "$input_line"

  for cmd in "${commands[@]}"; do
    case "$cmd" in
      IMMORTALITY_ON|ACTIVATEIMMORTALITY)
        log "Activating immortality protocols..."
        bash "$HOME/gcs/scripts/ImmortalStart.sh"
        log "Immortality protocols activated."
        echo "[GCS AI] Immortality protocols activated."
        ;;
      PORTAL_OPEN|OPENPORTAL)
        log "Opening PHB portal..."
        sleep 2
        log "PHB portal opened."
        echo "[GCS AI] PHB portal opened."
        ;;
      HEAL_START|STARTHEALING)
        log "Triggering healing sequence..."
        sleep 2
        log "Healing sequence completed."
        echo "[GCS AI] Healing sequence completed."
        ;;
      PHB_TEST)
        log "Testing PHB scaffolding system..."
        echo "PHB scaffolding activated."
        echo "Quantum tunneling routes established."
        sleep 2
        log "PHB scaffolding test complete."
        echo "[GCS AI] PHB scaffolding test complete."
        ;;
      *)
        log "Unknown command received: $cmd"
        echo "[GCS AI] Unknown command received: $cmd"
        ;;
    esac
  done
done
