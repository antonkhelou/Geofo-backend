from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authtokenview

from proj599 import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^threads/$', views.ThreadList.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/$', views.ThreadDetail.as_view(), name='thread-detail'),
    url(r'^threadupvote/$', views.ThreadUpvoteList.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/comments/$', views.ThreadCommentList.as_view()),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view(), name='comment-detail'),
    url(r'^commentupvote/$', views.CommentUpvoteList.as_view()),
    url(r'^users/$', views.AppUserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.AppUserDetail.as_view(), name='user-detail'),
    url(r'^api-token-auth/', authtokenview.obtain_auth_token),
)

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
)