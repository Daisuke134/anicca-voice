"""Create the Anicca Pause agent on Bolna and trigger an outbound call.
Usage: BOLNA_API_KEY=... python pause.py create
       BOLNA_API_KEY=... python pause.py call +15551234567 [agent_id]
       BOLNA_API_KEY=... python pause.py execution <execution_id>"""
import json, os, sys, pathlib, urllib.request, urllib.error
API = "https://api.bolna.ai"
HERE = pathlib.Path(__file__).parent
def req(method, path, body=None):
    r = urllib.request.Request(API + path, method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + os.environ["BOLNA_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r) as f:
            return json.loads(f.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Bolna {e.code}: {e.read().decode()}")
def create():
    cfg = json.loads((HERE / "agent.json").read_text())
    cfg["agent_prompts"]["task_1"]["system_prompt"] = (HERE / "prompt.md").read_text()
    out = req("POST", "/v2/agent", cfg); print(json.dumps(out, indent=2)); return out["agent_id"]
def call(number, agent_id=None):
    agent_id = agent_id or os.environ.get("BOLNA_AGENT_ID") or create()
    print(json.dumps(req("POST", "/call", {"agent_id": agent_id, "recipient_phone_number": number}), indent=2))
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "create"
    if cmd == "create": create()
    elif cmd == "call": call(*sys.argv[2:4])
    elif cmd == "execution": print(json.dumps(req("GET", f"/executions/{sys.argv[2]}"), indent=2))
