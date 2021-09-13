import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

from . import Authentication, ordersmanager, paymentmanager, user, servicemanager, complaintmanager
from . import firebasemanager
from django.views.decorators.csrf import csrf_exempt
from . import authorization, productsmanager


def home(request):
    return render(request, 'index.html')


def web_dashboard(request):
    return render(request, "dashboard.html")


def web_cart(request):
    return render(request, "cart.html")


@csrf_exempt
def product_detail(request):
    return render(request, "product_detail.html")


@csrf_exempt
def login_user(request):
    response = Authentication.Authenticate(request).login()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
def register_user(request):
    response = Authentication.Authenticate(request).register()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
def token_validate(request):
    header = request.headers
    token = header['Authorization']
    response = authorization.Authorize().validate_token(token)
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def get_product(request):
    product_count = request.POST["product_count"]
    prev_product_count = request.POST["prev_prod_count"]
    product_search_name = request.POST["product_search_name"]

    if product_search_name == '':
        response = productsmanager.ProductsManager(request).get_product(product_count, prev_product_count)
    else:
        response = productsmanager.ProductsManager(request).get_product(product_count, prev_product_count,
                                                                        product_search_name)

    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def search_product(request):
    response = productsmanager.ProductsManager(request).search_products(request.POST["search_query"])
    return JsonResponse(response)


@csrf_exempt
@authorization.require_token_validation
def get_productDetails(request):
    product_id = request.POST['product_id']
    response = productsmanager.ProductsManager(request).fetch_product_detail(product_id)
    return JsonResponse(response)


@csrf_exempt
@authorization.require_token_validation
def place_order(request):
    user_id = request.POST["user_id"]
    product_id = request.POST["product_id"]
    product_price = request.POST["product_price"]
    product_quantity = request.POST["quantity"]

    response = ordersmanager.OrderManager(user_id, product_id, product_price, quantity=product_quantity).place_order()

    return JsonResponse(response)


@csrf_exempt
@authorization.require_token_validation
def confirm_order(request):
    user_id = request.POST["user_id"]
    txn_id = request.POST["txn_id"]
    payment_id = request.POST["payment_id"]
    signature = request.POST["signature"]
    order_id = request.POST["order_id"]
    payment_response = {
        "payment_id": payment_id,
        "status": "",
        "order_id": order_id
    }
    response = ordersmanager.OrderManager().confirm_order(payment_response)
    return JsonResponse(response)


@csrf_exempt
def payment_response(request):
    response = paymentmanager.PaymentManager(request.body, request.headers['X-Razorpay-Signature']).initiate_response()
    print(response)
    return JsonResponse(response)


@csrf_exempt
@authorization.require_token_validation
def get_user_detail(request):
    response = user.UserManager(request).get_user_details()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def set_user_detail(request):
    response = user.UserManager(request).set_user_detail()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def update_user_detail(request):
    response = user.UserManager(request).update_user_detail()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def add_to_cart(request):
    response = productsmanager.ProductsManager(request).add_to_cart()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def get_cart(request):
    response = productsmanager.ProductsManager(request).get_cart()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def delete_cart(request):
    response = productsmanager.ProductsManager(request).delete_item_from_cart()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def get_orders(request):
    response = productsmanager.ProductsManager(request).get_orders()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def cancel_orders(request):
    response = productsmanager.ProductsManager(request).cancel_order()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def save_fcm_token(request):
    response = user.UserManager(request).save_fcm_token()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def book_new_service(request):
    response = servicemanager.ServiceManager(request).book_new_service()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def get_booked_services(request):
    response = servicemanager.ServiceManager(request).get_booked_services()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def book_new_complaint(request):
    response = complaintmanager.ComplaintManager(request).book_new_complaint()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def get_booked_complaints(request):
    response = complaintmanager.ComplaintManager(request).get_booked_complaints()

    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def logout_user(request):
    response = user.UserManager(request).logout_user()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def save_user_image(request):
    response = user.UserManager(request).save_user_image()
    return JsonResponse(response, status=response.get("status"))


@csrf_exempt
@authorization.require_token_validation
def cancel_service(request):
    response = servicemanager.ServiceManager(request).cancel_service()
    return JsonResponse(response, status=response.get("status"))
