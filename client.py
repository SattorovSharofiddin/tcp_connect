import asyncio
import websockets

clients_set = set()


async def connect_websocket():
    MAX_CONNECTION = 10_000
    try:
        for _ in range(MAX_CONNECTION):
            websocket = await websockets.connect('ws://localhost:8000/ws')
            clients_set.add(websocket)
            message = 'input("Enter message: ")'
            await websocket.send(message)
        while 1: pass

    except KeyboardInterrupt:
        for websocket in clients_set:
            await websocket.close()


asyncio.new_event_loop().run_until_complete(connect_websocket())
