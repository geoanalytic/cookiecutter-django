from django.contrib.gis import admin

# Register your models here.
from profiles.models import Project, UserProject, Tag, Basemap, Spatialitedbs, Otherfiles, Profile, ProfileSet

# a simple django admin page for a model
admin.site.register(Project)

# here is a more complex ModelAdmin example
class UserProjectAdmin(admin.ModelAdmin):
    date_hierarchy = 'modifieddate'
    list_display = ('__str__', 'owner')
    list_filter = ('owner',)
    search_fields = ['document', 'description', 'owner__name', 'owner__email']
    
admin.site.register(UserProject, UserProjectAdmin)

admin.site.register(Tag)
admin.site.register(Basemap)
admin.site.register(Spatialitedbs)
admin.site.register(Otherfiles)
admin.site.register(Profile)
admin.site.register(ProfileSet)