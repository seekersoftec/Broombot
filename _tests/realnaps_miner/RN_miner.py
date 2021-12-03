import time
import asyncio
from pyppeteer import launch
from utils import *

#
# Realnaps virtual football league software
#
#
SLEEP_TIME = 10
#
SITE_URL = 'https://realnaps.com'
#
SITE_URLS = {
    'Bet9ja': f'{SITE_URL}/signal/',
    'Sportybet': f'{SITE_URL}/signal/sportybet-england-vfl-prediction.php',
    'Bettson': f'{SITE_URL}/signal/betsson-nordicbet-prediction.php',
    'Betking': f'{SITE_URL}/signal/betking-kings-league-mobile.php',
    'Justbet': f'{SITE_URL}/signal/justbet.php',
    'Betway': f'{SITE_URL}/signal/premium/stream2-free.php?site=BETWAY',
    'Betpawa': f'{SITE_URL}/signal/betpawa.php'
}
#


class REALNAPS_MINER:
    def __init__(self, page_obj):
        self.page = page_obj

    async def get_data(self):
        data = await self.page.querySelectorAllEval('table', '(nodes => nodes.map(n => n.innerText))')
        #
        return data
#


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(SITE_URLS['Sportybet'])
    #
    time.sleep(SLEEP_TIME)
    #
    #
    try:
        #
        rn_miner = REALNAPS_MINER(page)
        #
        _datum = await rn_miner.get_data()
        # print(_datum)
        print(concat(_datum, sep='\n'))
        #
        time.sleep(SLEEP_TIME)
        #
        # await page.screenshot({'path': 'example.png'})
        while True:
            #
            _current_state = await rn_miner.get_data()

            # print(f"\n\n{_current_state}")
            print(f"\n\n{concat(_current_state)}")
            #
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print('Exiting...')
        await browser.close()
    except:
        print('An error occurred, exiting....')

#
asyncio.get_event_loop().run_until_complete(main())
