from django.shortcuts import render, get_object_or_404
from .models import SneakersInstance
from django.views.generic import ListView
from django.utils import timezone
from .models import SneakersInstance

# Create your views here.


class SneakersList(ListView):
    model = SneakersInstance
    template_name = 'Shop/all_sneakers.html'


def sneaker_page(request, pk):
    sneaker_model = get_object_or_404(SneakersInstance, pk=pk)
    return render(request, 'Shop/sneaker_page.html', {'current_model': sneaker_model})


#def sneakers_list(request):
    #posts = SneakersInstance.objects.all()
    #return render(request, 'Shop/base.html', {'posts': posts})

