from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin


# Register your models here.


class profile_thalassemiaAdmin(ImportExportModelAdmin):
    pass


class demographic_thalassemiaAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_thalassemia, profile_thalassemiaAdmin),
admin.site.register(demographic_thalassemia, demographic_thalassemiaAdmin),
