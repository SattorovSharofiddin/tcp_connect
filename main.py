from fastapi import FastAPI
from fastapi import WebSocket

app = FastAPI()

# Store connected WebSocket clients
connected_clients = set()


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()

    # Add the client to the connected_clients set
    connected_clients.add(websocket)
    print(websocket.client)

    try:
        # Keep listening for incoming messages
        while True:
            # Receive message from the client
            message = await websocket.receive_text()

            # Broadcast the message to all connected clients
            await broadcast_message(message)

    except Exception as e:
        print(f"WebSocket error: {e}")

    finally:
        # Remove the client from the connected_clients set
        connected_clients.remove(websocket)


async def broadcast_message(message: str):
    # Iterate over all connected clients and send the message
    for client in connected_clients:
        await client.send_text(message)
