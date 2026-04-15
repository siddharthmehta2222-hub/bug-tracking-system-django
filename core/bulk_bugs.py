from core.models import Bug, Project
from django.contrib.auth import get_user_model
from random import choice, randint
from datetime import date, timedelta

User = get_user_model()

projects = list(Project.objects.all())
developers = list(User.objects.filter(role='developer'))
testers = list(User.objects.filter(role='tester'))

# fallback user (VERY IMPORTANT)
fallback_user = User.objects.first()

titles = [
    "Login button not working",
    "Payment gateway failure",
    "UI alignment issue",
    "API response delay",
    "Data not saving",
    "Crash on submit",
    "Search not working",
    "Image not loading",
    "Incorrect calculation",
    "Form validation missing",
]

descriptions = [
    "Unexpected logout after session timeout.",
    "System crashes under heavy load.",
    "UI overlaps on mobile screen.",
    "API returns wrong response.",
    "Data not saved in database.",
    "File upload fails for large files.",
    "Search returns incorrect results.",
    "Session expires too early.",
]

levels = ["low", "medium", "high"]
priorities = ["low", "medium", "high"]
types = ["ui", "backend", "performance"]

print("🚀 Adding bugs...")

for i in range(50):
    project = choice(projects)
    developer = choice(developers) if developers else fallback_user
    tester = choice(testers) if testers else fallback_user

    # 🔥 IMPORTANT FIX HERE
    bug = Bug.objects.create(
        title=choice(titles),
        description=choice(descriptions),
        project=project,
        priority=choice(priorities),
        status="open",

        bug_level=choice(levels),
        bug_type=choice(types),
        bug_date=date.today() - timedelta(days=randint(0, 30)),

        assigned_to=developer,
        reported_by=tester,   # ✅ FIXED (NO NULL NOW)
    )

    # optional tester code
    bug.tester_code = f"TST{randint(1000,9999)}"
    bug.save()

print("✅ 50 Bugs Added Successfully!")