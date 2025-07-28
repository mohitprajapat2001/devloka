from codespace.api.serializers import CodeSpaceSerializer, SyntaxSerializer
from codespace.models import CodeSpace, Syntax
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import redirect
from django_extensions.db.models import ActivatorModel
from rest_framework.decorators import action
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class SyntaxViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Syntax.objects.filter(status=ActivatorModel.ACTIVE_STATUS)
    serializer_class = SyntaxSerializer
    pagination_class = None
    lookup_field = "title"
    lookup_url_kwarg = "title"
    ordering = ["title"]
    ordering_fields = ["title"]
    search_fields = ["title", "description"]
    filterset_fields = ["title", "description"]


class CodeSpaceViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = CodeSpace.objects.filter(status=ActivatorModel.ACTIVE_STATUS)
    serializer_class = CodeSpaceSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    ordering = ["title"]
    ordering_fields = ["title"]
    search_fields = ["title", "description", "user__email", "user__first_name"]
    filterset_fields = ["title", "description", "is_private", "status"]
    permission_classes = [AllowAny]

    def get_object(self):
        """
        Override get_object to return the current codespace object.
        else:
            create a new codespace object.
        """
        try:
            return self.queryset.get(**self.kwargs)
        except CodeSpace.DoesNotExist:
            return CodeSpace.objects.create(
                **self.kwargs,
                title="Untitled",
                syntax=Syntax.objects.get(title="Plain Text"),
            )

    @action(
        detail=False,
        methods=["GET"],
        url_name="user-devspaces",
        url_path="user-devspaces",
        permission_classes=[IsAuthenticated],
    )
    def devspaces(self, request, *args, **kwargs):
        user = self.request.user
        self.queryset = user.codespaces.all()
        return self.list(request, *args, **kwargs)

    @action(
        detail=True, methods=["GET"], url_name="devspace-download", url_path="download"
    )
    def download(self, request, *args, **kwargs):
        codespace = self.get_object()
        content = codespace.content or ""
        response = FileResponse(content, content_type=codespace.syntax.content_type)
        response[
            "Content-Disposition"
        ] = rf'attachment; filename="{str(codespace.filename)}"'
        return response

    @action(
        detail=False,
        methods=["GET"],
        url_name="create-codespace",
        url_path="create-codespace",
    )
    def create_codespace(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            codespace = CodeSpace.objects.create(
                user=request.user,
                title="Untitled",
                syntax=Syntax.objects.get(title="Plain Text"),
            )
        else:
            codespace = CodeSpace.objects.create(
                title="Untitled",
                syntax=Syntax.objects.get(title="Plain Text"),
            )
        return redirect(settings.FRONTEND_URL + codespace.id)
