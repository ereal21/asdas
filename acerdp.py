import aiohttp
from typing import Any, Dict, Optional
from config import ACERDP_API_BASE, ACERDP_API_KEY

HEADERS = {
    "Authorization": f"Bearer {ACERDP_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

class AceRDPError(Exception):
    pass

def require_key():
    if not ACERDP_API_KEY:
        raise AceRDPError("ACERDP_API_KEY is not set. Add it to your .env")

async def _request(method: str, path: str, params: Optional[Dict]=None, json: Optional[Dict]=None) -> Dict[str, Any]:
    require_key()
    url = f"{ACERDP_API_BASE}{path}"
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, headers=HEADERS, params=params, json=json, timeout=60) as resp:
            try:
                data = await resp.json()
            except Exception:
                text = await resp.text()
                raise AceRDPError(f"Invalid response: {resp.status} {text}")
            if resp.status >= 400 or data.get("status") == "error" or data.get("error"):
                msg = data.get("message") or data.get("error") or f"HTTP {resp.status}"
                raise AceRDPError(msg)
            return data

async def list_os() -> Dict: return await _request("GET", "/os")
async def place_order(package_id: str, operating_system_id: str, days: int) -> Dict:
    return await _request("POST", "/order", json={"package_id": str(package_id), "operating_system_id": str(operating_system_id), "days": int(days)})
async def order_details(order_id: str) -> Dict: return await _request("GET", "/order-details", params={"order_id": order_id})
async def reset_password(order_id: str) -> Dict: return await _request("POST", "/reset-password", json={"order_id": order_id})
async def extend_order(order_id: str, days: int) -> Dict: return await _request("POST", "/extend-order", json={"order_id": order_id, "days": int(days)})
async def shutdown(order_id: str) -> Dict: return await _request("POST", "/shutdown", json={"order_id": order_id})
async def start(order_id: str) -> Dict: return await _request("POST", "/start", json={"order_id": order_id})
async def restart(order_id: str) -> Dict: return await _request("POST", "/restart", json={"order_id": order_id})
async def reinstall(order_id: str, operating_system_id: str) -> Dict:
    return await _request("POST", "/reinstall", json={"order_id": order_id, "operating_system_id": str(operating_system_id)})
async def verify_key() -> bool:
    try:
        await list_os(); return True
    except Exception:
        return False
