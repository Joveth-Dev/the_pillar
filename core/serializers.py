from djoser.serializers import UserSerializer as BaseUserSerializer, \
    UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

# REMOVE THIS IN CASE OF REUSING THIS APP/MODULE (core)
from publication.serializers import CustomReaderSerializer
from publication.models import Reader


# class UserCreateSerializer(BaseUserCreateSerializer):
#     reader = CustomReaderSerializer()

#     class Meta(BaseUserSerializer.Meta):
#         fields = ['id', 'username', 'email',
#                   'password', 're_password', 'reader']


class UserSerializer(BaseUserSerializer):
    reader = CustomReaderSerializer()

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'avatar', 'username', 'email', 'last_name',
                  'first_name', 'middle_initial', 'sex', 'reader']

    def update(self, instance, validated_data):
        reader_data = validated_data.pop('reader', None)
        if reader_data:
            reader_serializer = CustomReaderSerializer(
                instance=instance.reader,
                data=reader_data
            )
            reader_serializer.is_valid(raise_exception=True)
            reader_serializer.save()
        return super().update(instance, validated_data)
