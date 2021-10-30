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
