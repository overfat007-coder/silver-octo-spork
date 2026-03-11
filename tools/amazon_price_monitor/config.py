import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MonitorConfig:
    check_interval_minutes: int
    target_price: float
    telegram_bot_token: str
    telegram_chat_id: str
    request_timeout_s: int = 20
    user_agents: list[str] | None = None
    proxies: list[str] | None = None
    dynamic_enabled: bool = True


DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]


def load_config(path: str) -> MonitorConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return MonitorConfig(
        check_interval_minutes=int(data["check_interval_minutes"]),
        target_price=float(data["target_price"]),
        telegram_bot_token=str(data["telegram_bot_token"]),
        telegram_chat_id=str(data["telegram_chat_id"]),
        request_timeout_s=int(data.get("request_timeout_s", 20)),
        user_agents=list(data.get("user_agents") or DEFAULT_USER_AGENTS),
        proxies=list(data.get("proxies") or []),
        dynamic_enabled=bool(data.get("dynamic_enabled", True)),
    )


def load_urls(path: str) -> list[str]:
    lines = [ln.strip() for ln in Path(path).read_text(encoding="utf-8").splitlines()]
    return [ln for ln in lines if ln and not ln.startswith("#")]
