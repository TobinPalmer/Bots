from bot.Browser import Browser

class Bot:
    def __init__(self):
        self.browser = Browser()

    async def init(self) -> None:
        await self.browser.initialize()
        print(await self.list_games())

    async def list_games(self):
        if await (await self.browser.page.wait_for_selector(".entry.bombparty", timeout=10000)):
            return await self.browser.page.query_selector_all('.entry.bombparty')


async def get_prompt(self) -> str:
    pass
