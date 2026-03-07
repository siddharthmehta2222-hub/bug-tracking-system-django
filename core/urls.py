from django.urls import path
from .import views
from .views import dashboardView, userSignupView, loginView

urlpatterns = [
path('signup/', userSignupView, name='signup'),
path('login/', loginView, name='login'),
path('dashboard/', dashboardView, name='dashboard'),
path('add-bug/', views.add_bug, name='add_bug'),
path('bugs/', views.bug_list, name='bug_list'),

]
