# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
	objects = QuestionManager()
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateTimeField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	likes = models.ManyToManyField(User, related_name='question_like_user')

class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateTimeField(blank=True)
	question = models.OneToOneField(Question)
	author = models.CharField(max_length=50)

class QuestionManager(models.Manager):
	def new():
		return self.order_by('-added_at')
	def popular():
		return self.order_by('-rating')


