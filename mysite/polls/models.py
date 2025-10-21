import datetime

from django.db import models
from django.utils import timezone

from .utilities import get_timstamp_path

from django.contrib.auth.models import AbstractUser


class PolUser(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to=get_timstamp_path, verbose_name="Аватар")

    class Meta(AbstractUser.Meta):
        pass


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='date published', default=timezone.now())
    expiration_time = models.DateTimeField(verbose_name='expiration date', default=(timezone.now() + datetime.timedelta(days=2)))
    description = models.TextField(verbose_name='description', max_length=650, default='')
    short_description = models.CharField(verbose_name='short_description', max_length=50, default='')
    image = models.ImageField(blank=True, upload_to=get_timstamp_path, verbose_name="image", default=None)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=2)

    def was_expired(self):
        return self.expiration_time <= timezone.now()

    def short_description_former(self):
        
        chars = 0
        result = ""
        for i in self.description:
           result += i
           chars += 1
           if chars >= 45:
                break
        result += '...'
        self.short_description = result

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.choice_text

class ChoisedQuestions(models.Model):
    user = models.ForeignKey(PolUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('user', 'question'),)