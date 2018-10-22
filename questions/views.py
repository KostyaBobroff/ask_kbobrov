from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
# class AboutView(TemplateView):
#     template_name = "about.html"
questions = [{"title": "title{}".format(i),
              "text": "Something like text + {}".format(i),
              "number_of_answers": i,
              "tags": ['tag1', 'tag{}'.format(i),],
              "number":i
              } for i in range(10)]

def index(request):

    page_name = 'index'
    page, paginator = paginate(questions, request)

    return render(request, "questions/index.html", context={"questions": page, "page_name":page_name, 'paginator': paginator})


def get_best_questions(request):
    page_name = 'hot'
    return render(request, "questions/hot.html", context={"questions": questions, "page_name": page_name})


def get_tag_page(request, tag_name):
    questions_by_tags = []
    for question in questions:
        if tag_name in question['tags']:
            questions_by_tags.append(question)
    page_name = 'tags'
    return render(request, "questions/tagpage.html", context={"questions": questions_by_tags, "page_name": page_name, 'tag':tag_name})

def get_question_by_number(request, number):
    question = questions[number]
    answers =  [{
              "text": "Something like text + {}".format(i),
              } for i in range(10)]
    return render(request, "questions/answers.html",
                  context={"question": question, 'answers': answers})


def login(request):
    return render(request, "questions/login.html")


def signup(request):
    return render(request, "questions/signup.html")


def add_question(request):
    return  render(request, "questions/ask.html")


def paginate(objects_list, request):
    pag = Paginator(objects_list, 3)

    page = pag.get_page(request.GET.get('page'))
    page.number
    paginator = {'current_page':request.GET.get('page'),
                 'paginator': pag}
    return page, paginator


def settings(request):
    return render(request, "questions/settings.html")