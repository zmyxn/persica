from django.contrib.auth.models import Group
from .models import Tree
from rest_framework import generics, permissions, renderers, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import TreeSerializer


class TreeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
