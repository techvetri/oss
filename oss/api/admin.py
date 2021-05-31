from django.contrib import admin
from .models import UserLogin, UserDetails, Product, ProductDetail
from .models import OrderDetail, OrderTransaction, UserCart

# Register your models here.

admin.site.register(UserLogin)
admin.site.register(UserDetails)
admin.site.register(UserCart)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_name', 'id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ("id", "product_name", "product_price", "product_category", "product_stock")


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "product_brand", "manufacturer")
    search_fields = ('id', 'product_brand')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    @staticmethod
    def product_name(obj):
        return obj.product_id.product_name


class OrderTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "user_id_user", "product_id_product", "amount", "amount_paid")
    search_fields = ('id', 'order_id', 'payment_id', 'transaction_id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    @staticmethod
    def user_id_user(obj):
        return str(obj.id) + "  " + "(" + str(UserLogin.objects.get(id=obj.user_id).username) + ")"

    @staticmethod
    def product_id_product(obj):
        return str(obj.id) + "  " + "(" + str(Product.objects.get(id=obj.product_id).product_name) + ")"


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "user_id_user", "delivery_status",  "order_quantity")
    search_fields = ('id', 'order_id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    @staticmethod
    def user_id_user(obj):
        return str(obj.id) + "  " + "(" + str(UserLogin.objects.get(id=obj.user_id).username) + ")"


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(OrderTransaction, OrderTransactionAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
