#!/data/data/com.termux/files/usr/bin/bash

LOG_FILE="$HOME/gcs/logs/gcs_ai.log"
PHB_CMD_FILE="$HOME/gcs/scripts/phb_command.txt"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

to_uppercase_no_spaces() {
  echo "$1" | tr '[:lower:]' '[:upper:]' | tr -d ' \t\n\r'
}

ai_interface() {
  log "GCS AI Interface Activated. Speak your command."
  while true; do
    printf "\n[GCS AI] > "
    read -r user_input

    case "$(to_uppercase_no_spaces "$user_input")" in
      *IMMORTALITY*|*LIVEFOREVER*)
        log "Command understood: IMMORTALITY_ON"
        echo "IMMORTALITY_ON" > "$PHB_CMD_FILE"
        ;;
      *HEAL*|*CURE*)
        log "Command understood: HEAL_START"
        echo "HEAL_START" > "$PHB_CMD_FILE"
        ;;
      *PORTAL*|*GATE*)
        log "Command understood: PORTAL_OPEN"
        echo "PORTAL_OPEN" > "$PHB_CMD_FILE"
        ;;
      *JINN*|*SPIRIT*)
        log "Command understood: SUMMON_JINN"
        echo "SUMMON_JINN" > "$PHB_CMD_FILE"
        ;;
      *CLEANSE*|*DETOX*)
        log "Command understood: CLEANSE_BLOOD"
        echo "CLEANSE_BLOOD" > "$PHB_CMD_FILE"
        ;;
      *SCAN*|*ANALYZE*)
        log "Command understood: SCAN_ENV"
        echo "SCAN_ENV" > "$PHB_CMD_FILE"
        ;;
      *CUSTOM*|*RUNSCRIPT*)
        log "Command understood: CUSTOM_RUN"
        echo "CUSTOM_RUN" > "$PHB_CMD_FILE"
        ;;
      *EXIT*|*QUIT*)
        log "Exiting GCS AI Interface."
        break
        ;;
      *)
        log "Unknown command. Try again."
        ;;
    esac
    sleep 1
  done
}

ai_interface
