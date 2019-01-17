from django.contrib.auth.models import User, Group
from .models import UserInfo
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail",)
    class Meta:
        model = User
        # fields = ('url','username', 'email', )
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:group-detail",)
    class Meta:
        model = Group
        fields = ('url', 'id','name')
