# campus_hub/run_before_start.py

import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campus_hub.settings")
django.setup()

# Run DB migrations
call_command("migrate", interactive=False)

# Collect static files
call_command("collectstatic", interactive=False)
