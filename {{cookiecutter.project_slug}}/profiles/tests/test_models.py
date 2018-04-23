from test_plus.test import TestCase, APITestCase
from django.urls import reverse
from ..models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile
from ..serializers import ProjectSerializer, TagSerializer, BasemapSerializer, SpatialitedbsSerializer, OtherfilesSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist

# Some tests of the various REST endpoints for the geopaparazzi services
 
class GetAllProjects(APITestCase):
    def setUp(self):
        Project.objects.create(path="testpath",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
        Project.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
            
    def test_get_all_projects(self):
        response = self.get('project-list')
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

class GetSingleProjects(APITestCase):
    def setUp(self):
        self.test1 = Project.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
        self.test2 = Project.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='77756')
        self.test3 = Project.objects.create(path="testpath3",url='http://bobmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='66656')
            
    def test_get_single_projects(self):
        response = self.get(reverse('project-detail', kwargs={'pk': self.test1.pk}))
        project = Project.objects.get(pk=self.test1.pk)
        serializer = ProjectSerializer(project)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_projects(self):
        response = self.get(reverse('project-detail', kwargs={'pk': 30}))
        self.response_404(response)
        
class _ProjectAPITestCase(APITestCase):     
    def test_post(self):
        data = {'testing': {'path': 'SomeBs/trails.json', 'url': 'http://webmap.geoanalytic.com/download/Trails/trails.gpap', 'uploadurl': 'http://gpap.trailstewards.com/userprojects'}}
        self.post('project-list', data=data, extra={'format': 'json'})
        self.response_201()

class GetAllTags(APITestCase):
    def setUp(self):
        Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='56656')
        Tag.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='54056')
            
    def test_get_all_tags(self):
        response = self.get('tag-list')
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

class GetSingleTags(APITestCase):
    def setUp(self):
        self.test1 = Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='54056')
        self.test2 = Tag.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='56656')
        self.test3 = Tag.objects.create(path="testpath3",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='57756')        
            
    def test_get_single_tag(self):
        response = self.get(reverse('tag-detail', kwargs={'pk': self.test1.pk}))
        tag = Tag.objects.get(pk=self.test1.pk)
        serializer = TagSerializer(tag)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_tag(self):
        response = self.get(reverse('tag-detail', kwargs={'pk': 30}))
        self.response_404(response)

class TagAPITestCase(APITestCase):     
    def test_post(self):
        data = {'testing': {'path': 'SomeBs/trails.json', 'url': 'http://webmap.geoanalytic.com/download/Trails/trails.gpap', 'size': '55565' }}
        self.post('tag-list', data=data, extra={'format': 'json'})
        self.response_201()

class GetAllBasemaps(APITestCase):
    def setUp(self):
        Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656')
        Basemap.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.map', size='5405776')
            
    def test_get_all_basemaps(self):
        response = self.get('basemap-list')
        basemaps = Basemap.objects.all()
        serializer = BasemapSerializer(basemaps, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

class GetSingleBasemaps(APITestCase):
    def setUp(self):
        self.test1 = Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='54056')
        self.test2 = Basemap.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.map', size='56656')
        self.test3 = Basemap.objects.create(path="testpath3",url='http://webmap.geoanalytic.com/download/Trails/Canada.map', size='57756')        
            
    def test_get_single_basemap(self):
        response = self.get(reverse('basemap-detail', kwargs={'pk': self.test3.pk}))
        basemap = Basemap.objects.get(pk=self.test3.pk)
        serializer = BasemapSerializer(basemap)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_basemap(self):
        response = self.get(reverse('basemap-detail', kwargs={'pk': 30}))
        self.response_404(response)

class BasemapAPITestCase(APITestCase):     
    def test_post(self):
        data = {'testing': {'path': 'SomeBs/trails.json', 'url': 'http://webmap.geoanalytic.com/download/Trails/Manitoba.map', 'size': '5557765' }}
        self.post('basemap-list', data=data, extra={'format': 'json'})
        self.response_201()

