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


User = get_user_model()


# ==================================================
# ADMIN ONLY DECORATOR
# ==================================================
def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return HttpResponseForbidden("You are not allowed ❌")
        return view_func(request, *args, **kwargs)
    return wrapper


# ==================================================
# USER SIGNUP
# ==================================================
def userSignupView(request):
    print("METHOD:", request.method)   # 🔥 DEBUG

    if request.method == "POST":
        print("POST DATA:", request.POST)   # 🔥 DEBUG

        form = UserSignupForm(request.POST)

        if form.is_valid():
            print("FORM VALID ✅")   # 🔥 DEBUG
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
        else:
            print("FORM ERRORS ❌:", form.errors)   # 🔥 DEBUG

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

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request,
                username=user_obj.username,   # 🔥 FIX HERE
                password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password ❌")

    return render(request, "core/login.html")
# LOGOUT
# ==================================================
@login_required
def logoutView(request):
    logout(request)
    return redirect('login')


# ==================================================
# 🚀 DASHBOARD (FIXED + UPGRADED)
# ==================================================
@login_required
def dashboardView(request):

    user = request.user

    # 🔥 ROLE BASED DATA
    if user.role in ['admin', 'manager']:
        bugs = Bug.objects.all()

    elif user.role == 'developer':
        bugs = Bug.objects.filter(assigned_to=user)

    elif user.role == 'tester':
        bugs = Bug.objects.filter(reported_by=user)

    else:
        bugs = Bug.objects.none()


    # 🔍 SEARCH + FILTER ✅ (ADDED)
    search_query = request.GET.get('search')
    status_filter = request.GET.get('status')

    if search_query:
        bugs = bugs.filter(title__icontains=search_query)

    if status_filter:
        bugs = bugs.filter(status=status_filter)


    # 📊 COUNTS ✅ (UPDATED AFTER FILTER)
    total_bugs = bugs.count()
    open_bugs = bugs.filter(status='open').count()
    progress_bugs = bugs.filter(status='in_progress').count()
    closed_bugs = bugs.filter(status='closed').count()


    # 🔥 LATEST BUGS (AFTER FILTER)
    latest_bugs = bugs.order_by('-id')[:5]


    context = {
        'total_bugs': total_bugs,
        'open_bugs': open_bugs,
        'progress_bugs': progress_bugs,
        'closed_bugs': closed_bugs,
        'bugs': latest_bugs,
        'role': user.role
    }

    return render(request, "core/dashboard.html", context)

def change_status(request, id, status):
    bug = get_object_or_404(Bug, id=id)
    bug.status = status
    bug.save()
    return redirect('dashboard')


def edit_bug(request, id):
    bug = get_object_or_404(Bug, id=id)

    if request.method == 'POST':
        bug.title = request.POST.get('title')
        bug.priority = request.POST.get('priority')
        bug.save()
        return redirect('dashboard')

    return render(request, 'core/edit_bug.html', {'bug': bug})

@login_required
def delete_bug(request, id):
    bug = get_object_or_404(Bug, id=id)

    # only admin & manager allowed
    if request.user.role in ['admin', 'manager']:
        bug.delete()

    return redirect('dashboard')
# ==================================================
# BUG ACTIONS
# ==================================================
@login_required
def start_bug(request, id):
    bug = get_object_or_404(Bug, id=id)

    # 🔐 SECURITY CHECK
    if request.user.role not in ['developer', 'manager', 'admin']:
        return HttpResponseForbidden("You are not allowed ❌")

    # ✅ Only allow if assigned OR admin/manager
    if request.user.role == 'developer' and bug.assigned_to != request.user:
        return HttpResponseForbidden("Not your bug ❌")

    if bug.status == 'open':
        bug.status = "in_progress"
        bug.save()

    messages.success(request, "Bug moved to In Progress ✅")
    return redirect('dashboard')

@login_required
def close_bug(request, id):
    bug = get_object_or_404(Bug, id=id)

    # 🔐 SECURITY CHECK
    if request.user.role not in ['manager', 'admin']:
        return HttpResponseForbidden("You are not allowed ❌")

    if bug.status != 'closed':
        bug.status = "closed"
        bug.save()

    messages.success(request, "Bug closed successfully ✅")
    return redirect('dashboard')

# ==================================================
# ADD BUG
# ==================================================
@login_required
def add_bug(request):
    form = BugForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        bug = form.save(commit=False)

        # ✅ Reporter
        bug.reported_by = request.user

        # 🔥 AUTO ASSIGN TO ANY DEVELOPER
        from django.contrib.auth import get_user_model
        User = get_user_model()

        developer = User.objects.filter(role='developer').first()

        if developer:
            bug.assigned_to = developer
        else:
            bug.assigned_to = request.user  # fallback

        bug.save()

        messages.success(request, "Bug reported & assigned successfully ✅")
        return redirect('dashboard')

    return render(request, 'core/add_bug.html', {'form': form})

# ==================================================
# BUG LIST
# ==================================================
@login_required
def bug_list(request):
    query = request.GET.get('q')
    status = request.GET.get('status')

    bugs = Bug.objects.all().order_by('-id')

    if query:
        bugs = bugs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

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
    return render(request, 'core/home.html')


# ==================================================
# USER MANAGEMENT
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


@login_required
def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'core/user_list.html', {'users': users})


@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('user_list')


@login_required
def view_user(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'core/view_user.html', {'user': user})


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
# CHANGE PASSWORD
# ==================================================
@login_required
@admin_only
def change_password(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match ❌")
            return redirect('change_password', id=id)

        user.set_password(password)
        user.save()

        messages.success(request, "Password updated successfully ✅")
        return redirect('user_list')

    return render(request, 'core/change_password.html', {'user': user})


# ==================================================
# EXPORT USERS EXCEL
# ==================================================
@login_required
def export_users_excel(request):
    users = User.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Name', 'Email', 'Phone', 'Role'])

    for user in users:
        ws.append([
            user.id,
            f"{user.first_name} {user.last_name}",
            user.email,
            user.phone,
            user.role
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=users.xlsx'
    wb.save(response)

    return response


# ==================================================
# EXPORT USERS PDF
# ==================================================
@login_required
def export_users_pdf(request):
    users = User.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=users.pdf'

    p = canvas.Canvas(response)

    y = 800
    for user in users:
        p.drawString(30, y, f"{user.id} | {user.email} | {user.role}")
        y -= 20

    p.save()
    return response


# ==================================================
# EXPORT BUGS EXCEL
# ==================================================
@login_required
def export_bugs_excel(request):
    bugs = Bug.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Title', 'Priority', 'Status'])

    for bug in bugs:
        ws.append([
            bug.id,
            bug.title,
            bug.priority,
            bug.status
        ])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=bugs.xlsx'
    wb.save(response)

    return response


# ==================================================
# EXPORT BUGS PDF
# ==================================================
@login_required
def export_bugs_pdf(request):
    bugs = Bug.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=bugs.pdf'

    p = canvas.Canvas(response)

    y = 800
    for bug in bugs:
        text = f"{bug.id} | {bug.title} | {bug.status}"
        p.drawString(30, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response


# ==================================================
# USER REPORT
# ==================================================
@login_required
def user_report(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'core/user_report.html', {'users': users})