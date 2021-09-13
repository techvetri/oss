import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from pathlib import Path


def initialize():
    cred = credentials.Certificate(
        (Path(__file__).parent/'oss-push-service-firebase-adminsdk-8izsp-c665b49605.json')
    )
    firebase_admin.initialize_app(cred)


initialize()


class FirebaseManager(object):

    def __init__(self, user_token):
        self.token = user_token

    def send_message(self, data, send_to_all=False):
        if not send_to_all:
            msg = messaging.Message(token=self.token)
            response = messaging.send(msg)
        else:
            msg = messaging.MulticastMessage(tokens=self.token, data=data)
            response = messaging.send_multicast(msg)

    def send_notification(self, title, message, send_to_all=False):
        if not send_to_all:
            msg = messaging.Message(token=self.token, notification=messaging.Notification(title, message),
                                    data={"title": title, "message": message})
            response = messaging.send(msg)

        else:
            msg = messaging.MulticastMessage(tokens=self.token, notification=messaging.Notification(title, message))
            response = messaging.send_multicast(msg)
