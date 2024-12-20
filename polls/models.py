import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Recently published',
    )
    def was_published_recently(self):
        now = timezone.now()
        # return self.pub_date <= now and self.pub_date >= now - datetime.timedelta(days=1)
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=False,
        ordering='choice_count',
        description='Number of choices',
    )
    def num_of_choices(self) -> int:
        return self.choice_set.count()

    # def __eq__(self, other):
    #     if other is None:
    #         return False
    #     else:
    #         return self.pub_date == other.pub_date and self.question_text == other.question_text and self.id == other.id

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text