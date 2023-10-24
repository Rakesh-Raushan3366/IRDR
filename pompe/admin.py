from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


class profile_pompeAdmin(ImportExportModelAdmin):
    pass


class demographic_pompeAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_pompe, profile_pompeAdmin),
admin.site.register(demographic_pompe, demographic_pompeAdmin),
