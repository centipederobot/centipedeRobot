import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, MediaStreamTrack
from aiortc.contrib.signaling import BYE


class DummyVideoTrack(MediaStreamTrack):
    kind = "video"

    async def recv(self):
        # اینجا می‌تونی فریم واقعی از دوربین بگیری
        raise NotImplementedError("Video capture not implemented")


class WebRTCConnection:
    def __init__(self):
        self.pc = RTCPeerConnection()

    async def create_offer(self):
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        return offer

    async def create_answer(self, offer_sdp):
        offer = RTCSessionDescription(sdp=offer_sdp, type="offer")
        await self.pc.setRemoteDescription(offer)
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        return answer

    def add_data_channel(self, label="chat"):
        channel = self.pc.createDataChannel(label)
        channel.on("message", lambda msg: print("DataChannel message:", msg))
        return channel

    def add_video_track(self):
        track = DummyVideoTrack()
        self.pc.addTrack(track)

    async def close(self):
        await self.pc.close()
