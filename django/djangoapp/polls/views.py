from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Count
from .models import Question, Choice
# Create your views here.

# def index(request):
#     """[polls/views/index]

#     Args:
#         request ([HTTP]): [Request]

#     Returns:
#         [Render]: [Request, url, Dict(Questions.objects.all())]
#     """
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "latest_question_list" : latest_question_list
#         })

# def detail(request, question_id):
#     """[polls/views/detail]

#     Args:
#         request ([HTTP]): [Request]
#         question_id ([Query]): [Object]

#     Returns:
#         [Render]: [Request, url, Questions.objects.get(pk = question_id)]
#     """
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/detail.html", {
#         "question" : question
#         })

# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/results.html", {
#         "question" : question
#     })


class IndexView(generic.ListView):
    template_name =  "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):        
        """Return the last five published questions, that have at least two questions"""
        question = Question.objects.filter(pub_date__lte=timezone.now())
        question = question.alias(entries=Count("choice")).filter(entries__gte=1)
        return question.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Exclude any questions that aren't published yet
        """
        return Question.objects.filter(pub_date__lte = timezone.now())
    
class ResultView(DetailView):
    template_name = "polls/results.html"

    def get_queryset(self):
        return Question.objects.alias(entries=Count("choice")).filter(entries__gte=1)
    


def vote(request, question_id):
    """[polls/views/vote]

    Args:
        request ([HTTP]): [Request]
        question_id ([Query]): [Objects]

    Returns:
        [Render]: [Request, url, Questions.objects.get(pk = question_id), "No elegiste una respuesta"]
        [HttpResponseReditect] : [url(polls/question_id/results)]
    """
    
    
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])   
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question" : question,
            "error_message" : "No elegiste una respuesta"
        })
        
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))