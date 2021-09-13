from django.contrib import admin
from .models import UserLogin, UserDetails, Product, ProductDetail, ComplaintsBooking
from .models import OrderDetail, OrderTransaction, UserCart, ServiceBooking, Employee

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


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ('employee_name', 'employee_id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display = ("employee_id", "employee_name")


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
        return str(UserLogin.objects.get(id=obj.user_id).id) + "  " + "(" + str(
            UserLogin.objects.get(id=obj.user_id).username) + ")"

    @staticmethod
    def product_id_product(obj):
        return str(Product.objects.get(id=obj.product_id).id) + "  " + "(" + str(
            Product.objects.get(id=obj.product_id).product_name) + ")"


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "order_id", "user_id_user", "delivery_status", "order_quantity")
    search_fields = ('id', 'order_id', 'user_id')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    @staticmethod
    def user_id_user(obj):
        return str(obj.id) + "  " + "(" + str(UserLogin.objects.get(id=obj.user_id).username) + ")"


class ComplaintsBookingAdmin(admin.ModelAdmin):
    list_display = ('complaint_id', 'user_id', 'complaint_name', 'complaint_book_date', 'is_complaint_closed')
    list_filter = ('is_complaint_closed', 'complaint_book_date', 'complaint_name')
    search_fields = ('user_id', 'complaint_id', 'complaint_name')


class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'user_id', 'service_name', 'service_book_date', 'is_service_closed')
    list_filter = ('is_service_closed', 'service_book_date', 'service_name')
    search_fields = ('user_id', 'service_id', 'service_name')


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(OrderTransaction, OrderTransactionAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(ComplaintsBooking, ComplaintsBookingAdmin)
admin.site.register(ServiceBooking, ServiceBookingAdmin)
admin.site.register(Employee, EmployeeAdmin)
