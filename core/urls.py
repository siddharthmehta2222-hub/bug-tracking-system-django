from django.urls import path
from .views import dashboardView, userSignupView, loginView

urlpatterns = [
path('signup/', userSignupView, name='signup'),
path('login/', loginView, name='login'),
path('dashboard/', dashboardView, name='dashboard'),
]
