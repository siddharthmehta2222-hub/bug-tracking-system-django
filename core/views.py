from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .models import Bug
from .forms import BugForm, UserSignupForm

import openpyxl
from reportlab.pdfgen import canvas


# ==================================================
# ADMIN ONLY DECORATOR
# ==================================================
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            return HttpResponseForbidden("You are not allowed ❌")
        return view_func(request, *args, **kwargs)
    return wrapper


# ✅ Custom user model
User = get_user_model()


# ==================================================
# USER SIGNUP
# ==================================================
def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('/login/')
    else:
        form = UserSignupForm()

    return render(request, 'core/signup.html', {'form': form})


# ==================================================
# LOGIN
# ==================================================
def loginView(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "core/login.html")


# ==================================================
# LOGOUT
# ==================================================
@login_required
def logoutView(request):
    logout(request)
    return redirect('/login/')


# ==================================================
# DASHBOARD
# ==================================================
@login_required
def dashboardView(request):

    if request.user.role == 'admin':
        bugs = Bug.objects.all()
    else:
        bugs = Bug.objects.filter(assigned_to=request.user)

    context = {
        'total_bugs': bugs.count(),
        'open_bugs': bugs.filter(status='open').count(),
        'progress_bugs': bugs.filter(status='in_progress').count(),
        'closed_bugs': bugs.filter(status='closed').count(),
    }

    return render(request, "core/dashboard.html", context)

# ==================================================
# BUG ACTIONS
# ==================================================
@login_required
def start_bug(request, id):
    bug = get_object_or_404(Bug, id=id)
    bug.status = "in_progress"
    bug.save()
    messages.success(request, "Bug moved to In Progress")
    return redirect('dashboard')


@login_required
def close_bug(request, id):
    bug = get_object_or_404(Bug, id=id)
    bug.status = "closed"
    bug.save()
    messages.success(request, "Bug closed successfully")
    return redirect('dashboard')


# ==================================================
# ADD BUG
# ==================================================
@login_required
def add_bug(request):
    if request.method == "POST":
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.reported_by = request.user
            bug.save()
            messages.success(request, "Bug reported successfully")
            return redirect('dashboard')
    else:
        form = BugForm()

    return render(request, 'core/add_bug.html', {'form': form})


# ==================================================
# BUG LIST
# ==================================================
@login_required
def bug_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    bugs = Bug.objects.all().order_by('-id')

    # 🔍 SEARCH
    if query:
        bugs = bugs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # 🎯 FILTER
    if status:
        bugs = bugs.filter(status=status)

    return render(request, 'core/bug_list.html', {
        'bugs': bugs,
        'query': query,
        'status': status
    })

# ==================================================
# HOME
# ==================================================
def home(request):
    context = {
        'total_bugs': Bug.objects.count(),
        'open_bugs': Bug.objects.filter(status='open').count(),
        'progress_bugs': Bug.objects.filter(status='in_progress').count(),
        'closed_bugs': Bug.objects.filter(status='closed').count()
    }
    return render(request, 'core/home.html', context)


# ==================================================
# ADD USER
# ==================================================
@login_required
def add_user(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )

        user.role = request.POST.get('role')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')
        user.dob = request.POST.get('dob')
        user.address = request.POST.get('address')

        if request.FILES.get('image'):
            user.image = request.FILES.get('image')

        user.save()

        messages.success(request, "User Added Successfully ✅")
        return redirect('user_list')

    return render(request, 'core/add_user.html')


# ==================================================
# USER LIST (WITH SEARCH 🔥)
# ==================================================
@login_required
def user_list(request):
    query = request.GET.get('q')

    users = User.objects.all().order_by('-id')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone__icontains=query)
        )

    return render(request, 'core/user_list.html', {
        'users': users,
        'query': query
    })


# ==================================================
# DELETE USER
# ==================================================
@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('user_list')


# ==================================================
# VIEW USER
# ==================================================
@login_required
def view_user(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'core/view_user.html', {'user': user})


# ==================================================
# EDIT USER
# ==================================================
@login_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')
        user.dob = request.POST.get('dob')
        user.address = request.POST.get('address')
        user.role = request.POST.get('role')

        if request.FILES.get('image'):
            user.image = request.FILES.get('image')

        user.save()
        messages.success(request, "User updated successfully ✅")
        return redirect('user_list')

    return render(request, 'core/edit_user.html', {'user': user})


# ==================================================
# USER REPORT
# ==================================================
@login_required
def user_report(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'core/user_report.html', {'users': users})


# ==================================================
# EXPORT EXCEL
# ==================================================
@login_required
def export_users_excel(request):
    users = User.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"

    ws.append(['ID', 'Name', 'Email', 'Phone', 'Role', 'DOB'])

    for user in users:
        ws.append([
            user.id,
            f"{user.first_name} {user.last_name}",
            user.email,
            user.phone,
            user.role,
            str(user.dob)
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'

    wb.save(response)
    return response


# ==================================================
# EXPORT PDF
# ==================================================
@login_required
def export_users_pdf(request):
    users = User.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=users.pdf'

    p = canvas.Canvas(response)

    y = 800
    for user in users:
        text = f"{user.id} | {user.first_name} {user.last_name} | {user.email} | {user.role}"
        p.drawString(30, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response


# ==================================================
# CHANGE PASSWORD (ADMIN ONLY 🔐)
# ==================================================
@login_required
@admin_only
def change_password(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match ❌")
            return redirect('change_password', id=id)

        user.password = make_password(password)
        user.save()

        messages.success(request, "Password updated successfully ✅")
        return redirect('user_list')

    return render(request, 'core/change_password.html', {'user': user})

# ==========================================
# EXPORT BUGS EXCEL
# ==========================================
@login_required
def export_bugs_excel(request):
    bugs = Bug.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Bugs"

    # HEADER
    ws.append(['ID', 'Title', 'Project', 'Priority', 'Status', 'Assigned To'])

    # DATA
    for bug in bugs:
        ws.append([
            bug.id,
            bug.title,
            str(bug.project),
            bug.priority,
            bug.status,
            str(bug.assigned_to)
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=bugs.xlsx'

    wb.save(response)
    return response


# ==========================================
# EXPORT BUGS PDF
# ==========================================
@login_required
def export_bugs_pdf(request):
    bugs = Bug.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=bugs.pdf'

    p = canvas.Canvas(response)

    y = 800
    p.setFont("Helvetica", 10)

    for bug in bugs:
        text = f"{bug.id} | {bug.title} | {bug.priority} | {bug.status}"
        p.drawString(30, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response