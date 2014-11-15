from django.db import models
from django.contrib.auth.models import User

from geopy.geocoders import Nominatim

geolocator = Nominatim()


class AppUser(models.Model):
    user = models.OneToOneField(User)
    ban_status = models.BooleanField(default=False)

class Thread(models.Model):
    thread_poster = models.ForeignKey(AppUser, null=True, blank=True, related_name='posted_threads')
    subject = models.CharField(max_length=144)
    num_upvotes = models.IntegerField(default=0)
    num_views = models.IntegerField(default=0)
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=10000, blank=True)
    link = models.CharField(max_length=2000, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    geo_rank = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        reverse_address = geolocator.reverse("{0},{1}".format(self.latitude, self.longitude)).raw

        # need to check if reversal is succesful otherwise throw error

        address = reverse_address['address']
        self.city = address['city']
        self.state = address['state']
        self.country = address['country']

        super(Thread, self).save(*args, **kwargs)

class Comment(models.Model):
    comment_poster = models.ForeignKey(AppUser, null=True, blank=True, related_name='posted_comments')
    thread = models.ForeignKey(Thread, related_name='thread_comments')
    parent_comment = models.ForeignKey("Comment", null=True, blank=True, related_name='child_comments')
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    num_upvotes = models.IntegerField()
    message = models.CharField(max_length=10000, blank=True)
