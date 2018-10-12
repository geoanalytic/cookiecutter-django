from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from profiles import views

urlpatterns = [
    # RESTful urls
    url(r'^myprofiles/$', views.MyProfiles.as_view(), name='myprofiles'),
    url(r'^profiles/$', views.ProfileList.as_view(), name='profile-list'),
    url(r'^profiles/(?P<pk>[0-9]+)/$', views.ProfileDetail.as_view(), name='profile-detail'),
    url(r'^basemaps/$', views.BasemapList.as_view(), name='basemap-list'),
    url(r'^basemaps/(?P<pk>[0-9]+)/$', views.BasemapDetail.as_view(), name='basemap-detail'),
    url(r'^tags/$', views.TagList.as_view(), name='tag-list'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.TagDetail.as_view(), name='tag-detail'),
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^spatialitedbs/$', views.SpatialitedbsList.as_view(), name='spatialitedb-list'),
    url(r'^spatialitedbs/(?P<pk>[0-9]+)/$', views.SpatialitedbsDetail.as_view(), name='spatialitedb-detail'),
    url(r'^otherfiles/$', views.OtherfilesList.as_view(), name='otherfile-list'),
    url(r'^otherfiles/(?P<pk>[0-9]+)/$', views.OtherfilesDetail.as_view(), name='otherfile-detail'),
    url(r'^projects/upload/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    # allow authentication via REST
    url(r'^api-auth/', include('rest_framework.urls')),
    # HTML urls
    url(r'^index/$', views.Catalog, name='index'),
    url(r'^formbuilder/$', TemplateView.as_view(template_name="geopaparazzi-FormBuilder-master/index.html"), name="formbuilder"),
]

router = DefaultRouter()
router.register(r'userprojects', views.UserProjectsViewSet, base_name='userproject')

urlpatterns = format_suffix_patterns(urlpatterns) + router.urls
