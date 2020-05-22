from django.shortcuts import render, get_object_or_404, redirect
from .models import SneakersInstance
from django.views.generic import ListView
from django.utils import timezone
from .models import SneakersInstance
from .forms import SneakersForm

# Create your views here.


class SneakersList(ListView):
    model = SneakersInstance
    template_name = 'Shop/all_sneakers.html'


def sneaker_page(request, pk):
    sneaker_model = get_object_or_404(SneakersInstance, pk=pk)
    return render(request, 'Shop/sneaker_page.html', {'current_model': sneaker_model})


def edit_page(request, pk):
    sneaker_model = get_object_or_404(SneakersInstance, pk=pk)
    if request.method == 'POST':
        if 'save' in request.POST:
            form = SneakersForm(request.POST, instance=sneaker_model)
            if form.is_valid():
                sneaker_model = form.save(commit=False)
                sneaker_model.save()
                return redirect('sneaker_page', pk=sneaker_model.pk)

        if 'new' in request.POST:
            return redirect('new_page')

        if 'delete' in request.POST:
            form = SneakersForm(request.POST, instance=sneaker_model)
            if form.is_valid():
                sneaker_model.delete()
                return redirect('base_page')
    else:
        form = SneakersForm(instance=sneaker_model)
    return render(request, 'Shop/edit_page.html', {'form': form})


def new_page(request):
    if request.method == 'POST':
        form = SneakersForm(request.POST)
        if form.is_valid():
            sneaker_model = form.save(commit=False)
            sneaker_model.save()
            return redirect('base_page')
    else:
        form = SneakersForm()
    return render(request, 'Shop/new_page.html', {'form': form})


#def sneakers_list(request):
    #posts = SneakersInstance.objects.all()
    #return render(request, 'Shop/base.html', {'posts': posts})

