import json, os, sys

RUNTIME = "gcs/runtime"

def load_json(path):
    full = os.path.join(RUNTIME, path)
    if not os.path.exists(full):
        return {"error": "not_found", "path": full}
    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)

def endpoint_sync():
    return load_json("phb_vortex_sync_v2.json")

def endpoint_node_packet():
    return load_json("p2p_packets/node_packet.json")

def endpoint_global_veil():
    return load_json("p2p_veil_field_v3.json")

def endpoint_global_timeline():
    return load_json("global_timeline.json")

def endpoint_agents():
    dir_path = os.path.join(RUNTIME, "p2p_packets")
    agents = []
    if os.path.isdir(dir_path):
        for name in os.listdir(dir_path):
            if name.endswith(".json"):
                try:
                    with open(os.path.join(dir_path, name), "r", encoding="utf-8") as f:
                        pkt = json.load(f)
                    agents.append({
                        "agent_id": pkt.get("agent_id"),
                        "node_id": pkt.get("node_id"),
                        "label": pkt.get("label")
                    })
                except:
                    continue
    return {
        "engine": "PHB VORTEX AGENT DIRECTORY",
        "agents": agents
    }

ENDPOINTS = {
    "sync": endpoint_sync,
    "node_packet": endpoint_node_packet,
    "global_veil": endpoint_global_veil,
    "global_timeline": endpoint_global_timeline,
    "agents": endpoint_agents
}

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "engine": "PHB VORTEX API CLI",
            "usage": "python3 phb_vortex_api.py <sync|node_packet|global_veil|global_timeline|agents>"
        }, indent=2))
        return

    cmd = sys.argv[1]
    if cmd in ENDPOINTS:
        out = ENDPOINTS[cmd]()
        print(json.dumps(out, indent=2))
    else:
        print(json.dumps({"error": "unknown_endpoint", "endpoint": cmd}, indent=2))

if __name__ == "__main__":
    main()
