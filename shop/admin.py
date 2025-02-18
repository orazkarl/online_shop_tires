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
    filter_horizontal = ['city']

    inlines = [ProductImageInline]



# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = [ 'user', 'added_date']

admin.site.register(Height)
admin.site.register(Width)
admin.site.register(Diameter)
# admin.site.register(NumberOfHoles)
# admin.site.register(DiameterOfHoles)
# admin.site.register(Color)
admin.site.register(Review)
admin.site.register(City)



from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from allauth.account.admin import EmailAddress
from allauth.socialaccount.admin import SocialApp, SocialAccount,SocialToken
admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(Site)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created','payment_method', 'address', 'phone', 'is_paid', 'get_total_cost']

    def address(selfs, obj):
        return f"{obj.user.city}, {obj.user.address}"

    def phone(selfs, obj):
        return f"{obj.user.email}, {obj.user.phone_number}"


    inlines = [OrderItemInline]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


