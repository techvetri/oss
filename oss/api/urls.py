from django.urls import path
from . import views


urlpatterns = [
    path("user-login", views.login_user, name="user login"),
    path("user-register", views.register_user, name="user register"),
    path("validate-token", views.token_validate),
    path("get-product", views.get_product, name="get product"),
    path("search-product", views.search_product, name="search product"),
    path("get-product-details", views.get_productDetails, name="get product_details"),
    path("place-order", views.place_order, name="place order"),
    path("confirm-order", views.confirm_order, name="confirm order"),
    path("payment-response", views.payment_response, name="payment response"),
    path("set-user-detail", views.set_user_detail, name="set user details"),
    path("get-user-detail", views.get_user_detail, name="get user details"),
    path("update-user-detail", views.update_user_detail, name="update user details"),
    path("add-to-cart", views.add_to_cart, name="add product to cart"),
    path("get-cart", views.get_cart, name="get cart"),
    path("delete-cart-item", views.delete_cart, name="delete item from cart"),
    path("get-orders", views.get_orders, name="get orders"),
    path("cancel-order", views.cancel_orders, name="cancel order"),
    path("save-fcm-token", views.save_fcm_token, name="save firebase token"),
    path("book-new-service", views.book_new_service, name="book new service"),
    path("get-booked-services", views.get_booked_services, name="get booked services"),
    path("book-new-complaint", views.book_new_complaint, name="book new complaint"),
    path("get-booked-complaints", views.get_booked_complaints, name="get booked complaints"),
    path("logout", views.logout_user, name="logout the user"),
    path("upload-image", views.save_user_image, name="upload user image to server"),
    path("cancel-service", views.cancel_service, name="cancel service")
]
