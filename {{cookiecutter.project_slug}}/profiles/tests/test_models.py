from test_plus.test import TestCase
from django.urls import reverse
from ..models import Project, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, UserProject, ProfileSet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import Point
import tempfile
from django.test import override_settings

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

@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TestUserProject(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.tempfile =  tempfile.NamedTemporaryFile()
        self.description = 'a temporary file for testing'
        self.userproject = UserProject(owner=self.user, document=self.tempfile, description=self.description)

    def test__str__(self):
        self.assertEqual(self.userproject.__str__(), self.tempfile.name)
        
    def test_create_userproject(self):
        self.assertIsInstance(self.userproject, UserProject)

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

class TestProfile(TestCase):
    def setUp(self):
        self.project = Project.objects.create(path="testpath",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
        self.tag = Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='56656')
        self.basemap = Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656')
        self.spatialitedb = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])
        self.location = Point(-114.38, 52.12)
        self.otherfile = Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656', location=self.location)
        self.profile = Profile.objects.create(name='testprofile', description='a profile for testing', project=self.project, tags=self.tag)
        self.profile.basemaps.add(self.basemap)
        self.profile.spatialitedbs.add(self.spatialitedb)
        self.profile.otherfiles.add(self.otherfile)

    def test__str__(self):
        self.assertEqual(self.profile.__str__(), 'testprofile')

    def test_create_profile(self):
        self.assertIsInstance(self.profile, Profile)

class TestProfileSet(TestCase):
    def setUp(self):
        self.owner = self.make_user()
        self.owner.save()
        self.project = Project.objects.create(path="testpath",url='http://webmap.geoanalytic.com/download/Trails/trails.gpap',
            uploadurl='http://gpap.trailstewards.com/userprojects', size='54056')
        self.project.save()
        self.tag = Tag.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/trails.json', size='56656')
        self.tag.save()
        self.basemap = Basemap.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656')
        self.basemap.save()
        self.spatialitedb = Spatialitedbs.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', 
            uploadurl='http://webmap.geoanalytic.com/download/Trails/Alberta.sqlite', size='5666656', visible=["sites","atv"])
        self.spatialitedb.save()
        self.location = Point(-114.38, 52.12)
        self.otherfile = Otherfiles.objects.create(path="testpath1",url='http://webmap.geoanalytic.com/download/Trails/Alberta.map', size='5666656', location=self.location)
        self.otherfile.save()
        self.profile1 = Profile.objects.create(name='testprofile', description='a profile for testing', project=self.project, tags=self.tag)
        self.profile1.basemaps.add(self.basemap)
        self.profile1.spatialitedbs.add(self.spatialitedb)
        self.profile1.otherfiles.add(self.otherfile)
        self.profile1.save()
        self.profile2 = Profile.objects.create(name='testprofile2', description='a second profile for testing', project=self.project, tags=self.tag)
        self.profile2.basemaps.add(self.basemap)
        self.profile2.spatialitedbs.add(self.spatialitedb)
        self.profile2.save()
        self.profileset = ProfileSet(owner=self.owner)
        self.profileset.save()
        self.profileset.profiles.add(self.profile1)
        self.profileset.profiles.add(self.profile2)
        
    def test__str__(self):
        self.assertEqual(self.profileset.__str__(), self.owner.username)

    def test_create_profile(self):
        self.assertIsInstance(self.profileset, ProfileSet)

