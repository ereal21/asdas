import aiohttp
from aiohttp import web
from typing import Dict, Optional
from config import (
    NOWPAYMENTS_API_KEY,
    NOWPAYMENTS_API_URL,
    NOWPAYMENTS_IPN_URL,
    DEFAULT_CURRENCY,
    ADMIN_ID,
    PACKAGE_STATUSES,
)
from texts import T
from database import Database
from aiogram import Bot

bot: Optional[Bot] = None
db: Optional[Database] = None
qr_messages: Dict[int, int] = {}


def init_payments(bot_obj: Bot, db_obj: Database, qr_dict: Dict[int, int]):
    global bot, db, qr_messages
    bot = bot_obj
    db = db_obj
    qr_messages = qr_dict


async def create_invoice(
    price: float, pay_currency: str, order_id: str, description: str
) -> Dict:
    """Create a payment via NowPayments and return API response."""

    headers = {
        "x-api-key": NOWPAYMENTS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "price_amount": price,
        "price_currency": DEFAULT_CURRENCY,
        "pay_currency": pay_currency,
        "order_id": order_id,
        "order_description": description,
        "ipn_callback_url": NOWPAYMENTS_IPN_URL,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f"{NOWPAYMENTS_API_URL}/payment", json=payload) as resp:
            return await resp.json()


async def ipn_handler(request: web.Request):
    data = await request.json()
    status = data.get("payment_status")
    order_id = data.get("order_id", "")
    if status not in {"confirmed", "finished"}:
        return web.Response(text="OK")

    parts = order_id.split("-")
    if len(parts) < 2:
        return web.Response(text="OK")
    item = parts[0]
    try:
        user_id = int(parts[1])
    except ValueError:
        return web.Response(text="OK")

    tier_map = PACKAGE_STATUSES
    rdp_map = {"rdp1": "1 month", "rdp2": "2 months", "rdp3": "3 months"}
    new_status = tier_map.get(item)
    if new_status:
        db.set_status(user_id, new_status)
        db.set_config_seen(user_id, False)

    # remove invoice message
    if user_id in qr_messages:
        try:
            await bot.delete_message(user_id, qr_messages.pop(user_id))
        except Exception:
            qr_messages.pop(user_id, None)

    lang = db.get_language(user_id)
    if item in tier_map:
        await bot.send_message(user_id, T[lang]["purchase_success"])
    elif item in rdp_map:
        await bot.send_message(user_id, T[lang]["rdp_payment_success"])
    else:
        return web.Response(text="OK")

    if ADMIN_ID:
        user = db.get_user(user_id)
        uname = user[1] if user and user[1] else str(user_id)
        if item in tier_map:
            await bot.send_message(
                ADMIN_ID, f"{uname} (ID {user_id}) purchased {item} package"
            )
        elif item in rdp_map:
            amount = data.get("price_amount", "")
            months = rdp_map[item]
            await bot.send_message(
                ADMIN_ID,
                f"{uname} (ID {user_id}) purchased RDP {months} for {amount} {DEFAULT_CURRENCY}",
            )

    return web.Response(text="OK")
