import json

from django.db import models

from django.core.exceptions import ValidationError


# Create your models here.
def json_validation(value):
    json_create = "{" + value.replace("=", ":") + "}"
    try:
        raw_json = json.dumps(json_create)
        str_json = str(raw_json).replace('"', '').replace("{", '').replace("}", '').replace(" ", '')
    except Exception as e:
        print(e)
        raise ValidationError("please check entered details  or  \n key must be unique")

    json_list = []
    for i in str_json.split(','):
        if ':' in i:
            if i.__len__() > 2:
                json_list.append(i.split(':')[0])
            else:
                raise ValidationError("please enter more than one details")
        else:
            raise ValidationError("key value format error data should be in ( data=data,data1=data )")
    if len(json_list) != len(set(json_list)):
        raise ValidationError("duplicate product details not allowed!")


class Employee(models.Model):
    employee_id = models.BigIntegerField(primary_key=True)
    employee_name = models.CharField(max_length=50)
    employee_address = models.CharField(max_length=200)
    employee_phone = models.BigIntegerField()
    date_of_join = models.DateTimeField(auto_now=False)
    date_of_resign = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.employee_name.__str__() + "_" + "id=" + str(self.employee_id)


class UserLogin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    mobile = models.BigIntegerField()
    auth_token = models.CharField(max_length=500)
    user_image = models.ImageField(upload_to="static/user_images", default=None, )
    is_admin = models.BooleanField(default=False)
    is_address_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    fcm_token = models.CharField(max_length=2000)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email + "(" + self.username + ")"


class UserDetails(models.Model):
    user_id = models.BigIntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_address = models.CharField(max_length=300)
    landmark = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + self.last_name


class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_price = models.FloatField()
    product_image = models.ImageField(upload_to="static/product_images", default=None)
    product_ratings = models.FloatField()
    product_stock = models.IntegerField()
    product_category = models.CharField(max_length=200, default=None)
    isvalid_for_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name.__str__() + " " + "id=" + str(self.id)


class ProductDetail(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_name')
    prod_entry_date = models.DateTimeField(auto_now=True)
    product_description = models.CharField(max_length=500)
    offer_end_date = models.DateTimeField(auto_now=False)
    product_brand = models.CharField(max_length=200, default=None)
    manufacturer = models.CharField(max_length=200, default=None)
    sub_category = models.CharField(max_length=200, default=None)
    product_details = models.TextField(default=None, help_text="example: key=value and seprate by "
                                                               "comma(,) ",
                                       validators=[json_validation])

    def __unicode__(self):
        return self.product_id.product_name


class OrderTransaction(models.Model):
    order_id = models.BigIntegerField()
    transaction_id = models.CharField(max_length=200)
    user_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    payment_id = models.CharField(max_length=200, default="")
    amount = models.FloatField()
    currency = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now=False)
    status = models.CharField(max_length=40)
    amount_paid = models.BooleanField(default=False)
    payment_mode = models.IntegerField()
    order_receipt_id = models.CharField(max_length=100)
    order_quantity = models.IntegerField(default=1)


class OrderDetail(models.Model):
    user_id = models.BigIntegerField()
    order_id = models.BigIntegerField()
    delivery_status = models.CharField(max_length=20, default="processing")
    order_quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now=False)
    is_cancelled = models.BooleanField(default=False)
    product_id = models.BigIntegerField()
    total_amount = models.FloatField()


class UserCart(models.Model):
    user_id = models.BigIntegerField()
    product_id = models.BigIntegerField()
    date = models.DateTimeField(auto_now=True)


class ServiceBooking(models.Model):
    user_id = models.BigIntegerField()
    service_id = models.BigIntegerField()
    service_book_date = models.DateTimeField(auto_now=False)
    service_name = models.CharField(max_length=200)
    service_details = models.CharField(max_length=2000, null=True, blank=True)
    is_service_closed = models.BooleanField(default=False)
    service_complete_date = models.DateTimeField(null=True, blank=True)
    service_address = models.CharField(max_length=2000)
    service_description = models.CharField(max_length=2000)
    service_assign_to = models.ForeignKey(Employee, on_delete=models.CASCADE, db_column='employee_name', null=True)

    def __unicode__(self):
        return self.service_assign_to.employee_name


class ComplaintsBooking(models.Model):
    user_id = models.BigIntegerField()
    complaint_id = models.BigIntegerField()
    complaint_book_date = models.DateTimeField(auto_now=False)
    complaint_name = models.CharField(max_length=200)
    complaint_details = models.CharField(max_length=2000)
    is_complaint_closed = models.BooleanField(default=False)
    complaint_complete_date = models.DateTimeField(null=True)
    complaint_description = models.CharField(max_length=2000)
    is_complaint_closed_by = models.BigIntegerField(null=True)


class WebLoginQR(models.Model):
    qr_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    user_id = models.BigIntegerField(null=True)
