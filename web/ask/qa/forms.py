from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from qa.models import Question, Answer

class AskForm(forms.Form):
    title = forms.CharField(label='Your Title', max_length=100)
    text = forms.CharField(label='Your Text', widget=forms.Textarea)

    def clean(self):
        pass

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(label='Your Text', widget=forms.Textarea)
    question = forms.ModelChoiceField(queryset=Question.objects.all())

    def __init__(self, *args, **kwargs):    
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return User

