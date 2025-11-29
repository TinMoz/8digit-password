import json
import os
from dataclasses import dataclass
from urllib import request

from dotenv import load_dotenv


@dataclass
class Config:
    db_url: str


DEFAULT_REMOTE_ENV_HOST = "p01--eightdigit--vnwzhrpwlmrg.code.run"


def fetch_remote_db_url(host: str = DEFAULT_REMOTE_ENV_HOST) -> str:
    url = f"https://{host}/env"
    try:
        with request.urlopen(url, timeout=10) as resp:
            payload = json.load(resp)
    except Exception as exc:  # pragma: no cover - network dependent
        raise RuntimeError(f"Failed to fetch DB_URL from remote config server {host}: {exc}") from exc

    db_url = payload.get("DB_URL")
    if not db_url:
        raise RuntimeError(f"Remote config server {host} did not return DB_URL")  # pragma: no cover

    return db_url


def load_config() -> Config:
    load_dotenv()

    db_url = os.getenv("DB_URL")
    if not db_url:
        remote_host = os.getenv("REMOTE_ENV_HOST", DEFAULT_REMOTE_ENV_HOST)
        db_url = fetch_remote_db_url(remote_host)

    if not db_url:
        raise ValueError("DB_URL is not set in .env")

    return Config(db_url=db_url)
