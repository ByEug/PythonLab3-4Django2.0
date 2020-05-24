from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import SneakersInstance, ShopUser
from .forms import SneakersForm
# Create your views here.


class SneakersList(ListView):
    model = SneakersInstance
    template_name = 'Shop/all_sneakers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


def send_mail(request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    user = User.objects.get(username=request.user.username)
    message = render_to_string('Shop/active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = request.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return render(request, 'Shop/base.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.shopuser.verified = True
        user.save()
        return redirect('base_page')
    else:
        return HttpResponse('Activation link is invalid!')
