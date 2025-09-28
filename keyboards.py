
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    SUPPORT_USERNAME,
    DEFAULT_CURRENCY,
    RDP_PACKAGES,
    PACKAGE_ORDER,
    STATUS_TO_PACKAGE,
    get_package_price,
)
from texts import T
from typing import Optional, List, Tuple


def language_keyboard(lang: Optional[str] = None):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("🇬🇧 EN", callback_data="lang:en"),
        InlineKeyboardButton("🇷🇺 RU", callback_data="lang:ru"),
        InlineKeyboardButton("🇱🇹 LT", callback_data="lang:lt"),
    )
    if lang:
        kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb

def main_menu_keyboard(lang: str, is_admin: bool = False, show_purchase: bool = True):
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    if show_purchase:
        buttons.append(
            InlineKeyboardButton(T[lang]["menu_purchase"], callback_data="menu:purchase")
        )
    buttons.extend(
        [
            InlineKeyboardButton(T[lang]["menu_config"], callback_data="menu:config"),
            InlineKeyboardButton(T[lang]["menu_topup"], callback_data="menu:topup"),
            InlineKeyboardButton(
                T[lang]["menu_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
            ),
            InlineKeyboardButton(T[lang]["menu_language"], callback_data="menu:lang"),
        ]
    )
    kb.add(*buttons)
    if is_admin:
        kb.add(InlineKeyboardButton(T[lang]["menu_admin"], callback_data="menu:admin"))
    return kb


def config_keyboard(lang: str, setup_done: bool):
    kb = InlineKeyboardMarkup(row_width=1)
    if setup_done:
        kb.add(InlineKeyboardButton(T[lang]["config_rdp"], callback_data="config:rdp"))
    else:
        kb.add(InlineKeyboardButton(T[lang]["config_setup"], callback_data="config:setup"))
    kb.add(InlineKeyboardButton(T[lang]["config_functions"], callback_data="config:functions"))
    kb.add(
        InlineKeyboardButton(
            T[lang]["config_support"], url=f"https://t.me/{SUPPORT_USERNAME}"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_menu_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_protection"], callback_data="functions:protection"
        )
    )
    kb.add(
        InlineKeyboardButton(T[lang]["functions_admin"], callback_data="functions:admin")
    )
    kb.add(
        InlineKeyboardButton(T[lang]["functions_user"], callback_data="functions:user")
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["functions_payments"], callback_data="functions:payments"
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_protection_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            T[lang]["feature_anti_spam"], callback_data="feature:anti_spam"
        ),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def functions_admin_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            T[lang]["feature_assistant_management"],
            callback_data="feature:assistant_management",
        ),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def functions_user_keyboard(lang: str):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton(
            T[lang]["feature_user_levels"], callback_data="feature:user_levels"
        )
    )
    kb.add(
        InlineKeyboardButton(
            T[lang]["feature_stock_notifications"],
            callback_data="feature:stock_notifications",
        )
    )
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def functions_payments_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def setup_next_keyboard(lang: str, next_cb: str):
    return (
        InlineKeyboardMarkup(row_width=2)
        .add(
            InlineKeyboardButton(T[lang]["next"], callback_data=next_cb),
            InlineKeyboardButton(T[lang]["cancel"], callback_data="setup:cancel"),
        )
    )


def setup_cancel_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="setup:cancel")
    )


def setup_complete_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["complete"], callback_data="setup:finish")
    )

def purchase_keyboard(lang: str, status: str):
    cur = DEFAULT_CURRENCY
    kb = InlineKeyboardMarkup(row_width=1)

    current_package = STATUS_TO_PACKAGE.get(status)
    try:
        current_index = PACKAGE_ORDER.index(current_package) if current_package else -1
    except ValueError:
        current_index = -1

    label_map = {
        "template": "purchase_template",
        "semi": "purchase_semi",
        "full": "purchase_full",
    }

    for idx, package in enumerate(PACKAGE_ORDER):
        if idx <= current_index:
            continue
        price = get_package_price(package, status)
        kb.add(
            InlineKeyboardButton(
                T[lang][label_map[package]].format(price=price, cur=cur),
                callback_data=f"purchase:{package}",
            )
        )

    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def rdp_keyboard(lang: str):
    cur = DEFAULT_CURRENCY
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            T[lang]["rdp_1m"].format(price=RDP_PACKAGES["rdp1"], cur=cur),
            callback_data="rdp:1",
        ),
        InlineKeyboardButton(
            T[lang]["rdp_2m"].format(price=RDP_PACKAGES["rdp2"], cur=cur),
            callback_data="rdp:2",
        ),
        InlineKeyboardButton(
            T[lang]["rdp_3m"].format(price=RDP_PACKAGES["rdp3"], cur=cur),
            callback_data="rdp:3",
        ),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def purchase_item_keyboard(lang: str, item: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["buy"], callback_data=f"buy:{item}"),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def payment_method_keyboard(lang: str, item: str, allow_balance: bool = True):
    """Return keyboard with available payment methods."""

    kb = InlineKeyboardMarkup(row_width=1)
    if allow_balance:
        kb.add(
            InlineKeyboardButton(
                T[lang]["pay_with_balance"], callback_data=f"pay:{item}:BAL"
            )
        )
    kb.add(
        InlineKeyboardButton("🪙 SOL", callback_data=f"pay:{item}:SOL"),
        InlineKeyboardButton("🪙 USDT-TRC20", callback_data=f"pay:{item}:USDTTRC20"),
        InlineKeyboardButton("🪙 XMR", callback_data=f"pay:{item}:XMR"),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )
    return kb

def back_to_menu(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["back"], callback_data="back")
    )


def cancel_payment(lang: str):
    """Keyboard with cancel button for invoice screen."""

    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="cancel")
    )


def admin_panel_keyboard(lang: str, online: bool):
    toggle = (
        T[lang]["admin_set_offline"]
        if online
        else T[lang]["admin_set_online"]
    )
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton(toggle, callback_data="admin:toggle_online"))
    kb.add(InlineKeyboardButton(T[lang]["user_lookup"], callback_data="admin:user_lookup"))
    kb.add(InlineKeyboardButton(T[lang]["manage_rdps"], callback_data="admin:rdps"))
    kb.add(InlineKeyboardButton("Priskirti klientą", callback_data="admin:assign_customer"))
    kb.add(InlineKeyboardButton("Funkcijos", callback_data="cfg:back"))
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def user_profile_keyboard(user_id: int, lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(
            "💰 " + T[lang]["top_up_balance"], callback_data=f"admin:balance:{user_id}"
        ),
        InlineKeyboardButton(T[lang]["back"], callback_data="menu:admin"),
    )


def topup_amount_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="topup:cancel")
    )


def rdp_details_keyboard(lang: str):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(T[lang]["extend"], callback_data="rdp:extend"),
        InlineKeyboardButton(T[lang]["back"], callback_data="back"),
    )


def manage_rdps_keyboard(lang: str, users: List[Tuple[int, Optional[str]]]):
    kb = InlineKeyboardMarkup(row_width=1)
    for user_id, username in users:
        name = f"@{username}" if username else str(user_id)
        kb.add(InlineKeyboardButton(name, callback_data=f"admin:rdp:{user_id}"))
    kb.add(InlineKeyboardButton(T[lang]["back"], callback_data="back"))
    return kb


def admin_rdp_cancel_keyboard(lang: str):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(T[lang]["cancel"], callback_data="admin:rdp_cancel")
    )
