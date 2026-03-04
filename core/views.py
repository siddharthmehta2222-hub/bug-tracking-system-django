from django.shortcuts import render, redirect
from .forms import UserSignupForm
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