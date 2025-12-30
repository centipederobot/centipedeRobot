import asyncio
import websockets
import json


class SignalingServer:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.clients = set()

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                print("Received signaling message:", data)
                # پخش پیام به همه کلاینت‌های دیگر
                for client in self.clients:
                    if client != websocket:
                        await client.send(message)
        finally:
            self.clients.remove(websocket)

    def start(self):
        print(f"Signaling server running on ws://{self.host}:{self.port}")
        return websockets.serve(self.handler, self.host, self.port)


# اجرای سرور
if __name__ == "__main__":
    server = SignalingServer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())
    loop.run_forever()
