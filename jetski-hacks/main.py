import asyncio

from bot.Bot import Bot


async def main():
    bot = Bot()
    await bot.init()
    input("Press enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
