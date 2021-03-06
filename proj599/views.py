from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.response import Response

from django.http import Http404, HttpResponseBadRequest

from proj599.models import Thread, Comment, AppUser, ThreadUpvote, CommentUpvote
from proj599.serializers import ThreadSerializer, CommentSerializer, AppUserSerializer, ThreadUpvoteSerializer, CommentUpvoteSerializer
from proj599.permissions import IsThreadPosterOrReadOnly, IsCommentPosterOrReadOnly, IsUserOrReadOnly

from geopy.geocoders import Nominatim

geolocator = Nominatim()


class ThreadList(generics.ListCreateAPIView):
    """
    List all threads, or create a new thread.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def pre_save(self, obj):
        if not self.request.user.is_anonymous():
            obj.thread_poster = AppUser.objects.get(user=self.request.user)

    def get_queryset(self):
        queryset = Thread.objects.all()
        filtered_queryset = queryset

        city = self.request.QUERY_PARAMS.get('city', None)
        state = self.request.QUERY_PARAMS.get('state', None)
        country = self.request.QUERY_PARAMS.get('country', None)

        if city is not None and state is not None and country is not None:
            filtered_queryset = queryset.filter(geo_rank=3) | queryset.filter(geo_rank=2, country=country) | \
                queryset.filter(geo_rank=1, state=state) | queryset.filter(geo_rank=0, city=city)

        return filtered_queryset


class ThreadUpvoteList(generics.ListCreateAPIView):
    """
    List all thread upvotes, or create a new thread upvote.
    """
    queryset = ThreadUpvote.objects.all()
    serializer_class = ThreadUpvoteSerializer

    def pre_save(self, obj):
        if not self.request.user.is_anonymous():
            obj.upvote_user = AppUser.objects.get(user=self.request.user)


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


class CommentUpvoteList(generics.ListCreateAPIView):
    """
    List all thread upvotes, or create a new thread upvote.
    """
    queryset = CommentUpvote.objects.all()
    serializer_class = CommentUpvoteSerializer

    def pre_save(self, obj):
        if not self.request.user.is_anonymous():
            obj.upvote_user = AppUser.objects.get(user=self.request.user)


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
