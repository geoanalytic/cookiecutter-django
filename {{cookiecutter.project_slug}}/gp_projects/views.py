from rest_framework import generics, permissions
from .models import TrackFeature, ImageNote, Note
from .serializers import TrackFeatureSerializer, ImageNoteSerializer, NGImageNoteSerializer, NGTrackFeatureSerializer, NGNoteSerializer
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.shortcuts import render
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


class NGNoteList(generics.ListAPIView):
    serializer_class = NGNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner=user)


class NGNoteDetail(generics.RetrieveAPIView):
    serializer_class = NGNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(owner=user)


def UserView(request):
    """a view of all the userdata owned by the requesting owner"""
    date_list = Note.objects.annotate(date=TruncDate('timestamp')).distinct('date').values('date')
    note_list = Note.objects.filter(owner=request.user)
    image_list = ImageNote.objects.filter(owner=request.user)
    track_list = TrackFeature.objects.filter(owner=request.user)
    context = {'date_list': date_list, 'note_list': note_list, 'image_list': image_list, 'track_list': track_list}
    return render(request, 'userproj.html', context)
