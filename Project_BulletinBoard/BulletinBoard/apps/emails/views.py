from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
)
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from django.template.loader import render_to_string

from allauth.account.models import EmailAddress

from BulletinBoard.settings import DEFAULT_FROM_EMAIL
from .forms import NewsForm


class News(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    permission_required = (
        'account.view_emailaddress',
    )
    form_class = NewsForm
    template_name = 'emails/news_send.html'
    success_url = reverse_lazy('emails:send_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отправить новость'
        return context

    def form_valid(self, form):
        emailaddress_qs = EmailAddress.objects.exclude(user__groups__name='staff'
            ).filter(user__is_active=True).filter(verified=True)
        context = {
            'subject': form.cleaned_data.get('subject'),
            'message': form.cleaned_data.get('message'),
        }
        subject = render_to_string('emails/email/newsletter_subject.txt', context)
        message = render_to_string('emails/email/newsletter_message.txt', context)
        for recipient in emailaddress_qs:
            recipient.user.email_user(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
            )
        return super().form_valid(form)


class NewsSuccess(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    permission_required = (
        'account.view_emailaddress',
    )
    template_name = 'emails/news_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новость успешно отправлена.'
        return context
    