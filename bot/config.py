from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(slots=True)
class Settings:
    bot_token: str
    markup_percent: float
    service_cost: float
    admin_ids: list[int]


def _parse_admin_ids(value: str) -> list[int]:
    if not value.strip():
        return []
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def load_settings() -> Settings:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "")
    if not bot_token:
        raise ValueError("BOT_TOKEN is required in environment")

    return Settings(
        bot_token=bot_token,
        markup_percent=float(os.getenv("MARKUP_PERCENT", "35")),
        service_cost=float(os.getenv("SERVICE_COST", "1500")),
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
    )
