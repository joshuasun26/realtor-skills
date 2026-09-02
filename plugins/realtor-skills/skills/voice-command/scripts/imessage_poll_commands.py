#!/usr/bin/env python3
"""Poll the agent's iMessage self-thread for new commands (Mac only).

Prints new commands as JSON and advances a cursor so nothing is processed twice.
Prints nothing at all when there is nothing new, so a scheduled run is silent and
"did it print anything" is the cheap gate before waking Claude.

THE LOOP-BACK TRAP: a message the agent typed and a message this system sent are
both is_from_me=1 in chat.db, because the send script sends AS the agent. Without
a guard, Claude reads its own reply as a new command and answers itself forever.
Two guards, both required:
  1. Any message starting with OUT_PREFIX is skipped (that is our own output).
  2. A stored ROWID cursor means a message is only ever seen once.

Usage:
  python voice/imessage_poll_commands.py           # new commands since last run
  python voice/imessage_poll_commands.py --peek    # same, but do NOT advance cursor
  python voice/imessage_poll_commands.py --reset   # start from now, ignore backlog
"""
import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB = Path.home() / "Library" / "Messages" / "chat.db"
OUT_PREFIX = "[claude]"
APPLE_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)


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
    return workspace() / "voice" / ".imessage-cursor.json"


def read_cursor() -> int:
    p = cursor_path()
    if p.exists():
        return int(json.loads(p.read_text(encoding="utf-8")).get("last_rowid", 0))
    return 0


def write_cursor(rowid: int) -> None:
    p = cursor_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"last_rowid": rowid}), encoding="utf-8")


def connect() -> sqlite3.Connection:
    if not DB.exists():
        sys.exit(f"No Messages database at {DB}.")
    try:
        return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    except sqlite3.OperationalError as exc:
        sys.exit(f"Cannot open the Messages database ({exc}). Full Disk Access "
                 "is probably not granted to the app running this, or it was "
                 "granted without restarting that app afterward.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--peek", action="store_true", help="do not advance the cursor")
    ap.add_argument("--reset", action="store_true", help="skip the backlog, start from now")
    args = ap.parse_args()

    load_env()
    me = os.environ.get("IMESSAGE_SELF")
    if not me:
        sys.exit("Set IMESSAGE_SELF in .env to your Apple ID email or phone number.")

    con = connect()

    if args.reset:
        newest = con.execute("SELECT COALESCE(MAX(ROWID), 0) FROM message").fetchone()[0]
        write_cursor(newest)
        con.close()
        print(f"Cursor reset to {newest}. Backlog ignored.", file=sys.stderr)
        return

    last = read_cursor()
    if last == 0:
        # First ever run: only look at the last hour so an old thread does not
        # get replayed as a hundred fresh commands.
        since = int((datetime.now(timezone.utc) - timedelta(hours=1) - APPLE_EPOCH)
                    .total_seconds() * 1_000_000_000)
        rows = con.execute(
            """
            SELECT m.ROWID, m.text, m.date
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            JOIN chat c ON c.ROWID = cmj.chat_id
            WHERE m.is_from_me = 1 AND m.date > ? AND c.chat_identifier = ?
            ORDER BY m.ROWID ASC
            """,
            (since, me),
        ).fetchall()
    else:
        rows = con.execute(
            """
            SELECT m.ROWID, m.text, m.date
            FROM message m
            JOIN chat_message_join cmj ON cmj.message_id = m.ROWID
            JOIN chat c ON c.ROWID = cmj.chat_id
            WHERE m.is_from_me = 1 AND m.ROWID > ? AND c.chat_identifier = ?
            ORDER BY m.ROWID ASC
            """,
            (last, me),
        ).fetchall()
    con.close()

    commands = []
    highest = last
    for rowid, text, date in rows:
        highest = max(highest, rowid)
        text = (text or "").strip()
        if not text or text.startswith(OUT_PREFIX):
            continue  # our own output, never a command
        when = (APPLE_EPOCH + timedelta(seconds=date / 1_000_000_000)).astimezone()
        commands.append({"rowid": rowid, "at": when.isoformat(timespec="seconds"),
                         "text": text})

    if not args.peek and highest > last:
        write_cursor(highest)

    if commands:
        print(json.dumps(commands, indent=2))


if __name__ == "__main__":
    main()
