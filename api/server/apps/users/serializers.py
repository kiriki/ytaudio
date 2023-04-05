from rest_framework.serializers import CharField, ModelSerializer, Serializer

from django.contrib.auth.models import User

from server.apps.users.permissions import IsOwnerOrReadOnly


class LoginSerializer(Serializer):
    username = CharField(write_only=True)
    password = CharField(write_only=True)


class MeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
        )


class UserSerializer(ModelSerializer):
    permission_classes = (IsOwnerOrReadOnly,)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        )
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )
        read_only_fields = ('id', 'username', 'email')
