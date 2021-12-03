# import re
# import json
# import configparser
# import investpy
# from telethon.errors import SessionPasswordNeededError
# from telethon import TelegramClient, events, sync
# from telethon.tl.functions.messages import (GetHistoryRequest)
# from telethon.tl.types import (
#     PeerChannel
# )


# with client:
#     client.loop.run_until_complete(newMessageListener)
#
#
#
# async def main():
#     # Getting information about yourself
#     me = await client.get_me()

#     # "me" is a user object. You can pretty-print
#     # any Telegram object with the "stringify" method:
#     print(me.stringify())


# from telethon import TelegramClient, events

# client = TelegramClient('session_read', api_id, api_hash)

# @client.on(events.NewMessage(chats=("http")))
# async def my_event_handler(event):
#     print('{}'.format(event))

# client.start()
# client.run_until_disconnected()
#
#
# user_input_channel = 'https://t.me/<channel_name>' or 'me'
# subjectFilter = ['physics', 'mathematics', 'maths', 'math']
# levelFilter = ['sec', 'secondary', 'junior college', 'jc']
# Listen to mesages from target channel
# @client.on(events.NewMessage(chats=user_input_channel))
# async def newMessageListener(event):
#     # Get message text
#     newMessage = event.message.message
#     # Apply 1st round of Regex for subject for current messageContent - return list of keywords found (case-insensitive)
#     subjectFiltered = re.findall(
#         r"(?=("+'|'.join(subjectFilter)+r"))", newMessage, re.IGNORECASE)

#     if (len(subjectFiltered) != 0):
#         # Apply 2nd round of of Regex for level
#         levelFiltered = re.findall(
#             r"(?=("+'|'.join(levelFilter)+r"))", newMessage, re.IGNORECASE)

#         if (len(levelFiltered) != 0):
#             await client.forward_messages(entity='me', messages=event.message)


#
#
#
#
# Main
# call everything from here


# import required libraries
import investpy
from telethon import TelegramClient, events, sync
#
import datetime
import pandas as pd


#
# Remember to use your own values from my.telegram.org!
telegram_api_id = 2236382
telegram_api_hash = '53f80ff7bd3e47b6f9b29235ac86e2ff'


# Here you define the target channel(s) that you want to listen to [https://t.me/<channel_name>]:
base_channel_url = 'https://t.me'
user_other_input_channels = ['me',
                             f'{base_channel_url}/pancakeswapinstant',
                             f'{base_channel_url}/uniswapinstant',
                             f'{base_channel_url}/dex_list',
                             f'{base_channel_url}/mycryptopedia',
                             f'{base_channel_url}/scalpexindexbot']

user_fx_input_channels = ['me',
                          #   'Master Scalping',
                          'TEAM OF TRADERS',
                          'Xauusd Master accout management',
                          f'{base_channel_url}/goldbullTeam',
                          f'{base_channel_url}/joinchat/AAAAAFQZnXQ_Pw5BGDY7ug',
                          f'{base_channel_url}/joinchat/E71TlyXs2PU1ZmM0']

intervals = ['1min', '5mins', '15mins', '30mins',
             '1hour', '5hours', 'daily', 'weekly', 'monthly']

telegram_client = TelegramClient('anon', telegram_api_id, telegram_api_hash)


@telegram_client.on(events.NewMessage(chats=tuple(user_other_input_channels)))
async def SocialInvestorListener(event):
    """
        SocialInvestorListener

        Listen to message signals from targeted channel(s) on telegram
        and cross check it with the signal data from Investing.com
    """

    # Get message text
    new_message = event.message.message
    #
    # Check investing.com
    search_result = investpy.search_quotes(
        text='xau/usd', products=['currencies'], n_results=1)
    print(search_result)
    information = search_result.retrieve_information()["symbol"]
    print(information)
    #
    #
    # 'XAU/USD'.replace('/','_')
    # '{time},{complete},{o},{h},{l},{c},{v}' is the format of the data
    # df = pd.read_csv('2006-day-001.txt', columns=['time', 'complete', 'open','high','low', 'close', 'volume'], parse_dates=True, index_col='time')
    # simple_technical_analyzer(df)
    #
    recent_data = search_result.retrieve_recent_data()
    print(recent_data)
    #
    technical_indicators = {}
    for interval in intervals:
        # confirm it by adding some other indicators to the dataframe
        #
        technical_indicators[interval] = search_result.retrieve_technical_indicators(
            interval=interval)
        print(technical_indicators)
    #
    # await telegram_client.forward_messages(entity='me', messages=new_message)
    print('{}'.format(new_message))


def main():
    telegram_client.start()
    telegram_client.run_until_disconnected()


if __name__ == '__main__':
    main()

# df = pd.read_csv(os.getcwd()+'/DATASETS/XAU_USD/XAU_USD_H1.csv', names=['time', 'complete', 'open',
#                                                                         'high', 'low', 'close', 'volume'], parse_dates=True, index_col='time')
# simple_technical_analyzer(df)
