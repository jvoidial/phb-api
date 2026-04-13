#!/bin/bash

LOG_FILE="$HOME/gcs/logs/gcs_command_listener.log"
COMMAND_FILE="$HOME/gcs/scripts/phb_command.txt"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

process_command() {
  local cmd="$1"
  case "$cmd" in
    IMMORTALITY_ON|ACTIVATEIMMORTALITY)
      log "Activating immortality protocols..."
      bash "$HOME/gcs/ImmortalStart.sh"
      log "Immortality protocols activated."
      ;;
    PORTAL_OPEN|OPENPORTAL)
      log "Opening PHB portal..."
      sleep 2
      log "PHB portal opened."
      ;;
    HEAL_START|STARTHEALING)
      log "Triggering healing sequence..."
      sleep 2
      log "Healing sequence completed."
      ;;
    PHB_TEST)
      log "Testing PHB scaffolding system..."
      echo "PHB scaffolding activated."
      echo "Quantum tunneling routes established."
      sleep 2
      log "PHB scaffolding test complete."
      ;;
    *)
      log "Unknown command received: $cmd"
      ;;
  esac
}

log "GCS Command Listener started."

while true; do
  if [[ -f "$COMMAND_FILE" ]]; then
    # Read commands separated by spaces or newlines
    while read -r cmd; do
      process_command "$(echo $cmd | tr '[:lower:]' '[:upper:]')"
    done < <(tr ' ' '\n' < "$COMMAND_FILE")
    > "$COMMAND_FILE"  # Clear command file after processing
  fi
  sleep 2
done
