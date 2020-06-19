from django.urls import path, include
from . import views

# from rest_framework import routers

urlpatterns = (
    path('', views.IndexView.as_view(), name='home'),
    path('product/list/', views.ProductListView.as_view(), name='product_manager_product_list'),
    # path('product/create/', views.ProductCreateView.as_view(), name='product_manager_product_create'),
    path('product/detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product_manager_product_detail'),
    # path('product/update/<slug:slug>/', views.ProductUpdateView.as_view(), name='product_manager_product_update'),
    # path('product/delete/<slug:slug>/', views.ProductDeleteView.as_view(), name='product_manager_product_delete'),
    path('category/', views.CategoryListView.as_view(), name='product_manager_category_list'),
    path('category/detail/<slug:slug>/', views.CategoryDetailView.as_view(), name='product_manager_category_detail'),

    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
    path('del_wishlist/', views.del_wishlist, name='del_wishlist'),

    path('cart/', views.CartView.as_view(), name='cart'),

)
