import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        form = UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
                # request.user.upload.delete(save=True)
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
            login(request, form.get_user())
            return redirect("index")
        print(form.errors)
        return render(request, template_name="questions/login.html", context={'form': form})




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
            question = form.save()
            return redirect('question', number=question.pk)
        return render(request, 'questions/ask.html', context={'form':form})


@require_POST
@login_required
def set_like(request):
    if request.is_ajax():

        data = json.loads(request.body)
        print(data)
        if data['question_or_comment'] == 'question':
            data['question_or_comment'] = True
            rating = Question.objects.get(pk=data['id']).set_like(user=request.user, is_like=data['like'])
        else:
            data['question_or_comment'] = False
            rating = Comment.objects.get(pk=data['id']).set_like(user=request.user, is_like=data['like'])
        print(rating)

        return JsonResponse({'count': rating, "question_or_comment": data['question_or_comment'], "id":  data['id']})
    raise Http404('this url only for ajax')

@require_POST
@login_required
def set_correct(request):
    if request.is_ajax():
        data = json.loads(request.body)
        com = Comment.objects.get(pk=data['comment_id'])
        com.correct = data['correct']
        com.save()
        return JsonResponse({'correct': True})
    raise Http404('this url only for ajax')


def hello_world(request):
    return HttpResponse("Hello World!", content_type='text/plain')

@csrf_exempt
def parametrs(request):
    body = None
    if request.method == 'GET':
        body =str(request.GET)
    elif request.method == 'POST':
        body = str(request.body)

    return HttpResponse(body, content_type='text/plain')