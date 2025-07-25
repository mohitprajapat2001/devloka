import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from codespace.models import CodeSpace


class CodeSpaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.codespace_id = self.scope["url_route"]["kwargs"]["codespace_id"]
        self.room_group_name = f"codespace_{self.codespace_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send initial content snapshot so the editor shows the latest DB state
        content = await self.get_content()
        await self.send(text_data=json.dumps({"content": content}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """
        Backwards compatible:
        Accepts {"content": "..."} (no type/version required)
        """
        try:
            data = json.loads(text_data or "{}")
        except Exception:
            data = {}

        content = data.get("content")
        if content is None:
            return  # ignore malformed payloads

        # Save to DB
        await self.save_content(content)

        # Broadcast to everybody (including sender)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "code_update",
                "content": content,
            },
        )

    async def code_update(self, event):
        await self.send(text_data=json.dumps({"content": event["content"]}))

    # ------------ DB helpers ------------

    @database_sync_to_async
    def get_content(self) -> str:
        try:
            cs = CodeSpace.objects.only("content").get(pk=self.codespace_id)
            return cs.content or ""
        except CodeSpace.DoesNotExist:
            return ""

    @database_sync_to_async
    def save_content(self, content: str) -> None:
        CodeSpace.objects.filter(pk=self.codespace_id).update(content=content)
