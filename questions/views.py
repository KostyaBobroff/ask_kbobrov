from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from questions.models import *


# questions = [{"title": "title{}".format(i),
#               "text": "Something like text + {}".format(i),
#               "number_of_answers": i,
#               "tags": ['tag1', 'tag{}'.format(i),],
#               "number":i
#               } for i in range(15)]

def index(request):
    questions_paginate = paginate(Question.objects.all().prefetch_related(), request)

    return render(request, "questions/index.html", context={"questions": questions_paginate})


def get_best_questions(request):
    questions_paginate = paginate(Question.objects.get_hot(), request)
    return render(request, "questions/hot.html", context={"questions": questions_paginate, })


def get_tag_page(request, tag_name):
    # questions_by_tags = []
    # for question in questions:
    #     if tag_name in question['tags']:
    #         questions_by_tags.append(question)
    # page_name = 'tags'
    questions_paginate = paginate(Question.objects.get_by_tag(tag_name), request)
    # questions_paginate = paginate(questions_by_tags, request)
    return render(request, "questions/tagpage.html", context={"questions": questions_paginate,  'tag':tag_name})

def get_question_by_number(request, number):
    try:
        question = Question.objects.get(pk=number)
    except Question.DoesNotExist:
        question = None
    # question = questions[number]
    # answers =  [{
    #           "text": "Something like text + {}".format(i),
    #           } for i in range(10)]
    return render(request, "questions/answers.html",
                  context={"question": question})


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
    # paginator = {'current_page':request.GET.get('page'),
    #              'paginator': pag}
    # return page, paginator
    return page


def settings(request):
    return render(request, "questions/settings.html")

