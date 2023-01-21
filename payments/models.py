from django.db import models

# Create your models here.
class PaymentSession(models.Model):
    stripe_session_id = models.CharField(max_length=250)
    order = models.ForeignKey("main.Order", related_name="payment_session_order", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)