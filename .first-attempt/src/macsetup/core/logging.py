"""Structured per-run JSONL log under ~/.local/state/macsetup/.

Each app launch writes a timestamped file. Sections call `event()` to
record what they did and what they observed. Useful for postmortem when
a run fails partway through.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Union


LOG_ROOT = Path("~/.local/state/macsetup/logs").expanduser()


class RunLog:
    def __init__(self, path: Union[Path, None] = None) -> None:
        if path is None:
            LOG_ROOT.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            path = LOG_ROOT / f"{stamp}.jsonl"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path

    def event(self, kind: str, **fields: Any) -> None:
        record: dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "kind": kind,
            **fields,
        }
        with self.path.open("a") as f:
            f.write(json.dumps(record) + "\n")
