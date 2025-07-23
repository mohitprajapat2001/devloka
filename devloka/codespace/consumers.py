import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CodeSpaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.codespace_id = self.scope["url_route"]["kwargs"]["codespace_id"]
        self.room_group_name = f"codespace_{self.codespace_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data["content"]

        # Broadcast to all users in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "code_update",
                "content": content,
            },
        )

    async def code_update(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "content": event["content"],
                }
            )
        )
