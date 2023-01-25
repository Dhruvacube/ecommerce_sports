import random
import string

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, MaxLengthValidator


def random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class Category(models.Model):
    name = models.CharField(max_length=50, help_text=_("Enter the name of the category"), unique=True)
    description = models.TextField(_("Description"), help_text=_("Enter the description of the category"), blank=True, null=True)
    
    class Meta:
        verbose_name_plural = _("Categories")
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id = models.CharField(default=random_id, max_length=10, primary_key=True)
    name = models.CharField(max_length=150, help_text=_("Enter the name of the product"))
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.SET_NULL, null=True)
    image = FilerImageField(related_name="product_image", on_delete=models.RESTRICT)
    description = models.TextField(help_text=_("Enter the description of the product"))
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Enter the price of the product in ruppess in per hour rate"))
    out_of_stock = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, related_name="ordered_product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text=_("Enter the quantity of the product"),validators=[MinValueValidator(1), MaxValueValidator(5)])
    hours = models.PositiveIntegerField(help_text=_("Enter the rent hours of the product"),validators=[MinValueValidator(1)])
    

class Order(models.Model):
    order_id = models.CharField(default=random_id, max_length=10, primary_key=True)
    products = models.ManyToManyField(OrderedProduct, related_name="order_products")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order_user", on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)
    
class Cart(models.Model):
    order = models.ForeignKey(Order, related_name="cart_order", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cart_user", on_delete=models.CASCADE)
    
class FeedBack(models.Model):
    email = models.EmailField(help_text=_("Enter the email"))
    feedback = models.TextField(help_text=_("Enter the feedback"))

class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="testimonials_user", on_delete=models.CASCADE)
    feedback = models.TextField(help_text=_("Enter the feedback"))
    rating = models.PositiveIntegerField(help_text=_("Enter the rating out of 5"),validators=[MaxValueValidator(5)])
    product = models.ForeignKey(Product, related_name="testimonials_order", on_delete=models.CASCADE)
    