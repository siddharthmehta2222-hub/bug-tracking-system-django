from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # ===============================
    # AUTH & HOME
    # ===============================
    path('', views.home, name='home'),
    path('signup/', views.userSignupView, name='signup'),
    path('login/', views.loginView, name='login'),

    # ✅ Use your custom logout (better than auth_views)
    path('logout/', views.logoutView, name='logout'),

    # ===============================
    # DASHBOARD
    # ===============================
    path('dashboard/', views.dashboardView, name='dashboard'),

    # ===============================
    # BUG MANAGEMENT
    # ===============================
    path('add-bug/', views.add_bug, name='add_bug'),
    path('bug-list/', views.bug_list, name='bug_list'),
    path('start/<int:id>/', views.start_bug, name='start_bug'),
    path('close/<int:id>/', views.close_bug, name='close_bug'),

    # ===============================
    # USER MANAGEMENT
    # ===============================
    path('add-user/', views.add_user, name='add_user'),
    path('user-list/', views.user_list, name='user_list'),
    path('view-user/<int:id>/', views.view_user, name='view_user'),
    path('edit-user/<int:id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:id>/', views.delete_user, name='delete_user'),
    path('user-report/', views.user_report, name='user_report'),
    path('change-password/<int:id>/', views.change_password, name='change_password'),
    path('add-project/', views.add_project, name='add_project'),
    path('project-report/', views.project_report, name='project_report'),
    path('delete-project/<int:id>/', views.delete_project, name='delete_project'),
    path('edit-project/<int:id>/', views.edit_project, name='edit_project'),
    path('view-project/<int:id>/', views.view_project, name='view_project'),
    path('view-bug/<int:id>/', views.view_bug, name='view_bug'),
    path('edit-bug/<int:id>/', views.edit_bug, name='edit_bug'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('mark-read/<int:id>/', views.mark_read, name='mark_read'),
    path('resolve/<int:id>/', views.resolve_bug, name='resolve_bug'),
    path('verify/<int:id>/', views.verify_bug, name='verify_bug'),
    path('change-status/<int:id>/<str:status>/', views.change_status, name='change_status'),

    # ===============================
    # EXPORT FEATURES
    # ===============================
    path('export-users-excel/', views.export_users_excel, name='export_users_excel'),
    path('export-users-pdf/', views.export_users_pdf, name='export_users_pdf'),
    path('export-bugs-excel/', views.export_bugs_excel, name='export_bugs_excel'),
    path('export-bugs-pdf/', views.export_bugs_pdf, name='export_bugs_pdf'),
    path('export-projects-excel/', views.export_projects_excel, name='export_projects_excel'),
    path('export-projects-pdf/', views.export_projects_pdf, name='export_projects_pdf'),

    path('bug/edit/<int:id>/', views.edit_bug, name='edit_bug'),
    path('bug/status/<int:id>/<str:status>/', views.change_status, name='change_status'),
    path('bug/delete/<int:id>/', views.delete_bug, name='delete_bug'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
    

]