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
        fields = ('id', 'lat', 'lon', 'altitude', 'azimuth', 'timestamp', 'owner', 'note', 'image', 'thumbnail')


class NGTrackFeatureSerializer(serializers.ModelSerializer):
    """ A class to serialize Tracks without the geo bits """

    class Meta:
        model = TrackFeature
        fields = ('id', 'timestamp_start', 'timestamp_end', 'owner', 'text', 'lengthm')


class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class NoteSerializer(GeoFeatureModelSerializer):
    """ A class to serialize Notes as geojson """

    class Meta:
        model = Note
        geo_field = "location"
        fields = ('id', 'location', 'lat', 'lon', 'altitude', 'timestamp', 'owner', 'text', 'form')


class NGNoteSerializer(serializers.ModelSerializer):
    """ A class to serialize Notes without the geo bits """
    images = ImageUrlField(
        many=True,
        read_only=True,
     )


    class Meta:
        model = Note
        fields = ('id', 'lat', 'lon', 'altitude', 'timestamp', 'owner', 'text', 'form', 'images')
