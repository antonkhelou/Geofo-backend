from rest_framework import serializers
from proj599.models import Thread, Comment, AppUser, ThreadUpvote, CommentUpvote
from django.contrib.auth.models import User


class ThreadSerializer(serializers.ModelSerializer):
    thread_poster = serializers.Field(source='thread_poster.user.username')
    thread_comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    #geo_rank = serializers.Field()
    num_upvotes = serializers.Field()

    class Meta:
        model = Thread
        fields = ('id', 'thread_poster', 'thread_comments', 'subject', 'num_upvotes', 'num_views', 'datetime_posted', \
            'datetime_modified', 'message', 'link', 'latitude', 'longitude', 'city', 'state', 'country', 'geo_rank')


class ThreadUpvoteSerializer(serializers.ModelSerializer):
    upvote_user = serializers.Field(source='upvote_user.user.username')
    upvoted_thread = serializers.HyperlinkedRelatedField(view_name='thread-detail')

    class Meta:
        model = ThreadUpvote
        fields = ('id', 'upvote_user', 'upvoted_thread', 'datetime_upvoted', 'city', 'state', 'country')


class CommentSerializer(serializers.ModelSerializer):
    comment_poster = serializers.Field(source='comment_poster.user.username')
    parent_comment = serializers.HyperlinkedRelatedField(view_name='comment-detail', required=False)
    child_comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    thread = serializers.HyperlinkedRelatedField(view_name='thread-detail')
    num_upvotes = serializers.Field()

    class Meta:
        model = Comment
        fields = ('id', 'comment_poster', 'thread', 'parent_comment', 'child_comments', 'datetime_posted', 'datetime_modified', 'num_upvotes', 'message')


class CommentUpvoteSerializer(serializers.ModelSerializer):
    upvote_user = serializers.Field(source='upvote_user.user.username')
    upvoted_comment = serializers.HyperlinkedRelatedField(view_name='comment-detail')

    class Meta:
        model = CommentUpvote
        fields = ('id', 'upvote_user', 'upvoted_comment', 'datetime_upvoted', 'city', 'state', 'country')


class AppUserSerializer(serializers.ModelSerializer):
    posted_threads = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='thread-detail')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    ban_status = serializers.Field(source='ban_status')

    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'password', 'ban_status', 'posted_threads')

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.user.email = attrs.get('user.email', instance.user.email)
            instance.ban_status = attrs.get('ban_status', instance.ban_status)
            instance.user.password = attrs.get('user.password', instance.user.password)
            return instance

        user = User.objects.create_user(username=attrs.get('user.username'), email= attrs.get('user.email'), password=attrs.get('user.password'))

        #if there are other attributes that need to be used they need to be added manually here from the attrs parameter
        return AppUser(user=user)
