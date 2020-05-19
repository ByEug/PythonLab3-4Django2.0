from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import uuid

# Create your models here.


class ImageSneakers(models.Model):

    name = models.CharField(max_length=100, default="sneakers")
    image = models.ImageField()


class Brand(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    #def get_absolute_url(self):
        #return reverse('brand-detail', args=[str(self.id)])


class WayToUse(models.Model):

    way = models.CharField(max_length=100)

    def __str__(self):
        return self.way


class Sneakers(models.Model):

    sneakers_name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    way_to_use = models.ManyToManyField(WayToUse)

    #def get_absolute_url(self):
        #return reverse('sneakers-detail', args=[str(self.id)])


class SneakersInstance(models.Model):

    image = models.ForeignKey(ImageSneakers, on_delete=models.SET_NULL, null=True)
    Sneakers_info = models.ForeignKey(Sneakers, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=30)
    amount = models.IntegerField()
    size = models.IntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.Sneakers_info.sneakers_name)

