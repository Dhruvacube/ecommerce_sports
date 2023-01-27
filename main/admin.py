from django.contrib import admin
from .models import Product, Category, Order, FeedBack, Testimonial, Cart, OrderedProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'description': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    readonly_fields = ('product_id',)
    prepopulated_fields = {'description': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'payment')
    readonly_fields = ('order_id',)
    
    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('email', 'feedback')
    
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('product', 'feedback', 'rating', 'user')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'order')

@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'hours', 'quantity')
    
admin.site.site_header = admin.site.site_title = "Sportszy Admin"