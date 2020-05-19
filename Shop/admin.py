from django.contrib import admin
from .models import ImageSneakers, Brand, WayToUse, Sneakers, SneakersInstance

# Register your models here.

admin.site.register(ImageSneakers)
admin.site.register(Brand)
admin.site.register(WayToUse)
admin.site.register(Sneakers)
admin.site.register(SneakersInstance)
