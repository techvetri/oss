import hmac
import datetime
import json

from . import ordersmanager


class PaymentManager:

    def __init__(self, request_body, signature):
        self.request_body = request_body
        self.signature = signature
        self.key = "87jcpD.-a9:XhBB".encode('utf-8')

    def initiate_response(self):
        data = self._verify_signature()
        if data.get("status") != "200":
            return data
        else:
            return self._payment_event_director()

    def _verify_signature(self):
        hmac_signature = hmac.new(self.key, self.request_body, "sha256")
        if hmac_signature.hexdigest() == self.signature:
            return {"status": "200", "payload": "success"}
        else:
            return {"status": "401", "payload": "", "error": "unauthorized!", "date": datetime.datetime.now()}

    def _payment_event_director(self):
        response = json.loads(self.request_body)
        if response['event'] == "order.paid":
            return self._payment_paid()
        else:
            return {"status": "200", "payload": "success", "error": ""}

    def _payment_paid(self):
        body = json.loads(self.request_body)
        payment_response = {
            "payment_id": body["payload"]["payment"]["entity"]["id"],
            "status": body["payload"]["payment"]["entity"]["status"],
            "order_id": body["payload"]["order"]["entity"]['id']
        }
        ordersmanager.OrderManager().confirm_order(payment_response)
        return {"status": "200", "payload": "success", "error": ""}
