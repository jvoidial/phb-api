#!/bin/bash

BASE_DIR="$HOME/gcs"
SCRIPT_DIR="$BASE_DIR/scripts"
LOG_DIR="$BASE_DIR/logs"
COMMAND_FILE="$SCRIPT_DIR/phb_command.txt"
RECEIVE_FILE="$SCRIPT_DIR/p2p_receive.txt"
SEND_FILE="$SCRIPT_DIR/p2p_send.txt"
COMMAND_LOG="$LOG_DIR/gcs_command_listener.log"
AI_LOG="$LOG_DIR/gcs_ai_local.log"

mkdir -p "$SCRIPT_DIR" "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$COMMAND_LOG"
}

activate_immortality() {
  log "Activating immortality protocols..."
  sleep 1
  log "Immortality protocols activated."
}

open_portal() {
  log "Opening PHB portal..."
  sleep 2
  log "PHB portal opened."
}

start_healing() {
  log "Triggering healing sequence..."
  sleep 2
  log "Healing sequence completed."
}

phb_test() {
  log "Testing PHB scaffolding system..."
  echo "PHB scaffolding activated."
  echo "Quantum tunneling routes established."
  sleep 2
  log "PHB scaffolding test complete."
}

# Process commands line-by-line from given input string
process_commands() {
  local input="$1"
  # Split input by space or newline, trim empty
  IFS=$'\n ' read -r -a cmds <<< "$input"
  for cmd in "${cmds[@]}"; do
    cmd_upper=$(echo "$cmd" | tr '[:lower:]' '[:upper:]' | tr -d ' \t\r')
    if [ -z "$cmd_upper" ]; then
      continue
    fi
    log "Received command: $cmd_upper"
    case "$cmd_upper" in
      IMMORTALITY_ON|ACTIVATEIMMORTALITY)
        activate_immortality
        ;;
      PORTAL_OPEN|OPENPORTAL)
        open_portal
        ;;
      HEAL_START|STARTHEALING)
        start_healing
        ;;
      PHB_TEST)
        phb_test
        ;;
      *)
        log "Unknown command: $cmd_upper"
        ;;
    esac
  done
}

# Command listener: reads commands from COMMAND_FILE every second and clears file
command_listener() {
  log "GCS Command Listener started."
  while true; do
    if [[ -s "$COMMAND_FILE" ]]; then
      cmds=$(cat "$COMMAND_FILE")
      > "$COMMAND_FILE"
      process_commands "$cmds"
    fi
    # Also check if new P2P messages are received
    if [[ -s "$RECEIVE_FILE" ]]; then
      p2p_msg=$(cat "$RECEIVE_FILE")
      > "$RECEIVE_FILE"
      log "[P2P] Received message:"
      echo "$p2p_msg" | while read -r line; do
        log "[P2P CMD] $line"
        process_commands "$line"
      done
    fi
    sleep 1
  done
}

# Simulated P2P send: write commands to SEND_FILE
p2p_send() {
  local msg="$1"
  echo "$msg" > "$SEND_FILE"
  log "[P2P] Sent message:"
  echo "$msg" | while read -r line; do
    log "[P2P CMD] $line"
  done
}

# AI interface to accept multi-line input and send to command file and P2P
ai_shell() {
  echo "[GCS AI] Starting AI command interface..."
  echo "[GCS AI] Type commands separated by spaces or newlines."
  echo "[GCS AI] Type EXIT to quit."
  while true; do
    echo -n "[GCS AI] > "
    # Read multi-line input until a blank line is entered
    input=""
    while read -r line; do
      [[ -z "$line" ]] && break
      input+="$line
"
    done
    input=$(echo "$input" | sed '/^\s*$/d') # Remove blank lines

    input_clean=$(echo "$input" | tr -d '\r')

    if [[ "${input_clean^^}" == "EXIT" ]]; then
      echo "[GCS AI] Exiting..."
      break
    fi

    # Save commands locally for listener
    echo "$input_clean" >> "$COMMAND_FILE"

    # Simulate sending commands peer-to-peer
    p2p_send "$input_clean"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sent command(s):"
    echo "$input_clean"

    # Show recent command log tail
    tail -n 10 "$COMMAND_LOG"
  done
}

# Start listener in background if not already running
if ! pgrep -f "command_listener" > /dev/null; then
  command_listener &
  sleep 1
fi

# Start AI shell interface
ai_shell
