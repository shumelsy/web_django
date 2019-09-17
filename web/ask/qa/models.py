# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse

# Create your models here.
class QuestionManager(models.Manager):
	def new(self):
		return self.order_by('-added_at')
	def popular(self):
		return self.order_by('-rating')

class Question(models.Model):
	objects = QuestionManager()
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateTimeField(blank=True, auto_now_add=True)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	likes = models.ManyToManyField(User, related_name='question_like_user', blank=True)

	def __unicode__(self):
		return self.title

	def get_url(self):
		return reverse('question', kwargs={'id': self.id})

class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateTimeField(blank=True, auto_now_add=True)
	question = models.OneToOneField(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __unicode__(self):
		return self.author + self.added_at + self.text


