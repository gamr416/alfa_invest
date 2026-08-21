#!/usr/bin/env python3
"""Log inbound Ollama HTTP (e.g. via ssh -R) and forward to real Ollama.

  Local Ollama stays on 127.0.0.1:11434.
  This proxy listens on 127.0.0.1:11435 by default.
  Point the reverse tunnel at the proxy:

    ssh ... -R 11434:127.0.0.1:11435 ...

Env:
  OLLAMA_UPSTREAM    default http://127.0.0.1:11434
  OLLAMA_PROXY_BIND  default 127.0.0.1:11435
  OLLAMA_REQUEST_LOG default <repo>/logs/ollama-access.log
"""

from __future__ import annotations

import logging
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

UPSTREAM = os.getenv("OLLAMA_UPSTREAM", "http://127.0.0.1:11434").rstrip("/")
BIND = os.getenv("OLLAMA_PROXY_BIND", "127.0.0.1:11435")
LOG_PATH = os.getenv(
    "OLLAMA_REQUEST_LOG",
    str(Path(__file__).resolve().parents[1] / "logs" / "ollama-access.log"),
)

Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [ollama.access] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)
log = logging.getLogger("ollama.access")

HOP = {"host", "content-length", "transfer-encoding", "connection", "keep-alive"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:  # silence default access line
        return

    def _proxy(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        path = self.path
        t0 = time.perf_counter()
        preview = ""
        if body and "/api/chat" in path.split("?", 1)[0]:
            preview = body[:200].decode("utf-8", errors="replace").replace("\n", " ")
        log.info(
            "→ %s %s bytes=%s%s",
            self.command,
            path,
            len(body),
            f" body={preview!r}" if preview else "",
        )
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
        req = Request(
            f"{UPSTREAM}{path}",
            data=body if self.command not in ("GET", "HEAD") else None,
            headers=headers,
            method=self.command,
        )
        try:
            with urlopen(req, timeout=600) as resp:
                data = resp.read()
                status = resp.status
                ctype = resp.headers.get("Content-Type")
            ms = (time.perf_counter() - t0) * 1000
            log.info(
                "← %s %s status=%s %.0fms bytes=%s",
                self.command,
                path,
                status,
                ms,
                len(data),
            )
            self.send_response(status)
            if ctype:
                self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(data)
        except HTTPError as e:
            data = e.read()
            ms = (time.perf_counter() - t0) * 1000
            log.warning(
                "← %s %s status=%s %.0fms err_body=%s",
                self.command,
                path,
                e.code,
                ms,
                len(data),
            )
            self.send_response(e.code)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(data)
        except (URLError, TimeoutError, OSError) as e:
            ms = (time.perf_counter() - t0) * 1000
            msg = f"proxy error: {e}".encode()
            log.warning("← %s %s FAIL %.0fms %s", self.command, path, ms, e)
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(msg)

    def do_GET(self) -> None:
        self._proxy()

    def do_HEAD(self) -> None:
        self._proxy()

    def do_POST(self) -> None:
        self._proxy()

    def do_PUT(self) -> None:
        self._proxy()

    def do_DELETE(self) -> None:
        self._proxy()


def main() -> None:
    host, _, port_s = BIND.partition(":")
    port = int(port_s or "11435")
    httpd = ThreadingHTTPServer((host or "127.0.0.1", port), Handler)
    log.info("proxy listen=%s upstream=%s log=%s", BIND, UPSTREAM, LOG_PATH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        log.info("proxy stop")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
