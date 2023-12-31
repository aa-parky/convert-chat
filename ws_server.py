import asyncio
import websockets
from datetime import datetime
from ws_angry import generate_response
import time

connected = set()

async def chat(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            start_time = time.time()  # Start time for processing

            # Process the message through ws_angry.py
            modified_message = generate_response(message)
            processing_time = time.time() - start_time  # Calculate processing time

            if modified_message:
                broadcast_message = f"Someone said: {modified_message} | Received at: {datetime.now().strftime('%H:%M:%S')} | Processing time: {processing_time:.2f}s"
                sender_message = f"You said: {modified_message} | Received at: {datetime.now().strftime('%H:%M:%S')} | Processing time: {processing_time:.2f}s"
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

start_server = websockets.serve(chat, "0.0.0.0", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
