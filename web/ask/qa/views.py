# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout, get_user
from django.template.context_processors import csrf
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm, UserCreation


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
            question.author = request.user
            question.save()
            url = question.get_url()
            print('\nВопрос добавлен, переадресовываю на URL: ', url, '\nТекущий юзер: ', request.user)
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/question_add.html', {
        'form': form,
        'username': get_user(request).username,
    })


def answer_add(request, question, answers):
    print('\nОтрисовываю форму добавления ответа и связи с вопросом:\n request.POST = ', request.POST, ', type = ', type(request.POST), '\n requset.GET = ', request.GET, '\n request = ', request, '\n question = ', question, ', type = ', type(question), '\n question.get_url() = ', question.get_url(), '\n question.id = ', question.id, '\n answers = ', answers, '\n')
    if request.method == "POST":
        form = AnswerForm(request.POST, initial={'question': question.id})
        if form.is_valid():
            form.clean()
            answer = form.save()
            answer.author = request.user
            answer.save()
            url = question.get_url()
            print('\nОтвет добавлен, переадресовываю на URL: ', url, '\nТекущий юзер: ', request.user)
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': question.id})
    return render(request, 'qa/question.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'username': get_user(request).username,
    })


def login_user(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            sessionid = request.COOKIES
            print('\nПользователь залогинен\n sessionid = ', sessionid, '\n')
            return HttpResponseRedirect('/')
        else:
            args['login_error'] = "User or password is incorrect"
            return render_to_response('qa/login.html', args)
    else:
        return render(request, 'qa/login.html', args)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def signup_user(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)   
        print('\nРегистрация пользователя:\n request.POST = ', request.POST, '\nТекущий юзер:\n request.user = ', request.user)
        if form.is_valid():
            form.save()
            newUser = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, newUser)
            return HttpResponseRedirect('/')
    else:
        form = UserCreation()
    return render(request, 'qa/signup.html', {'form': form})

