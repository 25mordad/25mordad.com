"""Report an error into the sibling automation repo's shared error log
(inbox/error_log.json), which its hourly check_pipeline_errors.py cron reads
to decide what to auto-retry vs. escalate to a real diagnosis run.

Same reasoning as telegram_send.py right next to this file: this repo is
public, so the sibling repo's path/name is never hardcoded here — it comes
from TELEGRAM_BRIDGE_DIR in this repo's own gitignored .env (the same env
var telegram_send.py already uses, since it points at the same repo).

Usage (as a library, from lr_check_schedule.py or other scripts):
    from report_error import log_error
    log_error("lr_check_schedule.py:story_publish_error", "auto-retry",
              "Story publish failed for شادی", context={"asset_id": "..."})

Usage (CLI, mainly for connectivity testing):
    scripts/.venv/bin/python scripts/report_error.py "<source>" "<severity>" "<summary>"
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

_bridge_dir = os.environ.get("TELEGRAM_BRIDGE_DIR")
if not _bridge_dir:
    raise SystemExit(
        "TELEGRAM_BRIDGE_DIR not set in .env — should point to the sibling "
        "automation repo whose error log (inbox/error_log.json) and hourly "
        "check runs live. Not hardcoded here deliberately: this repo is public."
    )
BRIDGE_DIR = Path(_bridge_dir)


def log_error(source: str, severity: str, summary: str, context: Optional[dict] = None) -> Optional[str]:
    """Returns the logged entry's id, or None on failure. `severity` must be
    "auto-retry" (a known-safe, mechanical recovery exists) or
    "needs-diagnosis" (anything else)."""
    context_path = None
    cmd = [
        sys.executable, "log_error.py",
        "--project", "25mordad.com",
        "--source", source,
        "--severity", severity,
        "--summary", summary,
    ]
    try:
        if context:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
                json.dump(context, f, ensure_ascii=False)
                context_path = f.name
            cmd += ["--context-json", context_path]
        result = subprocess.run(cmd, cwd=BRIDGE_DIR, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return None
        return result.stdout.strip() or None
    finally:
        if context_path:
            Path(context_path).unlink(missing_ok=True)


def main():
    if len(sys.argv) != 4:
        raise SystemExit('Usage: report_error.py "<source>" "<auto-retry|needs-diagnosis>" "<summary>"')
    entry_id = log_error(sys.argv[1], sys.argv[2], sys.argv[3])
    print(entry_id if entry_id else "failed")
    sys.exit(0 if entry_id else 1)


if __name__ == "__main__":
    main()
