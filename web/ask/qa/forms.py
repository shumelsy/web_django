from django import forms
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

class UserCreation(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput, help_text='Password is be required')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').lower()
        try:
            user_name = User.objects.get(username=username)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(u'Username ***{}*** is already exists.'.format(username))
        
    def clean_email(self):
        bad_domains = ['mail.ru', 'gmail.ru', 'yandex.com']
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in bad_domains:
            raise forms.ValidationError(u'Registration with email ***{}*** is prohibited'.format(email_domain))
        return self.cleaned_data['email']

    def save(self):
        user = User.objects.create_user(**self.cleaned_data)
        user.save()
        return user

