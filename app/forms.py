from django.utils import timezone
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

from app.models import Profile, Question, Tag, User, Answers

class LoginForm(forms.Form):

    username = forms.CharField(min_length = 4, max_length=15)
    password = forms.CharField(min_length= 4, widget=forms.PasswordInput)


    def clean_username(self):
        try:
            username = self.cleaned_data.get('username')
            user = User.objects.get(username = username)
            return user
        except:
            raise ValidationError('User is not found')

    def save(self, **kwargs):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)



class SignupForm(forms.ModelForm):
    username = forms.CharField(min_length= 4)
    password = forms.CharField(min_length= 4, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length= 4, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password' ]
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            raise ValidationError('This username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise ValidationError('This email already exists')
        return email

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data.get('repeat_password')
        password = self.cleaned_data.get('password')
        if password != repeat_password:
            raise ValidationError('Password must be similar')
        return repeat_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    



class EditForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(required=False)
    username = forms.CharField(min_length= 4, required= False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]




class GiveAnswer(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answers
        fields = ['text']

    def save(self, question, profile, commit=True):
        answer = super().save(commit=False)
        answer.question = question
        answer.profile = profile
        answer.updated_at = timezone.now()
        if commit:
            answer.save()
        return answer
    

class AskQuestion(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    tag = forms.CharField(required=True)

    class Meta:
        model = Question
        fields = ['text', 'tag']
    def save(self, profile, **kwargs):
        text = self.cleaned_data.get('text')
        tag = self.cleaned_data.get('tag')
        date = timezone.now()
        
        question = Question.objects.create(text=text, updated_at=date, profile=profile)
        
        if tag:
            tags_list = [tag.strip() for tag in tag.split()]
            
            for tag_name in tags_list:
                if tag_name:
                    tag_instance, _ = Tag.objects.get_or_create(name=tag_name)
                    question.tag.add(tag_instance)

        return question


