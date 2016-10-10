from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail
# from django.core import mail
from search_img.models import *


@shared_task
def send_message():
    tags = SearchResult.objects.get_tags_per_day()
    results = ''
    if tags:
        for tag_ in tags:
            results += str(tag_['tag__name']) + ' '
        return send_mail(
                'Subject here',
                results,
                'natasha.kuskova@gmail.com',
                ['natasha.kuskova@gmail.com'],
                fail_silently=False,
        )
    # email = mail.EmailMessage('Subject', 'lalala', to=['natasha.kuskova@gmail.com'])
    #
    # email.send()
