from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import permission_classes

from django.http import Http404

from proj599.models import Thread, Comment, AppUser
from proj599.serializers import ThreadSerializer, CommentSerializer, AppUserSerializer
from proj599.permissions import IsThreadPosterOrReadOnly, IsCommentPosterOrReadOnly, IsUserOrReadOnly


class ThreadList(generics.ListCreateAPIView):
    """
    List all threads, or create a new thread.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def pre_save(self, obj):
        if not self.request.user.is_anonymous():
            obj.thread_poster = AppUser.objects.get(user=self.request.user)


class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a thread instance.
    """

    permission_classes = (IsThreadPosterOrReadOnly,)

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadCommentList(generics.ListAPIView):
    """
    List all comments from a thread.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(thread=self.kwargs['pk'])


class CommentList(generics.ListCreateAPIView):
    """
    List all comments, or create a new comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def pre_save(self, obj):
        if not self.request.user.is_anonymous():
            obj.comment_poster = AppUser.objects.get(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a comment instance.
    """

    permission_classes = (IsCommentPosterOrReadOnly,)

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AppUserList(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class AppUserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsUserOrReadOnly,)

    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
