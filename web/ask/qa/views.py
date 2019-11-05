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
        try:
            answers = Answer.objects.filter(question=question)
        except Answer.DoesNotExist:
            answers = None
    except Question.DoesNotExist:
	    raise Http404
    return answer_add(request, question, answers)

def question_add(request):
    if request.method == "POST":
        print('\n', request.POST, '\n', request, '\n')
        form = AskForm(request.POST)
        if form.is_valid():
            form.clean()
            question = form.save()
            print('\nВопрос добавлен\n')
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/question_add.html', {
        'form': form,
    })

def answer_add(request, question, answers):
    if request.method == "POST":
        print('\n', request.POST, '\n', question.get_url(), '\n', request, '\n', question, '\n', answers, '\n')
        form = AnswerForm(question, request.POST)
        if form.is_valid():
            form.clean()
            answer = form.save()
            print('\nОтвет добавлен\n')
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(question)
    return render(request, 'qa/question.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })

