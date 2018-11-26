from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from questions.models import *
from django.views import View
from questions.forms import SignUpForm, SignInForm, UserSettingsForm


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


# def login(request):
#     return render(request, "questions/login.html")


class SignUp(View):

    def get(self, request):
       form = SignUpForm()
       return render(request, "questions/signup.html", context={'form': form})

    def post(self,request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # login(request, user)
            return redirect("index")
        return render(request, "questions/signup.html", context={'form': form} )


# def signup(request):
#     return render(request, "questions/signup.html")
#

# class AddQuestion(View):
#
#     def get(self, request):
#         form =QuestionForm()
#         return render(request, "questions/ask.html", context={'form': form})
#
#     def post(self, request):
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             form

# def add_question(request):
#     return  render(request, "questions/ask.html")


def paginate(objects_list, request):
    pag = Paginator(objects_list, 3)
    try:
        page = pag.get_page(request.GET.get('page'))
    except PageNotAnInteger:
        page = pag.get_page(1)
    except EmptyPage:
        page = pag.get_page(pag.num_pages)
    return page

#
# def settings(request):
#     return render(request, "questions/settings.html")


class SettingsView(View):
    def get(self, request):
        form = UserSettingsForm(instance=request.user)
        return render(request, template_name="questions/settings.html", context={'form':form})

    def post(self, request):
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            # user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
                form.save()
                return redirect("index")
        print(form.errors)
        return render(request, template_name="questions/settings.html", context={'form': form})

class LoginView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, template_name='questions/login.html', context={'form':form})

    def post(self, request):
        form = SignInForm(data=request.POST)
        if form.is_valid():
            # user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
                login(request, form.get_user())
                return redirect("index")
        print(form.errors)
        return render(request, template_name="questions/login.html", context={'form': form})

            # user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
            # if user is not None:
            #     login(request, user)
            # else:
            #     pass

def questions_form(request):
    return render(request, 'questions_form.html', {'form':QuestionForm()})


def sign_out(request):
    logout(request)
    return redirect('index')