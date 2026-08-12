"""Report an error, both locally (logs/error_log.json, always, in this repo)
and into the sibling automation repo's shared error log (inbox/error_log.json,
best-effort), which its hourly check_pipeline_errors.py cron reads to decide
what to auto-retry vs. escalate to a real diagnosis run.

The local copy is written unconditionally, before the cross-repo bridge is
even attempted — so a network hiccup, a stale env var, or the bridge repo
being temporarily unreachable never means an error just vanishes with no
trace anywhere. It's an audit trail, not consumed by any automation itself
(check_pipeline_errors.py only reads the shared log) — if the bridge call
below fails, that's printed to stderr so cron's own log file catches it too.

Same reasoning as telegram_send.py right next to this file for the bridge
part: this repo is public, so the sibling repo's path/name is never
hardcoded here — it comes from TELEGRAM_BRIDGE_DIR in this repo's own
gitignored .env (the same env var telegram_send.py already uses, since it
points at the same repo).

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

LOCAL_LOG_FILE = REPO_ROOT / "logs" / "error_log.json"

_bridge_dir = os.environ.get("TELEGRAM_BRIDGE_DIR")
if not _bridge_dir:
    raise SystemExit(
        "TELEGRAM_BRIDGE_DIR not set in .env — should point to the sibling "
        "automation repo whose error log (inbox/error_log.json) and hourly "
        "check runs live. Not hardcoded here deliberately: this repo is public."
    )
BRIDGE_DIR = Path(_bridge_dir)


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


def log_error(source: str, severity: str, summary: str, context: Optional[dict] = None) -> Optional[str]:
    """Always writes a local record first (see module docstring), then tries
    the cross-repo bridge. Returns the shared log's entry id, or None if the
    bridge call itself failed (the local record still exists either way).
    `severity` must be "auto-retry" (a known-safe, mechanical recovery
    exists) or "needs-diagnosis" (anything else)."""
    _log_local(source, severity, summary, context)

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
        try:
            result = subprocess.run(cmd, cwd=BRIDGE_DIR, capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.TimeoutExpired) as e:
            # e.g. BRIDGE_DIR doesn't exist, or python itself isn't reachable —
            # subprocess.run raises here rather than returning a non-zero
            # returncode, so this needs its own catch (confirmed real
            # 2026-08-12: an unreachable bridge dir crashed the caller before
            # this existed). The local record above already exists either way.
            print(f"bridge call errored (logged locally only): {e}", file=sys.stderr)
            return None
        if result.returncode != 0:
            print(f"bridge call failed (logged locally only): {result.stderr.strip()}", file=sys.stderr)
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
