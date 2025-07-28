from codespace.models import CodeSpace, Syntax
from django.contrib import admin

admin.site.register(CodeSpace)


@admin.register(Syntax)
class SyntaxAdmin(admin.ModelAdmin):
    list_display = ["title", "extension"]
