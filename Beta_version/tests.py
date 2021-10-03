import asyncio
import websockets
import gzip
import shutil
import zlib

async def hello():
    uri = "wss://api.huobi.pro/ws"
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(greeting)


asyncio.run(hello())


