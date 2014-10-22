from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    poster = models.ForeignKey('auth.User', null=True, blank=True, related_name='threads')
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
    thread = models.ForeignKey(Thread)
    parent_comment = models.OneToOneField("Comment", null=True, blank=True)
    datetime_posted = models.DateTimeField()
    num_upvotes = models.IntegerField()
    message = models.CharField(max_length=10000, blank=True)
