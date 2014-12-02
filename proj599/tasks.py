from celery import task
import math
import operator
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from proj599.models import Thread

import django
django.setup()

@task()
def update_city_geo_ranks(city):
    current_time = timezone.now()
    threads = Thread.objects.filter(geo_rank=0, city=city, datetime_posted__gte=(current_time - timedelta(hours=3)))

    #total_up_votes = threads.aggregate(Sum('num_upvotes'))

    thread_scores = {}

    for thread in threads:
        thread_scores[thread] = (float(thread.num_upvotes) / math.pow((current_time - thread.datetime_posted).total_seconds(), 1.5))

    sorted_scores = sorted(thread_scores.items(), key=operator.itemgetter(1), reverse=True)

    eligible_threads = sorted_scores[:int(math.ceil(len(sorted_scores)/4.0))]

    # for elig_thread in eligible_threads:
    #     elig_thread[0].geo_rank = 1

    print sorted_scores
    print eligible_threads


@task()
def update_state_geo_ranks(state):
    current_time = timezone.now()
    threads = Thread.objects.filter(geo_rank=1, state=state, datetime_posted__gte=(current_time - timedelta(hours=3)))

    #total_up_votes = threads.aggregate(Sum('num_upvotes'))

    thread_scores = {}

    for thread in threads:
        thread_scores[thread] = (float(thread.num_upvotes) / math.pow((current_time - thread.datetime_posted).total_seconds(), 1.5))

    sorted_scores = sorted(thread_scores.items(), key=operator.itemgetter(1), reverse=True)

    eligible_threads = sorted_scores[:int(math.ceil(len(sorted_scores)/4.0))]

    # for elig_thread in eligible_threads:
    #     elig_thread[0].geo_rank = 2

    print sorted_scores
    print eligible_threads

@task()
def update_country_geo_ranks(country):
    current_time = timezone.now()
    threads = Thread.objects.filter(geo_rank=2, country=country, datetime_posted__gte=(current_time - timedelta(hours=3)))

    #total_up_votes = threads.aggregate(Sum('num_upvotes'))

    thread_scores = {}

    for thread in threads:
        thread_scores[thread] = (float(thread.num_upvotes) / math.pow((current_time - thread.datetime_posted).total_seconds(), 1.5))

    sorted_scores = sorted(thread_scores.items(), key=operator.itemgetter(1), reverse=True)

    eligible_threads = sorted_scores[:int(math.ceil(len(sorted_scores)/4.0))]

    # for elig_thread in eligible_threads:
    #     elig_thread[0].geo_rank = 3

    print sorted_scores
    print eligible_threads