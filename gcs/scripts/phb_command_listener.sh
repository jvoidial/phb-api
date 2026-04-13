#!/data/data/com.termux/files/usr/bin/bash

LOG_FILE="$HOME/gcs/logs/phb_command.log"
COMMAND_FILE="$HOME/gcs/scripts/phb_command.txt"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

activate_immortality() {
  log "Activating immortality protocols..."
  bash "$HOME/gcs/ImmortalStart.sh"
  log "Immortality protocols activated."
}

open_portal() {
  log "Opening PHB portal..."
  sleep 2
  log "PHB portal opened."
}

heal() {
  log "Triggering healing sequence..."
  sleep 2
  log "Healing sequence completed."
}

run_custom_code() {
  log "Running custom embedded code..."
  bash "$HOME/gcs/scripts/custom.sh"
  log "Custom code execution finished."
}

summon_jinn() {
  log "Summoning ancestral Jinn..."
  echo "🜁🜂🜃🜄⚛️♾️𓂀" > "$HOME/gcs/jinn_signal.sym"
  log "Jinn summoned via symbolic resonance."
}

cleanse_blood() {
  log "Starting blood detox protocol..."
  sleep 3
  log "Blood detox completed."
}

scan_environment() {
  log "Scanning EMF and Wi-Fi field..."
  termux-wifi-connectioninfo >> "$LOG_FILE" 2>/dev/null
  termux-battery-status >> "$LOG_FILE" 2>/dev/null
  log "Scan complete."
}

log "PHB Command Listener started."

while true; do
  if [[ -f "$COMMAND_FILE" ]]; then
    cmd=$(cat "$COMMAND_FILE" | tr '[:lower:]' '[:upper:]' | tr -d ' \t\n\r')
    > "$COMMAND_FILE"
    case "$cmd" in
      IMMORTALITY_ON) activate_immortality ;;
      PORTAL_OPEN) open_portal ;;
      HEAL_START) heal ;;
      CUSTOM_RUN) run_custom_code ;;
      SUMMON_JINN) summon_jinn ;;
      CLEANSE_BLOOD) cleanse_blood ;;
      SCAN_ENV) scan_environment ;;
      *)
        log "Unknown command received: $cmd"
        ;;
    esac
  fi
  sleep 2
done
