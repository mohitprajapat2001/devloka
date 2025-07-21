from django_extensions.db.models import ActivatorModel, TimeStampedModel, TitleDescriptionModel
from django.db import models
from secrets import token_hex

def _code_space_id(self):
    """
    Generates ID for codespace
    """
    while True:
        id = token_hex(4)
        if not CodeSpace.objects.filter(id=id).exists():
            return id

class Syntax(TitleDescriptionModel, ActivatorModel):

    def __str__(self):
        """String Representation for Syntax"""

        return self.title
    
    class Meta:
        unique_together = ("title", "status")


class CodeSpace(TitleDescriptionModel, TimeStampedModel, ActivatorModel):
    id = models.CharField(primary_key=True, max_length=8, unique=True, default=_code_space_id, editable=False)
    syntax = models.ForeignKey("codespace.Syntax", on_delete=models.PROTECT, related_name="codespaces")
    user = models.ForeignKey("user.User", on_delete=models.PROTECT, related_name="codespaces", null=True, blank=True)    
    content = models.TextField()