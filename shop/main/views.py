from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from cart.forms import (CartAddProductForm, ComparisonAddProductForm,
                        FavoritesAddProductForm)
from cart.views import recently_viewed, recently_viewed_detail

from .forms import ReviewForm
from .models import Category, Product, Review


class Main_page(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'main_page.html'

    def get_context_data(self, **kwargs):
        context = super(Main_page, self).get_context_data(**kwargs)
        context['on_sale_soon'] = Product.objects.filter(on_sale_soon=True)[:5]
        context['novelties'] = Product.objects.filter(date=datetime.today(), on_sale_soon=False, available=True)[:5]
        context['favorites_product_form'] = FavoritesAddProductForm()
        context['recently_viewed'] = recently_viewed_detail(self.request)
        return context


class CategoryList(ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'category.html'


class CatalogView(ListView):
    context_object_name = 'products'
    template_name = 'catalog.html'
    paginate_by = 1

    def get_queryset(self):
        products = Product.objects.filter(category=self.kwargs['pk'])
        return products


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'productdetail.html'

    def get(self, request, *args, **kwargs):
        recently_viewed(request, kwargs['pk'])
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['comparison_product_form'] = ComparisonAddProductForm()
        context['favorites_product_form'] = FavoritesAddProductForm()
        context['reviews'] = Review.objects.filter(product=self.kwargs['pk'], is_published=True)[:3]
        return context


class ReviewList(ListView):
    context_object_name = 'reviews'
    template_name = 'review.html'
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super(ReviewList, self).get_context_data(**kwargs)
        context['product_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        products = Review.objects.filter(product=self.kwargs['pk'], is_published=True)
        return products


class ReviewCreate(CreateView):
    form_class = ReviewForm
    template_name = 'reviewcreate.html'

    def form_valid(self, form):
        product = Product.objects.get(id=self.kwargs['pk'])
        review = Review(user=self.request.user, product=product)
        form = self.form_class(self.request.POST, instance=review)
        return super().form_valid(form)


class SearchListView(ListView):
    template_name = 'search.html'
    model = Product

    def get(self, request, *args, **kwargs):
        context = {}
        question = request.GET.get('q')

        if question is not None:
            object_list = Product.objects.filter(Q(name__icontains=question), available=True).prefetch_related(
                'category')
            context['last_question'] = '?q=%s' % question
            context['len_products'] = len(object_list)
            context['categories'] = Category.objects.filter(Category__in=object_list).distinct()
            context['recently_viewed'] = recently_viewed_detail(self.request)

            current_page = Paginator(object_list, 5)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request, self.template_name, context=context)
