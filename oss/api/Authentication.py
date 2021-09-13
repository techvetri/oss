from .models import UserLogin, UserDetails
from . import authorization
from datetime import datetime


class Authenticate(object):

    def __init__(self, request):
        self.request = request

    def login(self):
        username = self.request.POST['username']
        password = self.request.POST['password']

        try:
            user = UserLogin.objects.get(username=username)
            if password == user.password:
                date = datetime.utcnow()
                token = authorization.Authorize().get_token(id=user.id, name=username, date=str(date))
                user.auth_token = token
                user.save()
                return {"status": "200", "payload": {"id": user.id,
                                                     "username": user.username,
                                                     "user_image": str(user.user_image),
                                                     "user_email": user.email,
                                                     "user_phone": user.mobile,
                                                     "token": token,
                                                     "is_address_available": user.is_address_available,
                                                     "is_admin": user.is_admin},
                        "error": "", "date": datetime.now()}
            else:
                return {"status": "200", "payload": {}, "error": "username or password incorrect!",
                        "date": datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": {}, "error": "username or password incorrect!",
                    "date": datetime.now()}

    def register(self):
        username = self.request.POST['username']
        password = self.request.POST['password']
        email = self.request.POST['email']
        phone_num = self.request.POST['phone']

        try:
            if UserLogin.objects.filter(username=username).exists():
                return {"status": "200", "payload": {}, "error": "User already exist!", "date": datetime.now()}
            else:
                new_user = UserLogin.objects.create(username=username,
                                                    password=password,
                                                    email=email,
                                                    mobile=phone_num)
                new_user.save()
                user = UserLogin.objects.get(username=username)
                token = authorization.Authorize().get_token(id=user.id, name=user.username)
                user.auth_token = token
                user.save()

                return {"status": "200", "payload": {"id": user.id,
                                                     "username": user.username,
                                                     "user_image": str(user.user_image),
                                                     "user_email": user.email,
                                                     "user_phone": user.mobile,
                                                     "token": token},
                        "error": "", "date": datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": {}, "error": "User does not saved!", "date": datetime.now()}





