#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


with open(file=".env", mode="a+") as file:
    file.close()


def main():
    """Run administrative tasks."""
    if os.getenv("env", "prod") == "dev" or config("env", "prod") == "dev":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopeps_bank_email_backend.settings.dev')

    elif os.getenv("env", "dev") == "prod" or config("env", "dev") == "prod":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopeps_bank_email_backend.settings.prod')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hopeps_bank_email_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
