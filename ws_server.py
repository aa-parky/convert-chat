import asyncio
import websockets
from ws_angry import generate_response  # Import the function from convert_angry.py

connected = set()

async def chat(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            # Process the message through ws_angry.py
            modified_message = generate_response(message)
            if modified_message:
                broadcast_message = f"Someone said: {modified_message}"
                sender_message = f"You said: {modified_message}"
            else:
                broadcast_message = "Error processing message."
                sender_message = "Error processing your message."

            # Send the converted message to the sender
            await websocket.send(sender_message)

            # Broadcast the processed message to other clients
            for conn in connected:
                if conn != websocket:
                    await conn.send(broadcast_message)
    finally:
        connected.remove(websocket)


start_server = websockets.serve(chat, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
