"""ask_kboborov URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from questions import views
# from questions.views import *

urlpatterns = [
    path('', views.index, name="index"),
    path('hot/',views.get_best_questions, name="hot"),
    path("tag/<str:tag_name>/", views.get_tag_page, name="tag"),
    path("question/<int:number>/", views.QuestionByNumber.as_view(), name="question"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path('logout/', views.sign_out, name='logout'),
    path('ask/', views.AskView.as_view(), name='ask')
]
