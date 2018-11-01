from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from questions.models import *



def index(request):
    questions_paginate = paginate(Question.objects.get_new(), request)

    return render(request, "questions/index.html", context={"questions": questions_paginate})


def get_best_questions(request):
    questions_paginate = paginate(Question.objects.get_hot(), request)
    return render(request, "questions/hot.html", context={"questions": questions_paginate, })


def get_tag_page(request, tag_name):
    questions_paginate = paginate(Question.objects.get_by_tag(tag_name), request)
    return render(request, "questions/tagpage.html", context={"questions": questions_paginate,  'tag':tag_name})

def get_question_by_number(request, number):
    return render(request, "questions/answers.html",
                  context={"question": get_object_or_404(Question,pk=number) })


def login(request):
    return render(request, "questions/login.html")


def signup(request):
    return render(request, "questions/signup.html")


def add_question(request):
    return  render(request, "questions/ask.html")


def paginate(objects_list, request):
    pag = Paginator(objects_list, 3)
    try:
        page = pag.get_page(request.GET.get('page'))
    except PageNotAnInteger:
        page = pag.get_page(1)
    except EmptyPage:
        page = pag.get_page(pag.num_pages)
    return page


def settings(request):
    return render(request, "questions/settings.html")

