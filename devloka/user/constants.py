# User App's Constants
from django.utils.translation import gettext_lazy as _


class ValidationErrors:
    USERNAME_ALREADY_EXISTS = _("Username already exists.")
    PASSWORDS_DO_NOT_MATCH = _("Passwords do not match.")
    INVALID_CREDENTIALS = _("Invalid credentials provided.")
