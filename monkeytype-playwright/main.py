import asyncio
import os
import time

from dotenv import load_dotenv

from bot.Bot import Bot

load_dotenv()

username = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')

bot = Bot()


async def main():
    await bot.init(username, password)
    await restart_after_hour()


async def restart_after_hour():
    time_then = time.time()
    while True:
        time.sleep(5)
        # if time.time() - time_then > 3600:
        if time.time() - time_then > 5:
            print("Restarting browser...")
            await bot.browser.close()
            await bot.browser.initialize()

            time_then = time.time()


if __name__ == "__main__":
    asyncio.run(main())
