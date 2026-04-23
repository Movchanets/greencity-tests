import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Config:
    BASE_UI_URL = os.getenv("BASE_UI_URL", "https://www.greencity.cx.ua/#/greenCity/events")
    IMPLICIT_WAIT_TIMEOUT = int(os.getenv("IMPLICIT_WAIT_TIMEOUT", "3"))
    EXPLICIT_WAIT_TIMEOUT = int(os.getenv("EXPLICIT_WAIT_TIMEOUT", "15"))
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    USER_NAME = os.getenv("USER_NAME")
    BROWSER_LANG = os.getenv("BROWSER_LANG", "uk-UA")
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "False").lower() in ("true", "1", "t")
