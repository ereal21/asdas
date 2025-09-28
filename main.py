import logging
import io
import os
from datetime import datetime, timedelta
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiohttp import web

import qrcode
from config import (
    BOT_TOKEN,
    RDP_PACKAGES,
    ADMIN_ID,
    STEP1_IMAGE,
    STEP2_IMAGE,
    STEP3_IMAGE,
    STEP4_IMAGE,
    STEP5_IMAGE,
    STEP6_IMAGE,
    STEP7_IMAGE,
    PACKAGE_STATUSES,
    get_package_price,
)
from database import Database
from keyboards import (
    language_keyboard,
    main_menu_keyboard,
    purchase_keyboard,
    back_to_menu,
    purchase_item_keyboard,
    payment_method_keyboard,
    cancel_payment,
    admin_panel_keyboard,
    user_profile_keyboard,
    config_keyboard,
    functions_menu_keyboard,
    functions_protection_keyboard,
    functions_admin_keyboard,
    functions_user_keyboard,
    functions_payments_keyboard,
    rdp_keyboard,
    setup_next_keyboard,
    setup_cancel_keyboard,
    setup_complete_keyboard,
    topup_amount_keyboard,
    rdp_details_keyboard,
    manage_rdps_keyboard,
    admin_rdp_cancel_keyboard,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from texts import T
from payments import create_invoice, ipn_handler, init_payments

logging.basicConfig(level=logging.INFO)
db = Database()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage())
history = defaultdict(list)
qr_messages = {}
init_payments(bot, db, qr_messages)
FULL_STATUS = PACKAGE_STATUSES["full"]


class AdminStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_balance = State()


class TopUpStates(StatesGroup):
    waiting_for_amount = State()


class SetupStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_ngrok = State()
    waiting_for_crypto = State()
    waiting_for_api_key = State()
    waiting_for_ipn_key = State()
    waiting_for_user_id = State()
    waiting_for_botfather = State()
    waiting_for_bot_token = State()


class ManageRDPStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    waiting_for_ip = State()
    waiting_for_name = State()
    waiting_for_rdp_password = State()
    waiting_for_expiry = State()


