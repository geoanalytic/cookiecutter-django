# Create your tasks here
from __future__ import absolute_import, unicode_literals
import os
from datetime import datetime, timezone
# from celery import shared_task
from geopaparazzi_reference_server.taskapp.celery import app
import sqlite3
import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from gp_projects.models import ImageNote, Note, TrackFeature
from django.contrib.gis.geos import Point, LineString
from django.core.files import File
from django.core.files.storage import default_storage


@app.task
def LoadUserProject(userproject_file, ownerid):
    """ given an uploaded Geopaparazzi UserProject
    extract the useful bits and load them to the database
    """
    # before we can open the database file, it must be copied locally!
    document = default_storage.open(userproject_file, 'rb')
    userproject = tempfile.NamedTemporaryFile(delete=False)
    # this might be a memory problem!
    data = document.read()
    userproject.write(data)
    userproject.close()

    # get the owner from the ownerid
    User = get_user_model()
    owner = User.objects.get(id=ownerid)

    # connect to the database
    conn = sqlite3.connect(userproject.name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # import gpstracks if any
    for gpslog in c.execute('SELECT * FROM gpslogs;'):
        log_dict = dict(gpslog)
        rcd = TrackFeature(owner=owner, text=log_dict['text'])
        rcd.timestamp_start = datetime.utcfromtimestamp(log_dict['startts']/1000).replace(tzinfo=timezone.utc)
        rcd.timestamp_end = datetime.utcfromtimestamp(log_dict['endts']/1000).replace(tzinfo=timezone.utc)
        rcd.lengthm = log_dict['lengthm']
        d = conn.cursor()
        plist = []
        for pt in d.execute('SELECT * FROM gpslogsdata WHERE logid=? ORDER BY ts ASC', (log_dict['_id'],)):
            pt_dict = dict(pt)
            plist.append(Point(pt_dict['lon'], pt_dict['lat']))
        rcd.linestring = LineString(plist)
        rcd.save()
        d.close()

    # import notes and images together in order to preserve relationships
    for nt in c.execute('SELECT * from notes;'):
        nt_dict = dict(nt)
        rcd = Note(owner=owner, text= nt_dict['text'], form = nt_dict['form'])
        rcd.timestamp = datetime.utcfromtimestamp(nt_dict['ts']/1000).replace(tzinfo=timezone.utc)
        rcd.description = nt_dict['description']
        rcd.lat = nt_dict['lat']
        rcd.lon = nt_dict['lon']
        rcd.location = Point(rcd.lon, rcd.lat)
        rcd.altitude = nt_dict['altim']
        rcd.save()  # save the Note here so that we can refer to it when creating ImageNote records
        d = conn.cursor()
        for im in d.execute('SELECT * FROM images WHERE note_id=?;', (nt_dict['_id'],)):
            im_dict = dict(im)
            imgrcd = ImageNote(owner=owner, note=rcd, azimuth=im_dict['azim'])
            imgrcd.timestamp = datetime.utcfromtimestamp(im_dict['ts']/1000).replace(tzinfo=timezone.utc)
            imgrcd.lat = im_dict['lat']
            imgrcd.lon = im_dict['lon']
            imgrcd.location = Point(imgrcd.lon, imgrcd.lat)
            imgrcd.altitude = im_dict['altim']
            e = conn.cursor()
            e.execute('SELECT * FROM imagedata WHERE _id=?;', (im_dict['_id'],))
            img = e.fetchone()
            img_dict = dict(img)
            # the full image
            blob = img_dict['data']
            with open(im_dict['text'], 'wb') as output_file:
                output_file.write(blob)
            qf = open(im_dict['text'], 'rb')
            imgrcd.image = File(qf)
            # the thumbnail
            blob = img_dict['thumbnail']
            thmname = 'thm_{0}'.format(im_dict['text'])
            with open(thmname, 'wb') as output_file:
                output_file.write(blob)
            qt = open(thmname, 'rb')
            imgrcd.thumbnail = File(qt)
            imgrcd.save()
            # clean up temporary image files
            qf.close()
            os.remove(im_dict['text'])
            qt.close()
            os.remove(thmname)

    # clean up the temporary file
    userproject.close()
    os.remove(userproject.name)

