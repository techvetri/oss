import base64
import datetime
import json
import random

import PIL.Image
from channels.generic.websocket import AsyncWebsocketConsumer
import qrcode
from channels.db import database_sync_to_async
from PIL import Image
import io

from asgiref.sync import sync_to_async
from api.models import WebLoginQR
from channels.layers import get_channel_layer


class WebLogin(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data == "get-qr":
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr_id = await self.createQR()
            qr.add_data(qr_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            img.save(buffer, format="png")

            await self.channel_layer.group_add(
                str(qr_id["qr_id"]),
                self.channel_name
            )

            await self.send(
                json.dumps({"type": "qr-img", "data": str(base64.b64encode(buffer.getvalue()).decode('utf-8'))}))
        else:
            self.json_data = json.loads(json.dumps(str(text_data).replace("'", '"')))
            self.data = json.loads(self.json_data)
            await self.channel_layer.group_send(
                self.data["qr_id"],
                {
                    'type': 'chat_message',
                    'message': self.json_data
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"type": "message", "data": json.loads(message)}))

    async def close(self, code=None):
        await self.channel_layer.group_discard(
            self.data['qr_id'],
            self.channel_name
        )
        await self.close()

    @database_sync_to_async
    def createQR(self):
        qr_id = str(random.randrange(1200, 1200000)) + str(datetime.datetime.now().date()).replace('-', '')
        qr_db = WebLoginQR.objects.create(qr_id=qr_id)
        qr_db.save()
        return {"qr_id": qr_id}
