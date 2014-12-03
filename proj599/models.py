from django.db import models
from django.contrib.auth.models import User

from djcelery.models import PeriodicTask, IntervalSchedule
from datetime import datetime, timedelta

import settings
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


        #check if task exists for city, state and country
        geo_schedulers_objects = GeoRankerTaskScheduler.objects

        grts = None

        if len(geo_schedulers_objects.filter(city=address['city'])) == 0:
            print u"No existant georank tasks for {0} city. Creating task.".format(address['city'])
            grts = GeoRankerTaskScheduler.schedule_every(task_name='proj599.tasks.update_city_geo_ranks', period=settings.CITY_TASK_PERIOD, every=settings.CITY_TASK_EVERY, args=[address['city'],])
            grts.city = address['city']

        if len(geo_schedulers_objects.filter(state=address['state'])) == 0:
            print u"No existant georank tasks for {0} state. Creating task.".format(address['state'])
            grts = GeoRankerTaskScheduler.schedule_every(task_name='proj599.tasks.update_state_geo_ranks', period=settings.STATE_TASK_PERIOD, every=settings.STATE_TASK_EVERY, args=[address['state'],])
            grts.state = address['state']

        if len(geo_schedulers_objects.filter(country=address['country'])) == 0:
            print u"No existant georank tasks for {0} country. Creating task.".format(address['country'])
            grts = GeoRankerTaskScheduler.schedule_every(task_name='proj599.tasks.update_country_geo_ranks', period=settings.COUNTRY_TASK_PERIOD, every=settings.COUNTRY_TASK_EVERY, args=[address['country'],])
            grts.country = address['country']

        if grts is not None:
            grts.start()
            grts.save()

        super(Thread, self).save(*args, **kwargs)


# class ThreadUpvote(models.Model):
#     upvote_user = models.ForeignKey(AppUser, null=True, blank=True)
#     thread = models.OneToOneField(Thread, null=False)
#     datetime_upvoted = models.DateTimeField(auto_now_add=True)
    # city = models.CharField(max_length=100, blank=True)
    # state = models.CharField(max_length=100, blank=True)
    # country = models.CharField(max_length=100, blank=True)


class Comment(models.Model):
    comment_poster = models.ForeignKey(AppUser, null=True, blank=True, related_name='posted_comments')
    thread = models.ForeignKey(Thread, related_name='thread_comments')
    parent_comment = models.ForeignKey("Comment", null=True, blank=True, related_name='child_comments')
    datetime_posted = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    num_upvotes = models.IntegerField()
    message = models.CharField(max_length=10000, blank=True)

# class CommentUpvote(models.Model):
#     upvote_user = models.ForeignKey(AppUser, null=True, blank=True)
#     comment = models.OneToOneField(Comment, null=False)
#     datetime_upvoted = models.DateTimeField(auto_now_add=True)
    # city = models.CharField(max_length=100, blank=True)
    # state = models.CharField(max_length=100, blank=True)
    # country = models.CharField(max_length=100, blank=True)


class GeoRankerTaskScheduler(models.Model):
    periodic_task = models.ForeignKey(PeriodicTask)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    @staticmethod
    def schedule_every(task_name, period, every, args=None, kwargs=None):
        """ 
         schedules a task by name every "every" "period". So an example call would be:
         GeoRankerTaskScheduler.schedule_every('mycustomtask', 'seconds', 30, [1,2,3]) 
         that would return you an GeoRankerTaskScheduler object which is ready to be scheduled using
         the .start() method. Make sure to save the object as well.
         In this example, your custom task to run every 30 seconds with the arguments 1,2 and 3 passed to the actual task. 
        """
        permissible_periods = ['days', 'hours', 'minutes', 'seconds']
        if period not in permissible_periods:
            raise Exception('Invalid period specified')

        # create the periodic task and the interval
        ptask_name = "%s_%s" % (task_name, datetime.now()) # create some name for the period task
        interval_schedules = IntervalSchedule.objects.filter(period=period, every=every)

        if interval_schedules: # just check if interval schedules exist like that already and reuse em
            interval_schedule = interval_schedules[0]
        else: # create a brand new interval schedule
            interval_schedule = IntervalSchedule()
            interval_schedule.every = every # should check to make sure this is a positive int
            interval_schedule.period = period 
            interval_schedule.save()

        ptask = PeriodicTask(name=ptask_name, task=task_name, interval=interval_schedule)

        if args:
            ptask.args = args
        if kwargs:
            ptask.kwargs = kwargs

        ptask.save()

        return GeoRankerTaskScheduler.objects.create(periodic_task=ptask)

    def stop(self):
        """pauses the task"""
        ptask = self.periodic_task
        ptask.enabled = False
        ptask.save()

    def start(self):
        """starts the task"""
        ptask = self.periodic_task
        ptask.enabled = True
        ptask.save()

    def terminate(self):
        self.stop()
        ptask = self.periodic_task
        self.delete()
        ptask.delete()
