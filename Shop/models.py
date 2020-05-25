from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import uuid

# Create your models here.


class ShopUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.shopuser.save()


class ImageSneakers(models.Model):

    name = models.CharField(max_length=100, default="sneakers")
    image = models.ImageField(upload_to='images/')


class Brand(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WayToUse(models.Model):

    way = models.CharField(max_length=100)

    def __str__(self):
        return self.way


class Sneakers(models.Model):

    sneakers_name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    way_to_use = models.ManyToManyField(WayToUse)


class SneakersInstance(models.Model):

    image = models.ForeignKey(ImageSneakers, on_delete=models.SET_NULL, null=True)
    Sneakers_info = models.ForeignKey(Sneakers, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=30)
    amount = models.IntegerField()
    size = models.IntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.Sneakers_info.sneakers_name)
