#!/usr/bin/env python3
"""Serve the portable game locally. No external dependencies or network calls."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8783);p.add_argument('--open',action='store_true');args=p.parse_args()
root=Path(__file__).resolve().parent/'clinic'
server=ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(root)))
url=f'http://127.0.0.1:{server.server_port}'
print(f'醫館 · 청사진 · v2 1단계: {url}',flush=True)
if args.open:webbrowser.open(url)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
