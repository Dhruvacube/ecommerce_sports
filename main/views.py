import razorpay
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.contrib import messages

from payments.models import Payments

from .forms import FeedBackForm
from .models import Cart, Category, Order, OrderedProduct, Product, Testimonial

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))


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
def feedback(request):
    # create object of form
    form = FeedBackForm(request.POST or None)
     
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
    return render(
        request, 
        "feedback.html",
        {
            "form": form
        }
    )

@sync_to_async
@require_POST
@login_required
def add_to_cart(request):
    messages.success(request, "Added to cart!")
    cart, create_new = Cart.objects.get_or_create(user=request.user)
    order = cart.order
    if create_new or cart.order is None:
        order = Order.objects.create(user=request.user)
        cart.order=order
        cart.save()
    product_id = request.POST.get('product_id')
    hours = request.POST.get('hours')
    quantity = request.POST.get('quantity')
    product = Product.objects.get(product_id=product_id)
    if product not in list(map(lambda i: i.product, order.products.iterator())):
        order.products.add(OrderedProduct.objects.create(product=product, quantity=quantity, hours=hours))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    for i in order.products.iterator():
        if i.product == product:
            i.quantity = int(quantity)
            i.hours = int(hours)
            i.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@sync_to_async
@require_POST
@login_required
def remove_from_cart(request):
    messages.warning(request, "Removed from cart!")
    cart = Cart.objects.get(user=request.user)
    product_id = request.POST.get('product_id')
    for i in cart.order.products.iterator():
        if i.product.product_id == product_id:
            cart.order.products.remove(i)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@sync_to_async
@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        total_amt = 0 if cart.order is None else sum([i.product.price*i.quantity*i.hours for i in cart.order.products.iterator()])
    except ObjectDoesNotExist:
        cart = Cart.objects.create(user=request.user)
        total_amt = 0
    if total_amt <= 0:
        messages.error(request, "Cart is empty")
        if reverse("cart") not in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(reverse("home"))
    dict_add = {
        "order": cart.order,
        "no_of_items": cart.order.products.count(),
        "total_amount": total_amt,
        "verify_details": True,
        "remove_from_cart": True,
        "title": "Cart",
    }
    if request.method == 'POST':
        current_site = get_current_site(request)
        try:
            razorpay_order = razorpay_client.order.create(
                dict(
                    amount=int(total_amt) * 100,
                    currency="INR",
                    receipt=cart.order.order_id,
                    notes={"order": str(cart.order)},
                    payment_capture="0",
            ))
            Payments.objects.create(
                order_id=cart.order.order_id,
                order_id_merchant=razorpay_order["id"],
                amount=total_amt
            )
            request.session["total_value"] = int(total_amt)
            request.session["order_id"] = cart.order.order_id
            dict_add.update({
                "razor_pay_total_amount": int(total_amt)*100,
                "razorpay_merchant_key": settings.RAZOR_KEY_ID,
                "image_url":f"{request.scheme}://{current_site.domain}{settings.STATIC_URL}img/selogo.png",
                "checkout": True,
                "verify_details": False,
                "callback_url": reverse("payment_stats_verify"),
                "razorpay_order_id": razorpay_order["id"]
            })
            messages.success(request, "Details verified, please proceed to payment")
        except Exception as e:
            messages.error(request, e)
    return render(
        request, 
        "cart.html",
        dict_add
    )


@sync_to_async
@login_required
def orders(request):
    return render(
        request, 
        "orders.html",
        {
            "orders": Order.objects.filter(user=request.user, payment=True).all()
        }
    )

@sync_to_async
@login_required
def order_details(request, order_id: str):
    try:
        order = Order.objects.get(order_id=order_id)
    except ObjectDoesNotExist:
        messages.error(request, "Order not found")
        return HttpResponseRedirect(reverse("home"))
    if not order.payment:
        messages.warning(request, "Order not paid")
        return HttpResponseRedirect(reverse("home"))

    return render(
        request, 
        "cart.html",
        {
            "order": order,
            "no_of_items": order.products.count(),
            "total_amount": sum([i.product.price*i.quantity*i.hours for i in order.products.iterator()]),
            "title": "Order Details"
        }
    )