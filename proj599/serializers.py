from rest_framework import serializers
from proj599.models import Thread
from django.contrib.auth.models import User

class ThreadSerializer(serializers.ModelSerializer):
    poster = serializers.Field(source='poster.username')

    class Meta:
        model = Thread
        fields = ('id', 'poster', 'subject', 'num_upvotes', 'num_views', 'datetime_posted', \
            'datetime_modified', 'message', 'link', 'longitude', 'latitude')


class UserSerializer(serializers.ModelSerializer):
    threads = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'threads')
