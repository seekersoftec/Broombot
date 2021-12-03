import asyncio
import socketio

sio = socketio.AsyncClient()
url = 'wss://virtual-proxy.golden-race.net:9443/vs'
headers = {
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-websocket-extensions": "permessage-deflate; client_max_window_bits",
    "sec-websocket-key": "4sbHG6rHN5mSzFxbc8niMw==",
    "sec-websocket-version": "13"
}


@sio.event
async def connect():
    print('connection established')


@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})


@sio.event
async def disconnect():
    print('disconnected from server')


async def main():
    # await sio.connect('http://localhost:5000')
    await sio.connect(url, headers=headers)
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())


#
#
# GET wss://virtual-proxy.golden-race.net:9443/vs HTTP/1.1
# Host: virtual-proxy.golden-race.net:9443
# Connection: Upgrade
# Pragma: no-cache
# Cache-Control: no-cache
# User-Agent: Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36
# Upgrade: websocket
# Origin: https://virtual.golden-race.net
# Sec-WebSocket-Version: 13
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9
# Sec-WebSocket-Key: BzUp1zDRBft3eFuQCvU5ow==
# Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits


# fetch("wss://virtual-proxy.golden-race.net:9443/vs", {
#   "headers": {
#     "accept-language": "en-US,en;q=0.9",
#     "cache-control": "no-cache",
#     "pragma": "no-cache",
#     "sec-websocket-extensions": "permessage-deflate; client_max_window_bits",
#     "sec-websocket-key": "4sbHG6rHN5mSzFxbc8niMw==",
#     "sec-websocket-version": "13"
#   },
#   "body": null,
#   "method": "GET"
# });
#
# https://socket.io/docs/v4/
