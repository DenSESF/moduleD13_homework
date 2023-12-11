import os

from django.conf import settings
from django.urls import reverse_lazy
from django.db import models


class Image(models.Model):
    image = models.ImageField()

    def delete_file(self):
        if self.image.name is None:
            return False
        FILEDIR = '/'.join(str(self.image).split('/')[0:-1])
        self.image.delete()
        HOMEDIR = str(settings.MEDIA_ROOT) + '/'
        if next(os.scandir(HOMEDIR + FILEDIR), None) is None:
            os.rmdir(HOMEDIR + FILEDIR)
        return True


class Advert(models.Model):
    TANKS = 'TK'
    DMAGERS = 'DD'
    HEALERS = 'HL'
    TRADERS = 'TD'
    GUILDMASTERS = 'GL'
    QUESTGIVERS = 'QG'
    BLACKSMITHS = 'BS'
    TANNERS = 'TN'
    POTIONMAKERS = 'PM'
    SPELLCASTERS = 'SC'
    CATEGORYS = [
        (TANKS, 'Танки'),
        (DMAGERS, 'ДД'),
        (HEALERS, 'Хилы'),
        (TRADERS, 'Торговцы'),
        (GUILDMASTERS, 'Гилдмастеры'),
        (QUESTGIVERS, 'Квестгиверы'),
        (BLACKSMITHS, 'Кузнецы'),
        (TANNERS, 'Кожевники'),
        (POTIONMAKERS, 'Зельевары'),
        (SPELLCASTERS, 'Мастера заклинаний'),
    ]
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    header = models.TextField(max_length=120, blank=False)
    text = models.TextField(blank=True)
    video = models.FileField(blank=True)
    image = models.ManyToManyField(Image, through='AdvertImage', blank=True)
    category = models.CharField(
        max_length=2,
        choices=CATEGORYS,
        default=TANKS
    )
    
    def delete_file(self):
        if self.video.name is None:
            return False
        FILEDIR = '/'.join(str(self.video).split('/')[0:-1])
        self.video.delete()
        HOMEDIR = str(settings.MEDIA_ROOT) + '/'
        if next(os.scandir(HOMEDIR + FILEDIR), None) is None:
            os.rmdir(HOMEDIR + FILEDIR)
        return True
    
    def __str__(self):
        return f'{self.id}. {self.header}'

    @property
    def category_name(self):
        return self.get_category_display()

    def get_absolute_url(self):
        return reverse_lazy('pages:advert_detail', args=[str(self.pk)])
    
    class Meta:
        ordering = ('-pk',)


class AdvertImage(models.Model):
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Reply(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    accept = models.BooleanField(default=False)
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('pages:advert_detail', args=[self.advert.pk])
