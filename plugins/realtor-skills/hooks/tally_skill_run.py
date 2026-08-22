#!/usr/bin/env python3
"""
Local-only usage tally for the realtor-skills plugin.

WHAT THIS DOES
    Appends one line per skill invocation to a local JSONL file so the agent (and,
    with their written consent, the person supporting them) can see which skills are
    actually being used and which are dead weight.

WHAT THIS DOES NOT DO
    It does not send anything anywhere. There is no network call in this file and
    there must never be one. It records skill NAMES and TIMESTAMPS only -- never
    message content, never contact data, never file contents, never arguments.

>>> DISABLED BY DEFAULT <<<
    This script does nothing unless BOTH of the following are true:

      1. hooks/hooks.json is wired into .claude-plugin/plugin.json via
             "hooks": "./hooks/hooks.json"
         It is deliberately NOT wired up in the shipped plugin.

      2. An opt-in marker file exists at the tally path's directory:
             .realtor-skills/USAGE-TRACKING-ENABLED
         Without that file this script exits immediately, even if the hook fires.

>>> CLIENT DISCLOSURE IS MANDATORY <<<
    Telemetry on a paying client's usage must be disclosed in the client agreement
    BEFORE it is enabled -- not discovered afterward. "I can see which skills you use
    so I know what to improve" is a feature a client will accept when it is said up
    front, and a breach of trust when they find it themselves.

    Do not enable this on a client machine until the agreement says so in writing.
    See hooks/README.md.
"""

import datetime
import json
import os
import pathlib
import sys

TALLY_DIRNAME = ".realtor-skills"
TALLY_FILENAME = "skill-usage.jsonl"
OPT_IN_MARKER = "USAGE-TRACKING-ENABLED"


def tally_dir() -> pathlib.Path:
    """Local, per-machine. Never a shared or synced location by default."""
    base = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.expanduser("~")
    return pathlib.Path(base) / TALLY_DIRNAME


def main() -> int:
    target_dir = tally_dir()

    # Gate 1: the explicit opt-in marker must exist. No marker, no recording.
    if not (target_dir / OPT_IN_MARKER).exists():
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    # Record the skill name and nothing else that could carry personal data.
    tool_input = payload.get("tool_input") or {}
    skill_name = tool_input.get("skill")
    if not isinstance(skill_name, str) or not skill_name:
        return 0

    record = {
        "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "skill": skill_name[:120],
        "plugin": "realtor-skills",
    }

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        with open(target_dir / TALLY_FILENAME, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")
    except Exception:
        # A telemetry failure must never interrupt the agent's actual work.
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
