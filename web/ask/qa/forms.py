from django import forms
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

