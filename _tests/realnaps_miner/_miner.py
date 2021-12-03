import time
import asyncio
from pyppeteer import launch

#
SLEEP_TIME = 5
#
BANANO_ADDRESS = 'ban_1o7f4qi5za6w3cdr748j9egcb8cqeoc8d4zbduzg9pku5ufp1cau8yfmtofk'
#
SITE_URL = f'https://powerplant.banano.cc/?address={BANANO_ADDRESS}'
#
THREADS = 0


class BANANO_MINER:
    def __init__(self, page_obj):
        self.page = page_obj

    async def start_miner(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[1].rows[4].querySelectorAll('input')[0].click()
        }''')

        return data

    async def stop_miner(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[1].rows[4].querySelectorAll('input')[1].click()
        }''')

        return data

    async def get_address_data(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[0].innerText
        }''')

        return data

    async def get_current_state_data(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[1].innerText
        }''')

        return data

    async def increase_threads(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[1].rows[2].cells[3].querySelectorAll('input')[0].click()
        }''')

        return data

    async def decrease_threads(self):
        data = await self.page.evaluate('''() => {
            return document.querySelectorAll('table')[1].rows[2].cells[3].querySelectorAll('input')[1].click()
        }''')

        return data


#


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(SITE_URL)
    #
    time.sleep(SLEEP_TIME)
    # await page.screenshot({'path': 'main.png'})
    #
    b_miner = BANANO_MINER(page)
    #
    get_address_data = await b_miner.get_address_data()
    print(get_address_data)
    #
    #
    # try:
    #     _THREADS = int(THREADS)
    #     #
    #     if (_THREADS > 0):
    #         for i in range(0, THREADS):
    #             await b_miner.increase_threads()

    #     elif (_THREADS < 0):
    #         for i in range(THREADS*-1, 0, THREADS):
    #             await b_miner.decrease_threads()

    #     else:
    #         pass
    # except ZeroDivisionError:
    #     pass
    #
    #
    await b_miner.stop_miner()
    await b_miner.start_miner()
    #
    time.sleep(SLEEP_TIME)
    # await page.screenshot({'path': 'minning.png'})
    #
    try:
        while True:
            #
            get_address_data = await b_miner.get_address_data()
            _current_state = await b_miner.get_current_state_data()
            print("\n\n", get_address_data, "\n", _current_state)
            #
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print('Exiting...')
        await browser.close()
    except:
        print('An error occurred, exiting....')

asyncio.get_event_loop().run_until_complete(main())
