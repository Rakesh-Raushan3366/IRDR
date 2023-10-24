from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


class profile_metabolismAdmin(ImportExportModelAdmin):
    pass


class demographic_matabolismAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_metabolism, profile_metabolismAdmin),
admin.site.register(demographic_matabolism, demographic_matabolismAdmin),
