from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import TrackFeature, ImageNote, Note


class TrackFeatureSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = TrackFeature
        geo_field = "linestring"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('timestamp_start', 'timestamp_end', 'owner', 'lengthm', 'text')


class ImageNoteSerializer(GeoFeatureModelSerializer):
    """ A class to serialize ImageNotes as geojson """
    class Meta:
        model = ImageNote
        geo_field = "location"
        fields = ('id', 'location', 'lat', 'lon', 'altitude', 'azimuth', 'timestamp', 'owner', 'note')


class NGImageNoteSerializer(serializers.ModelSerializer):
    """ A class to serialize ImageNotes without the geo bits """
    class Meta:
        model = ImageNote
        fields = ('id', 'lat', 'lon', 'altitude', 'azimuth', 'timestamp', 'owner', 'note', 'image')


class NGTrackFeatureSerializer(serializers.ModelSerializer):
    """ A class to serialize Tracks without the geo bits """
    class Meta:
        model = TrackFeature
        fields = ('id', 'timestamp_start', 'timestamp_end', 'owner', 'text', 'lengthm')
