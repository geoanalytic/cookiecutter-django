from rest_framework import generics, permissions
from .models import TrackFeature, ImageNote, Note
from .serializers import TrackFeatureSerializer, ImageNoteSerializer, NGImageNoteSerializer, NGTrackFeatureSerializer
from django.http import HttpResponse
from django.core.serializers import serialize


# Geojson serializer
def geojsonTrackFeed(request):
    return HttpResponse(serialize('geojson', TrackFeature.objects.all(), fields=('timestamp_start', 'linestring')))


class TrackList(generics.ListAPIView):
    serializer_class = TrackFeatureSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return TrackFeature.objects.filter(owner=user).defer('linestring')


class TrackDetail(generics.RetrieveAPIView):
    queryset = TrackFeature.objects.all()
    serializer_class = TrackFeatureSerializer
    permission_classes = (permissions.IsAuthenticated,)


class NGTrackFeatureList(generics.ListAPIView):
    serializer_class = NGTrackFeatureSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return TrackFeature.objects.filter(owner=user)


class ImageNoteList(generics.ListAPIView):
    serializer_class = ImageNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ImageNote.objects.filter(owner=user)

class ImageNoteDetail(generics.RetrieveAPIView):
    serializer_class = ImageNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ImageNote.objects.filter(owner=user)

class NGImageNoteList(generics.ListAPIView):
    serializer_class = NGImageNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ImageNote.objects.filter(owner=user)


class NGImageNoteDetail(generics.RetrieveAPIView):
    serializer_class = NGImageNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ImageNote.objects.filter(owner=user)


