import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpRequest
import psutil
from api.models import UserLogin, OrderTransaction, OrderDetail, ComplaintsBooking, ServiceBooking

from channels.db import database_sync_to_async


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        request = HttpRequest()
        request.method = "GET"
        request.GET = {'user_id': '2'}
        total_users, active_users = await self.get_db_user()
        total_orders, completed_orders = await self.get_order_status()
        total_complaints, solved_complaints = await self.get_complaint_status()
        total_services, solved_services = await self.get_service_status()

        await self.send(text_data=json.dumps({
            "cpu_load": psutil.cpu_percent(),
            "ram_load": psutil.virtual_memory().percent,
            "total_users": total_users,
            "active_users": active_users,
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "total_complaints": total_complaints,
            "solved_complaints": solved_complaints,
            "total_services": total_services,
            "solved_services": solved_services

        }))

    @database_sync_to_async
    def get_db_user(self):
        db_user = UserLogin.objects.all()

        return db_user.count(), db_user.filter(is_active=True).count()

    @database_sync_to_async
    def get_order_status(self):
        db_order_trans = OrderTransaction.objects.all()
        db_orders = OrderDetail.objects.all()

        return db_order_trans.count(), db_orders.count()

    @database_sync_to_async
    def get_complaint_status(self):
        db_complaints = ComplaintsBooking.objects.all()

        return db_complaints.count(), db_complaints.filter(is_complaint_closed=True).count()

    @database_sync_to_async
    def get_service_status(self):
        db_service = ServiceBooking.objects.all()

        return db_service.count(), db_service.filter(is_service_closed=True).count()