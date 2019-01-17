from .models import Tree
from rest_framework import serializers

class TreeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="common:tree-detail", )
    class Meta:
        model = Tree
        fields = ('url', 'name', 'node', 'parent')
