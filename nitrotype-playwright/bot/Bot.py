import time

import pyautogui

from bot.Browser import Browser


class Bot:
    def __init__(self):
        self.browser = Browser()
        self.sentences = []

    async def init(self, username: str, password: str) -> None:
        await self.browser.initialize()
        await self._sign_in(username, password)

    async def get_prompt(self) -> str:
        text_wrapper = (await self.browser.page.wait_for_selector(".dash-copyContainer", timeout=120_000))
        words = await text_wrapper.query_selector_all('.dash-word')
        sentence = ""

        for word in words:
            sentence += await word.inner_text() + " "

        return sentence

    async def _start_race(self) -> None:
        await self.browser.page.goto("https://www.nitrotype.com/race")

    async def _sign_in(self, username: str, password: str) -> None:
        try:
            await (await self.browser.page.wait_for_selector("#username", timeout=5000)).fill(username)
            await (await self.browser.page.wait_for_selector("#password")).fill(password)
            await (await self.browser.page.wait_for_selector("button[type='submit']")).click()

        except TimeoutError as err:
            print(f"Timed Out: {err}")

        finally:
            time.sleep(1.5)
            await self._start_race()
            await self._start_typing()
            await self._anti_fuckup(username, password)

    async def _start_typing(self) -> None:
        try:
            while True:
                time.sleep(0.5)
                prompt = (await self.get_prompt())[0].upper() + (await self.get_prompt())[1:]
                if await (
                        await self.browser.page.wait_for_selector(".dash-pos > .tsxxl.mbf.tlh-1")).inner_text() != "1":
                    pyautogui.press('shift')
                    pyautogui.write(prompt, interval=0)

                    await self._next_game()

        except TimeoutError as err:
            print(f"Timed Out: {err}")

    async def close_modal(self) -> None:
        try:
            await (await self.browser.page.wait_for_selector(".modal-close")).click()

        except TimeoutError as err:
            print(f"Timed Out: {err}")

    async def _anti_fuckup(self, username: str, password: str) -> None:
        """
        Avoids common bloat that gets in the way of the bot.
        """
        try:
            while True:
                time.sleep(0.5)
                if await self.browser.page.is_visible(".modal-close"):
                    time.sleep(2)
                    await self.close_modal()

                if await self.browser.page.is_visible("#username"):
                    await self._sign_in(username, password)

        except TimeoutError as err:
            print(f"Timed Out: {err}")

    # noinspection PyBroadException
    async def _next_game(self) -> None:
        try:
            time.sleep(5)
            await self.browser.page.reload()

        except Exception as err:
            print(f"Error, maybe lost connection with the browser: {err}")
