from django import http
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

"""
def index(request: http.HttpRequest) -> http.HttpResponse:
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
"""

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

"""
def detail(request:http.HttpRequest, question_id:int) -> http.HttpResponse:
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise http.Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return http.HttpResponse(render(request, 'polls/detail.html', {'question': question}))
"""

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def results(request: http.HttpRequest, question_id:int) -> http.HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""

def vote(request: http.HttpRequest, question_id:int) -> http.HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') +1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
