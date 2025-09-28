
import json, hmac, hashlib
from copy import deepcopy
from pathlib import Path
from typing import Dict, List

SECRET = "supersecret"
BASE_DIR = Path(__file__).resolve().parent
CONFIGS_DIR = BASE_DIR / "configs"
TENANTS_PATH = CONFIGS_DIR / "tenants.json"

DEFAULTS = {
    "version": 1,
    "features": {
        "broadcasting": False,
        "leveling": False,
        "blackjack": False,
        "assistants": False,
    },
}


def _fresh_defaults() -> dict:
    base = deepcopy(DEFAULTS)
    base["features"] = dict(DEFAULTS["features"])
    return base

def _signable(data: dict) -> bytes:
    d = dict(data)
    d.pop("sig", None)
    return json.dumps(d, separators=(",", ":"), sort_keys=True).encode()

def _sign_inplace(data: dict) -> dict:
    raw = _signable(data)
    data["sig"] = hmac.new(SECRET.encode(), raw, hashlib.sha256).hexdigest()
    return data

def _read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def _write_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")

def tenants() -> List[dict]:
    t = _read_json(TENANTS_PATH)
    return t.get("tenants", [])

def set_tenants(data: List[dict]):
    _write_json(TENANTS_PATH, {"tenants": data})

def ensure_config_for(tenant_id: str) -> dict:
    cfg_path = CONFIGS_DIR / f"{tenant_id}.json"
    if not cfg_path.exists():
        state = _fresh_defaults()
        return _persist_config(tenant_id, state)

    data = _read_json(cfg_path)
    # normalize keys (in case of missing fields)
    state = _fresh_defaults()
    state["features"].update({k: bool(v) for k, v in data.get("features", {}).items()})
    state["version"] = int(data.get("version", state["version"]))
    return _persist_config(tenant_id, state)

def _write_to_target_if_any(tenant_id: str, data: dict):
    # if tenant mapping has a config_path, write there as well
    for t in tenants():
        if t.get("id") == tenant_id:
            target = t.get("config_path")
            if target:
                try:
                    p = Path(target)
                    _write_json(p, data)
                except Exception:
                    pass
            break


def _persist_config(tenant_id: str, state: dict) -> dict:
    _sign_inplace(state)
    _write_json(CONFIGS_DIR / f"{tenant_id}.json", state)
    _write_to_target_if_any(tenant_id, state)
    return state

def toggle(tenant_id: str, feature_id: str) -> dict:
    state = ensure_config_for(tenant_id)
    feats: Dict[str, bool] = state.setdefault("features", {})
    current = bool(feats.get(feature_id, False))
    feats[feature_id] = not current
    state["version"] = int(state.get("version", 1)) + 1
    return _persist_config(tenant_id, state)


def set_feature(tenant_id: str, feature_id: str, enabled: bool) -> dict:
    state = ensure_config_for(tenant_id)
    feats: Dict[str, bool] = state.setdefault("features", {})
    desired = bool(enabled)
    if feats.get(feature_id, False) == desired:
        return state
    feats[feature_id] = desired
    state["version"] = int(state.get("version", 1)) + 1
    return _persist_config(tenant_id, state)
