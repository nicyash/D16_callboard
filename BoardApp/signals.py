from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from .models import UserResponse


@receiver(post_init, sender=UserResponse)
def pre(instance, **kwargs):
    instance.old_status = instance.status


@receiver(post_save, sender=UserResponse)
def response_created(instance, created, **kwargs):
    if created:
        user = User.objects.filter(email=instance.ad.author.email)
        email = user[0].email

        subject = f'Новый отклик'

        text_content = (
            f'Отклик: {instance.text}\n\n'
            f'Для перехода нажмите: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Отклик: {instance.text}<br><br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">Для перехода нажмите</a>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    if instance.old_status != instance.status:
        user = User.objects.filter(email=instance.author.email)
        email = user[0].email
        subject = f'Отклик принят'
        text_content = (
            f'Ваш отклик был принят. '
        )
        html_content = (
            f'Ваш отклик был принят.<br><br>'
        )
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
