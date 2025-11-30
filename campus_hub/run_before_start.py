from django.core.management import call_command

call_command("migrate", interactive=False)
call_command("collectstatic", interactive=False)
