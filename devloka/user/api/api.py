from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from user.api.serializers import UserSerailizer
from user.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerailizer
    filterset_fields = ["is_active"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["email"]
    lookup_field = "id"
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Override get_permissions to return the permission class based on action.
        The permissions are as follows:
        - list and create: AllowAny()
        - others: IsAuthenticated()
        """

        if self.action in ["create"]:
            return [AllowAny()]
        return super().get_permissions()

    def get_object(self):
        """
        Override get_object to return the current user object.
        """

        return self.queryset.get(id=self.request.user.id)
