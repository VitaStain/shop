from django.conf import settings

from .cart import Cart


class RecentlyViewed(Cart):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.RECENTLY_SESSION_ID)
        if not cart:
            cart = self.session[settings.RECENTLY_SESSION_ID] = {}
        self.cart = cart
