#!/usr/bin/env python3
"""Read recent iMessages from the local Messages database (Mac only).

REQUIRES Full Disk Access for the app running this (Terminal / iTerm / VS Code):
System Settings > Privacy & Security > Full Disk Access > add it > RESTART the app.
Without it this fails with 'unable to open database file' and no other explanation.

THE SELF-THREAD TRAP: the brief and the command loop both send TO the agent's own
Messages thread. Those sends land in chat.db like any other message, so a naive
read pulls the assistant's own output straight back in and starts summarizing its
own summaries. Two guards, on by default:
  1. The thread whose handle is IMESSAGE_SELF is skipped entirely.
  2. Any message starting with OUT_PREFIX is skipped wherever it appears.
Pass --include-self to read the self-thread anyway (the command loop wants it;
the daily brief never does).

Usage:
  python voice/imessage_read_recent.py            # last 24 hours, self-thread excluded
  python voice/imessage_read_recent.py --hours 72
  python voice/imessage_read_recent.py --unreplied
  python voice/imessage_read_recent.py --include-self
"""
import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DB = Path.home() / "Library" / "Messages" / "chat.db"
OUT_PREFIX = "[claude]"
# Apple stores message dates as nanoseconds since 2001-01-01 UTC.
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


def normalize_handle(handle: str) -> str:
    """Compare handles the way a human would.

    An Apple ID is matched case-insensitively. A phone number is matched on its
    last 10 digits, so +1 (626) 555-0100 and 6265550100 are the same person;
    chat.db is not consistent about which form it stores.
    """
    h = (handle or "").strip().lower()
    if "@" in h:
        return h
    digits = re.sub(r"\D", "", h)
    return digits[-10:] if len(digits) >= 10 else digits


def apple_time(dt: datetime) -> int:
    return int((dt - APPLE_EPOCH).total_seconds() * 1_000_000_000)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--unreplied", action="store_true",
                    help="only threads where the last message is inbound")
    ap.add_argument("--include-self", action="store_true",
                    help="also read the agent's own self-thread (off by default)")
    args = ap.parse_args()

    load_env()
    me = normalize_handle(os.environ.get("IMESSAGE_SELF", ""))
    if not me and not args.include_self:
        print("# WARNING: IMESSAGE_SELF is not set in .env, so the self-thread "
              "cannot be identified and this brief may read its own output back "
              "in. Set it before scheduling anything.", file=sys.stderr)

    if not DB.exists():
        sys.exit(f"No Messages database at {DB}. Is this a Mac signed into iMessage?")

    try:
        con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    except sqlite3.OperationalError as exc:
        sys.exit(f"Cannot open the Messages database ({exc}). "
                 "This almost always means Full Disk Access is not granted "
                 "to the app running this, or it was granted but the app was "
                 "not restarted afterward.")

    since = apple_time(datetime.now(timezone.utc) - timedelta(hours=args.hours))
    rows = con.execute(
        """
        SELECT h.id,
               m.is_from_me,
               m.date,
               COALESCE(m.text, '')
        FROM message m
        JOIN handle h ON m.handle_id = h.ROWID
        WHERE m.date > ?
        ORDER BY m.date ASC
        """,
        (since,),
    ).fetchall()
    con.close()

    threads = {}
    for handle, is_from_me, date, text in rows:
        if not text.strip():
            continue
        # Guard 2: never feed our own output back in, whatever thread it is in.
        if text.lstrip().startswith(OUT_PREFIX):
            continue
        # Guard 1: the self-thread is this system talking to itself.
        if not args.include_self and me and normalize_handle(handle) == me:
            continue
        threads.setdefault(handle, []).append((is_from_me, date, text))

    for handle, msgs in threads.items():
        if args.unreplied and msgs[-1][0] == 1:
            continue
        print(f"\n=== {handle} ===")
        for is_from_me, date, text in msgs:
            when = (APPLE_EPOCH + timedelta(seconds=date / 1_000_000_000)).astimezone()
            who = "me" if is_from_me else "them"
            print(f"[{when:%m/%d %H:%M}] {who}: {text}")


if __name__ == "__main__":
    main()
