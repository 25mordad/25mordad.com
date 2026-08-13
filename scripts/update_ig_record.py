#!/usr/bin/env python3
"""Update fields on an images/ig-queue/<asset_id>.json record.

Every /photo-beshno record write goes through this pre-approved `python3 *`
call instead of the Edit/Write tool, so an unattended `claude -p` run never
stalls waiting for an interactive permission prompt nobody is there to grant
(confirmed real stall, Telegram msg 1153, 2026-08-14 — a title confirmation
was parsed correctly but the Edit tool call to save it hung on approval,
`/photo-beshno` exited 0 without saving, and the handoff file was left
undeleted, tripping the stall detector).
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id")
    parser.add_argument(
        "--set", action="append", default=[], metavar="KEY=VALUE",
        help="set a short field, e.g. --set pipeline_state=awaiting_story",
    )
    parser.add_argument(
        "--set-stdin", metavar="KEY",
        help="set one field to the full contents of stdin "
             "(for long/multiline text like story or caption)",
    )
    args = parser.parse_args()

    record_path = QUEUE_DIR / f"{args.asset_id}.json"
    if not record_path.exists():
        raise SystemExit(f"No record at {record_path}")
    record = json.loads(record_path.read_text())

    updated = []
    for pair in args.set:
        if "=" not in pair:
            raise SystemExit(f"--set expects KEY=VALUE, got: {pair}")
        key, value = pair.split("=", 1)
        record[key] = value
        updated.append(key)

    if args.set_stdin:
        record[args.set_stdin] = sys.stdin.read()
        updated.append(args.set_stdin)

    if not updated:
        raise SystemExit("Nothing to update — pass --set KEY=VALUE and/or --set-stdin KEY")

    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(f"Updated {args.asset_id}: {', '.join(updated)}")


if __name__ == "__main__":
    main()
