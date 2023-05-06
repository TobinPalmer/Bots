import asyncio

from bot.Bot import Bot

bot = Bot()


async def main():
    await bot.init()
    input()


if __name__ == "__main__":
    asyncio.run(main())
