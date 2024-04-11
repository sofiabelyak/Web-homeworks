from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Question, Answers

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

def question(request, question_id):
    item = Question.objects.get(pk=question_id)
    paginator, answers, page_num = paginate(request, Answers.objects.get_answers(question_id), 2)
    context =  {"question" :item, "answers": answers, "paginator": paginator}
    return render(request, 'question.html', context)

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return redirect('/login')

def signup(request):
    return render(request, 'signup.html')

def settings(request):
    return render(request, 'settings.html')

def tag(request, tag_name):
    paginator, question, page_num = paginate(request, Question.objects.get_questions_by_tag(tag_name))
    context = {"tag": tag_name, "questions" :question, "paginator": paginator}
    return render(request, 'tag.html', context)
