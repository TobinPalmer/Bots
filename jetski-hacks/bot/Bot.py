import time

from bot.Browser import Browser


class Bot:
    def __init__(self):
        self.browser = Browser()

    async def init(self) -> None:
        await self.browser.initialize()

        time.sleep(15)
        await self.start_winning()

    async def start_winning(self) -> None:
        frame = await (await self.browser.page.wait_for_selector('iframe')).content_frame()
        question = await frame.wait_for_selector('rect[stroke-width="2"] + text + text + text[text-anchor="middle"]')
        answer = int((await question.inner_text())[0]) * int((await question.inner_text())[4])

        choices = await frame.query_selector_all(
            'g[transform="translate(104, 6) scale(1, 1) rotate(0 0 0)"] g[cursor="pointer"][tabindex="0"]')

        for choice in choices:
            print(await choice.inner_text(), answer)
            if int((await choice.inner_text())[2:]) == answer:
                await choice.click()
                break

        """
    const root = document.querySelector('iframe').contentWindow
    const question = root.document.querySelector('rect[stroke-width="2"] + text + text + text[text-anchor="middle"]').textContent
    const answer = question[0] * question[4]

    const choices = root.document.querySelectorAll('g[transform="translate(104, 6) scale(1, 1) rotate(0 0 0)"] g[cursor="pointer"][tabindex="0"]')

    for (let i = 0; i < choices.length; i++) {
        console.log(choices[i].textContent.substring(2), answer)
        if (choices[i].textContent.substring(2) === answer.toString()) {
            const event = new MouseEvent("click", {
                bubbles: true,
                cancelable: true,
                view: window,
              });

            console.log("CLICKING: ", choices[i], event)

            choices[i].dispatchEvent(event);
            break
        }
}"""
