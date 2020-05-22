from django import forms
from .models import SneakersInstance


class SneakersForm(forms.ModelForm):

    class Meta:
        model = SneakersInstance
        fields = ('image', 'Sneakers_info', 'color', 'amount', 'size')
