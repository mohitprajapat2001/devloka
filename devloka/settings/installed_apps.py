THIRD_PARTY_APPS = [
    "django_extensions",
    "django_rq",
]


PROJECT_APPS = [
    "user.apps.UserConfig",
    "codespace.apps.CodespaceConfig",
]
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS
