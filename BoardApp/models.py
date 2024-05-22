from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.core.cache import cache
from ckeditor_uploader.fields import RichTextUploadingField


class Ad(models.Model):
    TYPE = [
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('DD', 'ДД'),
        ('traders', 'Торговцы'),
        ('gildemasters', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=TYPE, default='tank')
    ad_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default='Загаловок')
    text = RichTextUploadingField(blank=True, null=True)
    upload = models.ImageField(
        upload_to='uploads/', help_text='Загрузите файл', blank=True, verbose_name='Загрузка файла'
    )

    def __str__(self):
        return f'{self.title}: {self.category}, {self.text}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    response_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default='Текст отклика')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
