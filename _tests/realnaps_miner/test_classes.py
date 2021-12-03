
class SPORTY_BET_VIRTUALS:
    # document.querySelectorAll('#golden-race-desktop-app > iframe')[0].src
    def __init__(self):
        self.SITE_URL = 'https://www.sportybet.com/ng/virtual/'
        self.SLEEP_TIME = 10
        # self.page = page_obj

    async def get_golden_race_address(self):
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.SITE_URL)
        #
        time.sleep(SLEEP_TIME)
        #
        data = await page.querySelectorAllEval('#golden-race-desktop-app > iframe', '(nodes => nodes.map(n => n.src))')
        #
        await browser.close()
        #
        return data

#
#
#
# golden_race_address = await SPORTY_BET_VIRTUALS().get_golden_race_address()
#
#
#
#
#
# id = loading-screen
#
# document.querySelectorAll('#golden-race-desktop-app > iframe')
# document.querySelectorAll('#golden-race-desktop-app > iframe')[0].src
#
# https://virtual.golden-race.net/desktop-v3/default/?checkScroll=true&containerId=golden-race-desktop-app&profile=sportybet&hwId=e4aca768fe1e3fa59da03bf5ff986bbd&showHeader=true#/scheduled/league/playlist/14013
#
# id = loading-screen
#
# document.querySelectorAll('#main')
# document.querySelectorAll('main')
#
# Live Result:
# document.querySelectorAll('.live-result-header')[0].innerText [table-header]
# document.querySelectorAll('.live-result-table')[0].innerText [table-body]
#
# Ranking:
# document.querySelectorAll('.panel-heading')[0].innerText [table-header]
# document.querySelectorAll('table')[0].innerText [table-body]
#
#
