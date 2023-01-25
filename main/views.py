from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Order, OrderedProduct, Product, Category, Cart, Testimonial


@sync_to_async
def home(request):
    return render(
        request, 
        "index.html",
        {
            "products_dict": {i.name: Product.objects.filter(category=i,out_of_stock=False).all()[:6] for i in Category.objects.iterator()},
            "header": True
        }
    )

@sync_to_async
def product(request, product_id: str):
    product = Product.objects.get(product_id=product_id)
    return render(
        request, 
        "productpage.html",
        {
            "product": product,
            "testimonials": Testimonial.objects.filter(product=product).all(),
        }
    )

@sync_to_async
@require_POST
@login_required
def add_to_cart(request):
    cart, create_new = Cart.objects.get_or_create(user=request.user)
    order = cart.order
    if order is None:
        order = Order.objects.create(user=request.user)
    product_id = request.POST.get('product_id')
    hours = request.POST.get('hours')
    quantity = request.POST.get('quantity')
    product = Product.objects.get(product_id=product_id)
    if product not in list(map(lambda i: i.product, order.products.iterator())):
        order.products.add(OrderedProduct.objects.create(product=product, quantity=quantity, hours=hours))
        return JsonResponse({"success": True})
    
    for i in order.products.iterator():
        if i.product == product:
            i.quantity = int(quantity)
            i.hours = int(hours)
            i.save()
            return JsonResponse({"success": True})
    

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
        return JsonResponse({"success": True})



    