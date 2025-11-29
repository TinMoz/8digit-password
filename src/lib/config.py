import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    db_url: str


def load_config() -> Config:
    load_dotenv()

    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("DB_URL is not set in .env")

    return Config(db_url=db_url)
