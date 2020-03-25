from django.urls import reverse_lazy
from django.views.generic import *


from .models import Product, Category



class IndexView(ListView):
    template_name = 'shop/index.html'

    def get_queryset(self):
        return Product.objects.order_by('-id')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'categories': categories
        })
        return context

class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'categories': categories
        })
        return context
class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'categories': categories
        })
        return context



class CategoryListView(ListView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context.update({
            'categories': categories
        })
        return context

class CategoryDetailView(DetailView):
    """ Allows you to view details of a category (will be used for inline product display). """
    model = Category

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the current category taken from above context.
        context['products_in_category'] = Product.objects.filter(category=context['object'])
        context['categories'] = Category.objects.all()
        return context