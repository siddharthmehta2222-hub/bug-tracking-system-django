from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Bug
from .forms import BugForm, UserSignupForm

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
        role = request.POST.get("role")

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
    total_bugs = Bug.objects.count()

    open_bugs = Bug.objects.filter(status='open').count()
    progress_bugs = Bug.objects.filter(status='in_progress').count()
    closed_bugs = Bug.objects.filter(status='closed').count()

    open_bug_list = Bug.objects.filter(status='open')
    progress_bug_list = Bug.objects.filter(status='in_progress')
    closed_bug_list = Bug.objects.filter(status='closed')

    context = {
        'total_bugs': total_bugs,
        'open_bugs': open_bugs,
        'progress_bugs': progress_bugs,
        'closed_bugs': closed_bugs,
        'open_bug_list': open_bug_list,
        'progress_bug_list': progress_bug_list,
        'closed_bug_list': closed_bug_list,
        'user': request.user
    }

    return render(request, "core/dashboard.html", context)

# ==================================================
# START BUG
# ==================================================

@login_required
def start_bug(request, id):
    bug = get_object_or_404(Bug, id=id)
    bug.status = "in_progress"
    bug.save()
    messages.success(request, "Bug moved to In Progress")
    return redirect('dashboard')

# ==================================================
# CLOSE BUG
# ==================================================

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
    bugs = Bug.objects.all().order_by('-id')
    return render(request, 'core/bug_list.html', {'bugs': bugs})

# ==================================================
# HOME PAGE
# ==================================================

def home(request):
    total_bugs = Bug.objects.count()
    open_bugs = Bug.objects.filter(status='open').count()
    progress_bugs = Bug.objects.filter(status='in_progress').count()
    closed_bugs = Bug.objects.filter(status='closed').count()

    context = {
        'total_bugs': total_bugs,
        'open_bugs': open_bugs,
        'progress_bugs': progress_bugs,
        'closed_bugs': closed_bugs
    }

    return render(request, 'core/home.html', context)