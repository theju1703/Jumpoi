import os
import logging
from typing import List, Dict, Any, Optional

try:
    from google.cloud import bigquery
    from google.api_core.exceptions import NotFound
    BQ_AVAILABLE = True
except ImportError:
    BQ_AVAILABLE = False

logger = logging.getLogger(__name__)

class BigQueryLoader:
    """Manages loading data into Google Cloud BigQuery datasets and tables."""

    def __init__(self, project_id: str, dataset_id: str, client: Optional[Any] = None):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self._client = client

    @property
    def client(self):
        if self._client is None:
            if not BQ_AVAILABLE:
                raise RuntimeError("google-cloud-bigquery library is not installed.")
            self._client = bigquery.Client(project=self.project_id)
        return self._client

    def is_connected(self) -> bool:
        """Checks if BigQuery client can connect and authenticate."""
        if not BQ_AVAILABLE:
            return False
        try:
            _ = self.client.project
            return True
        except Exception as e:
            logger.warning("BigQuery connection check failed: %s", e)
            return False

    def insert_rows(self, table_name: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Inserts rows into the target BigQuery table using streaming inserts.
        Returns a dict summarizing results and any row errors.
        """
        if not rows:
            return {"status": "skipped", "inserted_count": 0, "errors": []}

        table_id = f"{self.project_id}.{self.dataset_id}.{table_name}"
        try:
            errors = self.client.insert_rows_json(table_id, rows)
            if not errors:
                return {
                    "status": "success",
                    "table": table_id,
                    "inserted_count": len(rows),
                    "errors": []
                }
            else:
                return {
                    "status": "partial_error",
                    "table": table_id,
                    "inserted_count": len(rows) - len(errors),
                    "errors": errors
                }
        except Exception as e:
            return {
                "status": "failed",
                "table": table_id,
                "inserted_count": 0,
                "errors": [str(e)]
            }
