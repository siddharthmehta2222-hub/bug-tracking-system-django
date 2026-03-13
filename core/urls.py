from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('signup/', views.userSignupView, name='signup'),

    path('login/', views.loginView, name='login'),

    path('dashboard/', views.dashboardView, name='dashboard'),

    path('add-bug/', views.add_bug, name='add_bug'),

    path('bugs/', views.bug_list, name='bug_list'),

]