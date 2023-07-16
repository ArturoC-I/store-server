from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models import Product, ProductCategory, Basket
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    # def get_context_data(self, **kwargs):
    #    context = super(IndexView, self).get_context_data()
    #    context['title'] = 'Store'
    #    return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


# class ProductDetailView(TitleMixin, DetailView):
#    model = Product
#    template_name = 'products/product_card.html'
#    title = 'Store - Каталог'

def product(request, product_id):
    product_item = Product.objects.get(id=product_id)
    context = {'title': 'Store',
               'product_item': product_item}
    return render(request, 'products/product_card.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def index(request):
#    context = {'title': 'Store'}
#    return render(request, 'products/index.html', context)


# def products(request, category_id=None, page_number=1):
#    if category_id:
#        products = Product.objects.filter(category_id=category_id)
#    else:
#        products = Product.objects.all()

#    per_page = 3
#    paginator = Paginator(products, per_page)
#    products_paginator = paginator.page(page_number)

#    context = {'title': 'Store - Каталог',
#               'categories': ProductCategory.objects.all(),
#               'products': products_paginator,
#               }
#    return render(request, 'products/products.html', context)
