from django.contrib.gis import admin

# Register your models here.
from profiles.models import Project, UserProject, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, ProfileSet
admin.site.register(Project)
admin.site.register(UserProject)
admin.site.register(Tag)
admin.site.register(Basemap)
admin.site.register(Spatialitedbs)
admin.site.register(Otherfiles)
admin.site.register(Profile)
admin.site.register(ProfileSet)