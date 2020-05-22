from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import Shop.views
import uuid
from django.conf import settings


urlpatterns = [
    path('', Shop.views.SneakersList.as_view(), name='base_page'),
    path('sneakers/<uuid:pk>/', Shop.views.sneaker_page, name='sneaker_page'),
    path('sneakers/<uuid:pk>/edit/', Shop.views.edit_page, name='edit_page'),
    path('new/', Shop.views.new_page, name='new_page'),
]
