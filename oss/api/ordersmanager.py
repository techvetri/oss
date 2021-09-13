import random
from datetime import datetime
import razorpay
from django.utils import timezone

from . import firebasemanager, user
from .models import OrderTransaction, OrderDetail, Product


class OrderManager:

    def __init__(self, user_id=None, product_id=None, product_price=None, signature=None, payment_id=None,
                 order_id=None, txn_id=None, quantity=None):
        self.CURRENCY = "INR"
        self.PAYMENT_CAPTURE = 1
        self.user_id = user_id
        self.product_id = product_id
        self.product_price = product_price
        self.product_quantity = quantity
        self.razorpay_key = "rzp_test_oXZ9pehi2xGpF5"
        self.razorpay_secret = "Ps4OFIRTzNDiYfL3dEkxP4zY"
        self.signature = signature
        self.payment_id = payment_id
        self.order_id = order_id
        self.txn_id = txn_id
        self.db_order_Transaction = OrderTransaction
        self.db_order_detail = OrderDetail

    def place_order(self):
        receipt = str("receipt_id") + str(self.user_id)
        prod_db = Product.objects.get(id=self.product_id)
        prod_stock = prod_db.product_stock
        if prod_stock == 0:
            return {"status": "200",
                    "payload": "",
                    "error": "Products are sold out. Please try later!",
                    "date": datetime.utcnow()}
        elif int(self.product_quantity) > prod_stock:
            return {"status": "200",
                    "payload": "",
                    "error": "max available quantity is "+str(prod_db.product_stock),
                    "date": datetime.utcnow()}

        total_amount = float(float(prod_db.product_price) * int(self.product_quantity)) * 100
        checkout_data = {
            "amount": total_amount,
            "currency": self.CURRENCY,
            "receipt": receipt,
            "payment_capture": 1
        }

        client = razorpay.Client(auth=(self.razorpay_key, self.razorpay_secret))
        razorpay_response = razorpay.Order(client).create(data=checkout_data)

        order_id = self.product_id + self.user_id + str(datetime.today().year) + str(random.randrange(10000))

        db = self.db_order_Transaction.objects.create(order_id=order_id, transaction_id=razorpay_response["id"],
                                                      user_id=self.user_id, product_id=self.product_id,
                                                      currency=self.CURRENCY,
                                                      created_at=datetime.now(timezone.utc),
                                                      amount=float(prod_db.product_price) * int(self.product_quantity),
                                                      order_receipt_id=razorpay_response["receipt"], payment_mode="1",
                                                      status=razorpay_response["status"],
                                                      order_quantity=self.product_quantity)
        db.save()

        return {"status": "200",
                "payload": {"order_id": order_id, "txn_id": razorpay_response["id"], "total_amount": total_amount},
                "error": "",
                "date": datetime.utcnow()}

    def confirm_order(self, payment_response):
        try:
            db = self.db_order_Transaction.objects.get(transaction_id=payment_response["order_id"])
            db.payment_id = payment_response["payment_id"]
            db.status = payment_response["status"]
            db.amount_paid = True
            db.save()
            db_order_detail = self.db_order_detail.objects.create(order_id=db.order_id, user_id=db.user_id,
                                                                  delivery_status="processing",
                                                                  order_date=datetime.now(timezone.utc),
                                                                  order_quantity=db.order_quantity,
                                                                  product_id=db.product_id,
                                                                  total_amount=db.amount)
            db_order_detail.save()
            db_product = Product.objects.get(id=db.product_id)
            product_stock = int(db_product.product_stock) - int(db.order_quantity)
            db_product.product_stock = product_stock
            db_product.save()

            firebasemanager.FirebaseManager(user.UserManager.get_fcm_token(user_id=db.user_id)) \
                .send_notification("Payment", "Order successfully placed")

        except Exception as e:
            print(e)
