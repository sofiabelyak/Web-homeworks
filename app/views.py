from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": f"This is question number {i}",
        "tag": ['tag1', 'tag2', 'tag3'],
    } for i in range(10)
]

ANSWERS = [
    {
        "text": f"This is answer number {i}" 
    } for i in range(5)
]

def paginate(request, object_list, per_page = 5):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, per_page)
    page_obj = paginator.page(page_num)
    return paginator, page_obj, page_num

def index(request):
    paginator, question, page_num = paginate(request, QUESTIONS)
    return render(request,'base.html', {"questions": question, "paginator": paginator })

def hot(request):
    paginator, question, page_num = paginate(request, QUESTIONS)
    return render(request,'hot.html', {"questions": question, "paginator": paginator })

def question(request, question_id):
    item = QUESTIONS[question_id]
    paginator, answers, page_num = paginate(request, ANSWERS, 2)
    return render(request, 'question.html', {"question" :item, "answer": answers, "paginator": paginator})

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
    for q in QUESTIONS:
        q["tags"] = tag_name
    paginator, question, page_num = paginate(request, QUESTIONS)
    return render(request, 'tag.html', {"tag": tag_name, "questions" :question, "paginator": paginator})
