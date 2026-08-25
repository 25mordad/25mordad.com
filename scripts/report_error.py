"""Report an error, both locally (logs/error_log.json, always, unconditionally)
and as a direct, best-effort Telegram alert to this project's own dedicated
group (see CLAUDE.md's Personal Photo Series > Automated routine section).

The local copy is written first and unconditionally — so a Telegram hiccup
never means an error just vanishes with no trace anywhere.

`severity: "auto-retry"` entries (a known-safe, mechanical recovery exists)
are picked up by scripts/telegram_receive.py's cron-driven scan, which
invokes retry_story_publish.py and marks the entry with retried_at.
`severity: "needs-diagnosis"` entries are just alerted — nothing auto-retries
them.

Usage (as a library, from lr_check_schedule.py or other scripts):
    from report_error import log_error
    log_error("lr_check_schedule.py:story_publish_error", "auto-retry",
              "Story publish failed for شادی", context={"asset_id": "..."})

Usage (CLI, mainly for connectivity testing):
    scripts/.venv/bin/python scripts/report_error.py "<source>" "<severity>" "<summary>"
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_common import send_message  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCAL_LOG_FILE = REPO_ROOT / "logs" / "error_log.json"


def _log_local(source: str, severity: str, summary: str, context: Optional[dict]) -> None:
    entries = []
    if LOCAL_LOG_FILE.exists():
        try:
            entries = json.loads(LOCAL_LOG_FILE.read_text())
        except Exception:
            entries = []
    entries.append({
        "source": source,
        "severity": severity,
        "summary": summary,
        "context": context or {},
        "logged_at": datetime.now(timezone.utc).isoformat(),
    })
    LOCAL_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_LOG_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


def log_error(source: str, severity: str, summary: str, context: Optional[dict] = None) -> None:
    """Always writes a local record first (see module docstring), then sends
    a best-effort Telegram alert. `severity` must be "auto-retry" (a
    known-safe, mechanical recovery exists — picked up automatically by
    telegram_receive.py's cron scan) or "needs-diagnosis" (anything else)."""
    _log_local(source, severity, summary, context)

    icon = "↻" if severity == "auto-retry" else "⚠️"
    text = f"{icon} {source} [{severity}]\n{summary}"
    try:
        send_message(text)
    except SystemExit as e:
        print(f"Telegram alert failed (logged locally only): {e}", file=sys.stderr)


def main():
    if len(sys.argv) != 4:
        raise SystemExit('Usage: report_error.py "<source>" "<auto-retry|needs-diagnosis>" "<summary>"')
    log_error(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    main()
