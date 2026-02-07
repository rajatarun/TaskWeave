import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict

from agents.agent_initializer import create_agent_from_config


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Dict[str, Any]):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class TaskWeaveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            _json_response(self, 200, {"status": "ok"})
            return
        _json_response(self, 404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/invoke":
            _json_response(self, 404, {"error": "Not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
            config = payload["config"]
            question = payload.get("input") or payload.get("question")
            if not question:
                raise ValueError("Missing 'input' or 'question' in request body")

            agent, memory = create_agent_from_config(config)
            result = agent.invoke({"input": question})
            _json_response(self, 200, {"result": result, "shared_memory": memory})
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            _json_response(self, 400, {"error": str(exc)})
        except Exception as exc:
            _json_response(self, 500, {"error": str(exc)})


def run(host: str = "0.0.0.0", port: int = 8000):
    server = HTTPServer((host, port), TaskWeaveHandler)
    print(f"TaskWeave API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
