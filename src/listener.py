import asyncio
import websockets
import json

async def handle_message(message):
    # Your logic to process the received message goes here
    try: 
        response = json.loads(message)
        print(response)
        print(type(response))

        print(response["commandData"]["score"]["leaderboardPlayerInfo"]["id"])
        return 0
    except:
        print("darn")
    print("Received message:", message)
    print(type(message))
    print(message)


    
async def listen_to_websocket():
    websocket = await websockets.connect('wss://scoresaber.com/ws')  # Replace with your WebSocket URL
    while True:
        message = await websocket.recv()
        await handle_message(message)

def start_loop():
    asyncio.get_event_loop().run_until_complete(listen_to_websocket())

