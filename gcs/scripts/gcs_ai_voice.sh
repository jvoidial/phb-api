#!/data/data/com.termux/files/usr/bin/bash

LOG_FILE="$HOME/gcs/logs/gcs_ai_voice.log"
COMMAND_FILE="$HOME/gcs/scripts/phb_command.txt"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

speak() {
  termux-tts-speak "$1"
}

interpret() {
  input="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
  cmd=""

  if echo "$input" | grep -qE 'immortal|immortality|live forever'; then
    cmd="IMMORTALITY_ON"
  elif echo "$input" | grep -qE 'heal|repair|fix'; then
    cmd="HEAL_START"
  elif echo "$input" | grep -qE 'portal|open gate|other world|travel'; then
    cmd="PORTAL_OPEN"
  elif echo "$input" | grep -qE 'exit|shutdown|quit'; then
    log "User requested exit."
    speak "Goodbye, immortal one."
    exit 0
  else
    log "Unknown request: $input"
    speak "I did not understand. Try again."
    return
  fi

  echo "$cmd" > "$COMMAND_FILE"
  log "Recognized intent: $cmd"
  speak "Running $cmd now."
}

log "GCS AI Voice Interface Activated."

while true; do
  speak "Speak your command."
  input=$(termux-speech-to-text)
  interpret "$input"
  sleep 2
done
