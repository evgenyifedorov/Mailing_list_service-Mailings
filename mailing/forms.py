from django import forms

from common.views import StyleFormMixin
from mailing.models import MailingSettings, MailingMessage
from recipient.models import Recipient


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['recipients'].queryset = Recipient.objects.filter(owner=user)
        self.fields['message'].queryset = MailingMessage.objects.filter(owner=user)

    class Meta:
        model = MailingSettings
        fields = ('sending', 'recipients', 'message', 'end_time',)


class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ('title', 'content',)


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('setting_status',)
