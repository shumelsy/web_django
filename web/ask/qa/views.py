# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def template(request):
    return render(request, 'qa/index.html')

def question_list_all(request):
	questions = Question.objects.new()
	limit = request.GET.get('limit', 10)
	page = request.GET.get('page', 1)
	paginator = Paginator(questions, limit)
	paginator.baseurl = '/?page='
	page = paginator.page(page)
	return render(request, 'qa/paginator.html', {
		'questions': page.object_list,
		'paginator': paginator, 'page': page,
	})

def popular_question_list(request):
        questions = Question.objects.popular()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, limit)
        paginator.baseurl = '/popular/?page='
        page = paginator.page(page)
        return render(request, 'qa/paginator.html', {
                'questions': page.object_list,
                'paginator': paginator, 'page': page,
        })

def one_question(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        print('\nНахожу нужный вопрос:\n question_id = ', question_id, ', question = ', question, '\n')
        try:
            answers = Answer.objects.filter(question=question)
        except Answer.DoesNotExist:
            answers = None
    except Question.DoesNotExist:
	    raise Http404
    return answer_add(request, question, answers)

def question_add(request):
    print('\nОтрисовываю форму добавления вопроса:\n request.POST = ', request.POST, ', request = ', request, '\n')
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form.clean()
            question = form.save()
            url = question.get_url()
            print('\nВопрос добавлен, переадресовываю на URL: ', url, '\n')
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/question_add.html', {
        'form': form,
    })

def answer_add(request, question, answers):
    print('\nОтрисовываю форму добавления ответа и связи с вопросом:\n request.POST = ', request.POST, ', type = ', type(request.POST), '\n requset.GET = ', request.GET, '\n request = ', request, '\n question = ', question, ', type = ', type(question), '\n question.get_url() = ', question.get_url(), '\n question.id = ', question.id, '\n answers = ', answers, '\n')
    if request.method == "POST":
        form = AnswerForm(request.POST, initial={'question': question.id})
        if form.is_valid():
            form.clean()
            answer = form.save()
            url = question.get_url()
            print('\nОтвет добавлен, переадресовываю на URL: ', url, '\n')
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request, 'qa/question.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })

