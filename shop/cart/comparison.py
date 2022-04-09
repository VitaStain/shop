from django.conf import settings

from main.models import Category, Product

from .cart import Cart


class Comparison(Cart):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.COMPARISON_SESSION_ID)
        if not cart:
            cart = self.session[settings.COMPARISON_SESSION_ID] = {}
        self.cart = cart

    def get_categories(self):
        categories = Product.objects.filter(id__in=self.get_all_products_id()).prefetch_related('category')
        category = Category.objects.filter(Category__in=categories).distinct()
        return category
