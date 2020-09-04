from django.urls import reverse_lazy
from django.views.generic import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from cart.cart import Cart

from .models import Wishlist, Product, Height, Diameter, Width, NumberOfHoles, DiameterOfHoles, Color, Review, Order, OrderItem
import requests

token = '1381628865:AAESu6h386-wuLo5moCtFEZ_PYToXWsYUWs'
channel_id = '-1001419255027'
class IndexView(TemplateView):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):
        tires = Product.objects.filter(category=1, available=True)[:10]
        disks = Product.objects.filter(category=2, available=True)[:10]
        trucktires = Product.objects.filter(category=3, available=True)[:10]
        self.extra_context = {
            'tires': tires,
            'disks': disks,
            'trucktires': trucktires,
        }
        return super().get(request, *args, **kwargs)

class TireListView(ListView):
    template_name = 'shop/category_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category=1)
        season = 'any'
        if request.GET:
            if request.GET['submit'] == 'filter':
                season = request.GET['season']
                height = request.GET['height']
                width = request.GET['width']
                diameter = request.GET['diameter']

                if season != 'any':
                    queryset = queryset.filter(season=season)
                if height != 'any':
                    queryset = queryset.filter(height__height=float(height))

                if width != 'any':
                    queryset = queryset.filter(width__width=float(width))

                if diameter != 'any':
                    queryset = queryset.filter(diameter__diameter=diameter)
                sort = request.GET['sort']
                if sort == 'increase':
                    queryset = queryset.order_by('price')
                if sort == 'decrease':
                    queryset = queryset.order_by('-price')

            elif request.GET['submit'] == 'reset':
                return redirect('tires')
        self.queryset = queryset
        self.extra_context = {
            'count': self.queryset.count(),
            'heights': Height.objects.all(),
            'widths': Width.objects.all(),
            'diameters': Diameter.objects.all(),
            'season': season,
        }

        return super().get(request, *args, **kwargs)


class DiskListView(ListView):
    template_name = 'shop/category_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category=2)
        if request.GET:
            if request.GET['submit'] == 'filter':
                color = request.GET['color']
                diameter_of_holes = request.GET['diameter_of_holes']
                number_of_holes = request.GET['number_of_holes']
                width = request.GET['width']
                diameter = request.GET['diameter']
                if color != 'any':
                    queryset = queryset.filter(season=color)
                if diameter_of_holes != 'any':
                    queryset = queryset.filter(height__height=float(diameter_of_holes))
                if number_of_holes != 'any':
                    queryset = queryset.filter(height__height=float(number_of_holes))
                if width != 'any':
                    queryset = queryset.filter(width__width=float(width))
                if diameter != 'any':
                    queryset = queryset.filter(diameter__diameter=diameter)
            elif request.GET['submit'] == 'reset':
                return redirect('disks')
        self.queryset = queryset
        self.extra_context = {
            'count': self.queryset.count(),
            'widths': Width.objects.all(),
            'diameters': Diameter.objects.all(),
            'number_of_holes': NumberOfHoles.objects.all(),
            'diameter_of_holes': DiameterOfHoles.objects.all(),
            'colors': Color.objects.all(),
        }

        return super().get(request, *args, **kwargs)


class TruckTireListView(ListView):
    template_name = 'shop/category_detail.html'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(category=3)
        season = 'any'
        if request.GET:
            if request.GET['submit'] == 'filter':
                season = request.GET['season']
                height = request.GET['height']
                width = request.GET['width']
                diameter = request.GET['diameter']

                if season != 'any':
                    queryset = queryset.filter(season=season)
                if height != 'any':
                    queryset = queryset.filter(height__height=float(height))

                if width != 'any':
                    queryset = queryset.filter(width__width=float(width))

                if diameter != 'any':
                    queryset = queryset.filter(diameter__diameter=diameter)
                sort = request.GET['sort']
                if sort == 'increase':
                    queryset = queryset.order_by('price')
                if sort == 'decrease':
                    queryset = queryset.order_by('-price')
            elif request.GET['submit'] == 'reset':
                return redirect('trucktires')
        self.queryset = queryset
        self.extra_context = {
            'count': self.queryset.count(),
            'heights': Height.objects.all(),
            'widths': Width.objects.all(),
            'diameters': Diameter.objects.all(),
            'season': season,
        }

        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product


class WishlistView(ListView):
    template_name = 'shop/wishlist.html'

    def get(self, request, *args, **kwargs):
        self.queryset = Wishlist.objects.filter(user_id=request.user.id)
        return super().get(request, *args, **kwargs)

@login_required(login_url="/users/login")
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

@login_required(login_url="/users/login")
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


@login_required(login_url="/users/login")
def write_review(request):
    product_id = request.POST['product']
    rating = request.POST['rating']
    comment = request.POST['comment']
    product = Product.objects.get(id=product_id)

    Review.objects.create(product_id=product_id, rating=rating, comment=comment, user=request.user)
    return redirect('/product/' + str(product_id))



@login_required(login_url="/users/login")
def checkout(request):
    pass

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class CheckoutView(TemplateView):
    template_name = 'shop/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        l = []
        for c in cart.cart.values():
            l.append(float(c['price']) * int(c['quantity']))
        total_price = sum(l)
        print(total_price)
        self.extra_context = {
            'total': total_price,
        }


        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        cart = Cart(request)
        fitst_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        address = request.POST['address']

        phone_number = request.POST['phone_number']
        comment = request.POST['comment']
        payment_method = request.POST['payment_method']

        user = request.user
        user.first_name = fitst_name
        user.last_name = last_name
        user.city = city
        user.address = address
        user.phone_number = phone_number
        user.save()

        order = Order.objects.create(user=user, payment_method=payment_method)

        for item in cart.cart.values():
            product = Product.objects.get(id=int(item['product_id']))
            OrderItem.objects.create(order=order,  product=product, price=item['price'], quantity=item['quantity'])


        cart.clear()
        return HttpResponse('Заказ принят')
        # return super().get(request, *args, **kwargs)