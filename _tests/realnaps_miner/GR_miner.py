import time
import asyncio
from pyppeteer import launch
from utils import *

#
# Golden race virtual football league miner
#
#
LEAGUE_URLS_CONFIG = {
    'SLEEP_TIME': 2,
    'SITE_URLS': {
        'English-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14013',
        'Spain-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14024',
        'Germany-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14040',
        'Italy-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14022',
        'France-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14020',
        'Turkey-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14025',
        'Nigeria-League': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14034'
    }

}
#
RESULT_HISTORY_URL_CONFIG = {
    'SLEEP_TIME': 5,
    'SITE_URLS': {
        'Results-History': 'https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/history'
    }

}
#


class GOLDEN_RACE:
    def __init__(self, page_obj):
        self.page = page_obj

    async def check_loading_screen(self):
        data = await self.page.querySelectorAllEval('#loading-screen', '(nodes => nodes.map(n => n.innerText))')
        if (len(data) == 0):
            return
        return data

    async def get_live_result(self):
        if (await self.check_loading_screen() != None):
            return 'Still loading...'
        #
        header_data = await self.page.querySelectorAllEval('.live-result-header', '(nodes => nodes.map(n => n.innerText))')
        table_data = await self.page.querySelectorAllEval('.live-result-table', '(nodes => nodes.map(n => n.innerText))')
        #
        return header_data + table_data

    async def get_live_rankings(self):
        if (await self.check_loading_screen() != None):
            return 'Still loading...'
        #
        header_data = await self.page.querySelectorAllEval('.panel-heading', '(nodes => nodes.map(n => n.innerText))')
        table_data = await self.page.querySelectorAllEval('table', '(nodes => nodes.map(n => n.innerText))')
        #
        return header_data + table_data

    async def get_results_history(self):
        return

#


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto(LEAGUE_URLS_CONFIG['SITE_URLS']['Italy-League'])
    #
    time.sleep(LEAGUE_URLS_CONFIG['SLEEP_TIME'])
    #
    #
    try:
        #
        gr_miner = GOLDEN_RACE(page)
        #
        result_datum = await gr_miner.get_live_result()
        rankings_datum = await gr_miner.get_live_rankings()
        # print(result_datum, rankings_datum)
        print(concat(result_datum))
        print("\n\n")
        # print(concat(rankings_datum))
        #
        time.sleep(LEAGUE_URLS_CONFIG['SLEEP_TIME'])
        #
        # await page.screenshot({'path': 'example.png'})
        while True:
            #
            _result_current_state = await gr_miner.get_live_result()
            _rankings_current_state = await gr_miner.get_live_rankings()

            # print(f"\n\n{_result_current_state}",
            #       f"\n{_rankings_current_state}")
            #
            #
            print(f"""\n\n{concat(_result_current_state)}""")
            # print(f"""\n{concat(_rankings_current_state)}""")
            #
            time.sleep(LEAGUE_URLS_CONFIG['SLEEP_TIME'])
    except KeyboardInterrupt:
        print('Exiting...')
        await browser.close()
    except:
        print('An error occurred, exiting....')

#
asyncio.get_event_loop().run_until_complete(main())


#
#
# LIVE EVENTS section:
#
# //*[@id="main-content"]/app-event-list/div/div/div[2]/app-live-event-selector/div/div[2]
#
# //*[@id="main-content"]/app-event-list/div/div/div[2]/app-live-event-selector/div/div[2]/app-live-event-selector-item
#
#
# //*[@id="path"]
#
#
#
# document.querySelectorAll('.filter-message')[0].innerText = ['  \nLoading...', 'No history records found for current selection. Please try with another date.', Error]
#
#
# document.querySelectorAll('.btn-load-more-tickets')[0].click()
#
#
# document.querySelectorAll('.item.ng-star-inserted')
#
# document.querySelectorAll('.menu')[0].innerHTML
