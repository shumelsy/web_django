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
#    question = forms.IntegerField(widget=forms.HiddenInput())
    question = forms.ModelMultipleChoiceField(label='Select Question', queryset=Question.objects.all())

    def __init__(self, question_id, *args, **kwargs):
        self._id = question_id
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['question'] = self._id
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

