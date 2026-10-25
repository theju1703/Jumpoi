import os
import sys
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

PORT = 8080

def start_server():
    print(f"===================================================================")
    print(f" Starting Jompoi Operational Backend & Analytics Hub at:")
    print(f" -> Dashboard UI:   http://localhost:{PORT}")
    print(f" -> REST API Docs:  http://localhost:{PORT}/docs")
    print(f"===================================================================")
    webbrowser.open(f"http://localhost:{PORT}")

    try:
        import uvicorn
        from src.api.main import app
        uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
    except ImportError:
        import http.server
        import socketserver
        WEB_DIR = BASE_DIR / "web"
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(WEB_DIR), **kwargs)
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")

if __name__ == "__main__":
    start_server()
