import razorpay
from django.conf import settings
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
)

from main.models import GameGroup

from .models import *

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "payment_id_merchant",
        "order_id_merchant",
        "amount",
        "payment_status",
        "created_at",
    )
    list_filter = (("payment_status", ChoiceDropdownFilter), "created_at")
    search_fields = list_display + ("orders_list", )
    readonly_fields = (
        "orders_list",
        "created_at",
        "payment_id_merchant",
        "order_id_merchant",
        "order",
    )
    list_per_page = 30

    fieldsets = (
        (
            _("Order ID"),
            {
                "fields":
                ("order", "payment_id_merchant", "order_id_merchant")
            },
        ),
        (_("Amount"), {
            "fields": ("amount", )
        }),
        (
            _("Status"),
            {
                "fields": (
                    "payment_status",
                    "created_at",
                )
            },
        ),
        (_("Orders List"), {
            "fields": ("orders_list", )
        }),
    )

    def refund_the_payment(self, request, queryset):
        for i in queryset:
            if i.payment_status == "S":
                try:
                    a = razorpay_client.payment.refund(i.payment_id_merchant,
                                                       i.amount * 100)
                    game_grup_model = GameGroup.objects.filter(payment_id=i)
                    game_grup_model.delete()
                    i.payment_status = "R"
                    i.save()
                    print("Done")
                except Exception as e:
                    print("Exception occurred:", e)
                    print("Payment request object", i)
        self.message_user(
            request,
            ngettext(
                "%d refund done successfully. Excluding the exception",
                "%d refunds were done successfully. Excluding the exception",
                len(queryset),
            ) % int(len(queryset)),
            messages.SUCCESS,
        )

    refund_the_payment.short_description = "Initiate the refund process"

    actions = [refund_the_payment]

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff