import jwt
from datetime import datetime
import base64
import json
from django.http import JsonResponse
from .models import UserLogin


def require_token_validation(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            try:
                token = arg.headers['Authorization']
            except ConnectionRefusedError as e:
                return JsonResponse({"status": "401", "payload": {}, "error": "Authorization error!",
                                     "date": datetime.now()}, status=401)

            response = Authorize.validate_token(Authorize(), token)
            if int(response['status']) != 200:
                return JsonResponse(response, status=response['status'])
            else:
                return func(*args, **kwargs)

    return wrapper


class Authorize(object):

    def __init__(self, ):
        self.JWT_SECRET_KEY = "django-insecure-u%as5xc3fmj4zn@$t#g)jbzr_%g!$nh*%fuhi2fjus_s@$)2*o"
        self.JWT_TIMEOUT = 20
        self.JWT_ALGORITHM = "HS256"
        self.ISS = "oss"

    def get_token(self, **kwargs):
        payload = {
            **kwargs,
            "iss": self.ISS
        }
        jwt_encoded = jwt.encode(payload=payload, key=self.JWT_SECRET_KEY, algorithm=self.JWT_ALGORITHM)

        return jwt_encoded

    def validate_token(self, token):
        try:
            token_split = str(token).split('.')
            encoded_header = token_split[0]
            encoded_payload = token_split[1]
            decoded_header = json.loads(base64.b64decode(encoded_header + "==").decode('utf-8'))
            decoded_payload = json.loads(base64.b64decode(encoded_payload + "==").decode('utf-8'))

            db = UserLogin.objects.get(id=decoded_payload['id'])

            if db.auth_token != token:
                return {"status": "401", "payload": "", "error": "token expired!",
                        "date": datetime.now()}

            if decoded_header["alg"] != "HS256":
                return {"status": "401", "payload": decoded_header, "error": "token validation failed!",
                        "date": datetime.now()}

            validated_token = jwt.decode(token, key=self.JWT_SECRET_KEY, algorithms=[self.JWT_ALGORITHM])
            return {"status": "200", "payload": {'token_validation': 'success', 'token_payload': validated_token},
                    "error": "", "date": datetime.now()}

        except Exception as e:
            return {"status": "401", "payload": {}, "error": "token not valid", "date": datetime.now()}
