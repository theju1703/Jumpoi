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
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        token_path = os.path.join(base_dir, "gcp_token.txt")
        token = os.environ.get("BIGQUERY_ACCESS_TOKEN")
        if not token and os.path.exists(token_path):
            try:
                with open(token_path, "r", encoding="utf-8") as f:
                    token = f.read().strip()
            except Exception:
                pass

        key_path = os.path.join(base_dir, "gcp_key.json")
        key_exists = os.path.exists(key_path)
        if getattr(self, "_key_exists", None) != key_exists:
            self._client = None
            self._key_exists = key_exists

        if getattr(self, "_current_token", None) != token:
            self._client = None
            self._current_token = token

        if self._client is None:
            if not BQ_AVAILABLE:
                raise RuntimeError("google-cloud-bigquery library is not installed.")
            
            # 1. Check for permanent service account key file (takes highest priority)
            key_path = os.path.join(base_dir, "gcp_key.json")
            if os.path.exists(key_path):
                from google.oauth2 import service_account
                creds = service_account.Credentials.from_service_account_file(key_path)
                self._client = bigquery.Client(project=self.project_id, credentials=creds)
            elif token:
                import google.auth.credentials
                class StaticTokenCredentials(google.auth.credentials.Credentials):
                    def __init__(self, tok):
                        super().__init__()
                        self.token = tok
                    def refresh(self, request):
                        pass
                    def apply(self, headers, token=None):
                        headers['authorization'] = f'Bearer {self.token}'
                    def before_request(self, request, method, url, headers):
                        headers['authorization'] = f'Bearer {self.token}'
                creds = StaticTokenCredentials(token)
                self._client = bigquery.Client(project=self.project_id, credentials=creds)
            else:
                self._client = bigquery.Client(project=self.project_id)
        return self._client

    def is_connected(self) -> bool:
        """Checks if BigQuery client can connect and authenticate."""
        if not BQ_AVAILABLE:
            return False
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        token_path = os.path.join(base_dir, "gcp_token.txt")
        key_path = os.path.join(base_dir, "gcp_key.json")
        has_auth = (
            bool(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")) or
            bool(os.environ.get("BIGQUERY_ACCESS_TOKEN")) or
            os.path.exists(key_path) or
            os.path.exists(token_path) or
            bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))
        )
        if not has_auth:
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
            # Dynamically filter row keys to match target BigQuery table schema
            try:
                table = self.client.get_table(table_id)
                valid_fields = {f.name for f in table.schema}
                filtered_rows = [{k: v for k, v in r.items() if k in valid_fields} for r in rows]
            except Exception:
                filtered_rows = rows

            # Deterministic insert IDs for BigQuery streaming deduplication
            row_ids = [str(r.get("_id") or r.get("item_code") or r.get("invoice_no")) for r in filtered_rows]
            has_valid_ids = all(bool(i and i != "None") for i in row_ids)
            errors = self.client.insert_rows_json(table_id, filtered_rows, row_ids=row_ids if has_valid_ids else None)
            if not errors:
                return {
                    "status": "success",
                    "table": table_id,
                    "inserted_count": len(filtered_rows),
                    "errors": []
                }
            else:
                str_errors = [str(e) for e in errors]
                return {
                    "status": "partial_error",
                    "table": table_id,
                    "inserted_count": len(filtered_rows) - len(errors),
                    "errors": str_errors
                }
        except Exception as e:
            return {
                "status": "failed",
                "table": table_id,
                "inserted_count": 0,
                "errors": [str(e)]
            }

    def query(self, query_string: str) -> List[Dict[str, Any]]:
        """
        Executes a SQL query against Google Cloud BigQuery.
        Returns a list of dicts representing each row.
        """
        query_job = self.client.query(query_string)
        results = query_job.result()
        return [dict(row) for row in results]
