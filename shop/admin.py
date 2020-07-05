from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created', 'modified']
    prepopulated_fields = {'slug': ('title',)}
# admin.site.register(Product)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'price']
    # prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductImageInline]



@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'added_date']

admin.site.register(Height)
admin.site.register(Width)
admin.site.register(Diameter)
admin.site.register(NumberOfHoles)
admin.site.register(DiameterOfHoles)
admin.site.register(Color)