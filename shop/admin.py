from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created', 'modified']
    prepopulated_fields = {'slug': ('title',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'detailpageurl', 'name', 'slug', 'description', 'short', 'price', 'sale_price',
                    'available', 'stock', 'created_at', 'updated_at', 'views', 'manufacturer']
    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductImageInline]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['wished_item', 'user', 'added_date']

