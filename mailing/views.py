from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from mailing.forms import MailingMessageForm, MailingSettingsForm, MailingModeratorForm
from mailing.models import MailingMessage, MailingSettings
from mailing.services import get_blog_from_cache
from recipient.models import Recipient


class MailingMessageTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blogs'] = get_blog_from_cache()
        mailing_settings = MailingSettings.objects.all()
        context_data['mailing_settings'] = len(mailing_settings)
        active_mailings = MailingSettings.objects.filter(setting_status='Started')
        context_data['active_mailings'] = len(active_mailings)
        recipients = Recipient.objects.all()
        context_data['recipient'] = len(recipients)
        return context_data


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list')


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:list')


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage


class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailingMessage


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def form_valid(self, form):
        settings = form.save()
        settings.owner = self.request.user
        settings.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingSettingsForm
        if user.has_perm('mailing.change_mailingsettings_setting_status'):
            return MailingModeratorForm
        return PermissionDenied

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings_list')
