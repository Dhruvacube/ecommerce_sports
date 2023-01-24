from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST

from .models import Order, OrderedProduct, Product, Category


@sync_to_async
def home(request):
    return render(
        request, 
        "index.html",
        {
            "products_dict": {i.name: Product.objects.filter(category=i).all()[:6] for i in Category.objects.iterator()},
            "header": True
        }
    )

@sync_to_async
def product(request, product_id: str):
    return render(
        request, 
        "productpage.html",
        {
            "product": Product.objects.get(product_id=product_id),
        }
    )

@sync_to_async
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

@sync_to_async
@require_POST
@login_required
def remove_from_cart(request):
    order = Order.objects.get_or_create(user=request.user)
    product_id = request.POST.get('product_id')
    product = Product.objects.get(product_id=product_id)
    order_product = OrderedProduct.objects.filter(product=product)
    if order_product in list(order.products.iterator()):
        order.products.remove(order_product)



    