def _display_name(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"
    if user.full_name:
        return user.full_name
    return str(user.id)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    user = message.from_user
    existing = db.get_user(user.id)
    history[user.id].clear()
    db.upsert_user(user.id, user.username)
    if existing is None:
        await message.answer(
            T["en"]["choose_language"], reply_markup=language_keyboard()
        )
        return
    lang = db.get_language(user.id)
    balance = db.get_balance(user.id)
    status = db.get_status(user.id)
    text = T[lang]["main_title"].format(
        name=_display_name(user), status=status, balance=balance
    )
    await message.answer(
        text,
        reply_markup=main_menu_keyboard(
            lang,
            is_admin=user.id == ADMIN_ID,
            show_purchase=status != FULL_STATUS,
        ),
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("lang:"))
async def cb_set_language(call: types.CallbackQuery):
    lang = call.data.split(":")[1]
    user = call.from_user
    db.upsert_user(user.id, user.username, language=lang)

    name = _display_name(user)
    balance = db.get_balance(user.id)
    status = db.get_status(user.id)
    text = T[lang]["main_title"].format(name=name, status=status, balance=balance)
    await call.message.edit_text(
        text,
        reply_markup=main_menu_keyboard(
            lang,
            is_admin=user.id == ADMIN_ID,
            show_purchase=status != FULL_STATUS,
        ),
    )


@dp.callback_query_handler(lambda c: c.data == "menu:lang")
async def cb_language_menu(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(T[lang]["choose_language"], reply_markup=language_keyboard(lang))


@dp.callback_query_handler(lambda c: c.data == "menu:purchase")
async def cb_purchase(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_language(user_id)
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    status = db.get_status(user_id)
    if status == FULL_STATUS:
        await call.message.edit_text(
            T[lang]["purchase_unavailable"], reply_markup=back_to_menu(lang)
        )
        return
    await call.message.edit_text(
        T[lang]["purchase_title"] + "\n\n" + T[lang]["purchase_hint"],
        reply_markup=purchase_keyboard(lang, status),
    )


@dp.callback_query_handler(lambda c: c.data == "menu:config")
async def cb_config(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    status = db.get_status(call.from_user.id)
    if status == "None":
        await call.message.edit_text(
            T[lang]["config_no_status"], reply_markup=back_to_menu(lang)
        )
        return
    first_time = not db.get_config_seen(call.from_user.id)
    if first_time:
        db.set_config_seen(call.from_user.id, True)
        text = T[lang]["config_first_time"]
    else:
        text = T[lang]["config_title"]
    setup_done = db.get_setup_done(call.from_user.id)
    await call.message.edit_text(text, reply_markup=config_keyboard(lang, setup_done))


@dp.callback_query_handler(lambda c: c.data == "config:functions")
async def cb_config_functions(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_title"], reply_markup=functions_menu_keyboard(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "functions:protection")
async def cb_functions_protection(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_protection_desc"],
        reply_markup=functions_protection_keyboard(lang),
    )


@dp.callback_query_handler(lambda c: c.data == "functions:admin")
async def cb_functions_admin(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_admin_desc"],
        reply_markup=functions_admin_keyboard(lang),
    )


@dp.callback_query_handler(lambda c: c.data == "functions:user")
async def cb_functions_user(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_user_desc"],
        reply_markup=functions_user_keyboard(lang),
    )


@dp.callback_query_handler(lambda c: c.data == "functions:payments")
async def cb_functions_payments(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["functions_payments_desc"],
        reply_markup=functions_payments_keyboard(lang),
    )


@dp.callback_query_handler(lambda c: c.data == "feature:anti_spam")
async def cb_feature_anti_spam(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["feature_anti_spam_desc"], reply_markup=back_to_menu(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "feature:assistant_management")
async def cb_feature_assistant(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["feature_assistant_management_desc"], reply_markup=back_to_menu(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "feature:user_levels")
async def cb_feature_user_levels(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["feature_user_levels_desc"], reply_markup=back_to_menu(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "feature:stock_notifications")
async def cb_feature_stock_notifications(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["feature_stock_notifications_desc"],
        reply_markup=back_to_menu(lang),
    )


@dp.callback_query_handler(lambda c: c.data == "config:rdp")
async def cb_config_rdp(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    info = db.get_rdp_config(call.from_user.id)
    if info:
        text = T[lang]["rdp_details"].format(
            email=info.get("email", "-"),
            password=info.get("password", "-"),
            ip=info.get("ip", "-"),
            name=info.get("name", "-"),
            rdp_password=info.get("rdp_password", "-"),
            expiry=info.get("expiry", "-"),
        )
        await call.message.edit_text(text, reply_markup=rdp_details_keyboard(lang))
    else:
        await call.message.edit_text(
            T[lang]["rdp_choose_package"], reply_markup=rdp_keyboard(lang)
        )


@dp.callback_query_handler(lambda c: c.data == "rdp:extend")
async def cb_rdp_extend(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["rdp_choose_package"], reply_markup=rdp_keyboard(lang)
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("rdp:"))
async def cb_rdp_package(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    months = call.data.split(":")[1]
    item = f"rdp{months}"
    await call.message.edit_text(
        T[lang]["choose_payment"],
        reply_markup=payment_method_keyboard(lang, item, allow_balance=False),
    )


@dp.callback_query_handler(lambda c: c.data == "config:setup")
async def cb_config_setup(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["setup_intro"],
        reply_markup=setup_next_keyboard(lang, "setup:create_email"),
    )


@dp.callback_query_handler(lambda c: c.data == "setup:create_email")
async def setup_create_email(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["setup_create_email"],
        reply_markup=setup_next_keyboard(lang, "setup:enter_email"),
    )


@dp.callback_query_handler(lambda c: c.data == "setup:enter_email")
async def setup_enter_email(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_language(call.from_user.id)
    await SetupStates.waiting_for_email.set()
    await call.message.edit_text(
        T[lang]["setup_enter_email"], reply_markup=setup_cancel_keyboard(lang)
    )


@dp.message_handler(state=SetupStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    lang = db.get_language(message.from_user.id)
    text = T[lang]["setup_ngrok_signup"]
    if STEP7_IMAGE and os.path.exists(STEP7_IMAGE):
        with open(STEP7_IMAGE, "rb") as media:
            if STEP7_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(
                    media,
                    caption=text,
                    reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
                )
            else:
                await message.answer_photo(
                    media,
                    caption=text,
                    reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
                )
    else:
        await message.answer(
            text,
            reply_markup=setup_next_keyboard(lang, "setup:ngrok_token"),
        )
    await message.delete()
    await SetupStates.waiting_for_ngrok.set()


@dp.callback_query_handler(
    lambda c: c.data == "setup:ngrok_token", state=SetupStates.waiting_for_ngrok
)
async def setup_ngrok_token(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_ngrok_token_prompt"]
    if call.message.content_type in ("photo", "video"):
        await call.message.edit_caption(text, reply_markup=setup_cancel_keyboard(lang))
    else:
        await call.message.edit_text(text, reply_markup=setup_cancel_keyboard(lang))
    await SetupStates.waiting_for_ngrok.set()


@dp.message_handler(state=SetupStates.waiting_for_ngrok)
async def process_ngrok_token(message: types.Message, state: FSMContext):
    await state.update_data(ngrok_token=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.answer(
        T[lang]["setup_np_signup"],
        reply_markup=setup_next_keyboard(lang, "setup:np_crypto"),
    )
    await message.delete()


@dp.callback_query_handler(
    lambda c: c.data == "setup:np_crypto", state=SetupStates.waiting_for_ngrok
)
async def setup_np_crypto(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_crypto_prompt"]
    keyboard = setup_next_keyboard(lang, "setup:np_start")
    if STEP1_IMAGE and os.path.exists(STEP1_IMAGE):
        with open(STEP1_IMAGE, "rb") as media:
            if STEP1_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard)
    await SetupStates.waiting_for_crypto.set()


@dp.callback_query_handler(
    lambda c: c.data == "setup:np_start", state=SetupStates.waiting_for_crypto
)
async def setup_np_start(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_start_integration"]

    keyboard_with_next = setup_next_keyboard(lang, "setup:np_settings")

    # Send STEP2 image/video if available
    if STEP2_IMAGE and os.path.exists(STEP2_IMAGE):
        with open(STEP2_IMAGE, "rb") as media:
            if STEP2_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard_with_next)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard_with_next)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard_with_next)

    await SetupStates.waiting_for_crypto.set()


@dp.message_handler(state=SetupStates.waiting_for_crypto)
async def process_crypto_address(message: types.Message, state: FSMContext):
    await state.update_data(crypto_address=message.text.strip())
    await message.delete()


@dp.callback_query_handler(
    lambda c: c.data == "setup:np_settings", state=SetupStates.waiting_for_crypto
)
async def setup_np_settings(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_settings"]
    keyboard = setup_next_keyboard(lang, "setup:np_api")
    await bot.send_message(call.from_user.id, text, reply_markup=keyboard)


@dp.callback_query_handler(
    lambda c: c.data == "setup:np_api", state=SetupStates.waiting_for_crypto
)
async def setup_np_api(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_np_api_prompt"]
    keyboard = setup_cancel_keyboard(lang)

    if STEP3_IMAGE and os.path.exists(STEP3_IMAGE):
        with open(STEP3_IMAGE, "rb") as media:
            if STEP3_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, text, reply_markup=keyboard)
    await SetupStates.waiting_for_api_key.set()


@dp.message_handler(state=SetupStates.waiting_for_api_key)
async def process_api_key(message: types.Message, state: FSMContext):
    await state.update_data(api_key=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    text = T[lang]["setup_np_ipn_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP4_IMAGE and os.path.exists(STEP4_IMAGE):
        with open(STEP4_IMAGE, "rb") as media:
            if STEP4_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(media, caption=text, reply_markup=keyboard)
            else:
                await message.answer_photo(media, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)
    await SetupStates.waiting_for_ipn_key.set()


@dp.message_handler(state=SetupStates.waiting_for_ipn_key)
async def process_ipn_key(message: types.Message, state: FSMContext):
    await state.update_data(ipn_key=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    text = T[lang]["setup_getid_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP5_IMAGE and os.path.exists(STEP5_IMAGE):
        with open(STEP5_IMAGE, "rb") as media:
            if STEP5_IMAGE.lower().endswith(".mp4"):
                await message.answer_video(media, caption=text, reply_markup=keyboard)
            else:
                await message.answer_photo(media, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)
    await SetupStates.waiting_for_user_id.set()


@dp.message_handler(state=SetupStates.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    await state.update_data(user_id=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await message.delete()
    await message.answer(
        T[lang]["setup_botfather_intro"],
        reply_markup=setup_next_keyboard(lang, "setup:botfather_token"),
    )
    await SetupStates.waiting_for_botfather.set()


@dp.callback_query_handler(
    lambda c: c.data == "setup:botfather_token", state=SetupStates.waiting_for_botfather
)
async def setup_botfather_token(call: types.CallbackQuery):
    await call.answer()
    lang = db.get_language(call.from_user.id)
    text = T[lang]["setup_botfather_token_prompt"]
    keyboard = setup_cancel_keyboard(lang)
    if STEP6_IMAGE and os.path.exists(STEP6_IMAGE):
        with open(STEP6_IMAGE, "rb") as media:
            await call.message.delete()
            if STEP6_IMAGE.lower().endswith(".mp4"):
                await bot.send_video(call.from_user.id, media, caption=text, reply_markup=keyboard)
            else:
                await bot.send_photo(call.from_user.id, media, caption=text, reply_markup=keyboard)
    else:
        await call.message.edit_text(text, reply_markup=keyboard)
    await SetupStates.waiting_for_bot_token.set()


@dp.message_handler(state=SetupStates.waiting_for_bot_token)
async def process_bot_token(message: types.Message, state: FSMContext):
    await state.update_data(bot_token=message.text.strip())
    data = await state.get_data()
    user = message.from_user
    status = db.get_status(user.id)
    summary = (
        f"Setup data for {_display_name(user)} (ID: {user.id})\n"
        f"Package: {status}\n"
        f"Email: {data.get('email')}\n"
        f"Ngrok token: {data.get('ngrok_token')}\n"
        f"NOWPayments API key: {data.get('api_key')}\n"
        f"IPN key: {data.get('ipn_key')}\n"
        f"GetID: {data.get('user_id')}\n"
        f"Bot token: {data.get('bot_token')}"
    )
    try:
        await bot.send_message(ADMIN_ID, summary)
    except Exception:
        pass
    lang = db.get_language(user.id)
    await state.finish()
    db.set_setup_done(user.id, True)
    await message.delete()
    final_text = (
        T[lang]["setup_done_online"]
        if db.get_admin_online()
        else T[lang]["setup_done"]
    )
    await message.answer(final_text, reply_markup=setup_complete_keyboard(lang))


@dp.callback_query_handler(lambda c: c.data == "setup:finish")
async def setup_finish(call: types.CallbackQuery):
    user_id = call.from_user.id
    lang = db.get_language(user_id)
    history[user_id] = history[user_id][:1]
    text = T[lang]["config_title"]
    await call.message.edit_text(
        text, reply_markup=config_keyboard(lang, True)
    )


@dp.callback_query_handler(lambda c: c.data == "setup:cancel", state="*")
async def setup_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["setup_cancelled"], reply_markup=back_to_menu(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "menu:topup")
async def cb_topup(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await TopUpStates.waiting_for_amount.set()
    await call.message.edit_text(
        T[lang]["enter_topup_amount"], reply_markup=topup_amount_keyboard(lang)
    )


@dp.callback_query_handler(
    lambda c: c.data == "topup:cancel", state=TopUpStates.waiting_for_amount
)
async def cb_topup_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.from_user.id
    if history[user_id]:
        text, markup = history[user_id].pop()
        await call.message.edit_text(text, reply_markup=markup)
    else:
        lang = db.get_language(user_id)
        name = _display_name(call.from_user)
        balance = db.get_balance(user_id)
        status = db.get_status(user_id)
        text = T[lang]["main_title"].format(
            name=name, status=status, balance=balance
        )
        await call.message.edit_text(
            text,
            reply_markup=main_menu_keyboard(
                lang,
                is_admin=user_id == ADMIN_ID,
                show_purchase=status != FULL_STATUS,
            ),
        )


@dp.callback_query_handler(lambda c: c.data == "menu:admin")
async def cb_admin_menu(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )


@dp.callback_query_handler(lambda c: c.data == "admin:toggle_online")
async def cb_toggle_admin_online(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    current = db.get_admin_online()
    db.set_admin_online(not current)
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, not current),
    )


@dp.callback_query_handler(lambda c: c.data == "admin:rdps")
async def cb_manage_rdps(call: types.CallbackQuery):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    users = db.get_setup_users()
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    if users:
        await call.message.edit_text(
            T[lang]["choose_rdp_user"],
            reply_markup=manage_rdps_keyboard(lang, users),
        )
    else:
        await call.message.edit_text(
            T[lang]["no_rdp_users"], reply_markup=manage_rdps_keyboard(lang, []),
        )


@dp.callback_query_handler(lambda c: c.data.startswith("admin:rdp:"))
async def cb_select_rdp_user(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    user_id = int(call.data.split(":")[2])
    await state.update_data(target_user=user_id)
    lang = db.get_language(call.from_user.id)
    await ManageRDPStates.waiting_for_email.set()
    await call.message.edit_text(
        T[lang]["enter_rdp_email"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.callback_query_handler(lambda c: c.data == "admin:user_lookup")
async def cb_user_lookup(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    await AdminStates.waiting_for_username.set()
    await call.message.edit_text(T[lang]["enter_username"])


@dp.message_handler(state=AdminStates.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    username = message.text.lstrip("@")
    user = db.get_user_by_username(username)
    lang = db.get_language(message.from_user.id)
    if user:
        user_id, uname, _, role, balance, _, _, regdate = user
        text = (
            f"{T[lang]['profile'].format(username=uname)}\n\n"
            f"{T[lang]['profile_username'].format(username=uname)}\n"
            f"{T[lang]['profile_id'].format(user_id=user_id)}\n"
            f"{T[lang]['profile_role'].format(role=role)}\n"
            f"{T[lang]['profile_regdate'].format(date=regdate)}\n"
            f"{T[lang]['profile_balance'].format(balance=balance)}"
        )
        await message.answer(text, reply_markup=user_profile_keyboard(user_id, lang))
    else:
        await message.answer(T[lang]["user_not_found"])
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith("admin:balance:"))
async def cb_set_balance(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id != ADMIN_ID:
        return
    lang = db.get_language(call.from_user.id)
    user_id = int(call.data.split(":")[2])
    await state.update_data(target_user=user_id)
    await AdminStates.waiting_for_balance.set()
    await call.message.answer(T[lang]["top_up_balance"])


@dp.message_handler(state=AdminStates.waiting_for_balance)
async def process_balance(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    lang = db.get_language(message.from_user.id)
    data = await state.get_data()
    user_id = data.get("target_user")
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer(T[lang]["invalid_amount"])
        await state.finish()
        return
    db.set_balance(user_id, amount)
    await message.answer(T[lang]["balance_set"].format(balance=amount))
    await state.finish()


@dp.message_handler(state=ManageRDPStates.waiting_for_email)
async def admin_rdp_email(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(email=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_password.set()
    await message.answer(
        T[lang]["enter_rdp_password"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.message_handler(state=ManageRDPStates.waiting_for_password)
async def admin_rdp_password(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(password=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_ip.set()
    await message.answer(
        T[lang]["enter_rdp_ip"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.message_handler(state=ManageRDPStates.waiting_for_ip)
async def admin_rdp_ip(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(ip=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_name.set()
    await message.answer(
        T[lang]["enter_rdp_name"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.message_handler(state=ManageRDPStates.waiting_for_name)
async def admin_rdp_name(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(name=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_rdp_password.set()
    await message.answer(
        T[lang]["enter_rdp_rdp_password"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.message_handler(state=ManageRDPStates.waiting_for_rdp_password)
async def admin_rdp_rdp_password(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    await state.update_data(rdp_password=message.text.strip())
    lang = db.get_language(message.from_user.id)
    await ManageRDPStates.waiting_for_expiry.set()
    await message.answer(
        T[lang]["enter_rdp_expiry"], reply_markup=admin_rdp_cancel_keyboard(lang)
    )


@dp.message_handler(state=ManageRDPStates.waiting_for_expiry)
async def admin_rdp_expiry(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.finish()
        return
    data = await state.get_data()
    user_id = data.get("target_user")
    db.set_rdp_config(
        user_id,
        data.get("email", ""),
        data.get("password", ""),
        data.get("ip", ""),
        data.get("name", ""),
        data.get("rdp_password", ""),
        message.text.strip(),
    )
    await state.finish()
    lang = db.get_language(message.from_user.id)
    await message.answer(
        T[lang]["rdp_saved"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )


@dp.callback_query_handler(
    lambda c: c.data == "admin:rdp_cancel", state=ManageRDPStates.all_states
)
async def admin_rdp_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    lang = db.get_language(call.from_user.id)
    await call.message.edit_text(
        T[lang]["admin_panel"],
        reply_markup=admin_panel_keyboard(lang, db.get_admin_online()),
    )


@dp.message_handler(state=TopUpStates.waiting_for_amount)
async def process_topup_amount(message: types.Message, state: FSMContext):
    lang = db.get_language(message.from_user.id)
    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(T[lang]["invalid_amount"])
        return
    history[message.from_user.id].append(
        (T[lang]["enter_topup_amount"], topup_amount_keyboard(lang))
    )
    await message.answer(
        T[lang]["choose_payment"],
        reply_markup=payment_method_keyboard(lang, f"topup-{amount}", allow_balance=False),
    )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("purchase:"))
async def cb_purchase_item(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    item = call.data.split(":")[1]
    desc_map = {
        "template": "desc_template",
        "semi": "desc_semi",
        "full": "desc_full",
    }
    msg = T[lang][desc_map.get(item, "desc_full")]
    await call.message.edit_text(msg, reply_markup=purchase_item_keyboard(lang, item))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("buy:"))
async def cb_buy_item(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    history[call.from_user.id].append((call.message.text or "", call.message.reply_markup))
    item = call.data.split(":")[1]
    await call.message.edit_text(
        T[lang]["choose_payment"], reply_markup=payment_method_keyboard(lang, item)
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("pay:"))
async def cb_pay(call: types.CallbackQuery):
    lang = db.get_language(call.from_user.id)
    user_id = call.from_user.id
    history[user_id].append((call.message.text or "", call.message.reply_markup))
    _, item, currency = call.data.split(":")

    status = db.get_status(user_id)
    if currency == "BAL":
        try:
            price = get_package_price(item, status)
        except (KeyError, ValueError):
            await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
            return

        if db.deduct_balance(user_id, price):
            new_status = PACKAGE_STATUSES.get(item)
            if new_status and new_status != status:
                db.set_status(user_id, new_status)
                db.set_config_seen(user_id, False)
            await call.message.edit_text(
                T[lang]["purchase_success"], reply_markup=back_to_menu(lang)
            )
            if ADMIN_ID:
                user = call.from_user
                uname = f"@{user.username}" if user.username else user.id
                await bot.send_message(ADMIN_ID, f"{uname} purchased {item} package via balance")
        else:
            await call.message.edit_text(
                T[lang]["insufficient_balance"], reply_markup=back_to_menu(lang)
            )
        return

    if item.startswith("topup-"):
        price = float(item.split("-")[1])
        order_id = f"topup-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = "topup"
    elif item.startswith("rdp"):
        price = RDP_PACKAGES[item]
        order_id = f"{item}-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = item
    else:
        try:
            price = get_package_price(item, status)
        except (KeyError, ValueError):
            await call.answer(T[lang]["purchase_unavailable"], show_alert=True)
            return
        order_id = f"{item}-{user_id}-{int(datetime.utcnow().timestamp())}"
        description = item

    invoice = await create_invoice(price, currency, order_id, description)
    amount = invoice.get("pay_amount", 0)
    address = invoice.get("pay_address", "")

    # Map currency codes for display
    display_cur = {"USDTTRC20": "USDT-TRC20"}.get(currency, currency)

    expires = (datetime.utcnow() + timedelta(minutes=30)).strftime("%H:%M UTC")
    text = (
        f"{T[lang]['invoice_created']}\n\n"
        f"*{T[lang]['amount']}:* `{amount} {display_cur}`\n"
        f"*{T[lang]['payment_address']}*\n`{address}`\n\n"
        f"*{T[lang]['expires_at']}* `{expires}`\n"
        f"_{T[lang]['invoice_warning']}_\n\n"
        f"_{T[lang]['invoice_exact'].format(cur=display_cur)}_\n"
        f"{T[lang]['invoice_confirm']}"
    )

    # Build QR code and send invoice photo
    qr = qrcode.make(address)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    await call.message.delete()
    msg = await bot.send_photo(
        user_id,
        buf,
        caption=text,
        reply_markup=cancel_payment(lang),
    )
    qr_messages[user_id] = msg.message_id


@dp.callback_query_handler(lambda c: c.data == "back")
async def cb_back(call: types.CallbackQuery):
    """Handle navigation when the user presses the back button."""
    user_id = call.from_user.id

    if history[user_id]:
        # Go back to previous message in history
        text, markup = history[user_id].pop()
        await call.message.edit_text(text, reply_markup=markup)
    else:
        # No history -> return to main menu
        lang = db.get_language(user_id)
        name = _display_name(call.from_user)
        balance = db.get_balance(user_id)
        status = db.get_status(user_id)
        text = T[lang]["main_title"].format(name=name, status=status, balance=balance)
        await call.message.edit_text(
            text,
            reply_markup=main_menu_keyboard(
                lang,
                is_admin=user_id == ADMIN_ID,
                show_purchase=status != FULL_STATUS,
            ),
        )


@dp.callback_query_handler(lambda c: c.data == "cancel")
async def cb_cancel(call: types.CallbackQuery):
    """Cancel invoice and return to previous message."""
    user_id = call.from_user.id

    # Delete the current message (e.g., QR/invoice)
    try:
        await call.message.delete()
    except Exception:
        pass

    # Remove QR code if one was tracked previously
    if user_id in qr_messages:
        try:
            await bot.delete_message(user_id, qr_messages.pop(user_id))
        except Exception:
            qr_messages.pop(user_id, None)

    # Return to previous UI or main menu
    if history[user_id]:
        text, markup = history[user_id].pop()
        await bot.send_message(user_id, text, reply_markup=markup)
    else:
        lang = db.get_language(user_id)
        name = _display_name(call.from_user)
        balance = db.get_balance(user_id)
        status = db.get_status(user_id)
        text = T[lang]["main_title"].format(name=name, status=status, balance=balance)
        await bot.send_message(
            user_id,
            text,
            reply_markup=main_menu_keyboard(
                lang,
                is_admin=user_id == ADMIN_ID,
                show_purchase=status != FULL_STATUS,
            ),
        )


if __name__ == "__main__":
    async def on_startup(dp: Dispatcher):
        app = web.Application()
        app.router.add_post("/nowpayments", ipn_handler)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 5000)
        await site.start()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



# === Feature Config Handlers (admin) ===
from aiogram import types
from aiogram.dispatcher.filters import Command
from .config import ADMIN_ID
from .config_manager import ensure_config, toggle as cfg_toggle

FEATURES = [("broadcasting","Broadcasting"), ("leveling","Leveling"), ("blackjack","Blackjack"), ("assistants","Assistants")]

def _features_kb(state: dict):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=1)
    feats = state.get("features", {})
    for fid, title in FEATURES:
        val = "Enabled" if feats.get(fid, False) else "Disabled"
        kb.add(InlineKeyboardButton(f"{title}: {val}", callback_data=f"cfg:toggle:{fid}"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="cfg:back"))
    return kb

@dp.message_handler(Command("config"))
async def cmd_config(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        return await message.answer("Config is admin-only.")
    state = ensure_config()
    await message.answer("⚙️ Feature Toggles", reply_markup=_features_kb(state))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cfg:toggle:"))
async def cb_cfg_toggle(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    fid = call.data.split(":", 2)[2]
    state = cfg_toggle(fid)
    await call.message.edit_reply_markup(reply_markup=_features_kb(state))
    await call.answer("Toggled.")

@dp.callback_query_handler(lambda c: c.data == "cfg:back")
async def cb_cfg_back(call: types.CallbackQuery):
    await call.message.delete()



# === Multi-tenant Feature Config (admin) ===
from aiogram import types
from aiogram.dispatcher.filters import Command
from .config import ADMIN_ID
from .config_manager import tenants as cfg_tenants, ensure_config_for as cfg_ensure, toggle as cfg_toggle

FEATURES = [("broadcasting","Broadcasting"), ("leveling","Leveling"), ("blackjack","Blackjack"), ("assistants","Assistants")]

def _tenants_kb():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=1)
    ts = cfg_tenants()
    if not ts:
        kb.add(InlineKeyboardButton("No tenants configured", callback_data="cfg:none"))
    for t in ts:
        label = f"🧑‍💼 {t.get('name','Unnamed')} ({t.get('id')})"
        kb.add(InlineKeyboardButton(label, callback_data=f"cfg:tenant:{t.get('id')}"))
    return kb

def _features_kb(state: dict, tenant_id: str):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=1)
    feats = state.get("features", {})
    for fid, title in FEATURES:
        val = "Enabled" if feats.get(fid, False) else "Disabled"
        kb.add(InlineKeyboardButton(f"{title}: {val}", callback_data=f"cfg:toggle:{tenant_id}:{fid}"))
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="cfg:back"))
    return kb

@dp.message_handler(Command("config"))
async def cmd_config(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        return await message.answer("Config is admin-only.")
    await message.answer("⚙️ Choose a tenant", reply_markup=_tenants_kb())

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cfg:tenant:"))
async def cb_cfg_tenant(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    tenant_id = call.data.split(":", 2)[2]
    state = cfg_ensure(tenant_id)
    await call.message.edit_text(f"⚙️ Feature Toggles for {tenant_id}", reply_markup=_features_kb(state, tenant_id))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cfg:toggle:"))
async def cb_cfg_toggle(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    _, _, tenant_id, fid = call.data.split(":", 3)
    state = cfg_toggle(tenant_id, fid)
    await call.message.edit_reply_markup(reply_markup=_features_kb(state, tenant_id))
    await call.answer("Toggled.")

@dp.callback_query_handler(lambda c: c.data == "cfg:back")
async def cb_cfg_back(call: types.CallbackQuery):
    await call.message.edit_text("⚙️ Choose a tenant", reply_markup=_tenants_kb())



# === Admin: Assign Customer to Telegram Username ===
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .config_manager import tenants as cfg_tenants, set_tenants as cfg_set_tenants

class AssignStates(StatesGroup):
    waiting_for_mapping = State()

@dp.callback_query_handler(lambda c: c.data == "admin:assign_customer")
async def cb_admin_assign(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    await state.set_state(AssignStates.waiting_for_mapping.state)
    await call.message.edit_text("Send mapping in format:\n<tenant_id> | @username\nExample: customer1 | @john")

@dp.message_handler(state=AssignStates.waiting_for_mapping)
async def assign_mapping(message: types.Message, state: FSMContext):
    if str(message.from_user.id) != str(ADMIN_ID):
        return
    text = message.text.strip()
    if "|" not in text:
        return await message.answer("Use format: tenant_id | @username")
    tenant_id, username = [x.strip() for x in text.split("|",1)]
    username = username.lstrip("@")
    ts = cfg_tenants()
    # find tenant or create new entry
    found = False
    for t in ts:
        if t.get("id")==tenant_id:
            t["tg_username"] = username
            found = True
            break
    if not found:
        ts.append({"id": tenant_id, "name": tenant_id, "tg_username": username, "config_path": ""})
    cfg_set_tenants(ts)
    await state.finish()
    await message.answer(f"Mapped @{username} → {tenant_id} ✅")

# === Functions Menu (same toggles UI) ===
FEATURES = [("broadcasting","Broadcasting"), ("leveling","Leveling"), ("blackjack","Blackjack"), ("assistants","Assistants")]

def _features_onoff_kb(state: dict, tenant_id: str):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=2)
    feats = state.get("features", {})
    for fid, title in FEATURES:
        is_on = feats.get(fid, False)
        kb.add(
            InlineKeyboardButton(f"{title} · {'ON' if is_on else 'OFF'}", callback_data="cfg:none"),
            InlineKeyboardButton("Turn Off" if is_on else "Turn On", callback_data=f"cfg:set:{tenant_id}:{fid}:{'off' if is_on else 'on'}")
        )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="cfg:back"))
    return kb

@dp.callback_query_handler(lambda c: c.data == "menu:functions")
async def cb_menu_functions(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Admin-only.", show_alert=True)
    # if username was assigned to a tenant, try to pick by username; else show tenant list
    ts = cfg_tenants()
    # Build a menu of tenants
    await call.message.edit_text("⚙️ Choose a tenant for Functions", reply_markup=_tenants_kb())

@dp.callback_query_handler(lambda c: c.data.startswith("cfg:set:"))
async def cb_cfg_set(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    _, _, tenant_id, fid, mode = call.data.split(":",4)
    state = cfg_ensure(tenant_id)
    # set explicit on/off
    cur = state["features"].get(fid, False)
    new = True if mode=="on" else False
    if cur != new:
        # emulate toggle until we add dedicated setter
        from .config_manager import toggle as _toggle
        # If states differ, ensure ends up desired
        tmp = _toggle(tenant_id, fid)
        if tmp["features"].get(fid, False) != new:
            tmp = _toggle(tenant_id, fid)
        state = tmp
    await call.message.edit_reply_markup(reply_markup=_features_onoff_kb(state, tenant_id))
    await call.answer(f"Set {fid} → {mode.upper()}")



# === Admin Shield: Assign customer → tenant; Functions On/Off ===
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_manager import tenants as cfg_tenants, set_tenants as cfg_set_tenants, ensure_config_for as cfg_ensure, set_feature as cfg_set_feature

FEATURES = [("broadcasting","Broadcasting"), ("leveling","Leveling"), ("blackjack","Blackjack"), ("assistants","Assistants")]

class AssignStates(StatesGroup):
    waiting = State()

def _tenants_kb():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=1)
    ts = cfg_tenants()
    if not ts:
        kb.add(InlineKeyboardButton("No tenants configured", callback_data="cfg:none"))
    for t in ts:
        label = f"🧑‍💼 {t.get('name','Unnamed')} ({t.get('id')})"
        kb.add(InlineKeyboardButton(label, callback_data=f"cfg:tenant:{t.get('id')}"))
    return kb

def _features_onoff_kb(state: dict, tenant_id: str):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=2)
    feats = state.get("features", {})
    for fid, title in FEATURES:
        on = feats.get(fid, False)
        kb.add(
            InlineKeyboardButton(f"{title} · {'ON' if on else 'OFF'}", callback_data="cfg:none"),
            InlineKeyboardButton("Turn Off" if on else "Turn On", callback_data=f"cfg:set:{tenant_id}:{fid}:{'off' if on else 'on'}")
        )
    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="cfg:back"))
    return kb

@dp.message_handler(Command("admin_shield"))
async def cmd_admin_shield(message: types.Message):
    if str(message.from_user.id) != str(ADMIN_ID):
        return await message.answer("Admin only.")
    await message.answer("🛡 Admin Shield\nChoose a tenant or use the panel buttons.", reply_markup=_tenants_kb())

@dp.callback_query_handler(lambda c: c.data == "admin:assign_customer")
async def cb_admin_assign(call: types.CallbackQuery, state: FSMContext):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    await state.set_state(AssignStates.waiting.state)
    await call.message.edit_text("Send mapping:\n<tenant_id> | @username | <config_path>\nExample:\ncustomer1 | @john | C:/path/to/customer1/config.json")

@dp.message_handler(state=AssignStates.waiting)
async def assign_map(message: types.Message, state: FSMContext):
    if str(message.from_user.id) != str(ADMIN_ID):
        return
    parts = [p.strip() for p in message.text.split("|")]
    if len(parts) < 2:
        return await message.answer("Format: tenant_id | @username | optional config_path")
    tenant_id = parts[0]
    username = parts[1].lstrip("@")
    cfg_path = parts[2] if len(parts) > 2 else ""
    ts = cfg_tenants()
    found = False
    for t in ts:
        if t.get("id")==tenant_id:
            t["tg_username"] = username
            if cfg_path: t["config_path"] = cfg_path
            found = True
            break
    if not found:
        ts.append({"id": tenant_id, "name": tenant_id, "tg_username": username, "config_path": cfg_path})
    cfg_set_tenants(ts)
    await state.finish()
    await message.answer(f"Mapped @{username} → {tenant_id} ✅")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cfg:tenant:"))
async def cb_cfg_tenant(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    tenant_id = call.data.split(":", 2)[2]
    state = cfg_ensure(tenant_id)
    await call.message.edit_text(f"⚙️ Functions for {tenant_id}", reply_markup=_features_onoff_kb(state, tenant_id))

@dp.callback_query_handler(lambda c: c.data and c.data.startswith("cfg:set:"))
async def cb_cfg_set(call: types.CallbackQuery):
    if str(call.from_user.id) != str(ADMIN_ID):
        return await call.answer("Not allowed.", show_alert=True)
    _, _, tenant_id, fid, mode = call.data.split(":",4)
    new = True if mode == "on" else False
    state = cfg_set_feature(tenant_id, fid, new)
    await call.message.edit_reply_markup(reply_markup=_features_onoff_kb(state, tenant_id))
    await call.answer(f"{fid} → {'ON' if new else 'OFF'}")
    
@dp.callback_query_handler(lambda c: c.data == "cfg:back")
async def cb_cfg_back(call: types.CallbackQuery):
    await call.message.edit_text("🛡 Admin Shield", reply_markup=_tenants_kb())
