from quart import Quart, websocket, redirect, request, render_template_string
import asyncio
import datetime
import uuid
import socket
import csv

app = Quart(__name__, static_folder="static")
sessions = {}

DEFAULT_DOMAIN = "domena.com"  # domyślna domena do dopisania


@app.route("/")
async def index():
    return await app.send_static_file("index.html")


@app.route("/connect")
async def connect():
    target_host = request.args.get("host")
    if not target_host:
        return "Brak hosta", 400

    # Utwórz unikalne ID sesji
    session_id = str(uuid.uuid4())
    sessions[session_id] = target_host

    # Logowanie połączeń
    with open("connections.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {request.remote_addr} -> {target_host}:5900\n")

    # Przekierowanie do noVNC
    return redirect(
        f"/static/novnc/vnc.html?"
        f"autoconnect=true&"
        f"host={request.host.split(':')[0]}&"
        f"port=8081&"
        f"path=ws/{session_id}"
    )


@app.websocket("/ws/<session_id>")
async def ws_proxy(session_id):
    target_host = sessions.get(session_id)
    if not target_host:
        return

    # Próba rozwiązania nazwy
    try:
        socket.getaddrinfo(target_host, 5900)
    except socket.gaierror:
        # fallback – spróbuj dopisać domenę
        fallback_host = f"{target_host}.{DEFAULT_DOMAIN}"
        try:
            socket.getaddrinfo(fallback_host, 5900)
            target_host = fallback_host
        except socket.gaierror:
            print(f"[ERROR] Nie można rozwiązać hosta: {target_host}")
            return

    # Połączenie TCP do VNC
    reader, writer = await asyncio.open_connection(target_host, 5900)

    async def tcp_to_ws():
        while True:
            data = await reader.read(4096)
            if not data:
                break
            await websocket.send(data)

    async def ws_to_tcp():
        while True:
            msg = await websocket.receive()
            if isinstance(msg, str):
                msg = msg.encode()
            writer.write(msg)
            await writer.drain()

    await asyncio.gather(tcp_to_ws(), ws_to_tcp())


# 🔥 Nowa ukryta strona
@app.route("/lukasz")
async def lukasz():
    csv_file = "otc.csv"  # lub devices.csv
    devices = []
    try:
        # wczytujemy wszystkie wiersze ze średnikiem jako separatorem
        with open(csv_file, newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh, delimiter=";"))

        if not rows:
            devices = []
        else:
            header = rows[0]
            data_rows = rows[1:]

            # znormalizuj nagłówki
            normalized_headers = []
            for i, h in enumerate(header):
                nh = (h or "").strip().lower()
                if not nh:
                    nh = f"col{i+1}"
                normalized_headers.append(nh)

            max_cols = max(len(normalized_headers), max((len(r) for r in data_rows), default=0))
            for i in range(len(normalized_headers), max_cols):
                normalized_headers.append(f"col{i+1}")

            for r in data_rows:
                rowd = {}
                for idx in range(max_cols):
                    key = normalized_headers[idx]
                    val = r[idx].strip() if idx < len(r) and isinstance(r[idx], str) else ""
                    rowd[key] = val
                devices.append(rowd)

    except FileNotFoundError:
        return f"Plik {csv_file} nie istnieje. Umieść go w katalogu aplikacji.", 500
    except Exception as e:
        return f"Błąd wczytywania {csv_file}: {e}", 500

    html_template = """
    <!doctype html>
    <html lang="pl">
    <head>
        <meta charset="utf-8">
        <title>Lista urządzeń OTC</title>
        <link rel="stylesheet" href="/static/bootstrap/bootstrap.min.css">
        <style>
          .table td, .table th { vertical-align: middle; text-align: center; }
        </style>
    </head>
    <body class="container py-5">
        <h2 class="mb-4 text-center">Lista urządzeń OTC</h2>
        <table class="table table-bordered table-striped">
            <thead class="table-light">
                <tr>
                    <th>Nazwa</th>
                    <th>Opis</th>
                    <th>Akcja</th>
                </tr>
            </thead>
            <tbody>
            {% for d in devices %}
                <tr>
                    <td>{{ d.get('\ufeffnazwa') or d.get('name') or d.get('col1','') }}</td>
                    <td>{{ d.get('opis') or d.get('description') or d.get('col2','') }}</td>
                    <td>
                        {% set host = d.get('\ufeffnazwa') or d.get('name') or d.get('col1','') %}
                        {% if host %}
                        <a href="/connect?host={{ host }}" target="_blank" class="btn btn-primary btn-sm">Połącz</a>
                        {% else %}
                        <span class="text-muted small">brak nazwy</span>
                        {% endif %}
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return await render_template_string(html_template, devices=devices)




if __name__ == "__main__":
    app.run()
