#!/usr/bin/env python3
"""Sider Chat local server + proxy (Python standard library only, no installs).

Why a proxy? sider.ai.id sends no CORS headers, so a browser page cannot
call it directly. This tiny server serves index.html and forwards:

    GET  /api/models  ->  GET  https://sider.ai.id/v1/models
    POST /api/chat    ->  POST https://sider.ai.id/v1/chat/completions

Your API key travels only in the Authorization header your browser sends;
it is never stored on disk or logged.

Run:  python3 server.py          (then open http://localhost:8000)
Port: PORT env var, default 8000.
"""
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://sider.ai.id/v1"
HERE = os.path.dirname(os.path.abspath(__file__))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # quiet: never log headers (they carry the API key)

    def _proxy(self, upstream_path, body=None):
        url = UPSTREAM + upstream_path
        req = urllib.request.Request(url, data=body, method="POST" if body else "GET")
        # Cloudflare in front of Sider blocks the default Python user agent
        # (error 1010), so present as a regular browser.
        req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
        req.add_header("Accept", "application/json")
        auth = self.headers.get("Authorization")
        if auth:
            req.add_header("Authorization", auth)
        if body:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=300) as res:
                payload, status = res.read(), res.status
        except urllib.error.HTTPError as e:
            payload, status = e.read(), e.code
        except Exception as e:  # network failure etc.
            payload = ('{"error":{"message":"Upstream unreachable: %s"}}' % e).encode()
            status = 502
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/models":
            self._proxy("/models")
        elif self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                payload = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/api/chat":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            self._proxy("/chat/completions", body=body)
        else:
            self.send_error(404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print("Sider Chat running at http://localhost:%d" % port)
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
