from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# ==================================================
# USER MODEL
# ==================================================
class User(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tester')

    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # ✅ FIXED METHOD NAME (_str_)
    def _str_(self):
        return f"{self.username} ({self.role})"


# ==================================================
# PROJECT MODEL (UPDATED 🔥)
# ==================================================
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    submission_date = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    client_name = models.CharField(max_length=200, blank=True, null=True)
    client_address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    # 🔥 NEW project status field
    status = models.CharField(max_length=20, choices=(
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ), default='active')

    project_lead = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    # ✅🔥 FINAL FIX (VERY IMPORTANT)
    def __str__(self):
        return self.name if self.name else "Unnamed Project"

    # 🔥 OPTIONAL (GOOD FOR DEBUGGING / ADMIN)
    def get_status_display_label(self):
        return dict(self._meta.get_field('status').choices).get(self.status, "Unknown")

# ==================================================
# BUG MODEL
# ==================================================
class Bug(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('verified', 'Verified'),
        ('closed', 'Closed'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reported_bugs'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bugs'
    )

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    

    # 🔥 NEW FIELDS ADDED (FOR EDIT PAGE + FUTURE FEATURES)
    bug_level = models.CharField(max_length=20, blank=True, null=True)
    bug_type = models.CharField(max_length=50, blank=True, null=True)
    bug_date = models.DateField(blank=True, null=True)

    # 🔥 IMAGE SUPPORT (IMPORTANT FEATURE)
    image = models.ImageField(upload_to='bug_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.message