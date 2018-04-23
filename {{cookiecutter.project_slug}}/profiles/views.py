from django.shortcuts import get_object_or_404
from profiles.models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, ProfileSet, UserProject
from profiles.serializers import ProjectSerializer, TagSerializer, BasemapSerializer, UserProjectSerializer
from profiles.serializers import SpatialitedbsSerializer, OtherfilesSerializer, ProfileSerializer, ProfileSetSerializer 
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from django.contrib.auth import get_user_model

class MyProfiles(generics.RetrieveAPIView):
#    queryset = ProfileList.objects.all
    serializer_class = ProfileSetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
#        user = self.request.user
        return ProfileSet.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, owner=self.request.user)
        return obj

class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BasemapList(generics.ListCreateAPIView):
    queryset = Basemap.objects.all()
    serializer_class = BasemapSerializer

class BasemapDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Basemap.objects.all()
    serializer_class = BasemapSerializer

class SpatialitedbsList(generics.ListCreateAPIView):
    queryset = Spatialitedbs.objects.all()
    serializer_class = SpatialitedbsSerializer

class SpatialitedbsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spatialitedbs.objects.all()
    serializer_class = SpatialitedbsSerializer
    
class OtherfilesList(generics.ListCreateAPIView):
    queryset = Otherfiles.objects.all()
    serializer_class = OtherfilesSerializer

class OtherfilesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Otherfiles.objects.all()
    serializer_class = OtherfilesSerializer

# generic fileupload view
class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

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
