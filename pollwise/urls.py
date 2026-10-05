"""
URL configuration for pollwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
# from rest_framework.routers import DefaultRouter
from poll.views import *
from rest_framework.authtoken.views import obtain_auth_token


# router=DefaultRouter()
# router.register('user',UserListView,basename='user')



urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('poll/', PollListView.as_view(), name='poll-list'),
    path('poll/create/', PollCreateView.as_view(), name='poll-create'),
    path('poll/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('poll/<int:pk>/addchoice/', ChoiceCreateView.as_view(), name='choice-create'),
    path('poll/<int:pk>/addvote/', VoteCreateView.as_view(), name='vote-create'),
]