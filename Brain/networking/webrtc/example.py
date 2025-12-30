import asyncio
import websockets
import json
from networking.webrtc.connection import WebRTCConnection
from networking.webrtc.utils import log

SIGNALING_SERVER = "ws://localhost:8765"


async def run_client():
    # اتصال به سرور سیگنالینگ
    async with websockets.connect(SIGNALING_SERVER) as ws:
        log("Connected to signaling server")

        # ساخت PeerConnection
        conn = WebRTCConnection()
        channel = conn.add_data_channel("chat")

        # ارسال پیام تستی روی DataChannel
        channel.on("open", lambda: channel.send("Hello from client!"))

        # ساخت Offer
        offer = await conn.create_offer()
        await ws.send(json.dumps({"type": "offer", "sdp": offer.sdp}))
        log("Offer sent to signaling server")

        # دریافت Answer
        async for message in ws:
            data = json.loads(message)
            if data["type"] == "answer":
                log("Answer received")
                await conn.pc.setRemoteDescription(
                    conn.pc._description.__class__(
                        sdp=data["sdp"], type="answer")
                )
                break

        # برنامه روشن می‌ماند تا ارتباط برقرار بماند
        await asyncio.sleep(30)
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_client())
