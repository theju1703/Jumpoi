import json
import os
import datetime
from pathlib import Path
from typing import Dict, Optional
from dateutil import parser

class SyncStateManager:
    """Manages the incremental ETL sync state stored in a JSON file."""

    def __init__(self, state_file_path: str):
        self.state_file = Path(state_file_path)
        self.default_epoch = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)

    def _read_state(self) -> Dict[str, str]:
        if not self.state_file.exists():
            return {}
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_state(self, state: Dict[str, str]) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def get_last_sync_time(self, collection_name: str) -> datetime.datetime:
        state = self._read_state()
        ts_str = state.get(collection_name)
        if ts_str:
            try:
                dt = parser.parse(ts_str)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
                return dt
            except Exception:
                pass
        return self.default_epoch

    def update_last_sync_time(self, collection_name: str, sync_time: Optional[datetime.datetime] = None) -> None:
        if sync_time is None:
            sync_time = datetime.datetime.now(datetime.timezone.utc)
        elif sync_time.tzinfo is None:
            sync_time = sync_time.replace(tzinfo=datetime.timezone.utc)

        state = self._read_state()
        state[collection_name] = sync_time.isoformat()
        self._write_state(state)

    def get_all_sync_times(self) -> Dict[str, str]:
        return self._read_state()

    def reset_state(self) -> None:
        if self.state_file.exists():
            self.state_file.unlink()
