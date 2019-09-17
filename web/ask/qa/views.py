# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from qa.models import Question, Answer
from django.http import Http404

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def template(request):
    return render(request, 'qa/index.html')

def question_list_all(request):
#	questions = Question.objects.all()
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
#	questions = Question.objects.all()
        questions = Question.objects.popular()
        limit = request.GET.get('limit', 10)
        page = request.GET.get('page', 1)
        paginator = Paginator(questions, limit)
        paginator.baseurl = '/?page='
        page = paginator.page(page)
        return render(request, 'qa/paginator.html', {
                'questions': page.object_list,
                'paginator': paginator, 'page': page,
        })

def one_question(request, num):
	try:
		question = Question.objects.get(id=num)
		try:
			answer = Answer.objects.get(question=question)
		except Answer.DoesNotExist:
			answer = None
	except Question.DoesNotExist:
		raise Http404
	return render(request, 'qa/question.html', {
		'question': question,
		'answer': answer,
	})

