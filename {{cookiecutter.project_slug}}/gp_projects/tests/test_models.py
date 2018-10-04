from django.test import TestCase
import datetime
from ..models import Note, ImageNote, TrackFeature
from django.contrib.gis.geos import Point, LineString
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


# Some tests of the various models for the geopaparazzi user project services
class TestNote(TestCase):
    def setUp(self):
        self.owner = UserFactory.build()
        self.owner.save()
        self.location = Point(-114.38, 52.12)
        self.form = '{"sectionname":"Image Note","sectiondescription":"note with image","forms":[{"formname":"image note","formitems":[{"key":"description","islabel":"true","value":"cutline 1","type":"string","mandatory":"no"},{"key":"pictures of the environment around the note","value":"11;12","type":"pictures"}]}]}'
        self.note = Note.objects.create(location=self.location,
                                        lat=52.12, lon=-114.38, altitude=1105.5,
                                        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                                        owner=self.owner, form=self.form, description='POI',
                                        text='Test text here')

    def test_create_note(self):
        self.assertIsInstance(self.note, Note)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class TestImageNote(TestCase):
    def setUp(self):
        self.owner = UserFactory.build()
        self.owner.save()
        self.location = Point(-114.38, 52.12)
        self.form = '{"sectionname":"Image Note","sectiondescription":"note with image","forms":[{"formname":"image note","formitems":[{"key":"description","islabel":"true","value":"cutline 1","type":"string","mandatory":"no"},{"key":"pictures of the environment around the note","value":"11;12","type":"pictures"}]}]}'
        self.note = Note.objects.create(location=self.location,
                                        lat=52.12, lon=-114.38, altitude=1105.5,
                                        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                                        owner=self.owner, form=self.form, description='POI',
                                        text='Image note')
        self.tempfile = tempfile.NamedTemporaryFile()
        self.document = SimpleUploadedFile(self.tempfile.name, b'some example data for our file')
        self.imagenote = ImageNote.objects.create(location=self.location,
                                                  lat=52.12, lon=-114 - 38, altitude=1105.5, azimuth=328.12,
                                                  timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
                                                  owner=self.owner, image=self.document,
                                                  note=self.note)

    def test_create_image(self):
        self.assertIsInstance(self.imagenote, ImageNote)

class TestTrackFeature(TestCase):
    def setUp(self):
        self.timestamp_start = datetime.datetime.now(tz=datetime.timezone.utc)
        self.owner = UserFactory.build()
        self.owner.save()
        self.linestring = LineString(Point(-114.38, 52.12),Point(-114.381, 52.123),Point(-114.389, 52.123),Point(-114.386, 52.119))
        self.timestamp_end = datetime.datetime.now(tz=datetime.timezone.utc)
        self.trackfeature = TrackFeature.objects.create(linestring=self.linestring, owner=self.owner,
                                                        timestamp_start=self.timestamp_start,
                                                        timestamp_end=self.timestamp_end, text='some test text')

    def test_create_track(self):
        self.assertIsInstance(self.trackfeature, TrackFeature)
