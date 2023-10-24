from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin

# Register your models here.


class profile_pidAdmin(ImportExportModelAdmin):
    pass


class demopraphic_pidAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_pid, profile_pidAdmin),
admin.site.register(demopraphic_pid, demopraphic_pidAdmin),