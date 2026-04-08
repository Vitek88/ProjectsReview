from waitress import serve
from app import app, start_ws_server

if __name__ == "__main__":
    # Start serwera WebSocket (proxy)
    start_ws_server()
    # Start serwera Flask (HTTP)
    serve(app, host="0.0.0.0", port=8081, threads=8)
