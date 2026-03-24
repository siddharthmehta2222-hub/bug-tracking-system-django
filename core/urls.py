from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [


    path('', views.home, name='home'),

    path('signup/', views.userSignupView, name='signup'),

    path('login/', views.loginView, name='login'),

    path('dashboard/', views.dashboardView, name='dashboard'),

    path('add-bug/', views.add_bug, name='add_bug'),

    path('bug-list/', views.bug_list, name='bug_list'),

    path('start/<int:id>/', views.start_bug, name='start_bug'),

    path('close/<int:id>/', views.close_bug, name='close_bug'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('add-user/', views.add_user, name='add_user'),

    path('user-list/', views.user_list, name='user_list'),

    path('view-user/<int:id>/', views.view_user, name='view_user'),


    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),

    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),

    path('user-report/', views.user_report, name='user_report'),

    path('export-users-excel/', views.export_users_excel, name='export_users_excel'),

    path('export-users-pdf/', views.export_users_pdf, name='export_users_pdf'),

    path('change-password/<int:id>/', views.change_password, name='change_password'),


     

]