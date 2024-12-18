import datetime

from django.test import TestCase
from django.utils import timezone

from polls import models


# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently(self):
        question = models.Question(pub_date=timezone.now() + datetime.timedelta(days=30))
        # self.assertTrue(question.was_published_recently())
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        question = models.Question(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        question = models.Question(pub_date=timezone.now() - datetime.timedelta(minutes=30))
        self.assertTrue(question.was_published_recently())