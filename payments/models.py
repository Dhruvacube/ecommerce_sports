from django.db import models
from django.utils.timezone import now
import uuid
from django.utils.translation import gettext_lazy as _

class Payments(models.Model):
    order = models.ForeignKey(
        "main.Order",
        help_text=_("The order ID by which the system refers"),
    )
    payment_id_merchant = models.CharField(
        default=uuid.uuid4,
        help_text=_("The Payment ID by which the Razorpay refers"),
        null=True,
        blank=True,
        max_length=250,
    )
    order_id_merchant = models.CharField(
        help_text=_("The Order ID by which the Razorpay refers"),
        null=True,
        blank=True,
        max_length=250,
    )
    amount = models.IntegerField()
    payment_status = models.CharField(
        max_length=250,
        help_text=_("The status of payment"),
        choices=(
            ("P", "Pending"),
            ("F", "Failed"),
            ("S", "Success"),
            ("R", "Refund Done"),
        ),
        default="P",
    )
    orders_list = models.TextField(help_text=_("The orders list value"))
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name_plural = "Payments"
        ordering = ("-created_at", )