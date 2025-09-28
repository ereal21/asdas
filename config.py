
import os
from dotenv import load_dotenv

# Load .env files
load_dotenv()
load_dotenv("steps.env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "Inereal").lstrip("@")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "EUR")
DB_PATH = os.getenv("DB_PATH", "bot.db")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# NowPayments configuration
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY", "").strip()
NOWPAYMENTS_IPN_URL = os.getenv("NOWPAYMENTS_IPN_URL", "").strip()
NOWPAYMENTS_API_URL = os.getenv("NOWPAYMENTS_API_URL", "https://api.nowpayments.io/v1").rstrip("/")

# Setup step media files (images or videos)
STEP1_IMAGE = os.getenv("STEP1_IMAGE", "").strip()
STEP2_IMAGE = os.getenv("STEP2_IMAGE", "").strip()
STEP3_IMAGE = os.getenv("STEP3_IMAGE", "").strip()
STEP4_IMAGE = os.getenv("STEP4_IMAGE", "").strip()
STEP5_IMAGE = os.getenv("STEP5_IMAGE", "").strip()
STEP6_IMAGE = os.getenv("STEP6_IMAGE", "").strip()
STEP7_IMAGE = os.getenv("STEP7_IMAGE", "").strip()

# Package prices in DEFAULT_CURRENCY
PACKAGES = {
    "template": 300,
    "semi": 500,
    "full": 800,
}

# Package ordering and status mapping
PACKAGE_ORDER = ["template", "semi", "full"]
PACKAGE_STATUSES = {
    "template": "Middle Tier",
    "semi": "Semi Tier",
    "full": "High Tier",
}
STATUS_TO_PACKAGE = {status: package for package, status in PACKAGE_STATUSES.items()}

# Upgrade price differences between tiers
UPGRADE_PRICES = {
    ("template", "semi"): PACKAGES["semi"] - PACKAGES["template"],
    ("template", "full"): PACKAGES["full"] - PACKAGES["template"],
    ("semi", "full"): PACKAGES["full"] - PACKAGES["semi"],
}


def get_package_price(item: str, status: str) -> float:
    """Return the payable amount for a package based on current status."""

    if item not in PACKAGES:
        raise KeyError(f"Unknown package: {item}")

    current_package = STATUS_TO_PACKAGE.get(status)
    if not current_package:
        return PACKAGES[item]

    try:
        current_index = PACKAGE_ORDER.index(current_package)
        target_index = PACKAGE_ORDER.index(item)
    except ValueError:
        return PACKAGES[item]

    if target_index > current_index:
        return UPGRADE_PRICES.get((current_package, item), PACKAGES[item])

    raise ValueError("Package not available for the current status")

# RDP package prices in DEFAULT_CURRENCY
RDP_PACKAGES = {
    "rdp1": 10,
    "rdp2": 20,
    "rdp3": 30,
}

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Put it in your .env file.")
