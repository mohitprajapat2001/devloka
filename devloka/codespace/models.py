from secrets import token_hex

from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleDescriptionModel,
)


def _code_space_id():
    """
    Generates ID for codespace
    """
    while True:
        id = token_hex(4)
        if not CodeSpace.objects.filter(id=id).exists():
            return id


class Syntax(TitleDescriptionModel, ActivatorModel):
    extension = models.CharField(max_length=10, unique=True)
    content_type = models.CharField(max_length=100)

    def __str__(self):
        """String Representation for Syntax"""

        return self.title

    class Meta:
        unique_together = ("title", "status", "extension")


class CodeSpace(TitleDescriptionModel, TimeStampedModel, ActivatorModel):
    id = models.CharField(primary_key=True, max_length=8, unique=True, editable=False)
    syntax = models.ForeignKey(
        "codespace.Syntax", on_delete=models.PROTECT, related_name="codespaces"
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.PROTECT,
        related_name="codespaces",
        null=True,
        blank=True,
    )
    content = models.TextField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    version = models.PositiveBigIntegerField(default=0)

    def save(self, **kwargs):
        """
        Generates id for codespace if it doesn't exist
        """
        if not self.id:
            self.id = _code_space_id()
        return super().save(**kwargs)

    @property
    def filename(self):
        """
        Returns the filename for this codespace as a string in the format:
        '<id>.<syntax_extension>'.
        """
        return f"{self.title}.{self.syntax.extension}"
