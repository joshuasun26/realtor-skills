#!/bin/bash
# Send an iMessage to yourself. Usage: ./voice/imessage_send.sh "text"
#
# There is no recipient argument on purpose. The only handle this script can reach
# is IMESSAGE_SELF from .env, which is the agent's own Messages account.
#
# Requires: the app running Claude Code (Terminal, iTerm, VS Code) granted Automation
# access to Messages. macOS prompts for this on the FIRST send only.
#
# The message is handed to osascript as an ARGUMENT, never interpolated into the
# AppleScript source, so there is nothing to escape.
set -euo pipefail

if [ -n "${VOICE_WORKSPACE:-}" ]; then
  ROOT="$VOICE_WORKSPACE"
elif [ -f "$PWD/.env" ]; then
  ROOT="$PWD"
else
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

if [ -z "${IMESSAGE_SELF:-}" ] && [ -f "$ROOT/.env" ]; then
  IMESSAGE_SELF="$(grep -E '^[[:space:]]*IMESSAGE_SELF[[:space:]]*=' "$ROOT/.env" \
    | tail -n 1 | cut -d= -f2- | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
fi

ME="${IMESSAGE_SELF:-}"
if [ -z "$ME" ]; then
  echo "Set IMESSAGE_SELF in .env to your Apple ID email or phone number." >&2
  exit 1
fi
[ $# -ge 1 ] || { echo 'Usage: ./voice/imessage_send.sh "message"' >&2; exit 1; }

MSG="$*"
[ -n "${MSG//[[:space:]]/}" ] || { echo "Refusing to send an empty message." >&2; exit 1; }

osascript - "$ME" "$MSG" <<'APPLESCRIPT'
on run argv
  set targetID to item 1 of argv
  set theBody to item 2 of argv
  tell application "Messages"
    set svc to 1st service whose service type = iMessage
    send theBody to buddy targetID of svc
  end tell
end run
APPLESCRIPT
echo "sent"
