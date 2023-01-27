import razorpay
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from post_office import mail
from post_office.models import EmailTemplate

from main.models import Order, Cart
from main.tasks import mail_queue

from .models import Payments

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))


@sync_to_async
@require_POST
@csrf_exempt
@login_required
def payment_stats(request):
    payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")
    try:
        result = razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id":razorpay_order_id,
            "razorpay_payment_id":payment_id,
            "razorpay_signature":signature,
        })
        if result:
            try:
                # capture the payemt
                razorpay_client.payment.capture(
                    payment_id,
                    int(request.session["total_value"]) * 100
                )
            except:
                messages.error(
                    request,
                    "Couldn't verify the payment signature!",
                )
                return HttpResponsePermanentRedirect(reverse("cart"))
            Payments.objects.filter(
                order_id=request.session["order_id"],
                order_id_merchant=razorpay_order_id,
                amount=int(request.session["total_value"]),
            ).update(payment_id_merchant=payment_id, payment_status="S")
            
            Order.objects.filter(order_id=request.session["order_id"]).update(
                payment=True
            )
            Cart.objects.filter(user=request.user).delete()
            messages.success(
                request,
                "Order Confirmed! You have successfully paid the amount!"
            )
            redirect_link = reverse("orders")
            current_site = get_current_site(request)
            ctx = {
                "user": request.user,
                "domain": current_site.domain,
                "username": request.user.username,
                "protocol": "https" if request.is_secure() else "http",
                "receipt_id": request.session.get("order_id"),
                "amount": request.session.get("total_value"),
            }
            if not EmailTemplate.objects.filter(name="payment_mail").exists():
                message = render_to_string("pay_mail.html")
                EmailTemplate.objects.create(
                    name="payment_mail",
                    description="Mail to send after payment",
                    subject="You have successfully made the payment for Sportszy Products",
                    html_content=message,
                )
            mail.send(
                request.user.email,
                settings.EMAIL_HOST_USER,
                template="payment_mail",
                context=ctx,
            )
            mail_queue.delay()
    except Payments.DoesNotExist:
        messages.error(request, "The transaction does not exists")
        redirect_link = reverse("cart")
    except Exception as e:
        messages.error(
            request,
            e,
        )
        redirect_link = reverse("cart")
    try:
        del request.session["order_id"]
    except:
        pass
    try:
        del request.session["total_value"]
    except:
        pass
    return HttpResponsePermanentRedirect(redirect_link)
