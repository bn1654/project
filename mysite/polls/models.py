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
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

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