from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Bug
from .forms import BugForm, UserSignupForm
import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# ✅ Use custom user model properly
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
    total_bugs = Bug.objects.count()
    open_bugs = Bug.objects.filter(status='open').count()
    progress_bugs = Bug.objects.filter(status='in_progress').count()
    closed_bugs = Bug.objects.filter(status='closed').count()

    context = {
        'total_bugs': total_bugs,
        'open_bugs': open_bugs,
        'progress_bugs': progress_bugs,
        'closed_bugs': closed_bugs,
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

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        image = request.FILES.get('image')

        # ✅ Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Extra fields
        user.role = role
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.gender = gender
        user.dob = dob
        user.address = address

        if image:
            user.image = image

        user.save()

        messages.success(request, "User Added Successfully ✅")
        return redirect('user_list')

    return render(request, 'core/add_user.html')

# ==================================================
# USER LIST
# ==================================================
@login_required
def user_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'core/user_list.html', {'users': users})

# ==================================================
# DELETE USER
# ==================================================
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

@login_required
def user_report(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'core/user_report.html', {'users': users})

@login_required
def export_users_excel(request):
    users = User.objects.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Users"

    # HEADER
    headers = ['ID', 'Name', 'Email', 'Phone', 'Role', 'DOB']
    ws.append(headers)

    # DATA
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

@login_required
def export_users_pdf(request):
    users = User.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=users.pdf'

    p = canvas.Canvas(response)

    y = 800
    p.setFont("Helvetica", 10)

    for user in users:
        text = f"{user.id} | {user.first_name} {user.last_name} | {user.email} | {user.role}"
        p.drawString(30, y, text)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response