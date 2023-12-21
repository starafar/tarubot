from config import settings
from src.tarubot.core import TaruBot


def main():
    bot = TaruBot()
    bot.run(settings.auth.discord)
