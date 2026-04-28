#!/usr/bin/env python3
"""Receive Slack Approve/Reject button clicks and execute trade tickets."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import pathlib
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs


ROOT = pathlib.Path(__file__).resolve().parents[1]


def verify_slack_signature(headers: Any, body: bytes, signing_secret: str) -> bool:
    timestamp = headers.get("X-Slack-Request-Timestamp", "")
    signature = headers.get("X-Slack-Signature", "")
    if not timestamp or not signature:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    if abs(time.time() - ts) > 300:
        return False
    basestring = b"v0:" + timestamp.encode() + b":" + body
    expected = "v0=" + hmac.new(signing_secret.encode(), basestring, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def run_executor(action: str, ticket_id: str, user: str) -> None:
    cmd = [
        "python3",
        str(ROOT / "scripts" / "execute_approved_trade.py"),
        action,
        ticket_id,
        "--approver",
        user,
    ]
    subprocess.run(cmd, cwd=ROOT, check=False)


class Handler(BaseHTTPRequestHandler):
    signing_secret = ""
    allow_unsigned = False

    def log_message(self, fmt: str, *args: Any) -> None:
        print("%s - %s" % (self.address_string(), fmt % args))

    def send_json(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/slack/actions":
            self.send_json(404, {"text": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        if not self.allow_unsigned:
            if not self.signing_secret:
                self.send_json(500, {"text": "SLACK_SIGNING_SECRET is not configured"})
                return
            if not verify_slack_signature(self.headers, raw, self.signing_secret):
                self.send_json(401, {"text": "invalid Slack signature"})
                return

        form = parse_qs(raw.decode())
        payload_raw = form.get("payload", ["{}"])[0]
        payload = json.loads(payload_raw)
        actions = payload.get("actions") or []
        if not actions:
            self.send_json(400, {"text": "missing action"})
            return
        action = actions[0]
        action_id = action.get("action_id")
        ticket_id = action.get("value")
        user = payload.get("user", {}).get("username") or payload.get("user", {}).get("id") or "slack"
        if action_id == "approve_trade":
            verb = "approve"
        elif action_id == "reject_trade":
            verb = "reject"
        else:
            self.send_json(400, {"text": f"unsupported action {action_id}"})
            return

        thread = threading.Thread(target=run_executor, args=(verb, ticket_id, user), daemon=True)
        thread.start()
        self.send_json(200, {"text": f"{verb.title()} received for {ticket_id}. I will post the final status here."})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("APPROVAL_PORT", "8787")))
    parser.add_argument("--allow-unsigned", action="store_true")
    args = parser.parse_args()
    Handler.signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    Handler.allow_unsigned = args.allow_unsigned
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Slack approval server listening on http://{args.host}:{args.port}/slack/actions")
    server.serve_forever()


if __name__ == "__main__":
    main()
