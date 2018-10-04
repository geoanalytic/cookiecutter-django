from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from gp_projects import views

urlpatterns = [
    url(r'^usertracks$', TemplateView.as_view(template_name="usertracks.html"), name='usertracks'),
    url(r'^tracks/$', views.TrackList.as_view(), name='track-list'),
    url(r'^tracks/(?P<pk>[0-9]+)/$', views.TrackDetail.as_view(), name='track-detail'),
    url(r'^tracklist/$', views.NGTrackFeatureList.as_view(), name='trackfeature-list'),
    url(r'^imagenotes/$', views.NGImageNoteList.as_view(), name='imagenote-list'),
    url(r'^imagenotes/(?P<pk>[0-9]+)/$', views.NGImageNoteDetail.as_view(), name='imagenote-detail'),
    url(r'^userimages', TemplateView.as_view(template_name="userimages.html"), name='userimages'),
    url(r'^track.geojson$', views.geojsonTrackFeed, name='track-json'),
    url(r'^api-auth/', include('rest_framework.urls')),
]

#router = DefaultRouter()
#router.register(r'userprojects', views.UserProjectsViewSet, base_name='userproject')

urlpatterns = format_suffix_patterns(urlpatterns) # + router.urls
