import datetime

from django.test import TestCase
from django.urls import reverse
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


def create_question(question_text, days):
    pub_date = timezone.now() + datetime.timedelta(days=days)
    # question = models.Question(question_text=question_text, pub_date=pub_date)
    # question.save()
    # return question
    return models.Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available now.')
        self.assertQuerySetEqual(response.context_data['latest_question_list'], [])

    def test_past_question(self):
        question = create_question('Past Question', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context_data['latest_question_list'], [question])

    def test_future_question(self):
        create_question('Future Question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context_data['latest_question_list'], [])
        self.assertContains(response, 'No polls are available now.')

    def test_future_question_and_past_question(self):
        question = create_question('Past Question', -30)
        create_question('Future Question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context_data['latest_question_list'], [question])

    def test_two_past_questions(self):
        question0 = create_question('Past Question 1', -30)
        question1 = create_question('Past Question 2', -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context_data['latest_question_list'], [question1, question0])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        question = create_question('Future Question', 30)
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        question = create_question('Past Question', -30)
        # question.question_text = "HAHA"
        response = self.client.get(reverse('polls:detail', args=(question.id,)))
        self.assertEqual(response.context_data['question'], question)
