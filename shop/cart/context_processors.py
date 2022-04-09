from .cart import Cart
from .comparison import Comparison
from .favorites import Favorites


def cart(request):
    return {'cart': Cart(request)}


def favorites(request):
    return {'favorites': Favorites(request)}


def comparison(request):
    return {'comparison': Comparison(request)}
