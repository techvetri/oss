import json
from .models import Product, ProductDetail, UserCart, OrderDetail, UserLogin
from datetime import datetime
import time


class ProductsManager:

    def __init__(self, request):
        self.request = request
        self.db_product = Product
        self.db_product_detail = ProductDetail

    def get_product(self, product_count, prev_product_count, product_name=None):

        try:
            data = Product.objects.all()
            data_count = data.count()

            if data_count is None:
                return {"status": "200", "payload": {}, "error": "No product is available", "date": datetime.now()}
            else:
                result, p_count = self._fetch_product(int(prev_product_count),
                                                      int(product_count) + int(prev_product_count),
                                                      filter_by=product_name)
                return {"status": "200", "payload": {"product_count": p_count, "product": result}, "error": "",
                        "date": datetime.now()}

        except Exception as e:
            print("error in get product")
            print(e)

    def search_products(self, search_text):

        split_text = str(search_text).split(' ')
        if split_text.__len__() > 1:
            print("pr")
            data = self.db_product.objects.raw(
                "SELECT id,product_name from api_product where (product_name)  LIKE CONCAT(%s, %s, %s)"
                , ['%', split_text[0], '%'])
        else:
            data = self.db_product.objects.raw(
                "SELECT id, product_name from api_product where (product_name)  LIKE CONCAT(%s, %s, %s)",
                ['%', search_text, '%'])
        result = {}
        for i in data:
            s_d = str(i).split(' ')
            value = ''
            for val in s_d[:-1]:
                value += val + " "
            result[s_d[-1]] = value

        return {"status": "200", "payload": {"product_name": result}, "error": "",
                "date": datetime.now()}

    def fetch_product_detail(self, product_id):
        try:
            db = self.db_product_detail.objects.get(product_id=product_id)
            db_product = self.db_product.objects.get(id=product_id)
            value = db.product_details
            json_create = "{" + value.replace("=", ":") + "}"
            raw_json = json.dumps(json_create)
            str_json = str(raw_json).replace('"', '').replace("{", '').replace("}", '') \
                .replace("\\r", '').replace("\\n", '').replace("\\t", '')

            json_list_key = []
            json_list_value = []
            json_dict = dict()

            for i in str_json.split(','):
                if ':' in i:
                    if i.__len__() > 0:
                        json_list_key.append(i.split(':')[0])
                        json_list_value.append(i.split(':')[1])

            for num in range(len(json_list_key)):
                json_dict[json_list_key[num]] = json_list_value[num]

            if db_product.isvalid_for_offer:
                is_offer = db.offer_end_date
            else:
                is_offer = ""

            json_data = {"product_description": db.product_description, "offer_end_date": is_offer,
                         "product_brand": db.product_brand, "manufacturer": db.manufacturer,
                         "product_details": json_dict}

            return {"status": "200", "payload": json_data, "error": "",
                    "date": datetime.now()}

        except Exception as e:
            return {"status": "200", "payload": "", "error": "product_not_found",
                    "date": datetime.now()}

    def _fetch_product(self, fetch_count_from, fetch_count_to, order_by=None, filter_by=None):
        result = {}
        if filter_by is not None:
            fetch_data = self.db_product.objects.filter(product_name=filter_by)
        else:
            fetch_data = self.db_product.objects.all()[fetch_count_from:fetch_count_to]

        for data in fetch_data:
            result[data.id] = {"product_id": data.id, "product_name": data.product_name,
                               "product_price": data.product_price, "product_image": str(data.product_image),
                               "product_category": data.product_category, "product_stock": data.product_stock,
                               "product_ratings": data.product_ratings, "isvalid_for_offer": data.isvalid_for_offer}
        return result, fetch_data.count()

    def _product_chooser(self, user_id=None):
        pass

    def add_to_cart(self):
        user_id = self.request.POST["user_id"]
        product_id = self.request.POST["product_id"]
        try:
            if UserCart.objects.filter(user_id=user_id, product_id=product_id).exists():
                return {"status": "200", "payload": "", "error": "product already added to cart",
                        "date": datetime.now()}
            db_user_cart = UserCart.objects.create(user_id=user_id, product_id=product_id)
            db_user_cart.save()

            return {"status": "200", "payload": "success", "error": "",
                    "date": datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.now()}

    def get_cart(self):
        user_id = self.request.POST["user_id"]
        try:
            if not UserCart.objects.filter(user_id=user_id).exists():
                return {"status": "200", "payload": "", "error": "cart is empty",
                        "date": datetime.now()}

            db_user_cart = UserCart.objects.filter(user_id=user_id)
            product_ids = []
            for i in db_user_cart:
                product_ids.append(i.product_id)
            result = {}
            db_product = Product.objects.filter(id__in=product_ids)
            for data in db_product:
                result[data.id] = {"product_id": data.id, "product_name": data.product_name,
                                   "product_price": data.product_price, "product_image": str(data.product_image),
                                   "product_category": data.product_category, "product_stock": data.product_stock,
                                   "product_ratings": data.product_ratings, "isvalid_for_offer": data.isvalid_for_offer}

            return {"status": "200", "payload": {"product": result}, "error": "",
                    "date": datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.now()}

    def delete_item_from_cart(self):
        user_id = self.request.POST["user_id"]
        product_id = self.request.POST["product_id"]
        try:
            db_user_cart = UserCart.objects.get(user_id=user_id, product_id=product_id)
            db_user_cart.delete()
            return {"status": "200", "payload": "success", "error": "",
                    "date": datetime.now()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.now()}

    def get_orders(self):
        user_id = self.request.POST["user_id"]
        try:

            db_orders = OrderDetail.objects.filter(user_id=user_id).order_by("-order_date")

            result_product = {}
            result_order_detail = {}

            for db_data in db_orders:
                result_order_detail[db_data.id] = {"order_id": db_data.order_id,
                                                   "delivery_status": db_data.delivery_status,
                                                   "order_quantity": db_data.order_quantity,
                                                   "order_date": self.utc2local(db_data.order_date),
                                                   "is_cancelled": db_data.is_cancelled,
                                                   "total_amount": db_data.total_amount
                                                   }

                db_product = Product.objects.filter(id=db_data.product_id)
                for data in db_product:
                    result_product[str(data.id) + str(db_data.order_id)] = {"product_id": data.id,
                                                                            "product_name": data.product_name,
                                                                            "product_price": data.product_price,
                                                                            "product_image": str(data.product_image),
                                                                            "product_category": data.product_category,
                                                                            "product_stock": data.product_stock,
                                                                            "product_ratings": data.product_ratings,
                                                                            "isvalid_for_offer": data.isvalid_for_offer}

            return {"status": "200", "payload": {"product": result_product, "order_details": result_order_detail},
                    "error": "", "date": datetime.now()}

        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.now()}

    def utc2local(self, utc):
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
        return utc + offset

    def cancel_order(self):
        order_id = self.request.POST["order_id"]

        try:
            if OrderDetail.objects.filter(order_id=order_id).exists():
                db_order_detail = OrderDetail.objects.get(order_id=order_id)
                db_order_detail.is_cancelled = True
                db_order_detail.save()
                return {"status": "200", "payload": "success", "error": "",
                        "date": datetime.now()}
        except Exception as e:
            print(e)
            return {"status": "200", "payload": "", "error": "something went wrong",
                    "date": datetime.now()}