class GetAllSpatialitedbss(APITestCase):
    def setUp(self):
        Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])
        Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', size='5666656', visible=[])
            
    def test_get_all_spatialitedbss(self):
        response = self.get('spatialitedb-list')
        spatialitedbs = Spatialitedbs.objects.all()
        serializer = SpatialitedbsSerializer(spatialitedbs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

class GetSingleSpatialitedbss(APITestCase):
    def setUp(self):
        self.test1 = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])
        self.test2 = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', size='5666656', visible=[])
        self.test3 = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Canada.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Canada.sqlite', size='5666656', visible=["one","two","three"])      
            
    def test_get_single_spatialitedbs(self):
        response = self.get(reverse('spatialitedb-detail', kwargs={'pk': self.test3.pk}))
        spatialitedbs = Spatialitedbs.objects.get(pk=self.test3.pk)
        serializer = SpatialitedbsSerializer(spatialitedbs)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_spatialitedbs(self):
        response = self.get(reverse('spatialitedb-detail', kwargs={'pk': 30}))
        self.response_404(response)

class SpatialitedbsAPITestCase(APITestCase):     
    def test_post(self):
        data = {'path': 'SomeBs/trails.json', 'modifieddate': '2018-01-24 13:00:00', 'url': 'http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', 'size': '5557765',
            'uploadurl': 'http://webmap.geoanalytic.com/download/Trails/Manitoba.sqlite', 'visible': ['one','two','three']}
        self.post('spatialitedb-list', data=data, extra={'format': 'json'})
        self.response_201()

class GetAllOtherfiles(APITestCase):
    def setUp(self):
        Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656')
        Otherfiles.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.map', size='5405776')
            
    def test_get_all_otherfiles(self):
        response = self.get('otherfile-list')
        otherfiles = Otherfiles.objects.all()
        serializer = OtherfilesSerializer(otherfiles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

class GetSingleOtherfiles(APITestCase):
    def setUp(self):
        self.test1 = Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='54056')
        self.test2 = Otherfiles.objects.create(path="testpath2",url='http://webmap.geoanalytic.com/download/Trails/Manitoba.map', size='56656')
        self.test3 = Otherfiles.objects.create(path="testpath3",url='http://webmap.geoanalytic.com/download/Trails/Canada.map', size='57756')        
            
    def test_get_single_otherfile(self):
        response = self.get(reverse('otherfile-detail', kwargs={'pk': self.test3.pk}))
        otherfile = Otherfiles.objects.get(pk=self.test3.pk)
        serializer = OtherfilesSerializer(otherfile)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_otherfile(self):
        response = self.get(reverse('otherfile-detail', kwargs={'pk': 30}))
        self.response_404(response)

class OtherfilesAPITestCase(APITestCase):     
    def test_post(self):
        data = {'path': 'SomeBs/trails.json', 'url': 'http://webmap.geoanalytic.com/download/Trails/Manitoba.map', 'size': '5557765' }
        self.post('otherfile-list', data=data, extra={'format': 'json'})
        self.response_201()

class GetAllProfiles(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(path="testpath",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
        self.tag = Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='54056')
        self.basemap = Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='54056')
        self.spatialitedb = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])
        self.otherfile = Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='54056')
        self.profile1 = Profile.objects.create(name="test", description="test profile", color="#FFFFFF",active=True,sdcardPath="MAINSTORAGE",
            mapView="52.0,-110.5,11", project=self.project, tags=self.tag)
        self.profile1.basemaps.add(self.basemap)
        self.profile1.spatialitedbs.add(self.spatialitedb)
        self.profile1.otherfiles.add(self.otherfile)
        self.profile2 = Profile.objects.create(name="test2", description="test profile2", color="#FFEFF",active=False,sdcardPath="MAINSTORAGE",
            mapView="52.0,-110.5,11", project=self.project, tags=self.tag)
        self.profile2.basemaps.add(self.basemap)
        self.profile2.spatialitedbs.add(self.spatialitedb)
            
    def test_get_all_profiles(self):
        response = self.get('profile-list')
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_single_profile(self):
        response = self.get(reverse('profile-detail', kwargs={'pk': self.profile1.pk}))
        profile = Profile.objects.get(pk=self.profile1.pk)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.response_200(response)

    def test_get_invalid_profile(self):
        response = self.get(reverse('profile-detail', kwargs={'pk': 30}))
        self.response_404(response)
        
