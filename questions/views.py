from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from questions.models import *
from django.views import View
from questions.forms import SignUpForm, SignInForm, UserSettingsForm, CommentForm, AskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import resolve

def index(request):
    questions_paginate = paginate(Question.objects.get_new(), request)
    return render(request, "questions/index.html", context={"questions": questions_paginate})


def get_best_questions(request):
    questions_paginate = paginate(Question.objects.get_hot(), request)
    return render(request, "questions/hot.html", context={"questions": questions_paginate, })


def get_tag_page(request, tag_name):
    questions_paginate = paginate(Question.objects.get_by_tag(tag_name), request)
    return render(request, "questions/tagpage.html", context={"questions": questions_paginate,  'tag':tag_name})


class QuestionByNumber(View):

    def get(self, request, number):
        form = CommentForm()
        return render(request, "questions/answers.html",context={"question": get_object_or_404(Question,pk=number), 'form': form })

    def post(self, request, number):
        form = CommentForm( request.user.pk, number,request.POST)
        if form.is_valid():
            form.save()
            form = CommentForm()
        return render(request, "questions/answers.html",
                      context={"question": get_object_or_404(Question, pk=number), 'form': form})

# def get_question_by_number(request, number):
#     return render(request, "questions/answers.html",
#                   context={"question": get_object_or_404(Question,pk=number) })

class SignUp(View):

    def get(self, request):
       form = SignUpForm()
       return render(request, "questions/signup.html", context={'form': form})

    def post(self,request):
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        return render(request, "questions/signup.html", context={'form': form} )



def paginate(objects_list, request):
    pag = Paginator(objects_list, 3)
    try:
        page = pag.get_page(request.GET.get('page'))
    except PageNotAnInteger:
        page = pag.get_page(1)
    except EmptyPage:
        page = pag.get_page(pag.num_pages)
    return page




class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserSettingsForm(instance=request.user)
        return render(request, template_name="questions/settings.html", context={'form':form})

    def post(self, request):
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
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
            print(resolve)
            # user = authenticate(request, username=form.cleaned_data.get('login'), password=form.cleaned_data.get('password'))
            login(request, form.get_user())
            return redirect("index")
        print(form.errors)
        return render(request, template_name="questions/login.html", context={'form': form})



# def questions_form(request):
#     return render(request, 'questions/answers.html', {'form':CommentForm()})

@login_required
def sign_out(request):
    logout(request)
    return redirect('index')


class AskView(LoginRequiredMixin, View):

    def get(self, request):
        form = AskForm()
        return render(request, 'questions/ask.html', context={'form':form})

    def post(self, request):
        form = AskForm(request.user.pk, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'questions/ask.html', context={'form':form})

#
# def ask(request):
#     return render(request, 'questions/ask.html')