from collections import OrderedDict
from rest_framework import serializers
from profiles.models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, ProfileSet
from profiles.models import UserProject
from django.contrib.auth import get_user_model
from rest_framework.fields import SkipField

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('path', 'modifieddate', 'url', 'uploadurl', 'size' )

    # this bit is for omitting empty fields (size)
    def to_representation(self, instance):
        result = super(ProjectSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class UserProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='id')
    
    class Meta:
        model = UserProject
        fields = ('modifieddate', 'owner', 'document', 'description')
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('path', 'modifieddate', 'url', 'size' )

    # this bit is for omitting empty fields (size)
    def to_representation(self, instance):
        result = super(TagSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class BasemapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basemap
        fields = ('path', 'modifieddate', 'url', 'size' )

    # this bit is for omitting empty fields (size)
    def to_representation(self, instance):
        result = super(BasemapSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class SpatialitedbsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spatialitedbs
        fields = ('path', 'modifieddate', 'url', 'size', 'uploadurl', 'visible' )

    # this bit is for omitting empty fields (size)
    def to_representation(self, instance):
        result = super(SpatialitedbsSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class OtherfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otherfiles
        fields = ('path', 'modifieddate', 'url', 'size' )

    # this bit is for omitting empty fields (size)
    def to_representation(self, instance):
        result = super(OtherfilesSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

class ProfileSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    tags = TagSerializer(read_only=True)
    basemaps = BasemapSerializer(many=True, read_only=True)
    spatialitedbs = SpatialitedbsSerializer(many=True, read_only=True)
    otherfiles = OtherfilesSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ('name', 'description', 'creationdate', 'modifieddate', 'color', 'active',
                  'sdcardPath', 'mapView', 'project', 'tags', 'basemaps', 'spatialitedbs', 'otherfiles' )

class ProfileSetSerializer(serializers.ModelSerializer):
    profiles = ProfileSerializer(read_only=True, many=True)
    class Meta:
        model = ProfileSet
        fields = ('formatVersion', 'profiles')
