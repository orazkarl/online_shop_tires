from django.urls import reverse_lazy
from django.views.generic import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from .models import Wishlist, Product, Height, Diameter, Width


class IndexView(TemplateView):
    template_name = 'shop/index.html'

    # def get_queryset(self):
    #     return Product.objects.order_by('-id')[:10]
    #
    # def get_context_data(self, **kwargs):
    #
    #     context = super().get_context_data(**kwargs)
    #     categories = Category.objects.all()
    #     context.update({
    #         'categories': categories
    #     })
    #     return context


class TireListView(ListView):
    template_name = 'shop/category_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category=1)

        if request.GET:
            season = request.GET['season']
            height = request.GET['height']
            width = request.GET['width']
            diameter = request.GET['diameter']

            if season != 'any':
                print(queryset)
                queryset = queryset.filter(season=season)
            if height != 'any':
                queryset = queryset.filter(height__height=float(height))
                print(queryset)
            if width != 'any':
                queryset = queryset.filter(width__width=float(width))
                print(queryset)
            if diameter != 'any':
                print(queryset)
                queryset = queryset.filter(diameter__diameter=diameter)
        self.queryset = queryset
        self.extra_context = {
            'count': self.queryset.count(),
            'heights': Height.objects.all(),
            'widths': Width.objects.all(),
            'diameters': Diameter.objects.all(),
        }

        return super().get(request, *args, **kwargs)


class DiskListView(ListView):
    template_name = 'shop/category_detail.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(category=2)
        self.extra_context = {
            'count': self.queryset.count(),

        }

        return super().get(request, *args, **kwargs)


# class TireDetailView(DetailView):
#     model = Tire
#
# class DiskDetailView(DetailView):
#     model = Disk


class ProductDetailView(DetailView):
    model = Product


# class ProductListView(ListView):
#     model = Product
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Category.objects.all()
#         context.update({
#             'categories': categories
#         })
#         return context
# from django.views.generic.edit import FormMixin


#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
# categories = Category.objects.all()
# context.update({
#     'categories': categories
# })
# return context


# class CategoryListView(ListView):
#     model = Category
#     pass
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = Category.objects.all()
#         context.update({
#             'categories': categories
#         })
#         return context

# class CategoryDetailView(ListView):
#     """ Allows you to view details of a category (will be used for inline product display). """
#     # model = Category
#     template_name = 'shop/category_detail.html'
#
#     def get(self, request, *args, **kwargs):
#         if 'disk' in request.path:
#             print('asd')
#             self.queryset = Disk.objects.all()
#         context = super().get(request, *args, **kwargs)
#         return context
# def get_context_data(self, **kwargs):
#     # Call the base implementation first to get a context
#     context = super().get_context_data(**kwargs)
#     # Add in a QuerySet of the current category taken from above context.
#     context['products_in_category'] = Product.objects.filter(category=context['object'])
#     # context['categories'] = Category.objects.all()
#     return context


class WishlistView(ListView):
    template_name = 'shop/wishlist.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Wishlist.objects.filter(user_id=request.user.id)
        return super().get(request, *args, **kwargs)


def add_wishlist(request):
    user = request.user
    product_id = request.GET['product_id']

    url = 'wishlist'

    item = get_object_or_404(Product, id=product_id)
    if not Wishlist.objects.filter(user_id=user.id, product_item=item):
        Wishlist.objects.create(user_id=user.id, product_item=item)
    wishlist_counter = Wishlist.objects.filter(user_id=request.user.id).count()
    user.wishlist_counter = wishlist_counter
    user.save()

    return redirect(url)


def del_wishlist(request):
    user = request.user

    product_id = request.GET['product_id']

    item = get_object_or_404(Product, id=product_id)
    if Wishlist.objects.filter(user_id=user.id, product_item=item):
        Wishlist.objects.filter(user_id=user.id, product_item=item).delete()
    wishlist_counter = Wishlist.objects.filter(user_id=request.user.id).count()
    user.wishlist_counter = wishlist_counter
    user.save()
    return redirect('/wishlist')


class CartView(TemplateView):
    template_name = 'shop/cart.html'


@login_required(login_url="/accounts/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect('cart_detail')


@login_required(login_url="/accounts/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_detail(request):
    cart = Cart(request)
    l = []
    for c in cart.cart.values():
        l.append(float(c['price']) * int(c['quantity']))
    total_price = sum(l)

    return render(request, 'shop/cart.html', {'total': total_price})
