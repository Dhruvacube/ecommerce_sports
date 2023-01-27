from django import template
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Iterable
    from main.models import OrderedProduct

register = template.Library()

DIV_TAGS = {
    "debug": "text-grey-800 rounded-lg bg-grey-50 dark:bg-gray-800 dark:text-grey-400",
    "success": "text-green-800 rounded-lg bg-green-50 dark:bg-green-800 dark:text-green-400",
    "error": "text-red-800 rounded-lg bg-red-50 dark:bg-red-800 dark:text-red-400",
    "warning": "text-yellow-800 rounded-lg bg-yellow-50 dark:bg-yellow-800 dark:text-yellow-400",
    "info": "text-blue-800 rounded-lg bg-blue-50 dark:bg-blue-800 dark:text-blue-400",
}

BUTTON_TAGS = {
    "info": "bg-blue-50 text-blue-500 rounded-lg focus:ring-2 focus:ring-blue-400 p-1.5 hover:bg-blue-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-blue-400 dark:hover:bg-gray-700",
    "debug": "bg-grey-50 text-grey-500 rounded-lg focus:ring-2 focus:ring-grey-400 p-1.5 hover:bg-grey-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-grey-400 dark:hover:bg-gray-700",
    "success": "bg-green-50 text-green-500 rounded-lg focus:ring-2 focus:ring-green-400 p-1.5 hover:bg-green-200 inline-flex h-8 w-8 dark:bg-green-800 dark:text-green-400 dark:hover:bg-green-700",
    "error": "bg-red-50 text-red-500 rounded-lg focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex h-8 w-8 dark:bg-red-800 dark:text-red-400 dark:hover:bg-red-700",
    "warning": "bg-yellow-50 text-yellow-500 rounded-lg focus:ring-2 focus:ring-yellow-400 p-1.5 hover:bg-yellow-200 inline-flex h-8 w-8 dark:bg-yellow-800 dark:text-yellow-400 dark:hover:bg-yellow-700"
}

@register.filter(name="div_tags")
def div_tags(key: str):
    return DIV_TAGS.get(key, "text-grey-800 rounded-lg bg-grey-50 dark:bg-gray-800 dark:text-grey-400")


@register.filter(name="button_tags")
def button_tags(key: str):
    return BUTTON_TAGS.get(key, "bg-grey-50 text-grey-500 rounded-lg focus:ring-2 focus:ring-grey-400 p-1.5 hover:bg-grey-200 inline-flex h-8 w-8 dark:bg-gray-800 dark:text-grey-400 dark:hover:bg-gray-700")

@register.filter(name="give_price")
def give_price(products: 'Iterable[OrderedProduct]') -> int:
    print(products)
    return sum(list(map(lambda a: a.product.price*a.quantity*a.hours, products)))