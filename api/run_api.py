"""
Top-level entry point launcher for the Jompoi Supermarket ERP Backend API.
Starts the FastAPI enterprise server on host 0.0.0.0 and port 8080.
"""

import uvicorn
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.main import app

def main():
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting Jompoi Supermarket ERP Backend API on http://{host}:{port}...")
    uvicorn.run("src.api.main:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
