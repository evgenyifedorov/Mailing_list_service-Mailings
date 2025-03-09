import smtplib
import pytz

from django.core.mail import send_mail
from datetime import datetime, timedelta
from mailing.models import MailingSettings, MailingStatus
from config import settings
from dateutil.relativedelta import relativedelta


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.filter(first_datetime__lte=current_datetime).filter(
        setting_status__in=['Create', 'Started'])

    for mailing in mailings:
        if mailing.first_datetime is None:
            mailing.first_datetime = current_datetime
        title = mailing.message.title
        content = mailing.message.content
        mailing.setting_status = 'Started'
        mailing.save()
        try:
            if mailing.end_time < mailing.first_datetime:
                mailing.first_datetime = current_datetime
                mailing.setting_status = 'Done'
                mailing.save()
                continue
            if mailing.first_datetime <= current_datetime:
                server_response = send_mail(
                    subject=title,
                    message=content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient.email for recipient in mailing.recipients.all()],
                    fail_silently=False,
                )
                if server_response == 1:
                    server_response = 'Письмо успешно отправлено'
                MailingStatus.objects.create(status='success', mailing_response=server_response, mailing_list=mailing)

                if mailing.sending == 'daily':
                    mailing.first_datetime = current_datetime + timedelta(days=1)

                elif mailing.sending == 'weekly':
                    mailing.first_datetime = current_datetime + timedelta(days=7)

                elif mailing.sending == 'monthly':
                    mailing.first_datetime = current_datetime + relativedelta(months=1)

            mailing.save()

        except smtplib.SMTPException as error:
            MailingStatus.objects.create(status='fail', mailing_response=error, mailing_list=mailing)
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