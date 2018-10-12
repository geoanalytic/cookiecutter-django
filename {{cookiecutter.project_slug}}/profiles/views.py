from django.shortcuts import get_object_or_404, render
from profiles.models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, ProfileSet, UserProject
from profiles.serializers import ProjectSerializer, TagSerializer, BasemapSerializer, UserProjectSerializer
from profiles.serializers import SpatialitedbsSerializer, OtherfilesSerializer, ProfileSerializer, ProfileSetSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class MyProfiles(generics.RetrieveAPIView):
#    queryset = ProfileList.objects.all
    serializer_class = ProfileSetSerializer
#    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
#        user = self.request.user
        return ProfileSet.objects.all()

    # only return ProfileSets that are linked to the user
    # for anonymous requests, return anything linked to username 'demo'
    def get_object(self):
        queryset = self.get_queryset()
        if self.request.user.is_authenticated:
            obj = get_object_or_404(queryset, owner=self.request.user)
        else:
            User = get_user_model()
            obj = get_object_or_404(queryset, owner=User.objects.get(username="demo"))
        return obj

class ProfileList(generics.ListCreateAPIView):
    """
    Returns a list of all available profiles.
    Profiles are actually SQLite database files set up for
    data collection with Geopaparazzi by an administrator.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

class BasemapList(generics.ListCreateAPIView):
    queryset = Basemap.objects.all()
    serializer_class = BasemapSerializer
    permission_classes = (permissions.IsAuthenticated,)

class BasemapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Basemap.objects.all()
    serializer_class = BasemapSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SpatialitedbsList(generics.ListCreateAPIView):
    queryset = Spatialitedbs.objects.all()
    serializer_class = SpatialitedbsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SpatialitedbsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spatialitedbs.objects.all()
    serializer_class = SpatialitedbsSerializer
    permission_classes = (permissions.IsAuthenticated,)

class OtherfilesList(generics.ListCreateAPIView):
    queryset = Otherfiles.objects.all()
    serializer_class = OtherfilesSerializer
    permission_classes = (permissions.IsAuthenticated,)

class OtherfilesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Otherfiles.objects.all()
    serializer_class = OtherfilesSerializer
    permission_classes = (permissions.IsAuthenticated,)

# generic fileupload view
class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

class UserProjectsViewSet(ModelViewSet):

    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, document=self.request.data.get('document'))

def Catalog(request):
    """ View function for home page
    showing summary info about the profile data
    """
    # counts of database records
    num_projects = Project.objects.count()
    num_otherfiles = Otherfiles.objects.count()
    num_tags = Tag.objects.count()
    num_spatialitedbs = Spatialitedbs.objects.count()
    num_basemaps = Basemap.objects.count()
    num_profiles = Profile.objects.count()
    num_userprojects = UserProject.objects.count()
    # user stats
    user = get_user_model()
    num_users = user.objects.count()
    num_superusers = user.objects.filter(is_superuser=True).count()
    num_profilesets = ProfileSet.objects.count()
    # get the latest dates
    rcd_dates = []
    try:
        rcd_dates.append(Project.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    try:
        rcd_dates.append(Otherfiles.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    try:
        rcd_dates.append(Tag.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    try:
        rcd_dates.append(Spatialitedbs.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    try:
        rcd_dates.append(Basemap.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    last_rcd = max(rcd_dates).strftime("%Y-%m-%d %H:%M:%S")
    usr_dates = []
    try:
        usr_dates.append(Profile.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    try:
        usr_dates.append(UserProject.objects.latest('modifieddate').modifieddate)
    except ObjectDoesNotExist:
        pass
    last_usr = max(usr_dates).strftime("%Y-%m-%d %H:%M:%S")

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context=dict(num_projects=num_projects, num_otherfiles=num_otherfiles, num_tags=num_tags,
                     num_spatialitedbs=num_spatialitedbs, num_basemaps=num_basemaps, num_profiles=num_profiles,
                     num_userprojects=num_userprojects, num_users=num_users, num_superusers=num_superusers,
                     num_profilesets=num_profilesets, last_rcd=last_rcd, last_usr=last_usr),
    )

