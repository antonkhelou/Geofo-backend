from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    thread_poster = models.ForeignKey('auth.User', null=True, blank=True, related_name='posted_threads')
    subject = models.CharField(max_length=144)
    num_upvotes = models.IntegerField(default=0)
    num_views = models.IntegerField(default=0)
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=10000, blank=True)
    link = models.CharField(max_length=2000, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)


class Comment(models.Model):
    comment_poster = models.ForeignKey('auth.User', null=True, blank=True, related_name='posted_comments')
    thread = models.ForeignKey(Thread, related_name='thread_comments')
    parent_comment = models.ForeignKey("Comment", null=True, blank=True)
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    num_upvotes = models.IntegerField()
    message = models.CharField(max_length=10000, blank=True)
