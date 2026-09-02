#!/usr/bin/env python3
"""Send a Telegram message to the one chat in .env. Usage: python voice/telegram_send.py "text"

There is no recipient argument on purpose. The only chat this script can reach is
TELEGRAM_CHAT_ID from .env, which is the agent's own phone. A bug in anything that
calls this script can, at worst, text the agent.

.env is found in this order: the VOICE_WORKSPACE environment variable, the current
folder, then the folder above this script (the workspace, when this lives in voice/).
"""
import json
import os
import sys
import urllib.request
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
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def send(text: str) -> None:
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env. "
                 "Run the voice-command skill's Level 1 setup first.")
    if not text.strip():
        sys.exit("Refusing to send an empty message.")

    # Telegram caps one message at 4096 characters; split long text rather than fail.
    for i in range(0, len(text), 4000):
        payload = json.dumps({"chat_id": chat_id, "text": text[i:i + 4000]}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
        if not body.get("ok"):
            sys.exit(f"Telegram rejected the send: {body}")
    print("sent")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python voice/telegram_send.py "your message"')
    send(" ".join(sys.argv[1:]))
