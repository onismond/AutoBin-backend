import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a common group for all drivers
        await self.channel_layer.group_add("drivers", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("drivers", self.channel_name)

    # async def receive(self, text_data):
    #     pass

    async def bin_update(self, event):
        # Send bin update to connected drivers
        await self.send(text_data=json.dumps(event["data"]))
