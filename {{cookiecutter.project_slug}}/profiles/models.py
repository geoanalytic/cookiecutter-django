import os
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import signals
from .tasks import LoadUserProject

# Geopaparrazi profiles model


class Project(models.Model):
    """ A geopaparrazi project is a SQLite database, typically with a .gpap extension.
    This table keeps track of the blank projects that are provided to the app
    via the profile downloads.  Note that the path field defines where the file
    is stored on the mobile device.

    Future enhancements:
    -  The uploadurl field should be changed to reflect the URL endpoint for uploading
    UserProjects.
    - the size field should be automatically generated
    """
    path = models.CharField(max_length=100, blank=True, default='')
    modifieddate = models.DateTimeField(auto_now_add=True)
    url = models.FileField(upload_to='projects/')
    uploadurl = models.URLField(blank=True)
    size = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        calculate the file size before saving
        """
        self.size = self.url.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path', '-modifieddate',)


def userproject_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/trailstewards/<owner>/userprojects/<filename>
    return 'trailstewards/{0}/userprojects/{1}'.format(instance.owner, os.path.basename(filename))


class UserProject(models.Model):
    """ A table for uploaded project databases
    """
    modifieddate = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('users.user', to_field='id', on_delete=models.CASCADE, blank=True, null=True)
    document = models.FileField(upload_to=userproject_directory_path)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.document.name

    class Meta:
        ordering = ('owner', '-modifieddate',)


def userproject_post_save(sender, instance, signal, *args, **kwargs):
    LoadUserProject.delay(instance.document.name, instance.owner.id)


signals.post_save.connect(userproject_post_save, sender=UserProject)


def tag_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/trailstewards/<owner>/tags/<filename>
    return 'trailstewards/{0}/tags/{1}'.format(instance.owner, os.path.basename(filename))


class Tag(models.Model):
    """ In geopaparrazi, Tags are actually form definitions, which are stored as JSON.
    This table keeps track of these JSON files.

    Future enhancement:  create a form for creating Tag files.
    """
    path = models.CharField(max_length=100, blank=True, default='')
    modifieddate = models.DateTimeField(auto_now_add=True)
    url = models.FileField(upload_to=tag_directory_path)
    size = models.CharField(max_length=30, blank=True, null=True)
    # add description and owner
    owner = models.ForeignKey('users.user', to_field='id', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.size = self.url.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path', '-modifieddate',)

class Basemap(models.Model):
    """ Basemap files are tiled backdrops
    """
    path = models.CharField(max_length=100, blank=True, default='')
    modifieddate = models.DateTimeField(auto_now_add=True)
    url = models.FileField(upload_to='basemaps/')
    size = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.size = self.url.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path', '-modifieddate',)

class Spatialitedbs(models.Model):
    """ Geopaparrazi uses SpatialiteDBs to display overlay vector data.

    Future enhancement:  generate these directly from a PostGIS database.
    """
    path = models.CharField(max_length=100, blank=True, default='')
    modifieddate = models.DateTimeField(auto_now_add=True)
    url = models.FileField(upload_to='spatialitedbs/')
    size = models.CharField(max_length=30, blank=True, null=True)
    uploadurl = models.URLField(blank=True)
    visible = ArrayField(models.CharField(max_length=30))

    def save(self, *args, **kwargs):
        self.size = self.url.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path', '-modifieddate',)

class Otherfiles(models.Model):
    """ This table tracks any other type of content, like images or documents.
    """
    path = models.CharField(max_length=100, blank=True, default='')
    modifieddate = models.DateTimeField(auto_now_add=True)
    url = models.FileField(upload_to='otherfiles/')
    size = models.CharField(max_length=30, blank=True, null=True)
    location = models.PointField(blank=True,null=True)

    def save(self, *args, **kwargs):
        self.size = self.url.size
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        ordering = ('path', '-modifieddate',)

class Profile(models.Model):
    """ The profile is a JSON structure that ties together the basemaps, tags, etc
    for a user to download to their mobile device.
    """
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    creationdate = models.DateTimeField(auto_now_add=True)
    modifieddate = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=30, default="#FBC02D")
    active = models.BooleanField(default=False)
    sdcardPath = models.CharField(max_length=100, default="MAINSTORAGE")
    # TODO capture the mapView field as a geometry point and zoom
    mapView = models.CharField(max_length=100, default="52.02025604248047,-115.70208740234375,10.0")
    project = models.ForeignKey(Project, on_delete = models.SET_NULL, blank=True, null=True)
    tags = models.ForeignKey(Tag, on_delete = models.SET_NULL, blank=True, null=True)
    basemaps = models.ManyToManyField(Basemap, blank=True)
    spatialitedbs = models.ManyToManyField(Spatialitedbs, blank=True)
    otherfiles = models.ManyToManyField(Otherfiles, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('modifieddate', 'name', )

class ProfileSet(models.Model):
    """ A profileset is an owner specific list of profiles that may be downloaded.
    The purpose of this list is to provide an easy entrypoint for geopaparrazi to get
    a list of available profiles using only the username.
    """
    owner = models.OneToOneField('users.user', related_name='profilesets', on_delete=models.CASCADE)
    profiles = models.ManyToManyField(Profile, blank=True)
    formatVersion = models.FloatField(default=1.1)

    def __str__(self):
        return self.owner.username

    class Meta:
        ordering = ('owner',)
