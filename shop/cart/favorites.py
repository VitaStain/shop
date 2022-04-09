from django.conf import settings

from .cart import Cart


class Favorites(Cart):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.FAVORITES_SESSION_ID)
        if not cart:
            cart = self.session[settings.FAVORITES_SESSION_ID] = {}
        self.cart = cart
