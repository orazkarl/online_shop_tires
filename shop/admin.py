from django.contrib import admin
from .models import *


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'slug', 'description', 'created', 'modified']
#     prepopulated_fields = {'slug': ('title',)}


class TireImageInline(admin.TabularInline):
    model = TireImage
    raw_id_fields = ['tire']
    extra = 1


@admin.register(Tire)
class TiretAdmin(admin.ModelAdmin):
    list_display = ['name', 'short', 'price']
    prepopulated_fields = {'slug': ('name',)}

    inlines = [TireImageInline]

class DiskImageInline(admin.TabularInline):
    model = DiskImage
    raw_id_fields = ['disk']
    extra = 1


@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ['name',  'short', 'price']
    prepopulated_fields = {'slug': ('name',)}

    inlines = [DiskImageInline]
# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ['wished_item', 'user', 'added_date']

