import sys, json
from client import CueDesktopAmbientTrigger

def handle_mcp():
    cue = CueDesktopAmbientTrigger()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(cue.run_cue_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-cue-desktop-ambient-context-trigger-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "detect_contextual_cues", "description": "Analyze active desktop context and clipboard.", "inputSchema": {"type": "object", "properties": {"active_app": {"type": "string"}, "window_title": {"type": "string"}, "clipboard_text": {"type": "string"}}}},
                    {"name": "run_cue_benchmark", "description": "Run Cue ambient trigger benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "detect_contextual_cues":
                    res = cue.detect_contextual_cues(args.get("active_app", ""), args.get("window_title", ""), args.get("clipboard_text", ""))
                else:
                    res = cue.run_cue_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
