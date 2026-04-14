import json
import os
from typing import Any, Dict
from phb_config_backup import PHB_CONFIG_BACKUP

CONFIG_PATH = "phb_intelligence_core_v2_1.json"

def load_json_config(path: str = CONFIG_PATH) -> Dict[str, Any]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return PHB_CONFIG_BACKUP

PHB_CONFIG_PACK: Dict[str, Any] = load_json_config()

def get_config() -> Dict[str, Any]:
    return PHB_CONFIG_PACK.get("phb_intelligence_core_v2_1", {})
