from django.contrib import admin
from .models import ImageSneakers, Brand, WayToUse, Sneakers, SneakersInstance, ShopUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.


class ShopUserInLine(admin.StackedInline):
    model = ShopUser
    can_delete = False
    verbose_name_plural = 'shop_user'


class UserAdmin(BaseUserAdmin):
    inlines = (ShopUserInLine,)


admin.site.register(ImageSneakers)
admin.site.register(Brand)
admin.site.register(WayToUse)
admin.site.register(Sneakers)
admin.site.register(SneakersInstance)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
