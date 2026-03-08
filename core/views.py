from django.shortcuts import render, redirect
from .models import Bug
from .forms import BugForm, UserSignupForm
from django.contrib.auth import authenticate, login


def userSignupView(request):

    if request.method == "POST":
        form = UserSignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/admin/')

    else:
        form = UserSignupForm()

    return render(request, 'core/signup.html', {'form': form})

def loginView(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin/')

    return render(request, "core/login.html")

def dashboardView(request):
    return render(request, "core/dashboard.html")

def add_bug(request):
    if request.method == 'POST':
        form = BugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.reported_by = request.user
            bug.save()
            return redirect('dashboard')
    else:
        form = BugForm()

    return render(request, 'core/add_bug.html', {'form': form})

def bug_list(request):
    bugs = Bug.objects.all()
    return render(request, 'core/bug_list.html', {'bugs': bugs})

def home(request):
    return render(request, 'core/home.html')