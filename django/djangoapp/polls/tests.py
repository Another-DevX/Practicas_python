import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given question_text, and published the given number of days offset to now 
    (negative to questions published in the past, positive for questions that have yet to be published)
    """
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(pk, choice_text):
    question = Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text = choice_text)


#Testing Models
class QuestionModelTests(TestCase):
    """
    Define a battery of test for Models
    """
    def test_was_published_recently_with_future_questions(self):
        """
        was_published_recenty returns False for questions whose pub_date is in the future
        """        
        future_question = create_question("¿Quién es el mejor Course Director de Platzi?",days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recenty_with_past_questions returns False for questions whose pub_date is in the past"""
        past_question = create_question("¿Quién es el mejor Course Director de Platzi?",days=-30)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_today_questions(self):
        """was_published_recenty returns True for questions whose pub_date is today"""
        today_question = create_question("¿Quién es el mejor Course Director de Platzi?",days=0)
        self.assertIs(today_question.was_published_recently(), True)

#Testing Views
class QuestionIndexViewTests(TestCase):
    """
    Define a battery of test for Views
    """
    def test_no_questions(self):
        """
        If no question exist, an appropiate message is displayed
        """
        response = self.client.get(reverse('polls:index')) #bring the results of polls index over a http request response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avalible.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_questions_with_future_pub_date(self):
        """
        Questions with date greater to timezone.now shouldn't be displayed at index
        """
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are avalible.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])

    def test_questions_with_past_pub_date(self):
        """
        Questions with date in the past to timezone.now should be displayed at index
        """
        question = create_question("Past question", days=-10)
        create_choice(question.pk, "choice")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past questions are displayed
        """
        past_question = create_question(question_text="Past question", days=-30)
        create_choice(past_question.pk, "choice")
        future_question = create_question(question_text="Future question", days=30)
        create_choice(future_question.pk, "choice")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[past_question])
        
    def test_two_past_questions(self):
        past_question1 = create_question(question_text="Past question1", days=-30)
        create_choice(past_question1.pk, "choice")
        past_question2 = create_question(question_text="Past question2", days=-30)
        create_choice(past_question2.pk, "choice")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question2, past_question1]
        )
    def test_two_future_questions(self):
        future_question1 = create_question(question_text="Future question1", days=30)
        future_question2 = create_question(question_text="Future question2", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )
        
    def test_question_has_no_choices(self):
        """
        If a question has no choices, the question can't be displayed
        """
        create_question(question_text="question", days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
            
    def test_question_has_choices(self):
        """
        If a question has choices, the question can be displayed
        """
        question = create_question(question_text="question", days=-2)
        create_choice(pk=question.pk,choice_text="choice")
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
        
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 error not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url =  reverse("polls:detail", args=(future_question.pk,))
        response =  self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The detail of view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-30)
        url =  reverse("polls:detail", args=(past_question.pk,))
        response =  self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
class QuestionResultViewTests(TestCase):
    def test_future_question_result(self):
        """
        The result view of a question with a pub_date in the future returns a 404 error not found
        """
        future_question = create_question(question_text="Future question", days=30)
        url =  reverse("polls:results", args=(future_question.pk,))
        response =  self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question_result(self):
        """
        The result of view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past question", days=-30)
        create_choice(past_question.id,"choice")
        url =  reverse("polls:results", args=(past_question.pk,))
        response =  self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    def test_question_has_no_choices(self):
        """
        If a question has no choices, the question can't be displayed
        """
        question = create_question(question_text="question", days=-2)
        response = self.client.get(reverse("polls:results", args=(question.pk,)))
        self.assertEqual(response.status_code, 404)
        
        
        
    def test_question_has_choices(self):
        """
        If a question has choices, the question can be displayed
        """
        question = create_question(question_text="question", days=-2)
        create_choice(pk=question.id,choice_text="choice")
        response = self.client.get(reverse("polls:results", args=(question.pk,)))
        self.assertEqual(response.status_code, 200)
        
        
        