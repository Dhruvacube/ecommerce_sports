import random
import string

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from django.core.validators import MaxValueValidator, MinValueValidator


def random_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class Category(models.Model):
    name = models.CharField(max_length=50, help_text=_("Enter the name of the category"), unique=True, db_index=True)
    image = FilerImageField(related_name="category_image", on_delete=models.RESTRICT, help_text=_("Upload the image of the category")) 
    description = models.TextField(_("Description"), help_text=_("Enter the description of the category"), blank=True, null=True, db_index=True)
    
    class Meta:
        verbose_name_plural = _("Categories")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.CharField(default=random_id, max_length=10, primary_key=True, db_index=True)
    name = models.CharField(max_length=150, help_text=_("Enter the name of the product"), db_index=True)
    category = models.ForeignKey(Category, related_name="product_category", on_delete=models.SET_NULL, null=True, db_index=True)
    image = FilerImageField(related_name="product_image", on_delete=models.RESTRICT)
    description = models.TextField(help_text=_("Enter the description of the product"), db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text=_("Enter the price of the product in ruppess in per hour rate"), db_index=True)
    out_of_stock = models.BooleanField(default=False)
    quantity_available = models.PositiveIntegerField(default=1, help_text=_("Enter the quantity of the product available"), db_index=True)
    carousel_entry = models.BooleanField(default=False, help_text=_("Check if you want to add this product to the carousel"), db_index=True)
    products_carousel_images = models.ManyToManyField("filer.Image", related_name="carousel_images", symmetrical=False, blank=True, db_index=True)
    def __str__(self):
        return self.name


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, related_name="ordered_product", on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(help_text=_("Enter the quantity of the product"),validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
    hours = models.PositiveIntegerField(help_text=_("Enter the rent hours of the product"),validators=[MinValueValidator(1)], db_index=True)
    

class Order(models.Model):
    order_id = models.CharField(default=random_id, max_length=10, primary_key=True, db_index=True)
    products = models.ManyToManyField(OrderedProduct, related_name="order_products", db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order_user", on_delete=models.CASCADE, db_index=True)
    payment = models.BooleanField(default=False, db_index=True)
    payment_date = models.DateTimeField(null=True, db_index=True)
    
    class Meta:
        ordering = ['-payment_date']
    
    def __str__(self) -> str:
        return self.order_id + ": " + self.user.username
    
class Cart(models.Model):
    order = models.ForeignKey(Order, related_name="cart_order", on_delete=models.CASCADE, null=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cart_user", on_delete=models.CASCADE, db_index=True)
    
    def __str__(self) -> str:
        return "Cart of " + self.user.username
    
class FeedBack(models.Model):
    email = models.EmailField(help_text=_("Enter the email"))
    feedback = models.TextField(help_text=_("Enter the feedback"))
    
    def __str__(self) -> str:
        return self.email

class Testimonial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="testimonials_user", on_delete=models.CASCADE, db_index=True)
    feedback = models.TextField(help_text=_("Enter the feedback"), db_index=True)
    rating = models.PositiveIntegerField(help_text=_("Enter the rating out of 5"),validators=[MaxValueValidator(5)], db_index=True)
    product = models.ForeignKey(Product, related_name="testimonials_order", on_delete=models.CASCADE, db_index=True)
    
    def __str__(self) -> str:
        return self.product.name + '-' + self.user.username
    