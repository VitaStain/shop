from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView

from main.models import CallBack, Order, Order_Product, Product, VirtualOrder

from .cart import Cart
from .comparison import Comparison
from .favorites import Favorites
from .forms import (CartAddProductForm, ComparisonAddProductForm,
                    FavoritesAddProductForm, OrderForm,
                    RecentlyViewedProductForm, VirtualOrderForm)
from .recentlyviewed import RecentlyViewed


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'detail.html', {'cart': cart})


@require_POST
def comparison_add(request, product_id):
    comparison = Comparison(request)
    product = get_object_or_404(Product, id=product_id)
    form = ComparisonAddProductForm(request.POST)
    if form.is_valid():
        comparison.add(product=product)
    return redirect(request.META.get('HTTP_REFERER'))


def comparison_detail(request):
    comparison = Comparison(request)
    for item in comparison:
        item['update_quantity_form'] = ComparisonAddProductForm(initial={'update': True})
    return render(request, 'comparison.html', {'comparison': comparison})


def comparison_remove(request, product_id):
    comparison = Comparison(request)
    product = get_object_or_404(Product, id=product_id)
    comparison.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))


@require_POST
def favorites_add(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    form = FavoritesAddProductForm(request.POST)
    if form.is_valid():
        favorites.add(product=product)
    return redirect(request.META.get('HTTP_REFERER'))


def favorites_detail(request):
    favorites = Favorites(request)
    for item in favorites:
        item['update_quantity_form'] = FavoritesAddProductForm(initial={'update': True})
    return render(request, 'favorites.html', {'favorites': favorites})


def favorites_remove(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    favorites.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))


def recently_viewed(request, product_id):
    recently_viewed = RecentlyViewed(request)
    product = get_object_or_404(Product, id=product_id)
    form = RecentlyViewedProductForm(request.POST)
    if form.is_valid():
        recently_viewed.add(product=product)
    return redirect(request.META.get('HTTP_REFERER'))


def recently_viewed_detail(request):
    recently_viewed = RecentlyViewed(request)
    if len(recently_viewed) < 5:
        products = Product.objects.filter(top_sales=True)[:5]
        for product in products:
            recently_viewed.add(product=product)
    for item in recently_viewed:
        item['update_quantity_form'] = RecentlyViewedProductForm(initial={'update': True})
    return recently_viewed


class VirtualOrderCreate(CreateView):
    form_class = VirtualOrderForm
    template_name = 'virtualorder.html'
    success_url = '/'

    def form_valid(self, form):
        cart = Cart(self.request)
        products = Product.objects.filter(id__in=cart.get_all_products_id())
        order = VirtualOrder(phone=form.cleaned_data['phone'])
        order.save()
        order.products.set(products)
        cart.clear()
        return redirect(self.success_url)


class OrderCreate(CreateView):
    form_class = OrderForm
    template_name = 'order.html'
    success_url = '/'

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save(commit=False)
        order.price = cart.get_total_price()
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order = form.save()
        for i in cart.cart.items():
            product = Product.objects.get(id=i[0])
            Order_Product.objects.create(order=order, product=product, number=i[1]['quantity'])
        cart.clear()
        return redirect(order.get_absolute_url())

    def get_initial(self):
        if self.request.user.is_authenticated:
            self.initial.update({
                'phone': self.request.user.phone,
                'email': self.request.user.email,
                'name': self.request.user.username,
            })
        return super().get_initial()


@receiver(post_save, sender=Order)
def order_message(sender, **kwargs):
    send_mail(
        'Заказ',
        f'Ваш заказ принят на обработку, номер вашего заказа {kwargs["instance"].id}',
        'vitalikstain@inbox.ru',
        [kwargs["instance"].email],
    )


@require_POST
def call_back(request):
    CallBack.objects.create(phone=request._post['callback'])
    return redirect(request.META.get('HTTP_REFERER'))


class OrderDetail(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'orderdetail.html'


class OrderList(ListView):
    context_object_name = 'orders'
    template_name = 'orderlist.html'

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders
