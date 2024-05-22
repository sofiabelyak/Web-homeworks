from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Answers, LikeQuestion, LikeAnswer
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, SignupForm, EditForm, AskQuestion, GiveAnswer

from app.models import Profile


def paginate(request, object_list, per_page = 5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, per_page)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return paginator, page_obj, page_num

def index(request):
    paginator, question, page_num = paginate(request, Question.objects.get_last_questions())
    context = {"questions" : question, "paginator": paginator}
    return render(request,'base.html', context)

def hot(request):
    paginator, question, page_num = paginate(request, Question.objects.get_hot_questions()[0:10])
    context = {"questions": question, "paginator": paginator }
    return render(request,'hot.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def question(request, question_id):
    item = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = GiveAnswer(request.POST)
        if form.is_valid():
            profile = request.user.profile if hasattr(request.user, 'profile') else Profile.objects.create(user=request.user)
            form.save(question=item, profile=profile)
            return HttpResponseRedirect(reverse('question', kwargs={'question_id': question_id}))
    else:
        form = GiveAnswer()
    paginator, answers, page_num = paginate(request, Answers.objects.get_answers(question_id), 2)
    context = {
        "question": item,
        "answers": answers,
        "paginator": paginator,
        "form": form
    }
    return render(request, 'question.html', context)



@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        form = AskQuestion()
    if request.method == 'POST':
        form = AskQuestion(request.POST)
        if form.is_valid():
            profile = request.user.profile if hasattr(request.user, 'profile') else Profile.objects.create(user=request.user)
            question = form.save(profile=profile)
            question.date = timezone.now()
            question.author_id = request.user.id
            question.save()
            return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, 'ask.html', {'form': form})




@csrf_protect
@require_http_methods(['GET', 'POST'])
def log_in(request):
    continue_url = request.GET.get('continue', '/')
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(continue_url)
        login_form.add_error('password', 'Invalid username or password')

    return render(request, "login.html", context={"form": login_form, "continue": continue_url})

@csrf_protect
def signup(request):
    if request.method == 'GET':
        signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(data=request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect(reverse('index'))
    return render(request, 'signup.html', {'form': signup_form})

@csrf_protect
def log_out(request):
    next_url = request.META.get('HTTP_REFERER', '/')
    logout(request)
    return redirect(next_url)


@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    if request.method == 'GET':
        edit_form = EditForm()
    if request.method == 'POST':
        edit_form = EditForm(data=request.POST)
        if edit_form.is_valid():
            user = edit_form.save()
            login(request, user)
    return render(request, 'settings.html', {'form': edit_form})

def tag(request, tag_name):
    paginator, question, page_num = paginate(request, Question.objects.get_questions_by_tag(tag_name))
    context = {"tag": tag_name, "questions" :question, "paginator": paginator}
    return render(request, 'tag.html', context)
