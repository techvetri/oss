import base64
import pathlib
import random

from .models import UserDetails, UserLogin
import datetime



class UserManager(object):

    def __init__(self, request):
        self.request = request

    def set_user_detail(self):
        user_id = self.request.POST['user_id']
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        address = self.request.POST["user_address"]
        landmark = self.request.POST["landmark"]
        district = self.request.POST["district"]
        state = self.request.POST['state']
        zip_code = self.request.POST["zip_code"]
        country = self.request.POST["country"]

        try:
            if UserDetails.objects.filter(user_id=user_id).exists():
                return {"status": "200", "payload": "", "error": "something went wrong!",
                        "date": datetime.datetime.utcnow()}
            db_user_detail = UserDetails.objects.create(user_id=user_id,
                                                        first_name=first_name,
                                                        last_name=last_name,
                                                        user_address=address,
                                                        landmark=landmark,
                                                        district=district,
                                                        state=state,
                                                        zip_code=zip_code,
                                                        country=country)
            db_user_detail.save()

            db_userlogin = UserLogin.objects.get(id=user_id)
            db_userlogin.is_address_available = True
            db_userlogin.save()

            result = {"first_name": first_name, "last_name": last_name,
                      "user_address": address, "landmark": landmark,
                      "district": district, "state": state,
                      "zip_code": zip_code, "country": country}
            return {"status": "200", "payload": result, "error": "",
                    "date": datetime.datetime.utcnow()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": {}, "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    def get_user_details(self):
        user_id = self.request.POST["user_id"]
        try:
            db_user_detail = UserDetails.objects.get(user_id=user_id)
            result = {"first_name": db_user_detail.first_name, "last_name": db_user_detail.last_name,
                      "user_address": db_user_detail.user_address, "landmark": db_user_detail.landmark,
                      "district": db_user_detail.district, "state": db_user_detail.state,
                      "zip_code": db_user_detail.zip_code, "country": db_user_detail.country}
            return {"status": "200", "payload": result, "error": "", "date": datetime.datetime.utcnow()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": {}, "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    def update_user_detail(self):
        user_id = self.request.POST['user_id']
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        address = self.request.POST["user_address"]
        landmark = self.request.POST["landmark"]
        district = self.request.POST["district"]
        state = self.request.POST['state']
        zip_code = self.request.POST["zip_code"]
        country = self.request.POST["country"]

        try:
            db_user_detail = UserDetails.objects.get(user_id=user_id)
            db_user_detail.first_name = first_name
            db_user_detail.last_name = last_name
            db_user_detail.user_address = address
            db_user_detail.landmark = landmark
            db_user_detail.district = district
            db_user_detail.state = state
            db_user_detail.zip_code = zip_code
            db_user_detail.country = country
            db_user_detail.save()

            result = {"first_name": first_name, "last_name": last_name,
                      "user_address": address, "landmark": landmark,
                      "district": district, "state": state,
                      "zip_code": zip_code, "country": country}
            return {"status": "200", "payload": result, "error": "",
                    "date": datetime.datetime.utcnow()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    def save_fcm_token(self):
        fcm_token = self.request.POST["fcm_token"]
        user_id = self.request.POST["user_id"]

        try:
            db_user = UserLogin.objects.get(id=user_id)
            db_user.fcm_token = fcm_token
            db_user.is_active = True
            db_user.save()
            return {"status": "200", "payload": "success", "error": "",
                    "date": datetime.datetime.utcnow()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    def logout_user(self):
        user_id = self.request.POST["user_id"]
        try:
            db_user = UserLogin.objects.get(id=user_id)
            db_user.is_active = False
            db_user.save()
            return {"status": "200", "payload": "success", "error": "", "date": datetime.datetime.utcnow()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    def save_user_image(self):
        user_id = self.request.POST["user_id"]
        string_data = self.request.POST["image"]
        file_name = "static/user_images/" + user_id + "_" + str(random.randrange(100000)) + str(datetime.datetime.now().year) + ".jpg"
        try:
            with open(file_name, 'wb') as file:
                file.write(base64.b64decode(string_data))
            db_user = UserLogin.objects.get(id=user_id)
            db_user.user_image = file_name
            db_user.save()
            return {"status": "200", "payload": {"status": "success", "image_path": file_name}, "error": "",
                    "date": datetime.datetime.utcnow()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong!",
                    "date": datetime.datetime.utcnow()}

    @staticmethod
    def get_fcm_token(user_id=None):
        if user_id is not None:
            db_user = UserLogin.objects.get(id=user_id)
            return db_user.fcm_token
        else:
            tokens = []
            db_user = UserLogin.objects.all()
            for fcm_tokens in db_user:
                tokens.append(fcm_tokens.fcm_token)
            return tokens
