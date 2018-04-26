from test_plus.test import TestCase
from django.urls import reverse
from ..models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile
from ..serializers import ProjectSerializer, TagSerializer, BasemapSerializer, SpatialitedbsSerializer, OtherfilesSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point

# Some tests of the various models for the geopaparazzi cloud profile services
 
class TestProject(TestCase):
    def setUp(self):
        self.project = Project.objects.create(path="testpath",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')

    def test__str__(self):
        self.assertEqual(self.project.__str__(), 'testpath')

    def test_size(self):
        self.assertEqual(self.project.size, '54056')

    def test_create_project(self):
        self.assertIsInstance(self.project, Project)


class TestTags(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='56656')

    def test__str__(self):
        self.assertEqual(self.tag.__str__(), 'testpath1')

    def test_size(self):
        self.assertEqual(self.tag.size, '56656')

    def test_create_tag(self):
        self.assertIsInstance(self.tag, Tag)

class TestBasemaps(TestCase):
    def setUp(self):
        self.basemap = Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656')

    def test__str__(self):
        self.assertEqual(self.basemap.__str__(), 'testpath1')

    def test_size(self):
        self.assertEqual(self.basemap.size, '5666656')

    def test_create_basemap(self):
        self.assertIsInstance(self.basemap, Basemap)

class TestSpatialitedbss(TestCase):
    def setUp(self):
        self.spatialitedb = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])

    def test__str__(self):
        self.assertEqual(self.spatialitedb.__str__(), 'testpath1')

    def test_size(self):
        self.assertEqual(self.spatialitedb.size, '5666656')

    def test_create_spatialitedb(self):
        self.assertIsInstance(self.spatialitedb, Spatialitedbs)

class TestOtherfiles(TestCase):
    def setUp(self):
        self.location = Point(-114.38, 52.12)
        self.otherfile = Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656', location=self.location)
        
    def test__str__(self):
        self.assertEqual(self.otherfile.__str__(), 'testpath1')

    def test_size(self):
        self.assertEqual(self.otherfile.size, '5666656')

    def test_location(self):
        self.assertEqual(self.otherfile.location.wkt, 'POINT (-114.38 52.12)')

    def test_create_otherfile(self):
        self.assertIsInstance(self.otherfile, Otherfiles)

