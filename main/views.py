from django.shortcuts import render
from .views import Product, OrderedProduct, Order
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST

@cache_page(60 * 15)
def home(request):
    return render(
        request, 
        "home.html",
        {
            "products": Product.objects.all()
        }
    )

def about(request):
    return render(request, "about.html")

@require_POST
@login_required
def add_to_cart(request):
    order = Order.objects.get_or_create(user=request.user)
    product_id = request.POST.get('product_id')
    hours = request.POST.get('hours')
    quantity = request.POST.get('quantity')
    
    product = Product.objects.get(product_id=product_id)
    order_product = OrderedProduct.objects.filter(product=product).update_or_create(quantity=quantity, hours=hours)
    if order_product not in list(order.products.iterator()):
        order.products.add(order_product)

@require_POST
@login_required
def remove_from_cart(request):
    order = Order.objects.get_or_create(user=request.user)
    product_id = request.POST.get('product_id')
    product = Product.objects.get(product_id=product_id)
    order_product = OrderedProduct.objects.filter(product=product)
    if order_product in list(order.products.iterator()):
        order.products.remove(order_product)
    