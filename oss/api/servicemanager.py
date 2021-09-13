import datetime
import random

from .models import ServiceBooking


class ServiceManager(object):

    def __init__(self, request):
        self.request = request

    def book_new_service(self):
        user_id = self.request.POST["user_id"]
        service_name = self.request.POST["service_name"]
        service_address = self.request.POST["service_address"]
        service_description = self.request.POST["service_description"]

        try:
            db_service = ServiceBooking.objects.create(user_id=user_id,
                                                       service_name=service_name,
                                                       service_address=service_address,
                                                       service_description=service_description,
                                                       service_id=self._create_service_id(user_id),
                                                       is_service_closed=False,
                                                       service_book_date=datetime.datetime.now())
            db_service.save()

            return {"status": "200", "payload": "success", "error": "",
                    "date": datetime.datetime.now()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.datetime.now()}

    def _create_service_id(self, user_id):
        rand_num = random.randrange(100000)
        service_id = str(user_id) + str(datetime.datetime.today().year) + str(rand_num)
        return service_id

    def get_booked_services(self):
        user_id = self.request.POST["user_id"]
        try:
            data = {}
            db_service = ServiceBooking.objects.select_related("service_assign_to").filter(user_id=user_id).order_by("-service_book_date")

            for items in db_service:

                data[items.service_id] = {"service_id": items.service_id,
                                          "is_service_closed": items.is_service_closed,
                                          "service_name": items.service_name,
                                          "service_book_date": items.service_book_date,
                                          "service_description": items.service_description,
                                          "service_response": items.service_details,
                                          "service_person_name": str(items.service_assign_to).split("_")[0]}

            return {"status": "200", "payload": {'services': data}, "error": "",
                    "date": datetime.datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.datetime.now()}

    def cancel_service(self):
        service_id = self.request.POST["service_id"]
        try:
            db = ServiceBooking.objects.get(service_id=service_id)
            db.is_service_closed = True
            db.save()



            return {"status": "200", "payload": "success", "error": "something went wrong",
                    "date": datetime.datetime.now()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.datetime.now()}
