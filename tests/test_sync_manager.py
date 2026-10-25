import tempfile
import datetime
from pathlib import Path
from src.etl.sync_manager import SyncStateManager

def test_sync_state_manager_lifecycle():
    with tempfile.TemporaryDirectory() as tmp_dir:
        state_file = Path(tmp_dir) / "test_state.json"
        manager = SyncStateManager(str(state_file))

        # Initial timestamp should be default epoch
        initial_ts = manager.get_last_sync_time("sales_invoice")
        assert initial_ts.year == 2000

        # Update timestamp
        now = datetime.datetime(2026, 8, 25, 10, 0, 0, tzinfo=datetime.timezone.utc)
        manager.update_last_sync_time("sales_invoice", now)

        # Retrieve updated timestamp
        updated_ts = manager.get_last_sync_time("sales_invoice")
        assert updated_ts == now

        # Reset state
        manager.reset_state()
        assert manager.get_last_sync_time("sales_invoice").year == 2000
