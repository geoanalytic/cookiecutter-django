from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile
from ..serializers import ProjectSerializer, TagSerializer, BasemapSerializer, SpatialitedbsSerializer, \
    OtherfilesSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


# Some tests of the various REST endpoints for the geopaparazzi services


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ProfilesAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = UserFactory.build()
        self.user1.save()
        self.client.login(username=self.user1.username, password=self.user1.password)
        self.tempfile = tempfile.NamedTemporaryFile()
        self.document = SimpleUploadedFile(self.tempfile.name, b'some example data for our file')

    def test_post_project(self):
        self.client.force_authenticate(self.user1)
        data = {'path': 'SomeBs/trails.json', 'url': self.document,
                'uploadurl': 'http://gpap.trailstewards.com/userprojects'}
        response = self.client.post(reverse('project-list'), data=data, extra={'format': 'multipart'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_tag(self):
        self.client.force_authenticate(self.user1)
        data = {'path': 'SomeBs/trails.json', 'url': self.document}
        response = self.client.post(reverse('tag-list'), data=data, extra={'format': 'multipart'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_basemap(self):
        self.client.force_authenticate(self.user1)
        data = {'path': 'SomeBs/trails.json', 'url': self.document}
        response = self.client.post(reverse('basemap-list'), data=data, extra={'format': 'multipart'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_spatialitedb(self):
        self.client.force_authenticate(self.user1)
        data = {'path': 'SomeBs/trails.json', 'url': self.document,
                'uploadurl': 'http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite',
                'visible': ['one', 'two', 'three']}
        response = self.client.post(reverse('spatialitedb-list'), data=data, extra={'format': 'multipart'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_otherfile(self):
        self.client.force_authenticate(self.user1)
        data = {'path': 'SomeBs/trails.json', 'url': self.document}
        response = self.client.post(reverse('otherfile-list'), data=data, extra={'format': 'multipart'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class GetAllProfiles(APITestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile()
        self.document = SimpleUploadedFile(self.tempfile.name, b'some example data for our file')
        self.project = Project.objects.create(path="testpath", url=self.document,
                                              uploadurl='http://gpap.trailstewards.com/userprojects')
        self.tag = Tag.objects.create(path="testpath1", url=self.document)
        self.basemap = Basemap.objects.create(path="testpath1", url=self.document)
        self.spatialitedb = Spatialitedbs.objects.create(path="testpath1", url=self.document,
                                                         uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite',
                                                         visible=["sites", "atv"])
        self.otherfile = Otherfiles.objects.create(path="testpath1", url=self.document)
        self.profile1 = Profile.objects.create(name="test", description="test profile", color="#FFFFFF", active=True,
                                               sdcardPath="MAINSTORAGE",
                                               mapView="52.0,-110.5,11", project=self.project, tags=self.tag)
        self.profile1.basemaps.add(self.basemap)
        self.profile1.spatialitedbs.add(self.spatialitedb)
        self.profile1.otherfiles.add(self.otherfile)
        self.profile2 = Profile.objects.create(name="test2", description="test profile2", color="#FFEFF", active=False,
                                               sdcardPath="MAINSTORAGE",
                                               mapView="52.0,-110.5,11", project=self.project, tags=self.tag)
        self.profile2.basemaps.add(self.basemap)
        self.profile2.spatialitedbs.add(self.spatialitedb)
        self.user1 = UserFactory.build()
        self.user1.save()
        self.client.login(username=self.user1.username, password=self.user1.password)

    def test_get_all_projects(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('project-list'))
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(response.data['results'][0]['path'], serializer.data[0]['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_projects(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('project-detail', kwargs={'pk': self.project.pk}))
        project = Project.objects.get(pk=self.project.pk)
        serializer = ProjectSerializer(project)
        self.assertEqual(response.data['path'], serializer.data['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_projects(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('project-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_tags(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('tag-list'))
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data['results'][0]['path'], serializer.data[0]['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_tag(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('tag-detail', kwargs={'pk': self.tag.pk}))
        tag = Tag.objects.get(pk=self.tag.pk)
        serializer = TagSerializer(tag)
        self.assertEqual(response.data['path'], serializer.data['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_tag(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('tag-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_basemaps(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('basemap-list'))
        basemaps = Basemap.objects.all()
        serializer = BasemapSerializer(basemaps, many=True)
        self.assertEqual(response.data['results'][0]['path'], serializer.data[0]['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_basemap(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('basemap-detail', kwargs={'pk': self.basemap.pk}))
        basemap = Basemap.objects.get(pk=self.basemap.pk)
        serializer = BasemapSerializer(basemap)
        self.assertEqual(response.data['path'], serializer.data['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_basemap(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('basemap-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_spatialitedbss(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('spatialitedb-list'))
        spatialitedbs = Spatialitedbs.objects.all()
        serializer = SpatialitedbsSerializer(spatialitedbs, many=True)
        self.assertEqual(response.data['results'][0]['path'], serializer.data[0]['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_spatialitedbs(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('spatialitedb-detail', kwargs={'pk': self.spatialitedb.pk}))
        spatialitedbs = Spatialitedbs.objects.get(pk=self.spatialitedb.pk)
        serializer = SpatialitedbsSerializer(spatialitedbs)
        self.assertEqual(response.data['path'], serializer.data['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_spatialitedbs(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('spatialitedb-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_otherfiles(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('otherfile-list'))
        otherfiles = Otherfiles.objects.all()
        serializer = OtherfilesSerializer(otherfiles, many=True)
        self.assertEqual(response.data['results'][0]['path'], serializer.data[0]['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_otherfile(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('otherfile-detail', kwargs={'pk': self.otherfile.pk}))
        otherfile = Otherfiles.objects.get(pk=self.otherfile.pk)
        serializer = OtherfilesSerializer(otherfile)
        self.assertEqual(response.data['path'], serializer.data['path'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_otherfile(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('otherfile-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_profiles(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('profile-list'))
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data['results'][0]['name'], serializer.data[0]['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_profile(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('profile-detail', kwargs={'pk': self.profile1.pk}))
        profile = Profile.objects.get(pk=self.profile1.pk)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_profile(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(reverse('profile-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
