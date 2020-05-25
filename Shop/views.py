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
from .models import SneakersInstance
from .forms import SneakersForm
import logging
# Create your views here.

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': '/home/eugene/PycharmProjects/lab_3_4_django/lab_3_4_django/debug.log'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
})

logger = logging.getLogger(__name__)


class SneakersList(ListView):
    model = SneakersInstance
    logger.debug("Show all sneakers")
    template_name = 'Shop/all_sneakers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def sneaker_page(request, pk):
    sneaker_model = get_object_or_404(SneakersInstance, pk=pk)
    logger.debug("Show sneakers instance")
    return render(request, 'Shop/sneaker_page.html', {'current_model': sneaker_model})


def edit_page(request, pk):
    sneaker_model = get_object_or_404(SneakersInstance, pk=pk)
    if request.method == 'POST':
        if 'save' in request.POST:
            logger.debug("Edit current sneakers")
            form = SneakersForm(request.POST, instance=sneaker_model)
            if form.is_valid():
                sneaker_model = form.save(commit=False)
                sneaker_model.save()
                return redirect('sneaker_page', pk=sneaker_model.pk)

        if 'new' in request.POST:
            logger.debug("Add new sneakers")
            return redirect('new_page')

        if 'delete' in request.POST:
            form = SneakersForm(request.POST, instance=sneaker_model)
            if form.is_valid():
                logger.debug("Delete current sneakers")
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
    logger.debug("Send mail")
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
        logger.error("Something goes wrong...")
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        logger.debug("Verification complete")
        user.shopuser.verified = True
        user.save()
        return redirect('base_page')
    else:
        return HttpResponse('Activation link is invalid!')
