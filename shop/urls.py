from django.urls import path, include
from . import views

# from rest_framework import routers

urlpatterns = (
    path('', views.IndexView.as_view(), name='home'),
    path('tires/', views.TireListView.as_view(), name='tires'),
    # path('disks/', views.DiskListView.as_view(), name='disks'),
    path('trucktires/', views.TruckTireListView.as_view(), name='trucktires'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_manager_product_detail'),
    # path('product/update/<slug:slug>/', views.ProductUpdateView.as_view(), name='product_manager_product_update'),
    # path('product/delete/<slug:slug>/', views.ProductDeleteView.as_view(), name='product_manager_product_delete'),
    # path('category/', views.CategoryListView.as_view(), name='product_manager_category_list'),
    # path('category/detail/<slug:slug>/', views.CategoryDetailView.as_view(), name='product_manager_category_detail'),

    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('del_wishlist/', views.del_wishlist, name='del_wishlist'),

    path('cart/', views.CartView.as_view(), name='cart'),

    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    path('write_review/', views.write_review, name='write_review'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
)
