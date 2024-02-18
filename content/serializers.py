from rest_framework import serializers
from .models import Blog, CustomUser


class UserSer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'passkey', 'email', 'mobile_number', 'pincode', 'role')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data.get('username', ''),
            email=validated_data.get('email', '')
        )
        user = CustomUser(**validated_data)
        user.save()
        return user


class BlogSer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'summary', 'category', 'createdBy')
