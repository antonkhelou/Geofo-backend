from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from proj599 import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^threads/$', views.ThreadList.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/$', views.ThreadDetail.as_view(), name='thread-detail'),
    url(r'^threads/(?P<pk>[0-9]+)/upvote/$', views.upvote_thread),
    url(r'^threads/(?P<pk>[0-9]+)/comments/$', views.ThreadCommentList.as_view()),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^comments/(?P<pk>[0-9]+)/upvote/$', views.upvote_comment),
    url(r'^users/$', views.AppUserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.AppUserDetail.as_view(), name='user-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)