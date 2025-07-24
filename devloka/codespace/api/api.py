from codespace.api.serializers import CodeSpaceSerializer, SyntaxSerializer
from codespace.models import CodeSpace, Syntax
from django_extensions.db.models import ActivatorModel
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
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
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = CodeSpace.objects.filter(status=ActivatorModel.ACTIVE_STATUS)
    serializer_class = CodeSpaceSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    ordering = ["title"]
    ordering_fields = ["title"]
    search_fields = ["title", "description", "user__email", "user__first_name"]
    filterset_fields = ["title", "description", "is_private", "status"]

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
                syntax=Syntax.objects.get(title="Plain Text").id
            )
