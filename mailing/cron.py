import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from config import settings
from mailing.models import MailingSettings, MailingStatus, LOGS_STATUS_CHOICES


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.filter(first_datetime__lte=current_datetime).filter(
        setting_status__in=['Create'])

    for mailing in mailings:
        title = mailing.message.title
        content = mailing.message.content
        mailing.setting_status = 'Started'
        mailing.save()
        try:
            server_response = send_mail(
                subject=title, message=content, from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.recipients.all()], fail_silently=False)
            if server_response == 1:
                server_response = 'Письмо успешно отправлено'
                MailingStatus.objects.create(status=LOGS_STATUS_CHOICES[0][1], mailing_response=server_response,
                                             mailing_list=mailing)

            mailing.setting_status = 'Create'

            if mailing.sending == 'daily' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='daily')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=1)
                mailing.setting_status = 'Create'

            elif mailing.sending == 'weekly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='weekly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=7)
                mailing.setting_status = 'Create'

            elif mailing.sending == 'monthly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='monthly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=30)
                mailing.setting_status = 'Create'

            mailing.save()

        except smtplib.SMTPException as error:
            MailingStatus.objects.create(status=LOGS_STATUS_CHOICES[1][1], mailing_response=error,
                                         mailing_list=mailing)
            mailing.setting_status = 'Create'
# import smtplib
# import pytz
#
# from django.core.mail import send_mail
# from datetime import datetime, timedelta
# from mailing.models import MailingSettings, MailingStatus,LOGS_STATUS_CHOICES
# from config import settings
# from dateutil.relativedelta import relativedelta
#
#
# def send_mailing():
#     zone = pytz.timezone(settings.TIME_ZONE)
#     current_time = datetime.now(zone)
#
#     mailing_settings = MailingSettings.objects.filter(first_datetime__lte=current_time).filter(
#         settings_status__in=['Create', 'Started'])
#     for mailing in mailing_settings:
#         if mailing.next_datetime is None:
#             mailing.next_datetime = current_time
#         title = mailing.message.title
#         content = mailing.message.content
#         mailing.setting_status = 'Started'
#         mailing.save()
#         try:
#             if mailing.end_time < mailing.next_datetime:
#                 mailing.next_datetime = current_time
#                 mailing.setting_status = 'Done'
#                 mailing.save()
#                 continue
#             if mailing.next_datetime <= current_time:
#                 server_response = send_mail(
#                     subject=title,
#                     message=content,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[recipient.email for recipient in mailing.recipients.all()],
#                     fail_silently=False,
#                 )
#                 if server_response == 1:
#                     server_response = 'Сообщение отправлено'
#                 MailingStatus.objects.create(status='success', mailing_response=server_response, mailing_id=mailing)
#
#                 if mailing.sending_period == 'daily':
#                     mailing.next_datetime = current_time + timedelta(days=1)
#
#                 elif mailing.sending_period == 'weekly':
#                     mailing.next_datetime = current_time + timedelta(days=7)
#
#                 elif mailing.sending_period == 'monthly':
#                     mailing.next_datetime = current_time + relativedelta(months=1)
#
#             mailing.save()
#
#         except smtplib.SMTPException as error:
#             MailingStatus.objects.create(status='fail', mailing_response=error, mailing_id=mailing)