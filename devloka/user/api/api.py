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
