from django.contrib import admin
from .models import Bug, Project, User

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Bug)