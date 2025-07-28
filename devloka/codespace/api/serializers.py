from codespace.models import CodeSpace, Syntax
from django.urls import reverse
from django_extensions.db.models import ActivatorModel
from rest_framework import serializers
from user.api.serializers import UserSerailizer
from user.models import User
from utils.serializers import DynamicFieldsModelSerializer


class SyntaxSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Syntax
        fields = (
            "id",
            "title",
            "description",
            "extension",
            "content_type",
            "status",
        )


class CodeSpaceSerializer(DynamicFieldsModelSerializer):
    syntax = SyntaxSerializer(read_only=True)
    syntax_id = serializers.PrimaryKeyRelatedField(
        source="syntax",
        queryset=Syntax.objects.filter(status=ActivatorModel.ACTIVE_STATUS),
        write_only=True,
        required=True,
    )
    user = UserSerailizer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.filter(is_active=True),
        write_only=True,
        required=False,
    )
    download = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CodeSpace
        fields = (
            "id",
            "title",
            "description",
            "status",
            "syntax",
            "syntax_id",
            "user",
            "user_id",
            "content",
            "is_private",
            "version",
            "filename",
            "download",
        )
        read_only_fields = ("id",)

    def get_download(self, obj):
        return self.context["request"].build_absolute_uri(
            reverse("codespace:codespaces-devspace-download", kwargs={"id": obj.id})
        )
