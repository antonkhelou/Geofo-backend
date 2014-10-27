from rest_framework import serializers
from proj599.models import Thread, Comment
from django.contrib.auth.models import User


class ThreadSerializer(serializers.ModelSerializer):
    thread_poster = serializers.Field(source='thread_poster.username')
    thread_comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')

    class Meta:
        model = Thread
        fields = ('id', 'thread_poster', 'thread_comments', 'subject', 'num_upvotes', 'num_views', 'datetime_posted', \
            'datetime_modified', 'message', 'link', 'longitude', 'latitude')


class CommentSerializer(serializers.ModelSerializer):
    comment_poster = serializers.Field(source='comment_poster.username')
    parent_comment = serializers.HyperlinkedRelatedField(view_name='comment-detail')
    thread = serializers.HyperlinkedRelatedField(view_name='thread-detail')

    class Meta:
        model = Comment
        fields = ('id', 'comment_poster', 'thread', 'parent_comment', 'datetime_posted', 'datetime_modified', 'num_upvotes', 'message')


class UserSerializer(serializers.ModelSerializer):
    posted_threads = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='thread-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'posted_threads')
