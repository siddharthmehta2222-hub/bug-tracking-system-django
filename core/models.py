from django.contrib.auth.models import AbstractUser
from django.db import models


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

    # EXTRA FIELDS
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # ✅ FIX: Use username for login (stable)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # ✅ FIX: Correct method name
    def _str_(self):
        return f"{self.username} ({self.role})"


# ==================================================
# PROJECT MODEL
# ==================================================
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):   # ✅ fixed method name
        return self.name


# ==================================================
# BUG MODEL
# ==================================================
class Bug(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
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

    # already correct ✅
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_bugs'
    )

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.status})"