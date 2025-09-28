from typing import Dict

T: Dict[str, Dict[str, str]] = {
    "en": {
        "choose_language": "🌐 *Choose your language:*",
        "main_title": (
            "✨ *Welcome {name}* 👋\n\n"
            "🪪 *Status:* _{status}_\n"
            "🤖 *Bots owned:* _0_\n"
            "💰 *Balance:* _€{balance}_"
        ),
        "menu_purchase": "🛒 Purchase",
        "menu_config": "⚙️ Config",
        "menu_topup": "➕ Top up",
        "menu_support": "🆘 Support",
        "menu_language": "🌐 Language",
        "purchase_title": "🛍️ *Choose a package:*",
        "purchase_template": "📦 Template bot ({price} {cur})",
        "purchase_semi": "⚡ Semi-service bot ({price} {cur})",
        "purchase_full": "🚀 Full-service bot ({price} {cur})",
        "desc_template": (
            "🟢 *Template Bot*\n"
            "A ready-to-use Telegram shop with essential tools:\n"
            "• 🏪 *Products & categories*\n"
            "• 📦 *Orders & inventory*\n"
            "• 🗒 *Discount codes*\n"
            "• 📣 *Mass messaging*\n"
            "• 👥 *User stats & management*\n\n"
            "🕘 *Runs 24/7 with no extra fees* (hosting: 10 EUR/month)."
        ),
        "desc_semi": (
            "🟡 *Semi-Service Bot*\n"
            "• ⚙️ *Real-time feature adjustments*\n"
            "• 🔄 *Regular updates included*\n"
            "• ➕ *Add one new custom feature every month*\n"
            "• 📊 *Advanced shop controls*\n\n"
            "🕘 *Runs 24/7 with no extra fees* (hosting: 10 EUR/month)."
        ),
        "desc_full": (
            "🔵 *Full-Service Bot*\n"
            "• ⚙️ *Change features in real time*\n"
            "• 🔄 *Frequent updates included*\n"
            "• 🎯 *Custom requests by developer - free*\n"
            "• 📊 *Advanced shop controls*\n\n"
            "🕘 *Runs 24/7 with no extra fees* (hosting: 10 EUR/month)."
        ),
        "purchase_hint": "💡 *Tap a package to see details.*",
        "buy": "💳 Purchase",
        "choose_payment": "💰 *Choose payment method:*",
        "invoice_created": "🧾 *Payment Invoice Created*",
        "amount": "Amount",
        "payment_address": "🏦 Payment Address:",
        "expires_at": "⏳ Expires At:",
        "invoice_warning": "⚠️ Payment must be completed within 30 minutes of invoice creation.",
        "invoice_exact": "❗️ Important: Send exactly this amount of {cur}.",
        "invoice_confirm": "✅ Confirmation is automatic via webhook after network confirmation.",
        "enter_topup_amount": "💶 Enter the amount to top up:",
        "invalid_amount": "❌ Invalid amount",
        "pay_with_balance": "💳 Pay with balance",
        "insufficient_balance": "❌ Insufficient balance. Please top up.",
        "purchase_success": "✅ Payment received! Go to *Config* to set up your bot.",
        "purchase_unavailable": "✅ You already own this package or a higher tier.",
        "config_first_time": (
            "🎉 *Welcome to settings!*\n"
            "It's your first time here. Tap *Set Up* below to configure your bot or contact support."
        ),
        "config_title": "⚙️ *Bot settings:*",
        "config_no_status": "🛑 *Purchase a bot to access settings.*",
        "config_setup": "🛠 Set Up",
        "config_rdp": "🖥 RDP",
        "config_functions": "🧩 Functions",
        "config_support": "🆘 Support",
        "functions_title": "🧩 *Choose a function category:*",
        "functions_protection": "🛡 Protection & utilities",
        "functions_admin": "🧑‍💼 Admin-side features",
        "functions_user": "👥 User-side features",
        "functions_payments": "💳 Payments",
        "functions_protection_desc": "🛡 *Protection & utilities*\nPick a tool below to see what it covers.",
        "functions_admin_desc": "🧑‍💼 *Admin-side features*\nTap an option to learn how it helps you run the shop.",
        "functions_user_desc": "👥 *User-side features*\nChoose a feature to see the customer experience upgrades.",
        "functions_payments_desc": (
            "💳 *Payments*\n"
            "Accept secure crypto payments via NOWPayments with automatic confirmations for SOL, USDT-TRC20, and XMR."
        ),
        "feature_anti_spam": "🛡 Anti-spam filter",
        "feature_anti_spam_desc": (
            "🛡 *Anti-spam filter*\n"
            "Automatically blocks suspicious sign-ups, repeated requests, and flood attempts to keep your bot clean."
        ),
        "feature_assistant_management": "🤝 Assistant management",
        "feature_assistant_management_desc": (
            "🤝 *Assistant management*\n"
            "Add or remove assistant accounts, assign roles, and delegate daily operations without sharing your main credentials."
        ),
        "feature_user_levels": "🎚 User levels",
        "feature_user_levels_desc": (
            "🎚 *User levels*\n"
            "Segment shoppers into tiers, unlock special pricing or rewards, and track loyalty progress automatically."
        ),
        "feature_stock_notifications": "🔔 Stock notifications",
        "feature_stock_notifications_desc": (
            "🔔 *Stock notifications*\n"
            "Alert users when items are back in stock or running low so they never miss a drop."
        ),
        "coming_soon": "🚧 *This feature is disabled for now.*",
        "rdp_choose_package": "🖥 *Choose your RDP package:*",
        "rdp_1m": "1️⃣ 1 Month ({price} {cur})",
        "rdp_2m": "2️⃣ 2 Months ({price} {cur})",
        "rdp_3m": "3️⃣ 3 Months ({price} {cur})",
        "rdp_payment_success": "✅ *Payment received!* RDP details will be sent to you soon.",
        "back": "⬅️ Back",
        "cancel": "❌ Cancel",
        "support_button": "💬 Contact Support",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Language changed to *{lang}*.",
        "menu_admin": "🛡 Admin Panel",
        "admin_panel": "🛡 *Admin Panel*",
        "admin_set_online": "Online",
        "admin_set_offline": "Offline",
        "user_lookup": "🔍 User lookup",
        "enter_username": "👤 Enter the user username to view or edit their data",
        "profile": "👤 Profile — {username}",
        "profile_username": "👤 Username — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Role — {role}",
        "profile_regdate": "🕢 Registration date — {date}",
        "profile_balance": "💰 Balance — {balance}",
        "top_up_balance": "Top up user's balance",
        "balance_set": "✅ Balance set to {balance}",
        "user_not_found": "❌ User not found",
        "manage_rdps": "🖥 Manage RDPs",
        "choose_rdp_user": "👤 Choose a user:",
        "enter_rdp_email": "📧 Enter RDP email:",
        "enter_rdp_password": "🔑 Enter email password:",
        "enter_rdp_ip": "🌐 Enter RDP IP:",
        "enter_rdp_name": "👤 Enter RDP name:",
        "enter_rdp_rdp_password": "🔒 Enter RDP password:",
        "enter_rdp_expiry": "📅 Enter expiry date:",
        "rdp_saved": "✅ RDP info saved.",
        "rdp_details": (
            "🖥 *Your RDP:*\n"
            "📧 Email: {email}\n"
            "🔑 Password: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Name: {name}\n"
            "🔒 RDP Password: {rdp_password}\n"
            "⏳ Expires: {expiry}"
        ),
        "extend": "🔄 Extend",
        "no_rdp_users": "❌ No users available",
        "next": "➡️ Next",
        "complete": "✅ Complete",
        "setup_intro": (
            "ℹ️ *To set up the bot you must fill in some details.* "
            "Follow the instructions carefully, otherwise the bot might not work."
        ),
        "setup_create_email": (
            "📧 *Create a new email.* You can use [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) or "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Enter the email you created:*",
        "setup_ngrok_signup": "🌐 *Register at [ngrok](https://dashboard.ngrok.com/signup).* Once registered, go to *Your Authtoken* and press *Copy*. Then press *Next*.",
        "setup_ngrok_token_prompt": "🔐 *Paste the Auth-Token you copied here:*",
        "setup_np_signup": (
            "🧾 *Sign up at [NOWPayments](https://account.nowpayments.io/create-account) with your new email.* "
            "Use the email you created, set a password, then confirm with the code sent to that address."
        ),
        "setup_np_crypto_prompt": "💰 *Enter the crypto address where you want to receive funds:*",
        "setup_np_start_integration": "⚙️ Click *Start integration*, set currency to *EUR*, select *Sender*, then press *Skip for now*.",
        "setup_np_settings": "🛠️ Go to *Settings* → *Payments*, then press *Next*.",
        "setup_np_api_prompt": "🔑 Go to *API keys* and send your API key here.",
        "setup_np_ipn_prompt": "📨 Go to *Instant payment notifications*, generate an IPN secret key and send it here.",
        "setup_getid_prompt": "🆔 *Open @GetIDcnBot, press Start, copy your ID and send it here.*",
        "setup_botfather_intro": "🤖 *Go to @BotFather, type /newbot and follow the instructions.* Then press *Next*.",
        "setup_botfather_token_prompt": "📮 *Copy the API code that is sent.*",
        "setup_cancelled": "❌ *Setup cancelled.*",
        "setup_done": "🎉 *Setup data sent to admin. Thank you!*",
        "setup_done_online": "🎉 Set up is complete, the owner is online your information was sent, and the bot will be turned on soon",
    },
    "ru": {
        "choose_language": "🌐 *Выберите язык:*",
        "main_title": (
            "✨ *Добро пожаловать, {name}* 👋\n\n"
            "🪪 *Статус:* _{status}_\n"
            "🤖 *Ботов куплено:* _0_\n"
            "💰 *Баланс:* _€{balance}_"
        ),
        "menu_purchase": "🛒 Покупка",
        "menu_config": "⚙️ Настройки",
        "menu_topup": "➕ Пополнить",
        "menu_support": "🆘 Поддержка",
        "menu_language": "🌐 Язык",
        "purchase_title": "🛍️ *Выберите пакет:*",
        "purchase_template": "📦 Шаблон-бот ({price} {cur})",
        "purchase_semi": "⚡ Бот с частичным сервисом ({price} {cur})",
        "purchase_full": "🚀 Полный сервис-бот ({price} {cur})",
        "desc_template": (
            "🟢 *Шаблон-бот*\n"
            "Готовый Telegram-магазин с необходимыми инструментами:\n"
            "• 🏪 *Товары и категории*\n"
            "• 📦 *Заказы и остатки*\n"
            "• 🗒 *Промокоды*\n"
            "• 📣 *Рассылки*\n"
            "• 👥 *Статистика и управление пользователями*\n\n"
            "🕘 *Работает 24/7 без доп. оплат* (хостинг: 10 EUR/мес)."
        ),
        "desc_semi": (
            "🟡 *Бот с частичным сервисом*\n"
            "• ⚙️ *Меняйте функции в реальном времени*\n"
            "• 🔄 *Регулярные обновления включены*\n"
            "• ➕ *Добавление одной новой функции каждый месяц*\n"
            "• 📊 *Расширенные инструменты управления*\n\n"
            "🕘 *Работает 24/7 без доп. оплат* (хостинг: 10 EUR/мес)."
        ),
        "desc_full": (
            "🔵 *Премиум-бот (полный сервис)*\n"
            "• ⚙️ *Меняйте функции в реальном времени*\n"
            "• 🔄 *Частые обновления включены*\n"
            "• 🎯 *Индивидуальные запросы - бесплатно*\n"
            "• 📊 *Расширенные инструменты управления*\n\n"
            "🕘 *Работает 24/7 без доп. оплат* (хостинг: 10 EUR/мес)."
        ),
        "purchase_hint": "💡 *Нажмите на пакет, чтобы увидеть детали.*",
        "buy": "💳 Купить",
        "choose_payment": "💰 *Выберите способ оплаты:*",
        "invoice_created": "🧾 *Счёт на оплату создан*",
        "amount": "Сумма",
        "payment_address": "🏦 Платёжный адрес:",
        "expires_at": "⏳ Истекает в:",
        "invoice_warning": "⚠️ Оплата должна быть завершена в течение 30 минут после создания счёта.",
        "invoice_exact": "❗️ Важно: Отправьте ровно эту сумму {cur}.",
        "invoice_confirm": "✅ Подтверждение происходит автоматически через вебхук после подтверждения сети.",
        "enter_topup_amount": "💶 Введите сумму пополнения:",
        "invalid_amount": "❌ Неверная сумма",
        "pay_with_balance": "💳 Оплатить с баланса",
        "insufficient_balance": "❌ Недостаточно средств. Пополните баланс.",
        "purchase_success": "✅ Оплата получена! Перейдите в *Настройки*, чтобы настроить бота.",
        "purchase_unavailable": "✅ Этот пакет уже приобретён или у вас есть более высокий уровень.",
        "config_first_time": (
            "🎉 *Добро пожаловать в настройки!*\n"
            "Вы здесь впервые. Нажмите *Настроить*, чтобы сконфигурировать бота или обратитесь в поддержку."
        ),
        "config_title": "⚙️ *Настройки бота:*",
        "config_no_status": "🛑 *Чтобы получить доступ к настройкам, сначала приобретите бота.*",
        "config_setup": "🛠 Настроить",
        "config_rdp": "🖥 RDP",
        "config_functions": "🧩 Функции",
        "config_support": "🆘 Поддержка",
        "functions_title": "🧩 *Выберите категорию функций:*",
        "functions_protection": "🛡 Защита и утилиты",
        "functions_admin": "🧑‍💼 Функции для админа",
        "functions_user": "👥 Функции для пользователей",
        "functions_payments": "💳 Платежи",
        "functions_protection_desc": "🛡 *Защита и утилиты*\nВыберите инструмент ниже, чтобы узнать подробности.",
        "functions_admin_desc": (
            "🧑‍💼 *Функции для админа*\n"
            "Нажмите на пункт, чтобы узнать, как он помогает управлять магазином."
        ),
        "functions_user_desc": (
            "👥 *Функции для пользователей*\n"
            "Выберите функцию, чтобы увидеть улучшения для клиентов."
        ),
        "functions_payments_desc": (
            "💳 *Платежи*\n"
            "Принимайте безопасные криптоплатежи через NOWPayments с авто-подтверждением для SOL, USDT-TRC20 и XMR."
        ),
        "feature_anti_spam": "🛡 Антиспам-фильтр",
        "feature_anti_spam_desc": (
            "🛡 *Антиспам-фильтр*\n"
            "Автоматически блокирует подозрительные регистрации, повторные запросы и флуд, чтобы бот оставался чистым."
        ),
        "feature_assistant_management": "🤝 Управление ассистентами",
        "feature_assistant_management_desc": (
            "🤝 *Управление ассистентами*\n"
            "Добавляйте или удаляйте аккаунты помощников, назначайте роли и делегируйте задачи без передачи основных данных."
        ),
        "feature_user_levels": "🎚 Уровни пользователей",
        "feature_user_levels_desc": (
            "🎚 *Уровни пользователей*\n"
            "Разделяйте покупателей на уровни, открывайте специальные цены и автоматически отслеживайте лояльность."
        ),
        "feature_stock_notifications": "🔔 Уведомления о наличии",
        "feature_stock_notifications_desc": (
            "🔔 *Уведомления о наличии*\n"
            "Сообщайте пользователям, когда товары появляются снова или заканчиваются, чтобы они не пропускали новинки."
        ),
        "coming_soon": "🚧 *Эта функция отключена.*",
        "rdp_choose_package": "🖥 *Выберите пакет RDP:*",
        "rdp_1m": "1️⃣ 1 месяц ({price} {cur})",
        "rdp_2m": "2️⃣ 2 месяца ({price} {cur})",
        "rdp_3m": "3️⃣ 3 месяца ({price} {cur})",
        "rdp_payment_success": "✅ *Оплата получена!* Данные RDP будут отправлены вам вскоре.",
        "back": "⬅️ Назад",
        "cancel": "❌ Отменить",
        "support_button": "💬 Связаться с поддержкой",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Язык изменён на *{lang}*.",
        "menu_admin": "🛡 Панель админа",
        "admin_panel": "🛡 *Панель администратора*",
        "admin_set_online": "Онлайн",
        "admin_set_offline": "Оффлайн",
        "user_lookup": "🔍 Поиск пользователя",
        "enter_username": "👤 Введите имя пользователя для просмотра или редактирования данных",
        "profile": "👤 Профиль — {username}",
        "profile_username": "👤 Имя пользователя — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Роль — {role}",
        "profile_regdate": "🕢 Дата регистрации — {date}",
        "profile_balance": "💰 Баланс — {balance}",
        "top_up_balance": "Пополнить баланс пользователя",
        "balance_set": "✅ Баланс установлен на {balance}",
        "user_not_found": "❌ Пользователь не найден",
        "manage_rdps": "🖥 Управление RDP",
        "choose_rdp_user": "👤 Выберите пользователя:",
        "enter_rdp_email": "📧 Введите RDP email:",
        "enter_rdp_password": "🔑 Введите пароль от email:",
        "enter_rdp_ip": "🌐 Введите IP RDP:",
        "enter_rdp_name": "👤 Введите имя RDP:",
        "enter_rdp_rdp_password": "🔒 Введите пароль RDP:",
        "enter_rdp_expiry": "📅 Введите дату окончания:",
        "rdp_saved": "✅ Данные RDP сохранены.",
        "rdp_details": (
            "🖥 *Ваш RDP:*\n"
            "📧 Email: {email}\n"
            "🔑 Пароль: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Имя: {name}\n"
            "🔒 Пароль RDP: {rdp_password}\n"
            "⏳ Истекает: {expiry}"
        ),
        "extend": "🔄 Продлить",
        "no_rdp_users": "❌ Пользователи отсутствуют",
        "next": "➡️ Далее",
        "complete": "✅ Готово",
        "setup_intro": (
            "ℹ️ *Для настройки бота необходимо заполнить данные.* "
            "Следуйте инструкциям тщательно, иначе бот может не работать."
        ),
        "setup_create_email": (
            "📧 *Создайте новый email.* Можно использовать [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) или "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Введите созданный email:*",
        "setup_ngrok_signup": "🌐 *Зарегистрируйтесь на [ngrok](https://dashboard.ngrok.com/signup).* После регистрации перейдите в *Your Authtoken* и нажмите *Copy*. Затем нажмите *Далее*.",
        "setup_ngrok_token_prompt": "🔐 *Вставьте скопированный Auth-Token сюда:*",
        "setup_np_signup": (
            "🧾 *Зарегистрируйтесь в [NOWPayments](https://account.nowpayments.io/create-account) с новым email.* "
            "Введите созданный адрес, придумайте пароль и подтвердите регистрацию кодом, отправленным на этот же email."
        ),
        "setup_np_crypto_prompt": "💰 *Введите крипто адрес, на который хотите получать средства:*",
        "setup_np_start_integration": "⚙️ Нажмите *Start integration*, установите валюту *EUR*, выберите *Sender* и нажмите *Skip for now*.",
        "setup_np_settings": "🛠️ Перейдите в *Settings* → *Payments*, затем нажмите *Далее*.",
        "setup_np_api_prompt": "🔑 Откройте *API keys* и отправьте сюда свой API ключ.",
        "setup_np_ipn_prompt": "📨 Перейдите в *Instant payment notifications*, сгенерируйте IPN secret key и отправьте его здесь.",
        "setup_getid_prompt": "🆔 *Откройте @GetIDcnBot, нажмите Start, скопируйте свой ID и отправьте здесь.*",
        "setup_botfather_intro": "🤖 *Откройте @BotFather, отправьте /newbot и следуйте инструкциям.* Затем нажмите *Далее*.",
        "setup_botfather_token_prompt": "📮 *Скопируйте отправленный API код.*",
        "setup_cancelled": "❌ *Настройка отменена.*",
        "setup_done": "🎉 *Данные отправлены администратору. Спасибо!*",
        "setup_done_online": "🎉 Настройка завершена, владелец в сети, ваша информация отправлена, бот скоро будет включён",
    },
    "lt": {
        "choose_language": "🌐 *Pasirinkite kalbą:*",
        "main_title": (
            "✨ *Sveikas, {name}* 👋\n\n"
            "🪪 *Statusas:* _{status}_\n"
            "🤖 *Turimų botų:* _0_\n"
            "💰 *Balansas:* _€{balance}_"
        ),
        "menu_purchase": "🛒 Pirkti",
        "menu_config": "⚙️ Nustatymai",
        "menu_topup": "➕ Papildyti",
        "menu_support": "🆘 Pagalba",
        "menu_language": "🌐 Kalba",
        "purchase_title": "🛍️ *Pasirinkite paketą:*",
        "purchase_template": "📦 Šabloninis botas ({price} {cur})",
        "purchase_semi": "⚡ Dalinio aptarnavimo botas ({price} {cur})",
        "purchase_full": "🚀 Pilno aptarnavimo botas ({price} {cur})",
        "desc_template": (
            "🟢 *Šabloninis botas*\n"
            "Paruoštas Telegram parduotuvės botas su svarbiausiais įrankiais:\n"
            "• 🏪 *Prekės ir kategorijos*\n"
            "• 📦 *Užsakymai ir atsargos*\n"
            "• 🗒 *Nuolaidų kodai*\n"
            "• 📣 *Masiniai pranešimai*\n"
            "• 👥 *Vartotojų statistika ir valdymas*\n\n"
            "🕘 *Veikia 24/7 be papildomų mokesčių* (hostingas: 10 EUR/mėn)."
        ),
        "desc_semi": (
            "🟡 *Dalinio aptarnavimo botas*\n"
            "• ⚙️ *Keiskite funkcijas realiu laiku*\n"
            "• 🔄 *Reguliarūs atnaujinimai įskaičiuoti*\n"
            "• ➕ *Kiekvieną mėnesį pridėkite po vieną naują funkciją*\n"
            "• 📊 *Pažangūs parduotuvės įrankiai*\n\n"
            "🕘 *Veikia 24/7 be papildomų mokesčių* (hostingas: 10 EUR/mėn)."
        ),
        "desc_full": (
            "🔵 *Pilno aptarnavimo botas*\n"
            "• ⚙️ *Keiskite funkcijas realiu laiku*\n"
            "• 🔄 *Dažni atnaujinimai įskaičiuoti*\n"
            "• 🎯 *Asmeniniai programuotojo prašymai - nemokamai*\n"
            "• 📊 *Pažangūs parduotuvės įrankiai*\n\n"
            "🕘 *Veikia 24/7 be papildomų mokesčių* (hostingas: 10 EUR/mėn)."
        ),
        "purchase_hint": "💡 *Paspauskite paketą, kad pamatytumėte detales.*",
        "buy": "💳 Pirkti",
        "choose_payment": "💰 *Pasirinkite mokėjimo metodą:*",
        "invoice_created": "🧾 *Sąskaita sukurta*",
        "amount": "Suma",
        "payment_address": "🏦 Mokėjimo adresas:",
        "expires_at": "⏳ Galioja iki:",
        "invoice_warning": "⚠️ Mokėjimą būtina atlikti per 30 minučių nuo sąskaitos sukūrimo.",
        "invoice_exact": "❗️ Svarbu: Siųskite tiksliai tokią {cur} sumą.",
        "invoice_confirm": "✅ Patvirtinimas automatinis per webhook'ą po tinklo patvirtinimo.",
        "enter_topup_amount": "💶 Įveskite papildymo sumą:",
        "invalid_amount": "❌ Neteisinga suma",
        "pay_with_balance": "💳 Mokėti iš balanso",
        "insufficient_balance": "❌ Nepakanka lėšų. Papildykite balansą.",
        "purchase_success": "✅ Mokėjimas gautas! Eikite į *Nustatymai* ir sukonfigūruokite botą.",
        "purchase_unavailable": "✅ Jūs jau turite šį paketą arba aukštesnį lygį.",
        "config_first_time": (
            "🎉 *Sveiki atvykę į nustatymus!*\n"
            "Jūs čia pirmą kartą. Paspauskite *Nustatyti*, kad sukonfigūruotumėte botą arba susisiekite su pagalba."
        ),
        "config_title": "⚙️ *Boto nustatymai:*",
        "config_no_status": "🛑 *Norėdami pasiekti nustatymus, pirmiausia įsigykite botą.*",
        "config_setup": "🛠 Nustatyti",
        "config_rdp": "🖥 RDP",
        "config_functions": "🧩 Funkcijos",
        "config_support": "🆘 Pagalba",
        "functions_title": "🧩 *Pasirinkite funkcijų kategoriją:*",
        "functions_protection": "🛡 Apsauga ir įrankiai",
        "functions_admin": "🧑‍💼 Administratoriaus funkcijos",
        "functions_user": "👥 Vartotojo funkcijos",
        "functions_payments": "💳 Mokėjimai",
        "functions_protection_desc": "🛡 *Apsauga ir įrankiai*\nPasirinkite įrankį ir sužinokite daugiau.",
        "functions_admin_desc": (
            "🧑‍💼 *Administratoriaus funkcijos*\n"
            "Bakstelėkite punktą ir sužinokite, kaip jis padeda valdyti parduotuvę."
        ),
        "functions_user_desc": (
            "👥 *Vartotojo funkcijos*\n"
            "Pasirinkite funkciją ir pažiūrėkite, kokią patirtį gauna klientai."
        ),
        "functions_payments_desc": (
            "💳 *Mokėjimai*\n"
            "Priimkite saugius kriptomokėjimus per NOWPayments su automatiniu SOL, USDT-TRC20 ir XMR patvirtinimu."
        ),
        "feature_anti_spam": "🛡 Anti-spamo filtras",
        "feature_anti_spam_desc": (
            "🛡 *Anti-spamo filtras*\n"
            "Automatiškai blokuoja įtartinus prisijungimus, pasikartojančias užklausas ir flood'ą, kad bot'as liktų švarus."
        ),
        "feature_assistant_management": "🤝 Asistentų valdymas",
        "feature_assistant_management_desc": (
            "🤝 *Asistentų valdymas*\n"
            "Pridėkite ar pašalinkite asistentų paskyras, priskirkite roles ir deleguokite darbus neatskleisdami pagrindinių prisijungimų."
        ),
        "feature_user_levels": "🎚 Vartotojų lygiai",
        "feature_user_levels_desc": (
            "🎚 *Vartotojų lygiai*\n"
            "Skirstykite pirkėjus į lygius, suteikite specialias kainas ir automatiškai sekite lojalumą."
        ),
        "feature_stock_notifications": "🔔 Atsargų pranešimai",
        "feature_stock_notifications_desc": (
            "🔔 *Atsargų pranešimai*\n"
            "Praneškite vartotojams, kai prekės grįžta į sandėlį arba baigiasi, kad jie nepraleistų pasiūlymų."
        ),
        "coming_soon": "🚧 *Ši funkcija išjungta.*",
        "rdp_choose_package": "🖥 *Pasirinkite RDP paketą:*",
        "rdp_1m": "1️⃣ 1 mėn. ({price} {cur})",
        "rdp_2m": "2️⃣ 2 mėn. ({price} {cur})",
        "rdp_3m": "3️⃣ 3 mėn. ({price} {cur})",
        "rdp_payment_success": "✅ *Mokėjimas gautas!* RDP informacija bus atsiųsta netrukus.",
        "back": "⬅️ Atgal",
        "cancel": "❌ Atšaukti",
        "support_button": "💬 Susisiekti su pagalba",
        "lang_en": "English",
        "lang_ru": "Русский",
        "lang_lt": "Lietuvių",
        "language_changed": "✅ Kalba pakeista į *{lang}*.",
        "menu_admin": "🛡 Admin skydelis",
        "admin_panel": "🛡 *Administratoriaus skydelis*",
        "admin_set_online": "Prisijungęs",
        "admin_set_offline": "Atsijungęs",
        "user_lookup": "🔍 Vartotojo paieška",
        "enter_username": "👤 Įveskite vartotojo naudotojo vardą peržiūrėti ar redaguoti duomenis",
        "profile": "👤 Profilis — {username}",
        "profile_username": "👤 Naudotojo vardas — @{username}",
        "profile_id": "🆔 ID — {user_id}",
        "profile_role": "🎛 Rolė — {role}",
        "profile_regdate": "🕢 Registracijos data — {date}",
        "profile_balance": "💰 Balansas — {balance}",
        "top_up_balance": "Papildyti naudotojo balansą",
        "balance_set": "✅ Balansas nustatytas į {balance}",
        "user_not_found": "❌ Vartotojas nerastas",
        "manage_rdps": "🖥 RDP valdymas",
        "choose_rdp_user": "👤 Pasirinkite vartotoją:",
        "enter_rdp_email": "📧 Įveskite RDP el. paštą:",
        "enter_rdp_password": "🔑 Įveskite el. pašto slaptažodį:",
        "enter_rdp_ip": "🌐 Įveskite RDP IP:",
        "enter_rdp_name": "👤 Įveskite RDP vardą:",
        "enter_rdp_rdp_password": "🔒 Įveskite RDP slaptažodį:",
        "enter_rdp_expiry": "📅 Įveskite galiojimo datą:",
        "rdp_saved": "✅ RDP informacija išsaugota.",
        "rdp_details": (
            "🖥 *Jūsų RDP:*\n"
            "📧 El. paštas: {email}\n"
            "🔑 Slaptažodis: {password}\n"
            "🌐 IP: {ip}\n"
            "👤 Vardas: {name}\n"
            "🔒 RDP slaptažodis: {rdp_password}\n"
            "⏳ Galioja iki: {expiry}"
        ),
        "extend": "🔄 Pratęsti",
        "no_rdp_users": "❌ Nėra vartotojų",
        "next": "➡️ Toliau",
        "complete": "✅ Baigti",
        "setup_intro": (
            "ℹ️ *Norint sukonfigūruoti botą, reikia užpildyti keletą duomenų.* "
            "Laikykitės instrukcijų, kitaip botas gali neveikti."
        ),
        "setup_create_email": (
            "📧 *Sukurkite naują el. paštą.* Galite naudoti [inbox.lv](https://login.inbox.lv/signup?redirect_url=https://www.inbox.lv/), "
            "[inbox.lt](https://login.inbox.lt/signup?redirect_url=https://www.inbox.lt/) arba "
            "[gmail.com](https://support.google.com/mail/answer/56256?hl=en)."
        ),
        "setup_enter_email": "✉️ *Įveskite sukurtą el. paštą:*",
        "setup_ngrok_signup": "🌐 *Užsiregistruokite [ngrok](https://dashboard.ngrok.com/signup).* Užsiregistravę eikite į *Your Authtoken* ir paspauskite *Copy*. Tada spauskite *Toliau*.",
        "setup_ngrok_token_prompt": "🔐 *Įklijuokite nukopijuotą Auth-Token čia:*",
        "setup_np_signup": (
            "🧾 *Užsiregistruokite [NOWPayments](https://account.nowpayments.io/create-account) su nauju el. paštu.* "
            "Įveskite sukurtą adresą, susikurkite slaptažodį ir registraciją patvirtinkite kodu, išsiųstu į tą patį el. paštą."
        ),
        "setup_np_crypto_prompt": "💰 *Įveskite kripto adresą, į kurį norite gauti lėšas:*",
        "setup_np_start_integration": "⚙️ Paspauskite *Start integration*, nustatykite valiutą į *EUR*, pasirinkite *Sender* ir spauskite *Skip for now*.",
        "setup_np_settings": "🛠️ Eikite į *Settings* → *Payments* ir spauskite *Toliau*.",
        "setup_np_api_prompt": "🔑 Atsidarykite *API keys* ir atsiųskite čia savo API raktą.",
        "setup_np_ipn_prompt": "📨 Eikite į *Instant payment notifications*, sugeneruokite IPN slaptą raktą ir atsiųskite jį čia.",
        "setup_getid_prompt": "🆔 *Atidarykite @GetIDcnBot, paspauskite Start, nukopijuokite savo ID ir atsiųskite čia.*",
        "setup_botfather_intro": "🤖 *Atidarykite @BotFather, įrašykite /newbot ir sekite instrukcijas.* Tada paspauskite *Next*.",
        "setup_botfather_token_prompt": "📮 *Nukopijuokite atsiųstą API kodą.*",
        "setup_cancelled": "❌ *Nustatymai atšaukti.*",
        "setup_done": "🎉 *Duomenys išsiųsti administratoriui. Ačiū!*",
        "setup_done_online": "🎉 Nustatymas baigtas, savininkas prisijungęs, jūsų informacija išsiųsta ir botas netrukus bus įjungtas",
    },
}
