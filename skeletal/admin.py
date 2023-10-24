from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin


# Register your models here.

class profile_skeletalAdmin(ImportExportModelAdmin):
    pass


class demographic_pompeAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_skeletal, profile_skeletalAdmin),
admin.site.register(demographic_skeletal, demographic_pompeAdmin),
