from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from django.http import Http404
from django.contrib.auth.models import User

from proj599.models import Thread
from proj599.serializers import ThreadSerializer, UserSerializer
from proj599.permissions import IsPosterOrReadOnly


class ThreadList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new thread.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def pre_save(self, obj):
        obj.poster = self.request.user
        print obj.poster


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a thread instance.
    """

    permission_classes = (IsPosterOrReadOnly,)

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def pre_save(self, obj):
        obj.poster = self.request.user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
