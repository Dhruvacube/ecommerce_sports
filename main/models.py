import random
import string

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from django.core.validators import MaxValueValidator


def random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class Category(models.Model):
    name = models.CharField(max_length=50, help_text=_("Enter the name of the category"))
    description = models.TextField(_("Description"), help_text=_("Enter the description of the category"), blank=True, null=True)
    
class Product(models.Model):
    product_id = models.CharField(default=random_id, max_length=10, primary_key=True)
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.SET_NULL)
    image = FilerImageField(related_name="product_image", on_delete=models.RESTRICT)
    description = models.TextField(help_text=_("Enter the description of the product"))
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Enter the price of the product in ruppess in per hour rate"))


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, related_name="ordered_product", on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text=_("Enter the quantity of the product"))
    hours = models.IntegerField(help_text=_("Enter the rent hours of the product"))
    

class Order(models.Model):
    order_id = models.CharField(default=random_id, max_length=10, primary_key=True)
    products = models.ManyToManyField(OrderedProduct, related_name="order_products")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order_user", on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    
class FeedBack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="feedback_user", on_delete=models.CASCADE)
    feedback = models.TextField(help_text=_("Enter the feedback"))
    rating = models.PositiveIntegerField(help_text=_("Enter the rating out of 5"),validators=[MaxValueValidator(5)])
    order = models.ForeignKey(Order, related_name="feedback_order", on_delete=models.CASCADE)

class Testimonials(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="testimonials_user", on_delete=models.CASCADE)
    feedback = models.TextField(help_text=_("Enter the feedback"))
    rating = models.PositiveIntegerField(help_text=_("Enter the rating out of 5"),validators=[MaxValueValidator(5)])
    product = models.ForeignKey(Product, related_name="testimonials_order", on_delete=models.CASCADE)
    