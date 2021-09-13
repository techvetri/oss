import datetime
import random

from .models import ComplaintsBooking


class ComplaintManager(object):

    def __init__(self, request):
        self.request = request

    def book_new_complaint(self):
        user_id = self.request.POST["user_id"]
        complaint_name = self.request.POST["service_name"]
        complaint_description = self.request.POST["service_description"]

        try:
            db_service = ComplaintsBooking.objects.create(user_id=user_id,
                                                          complaint_name=complaint_name,
                                                          complaint_description=complaint_description,
                                                          complaint_id=self._create_complaint_id(user_id),
                                                          is_complaint_closed=False,
                                                          complaint_book_date=datetime.datetime.now())
            db_service.save()

            return {"status": "200", "payload": "success", "error": "",
                    "date": datetime.datetime.now()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.datetime.now()}

    @staticmethod
    def _create_complaint_id(user_id):
        rand_num = random.randrange(100000)
        complaint_id = str(user_id) + str(datetime.datetime.today().year) + str(rand_num)
        return complaint_id

    def get_booked_complaints(self):
        user_id = self.request.POST["user_id"]
        try:
            data = {}
            db_service = ComplaintsBooking.objects.filter(user_id=user_id).order_by("complaint_book_date")
            for items in db_service:
                data[items.complaint_id] = {"complaint_id": items.complaint_id,
                                            "complaint_date": items.complaint_book_date,
                                            "complaint_detail": items.complaint_description,
                                            "complaint_response": items.complaint_details,
                                            "is_complaint_closed": items.is_complaint_closed,
                                            "complaint_name": items.complaint_name}

            return {"status": "200", "payload": {'complaints': data}, "error": "",
                    "date": datetime.datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.datetime.now()}
