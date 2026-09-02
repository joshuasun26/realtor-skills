#!/usr/bin/env python3
"""Poll the agent's own Telegram chat for new commands.

Prints new messages as JSON and advances a cursor so nothing is read twice.
Prints nothing at all when there is nothing new, so a scheduled run can use
"did it print anything" as the cheap gate before waking Claude.

Only messages from TELEGRAM_CHAT_ID are returned. Anything from another chat is
dropped, so a message someone else sends the bot is never treated as a command.
The bot is its own identity, so its replies can never come back as commands
(this is the reason Telegram has no loop-back trap the way iMessage does).

Usage:
  python voice/telegram_poll.py           # new commands since last run
  python voice/telegram_poll.py --peek    # same, but do NOT advance the cursor
  python voice/telegram_poll.py --reset   # skip the backlog, start from now
"""
import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def workspace() -> Path:
    override = os.environ.get("VOICE_WORKSPACE")
    if override:
        return Path(override)
    if (Path.cwd() / ".env").exists():
        return Path.cwd()
    return Path(__file__).resolve().parent.parent


def load_env() -> None:
    env = workspace() / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def cursor_path() -> Path:
    return workspace() / "voice" / ".telegram-cursor.json"


def read_cursor() -> int:
    p = cursor_path()
    if p.exists():
        return int(json.loads(p.read_text(encoding="utf-8")).get("last_update_id", 0))
    return 0


def write_cursor(update_id: int) -> None:
    p = cursor_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"last_update_id": update_id}), encoding="utf-8")


def fetch_updates(token: str, offset: int) -> list:
    url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=0"
    with urllib.request.urlopen(url, timeout=30) as resp:
        body = json.loads(resp.read())
    if not body.get("ok"):
        sys.exit(f"Telegram rejected getUpdates: {body}")
    return body.get("result", [])


def extract_commands(updates: list, chat_id: str) -> tuple:
    """Turn raw getUpdates results into commands from the agent's own chat only.

    Returns (commands, highest_update_id). Kept separate from the network call so
    it can be tested against a recorded payload without a bot token.
    """
    commands, highest = [], 0
    for upd in updates:
        highest = max(highest, int(upd.get("update_id", 0)))
        msg = upd.get("message") or upd.get("edited_message") or {}
        chat = msg.get("chat") or {}
        if str(chat.get("id", "")) != str(chat_id):
            continue  # not the agent's own chat: never a command
        text = (msg.get("text") or "").strip()
        if not text:
            continue  # stickers, photos, joins: nothing to act on
        when = datetime.fromtimestamp(int(msg.get("date", 0)), tz=timezone.utc).astimezone()
        commands.append({
            "update_id": upd.get("update_id"),
            "at": when.isoformat(timespec="seconds"),
            "text": text,
        })
    return commands, highest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--peek", action="store_true", help="do not advance the cursor")
    ap.add_argument("--reset", action="store_true", help="skip the backlog, start from now")
    args = ap.parse_args()

    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env.")

    last = read_cursor()
    # Telegram returns every update with update_id >= offset, so ask from last + 1.
    updates = fetch_updates(token, last + 1 if last else 0)
    commands, highest = extract_commands(updates, chat_id)

    if args.reset:
        write_cursor(max(highest, last))
        print(f"Cursor reset. {len(commands)} backlog message(s) ignored.", file=sys.stderr)
        return

    if not args.peek and highest > last:
        write_cursor(highest)

    if commands:
        print(json.dumps(commands, indent=2))


if __name__ == "__main__":
    main()
