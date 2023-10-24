from django.contrib import admin

# Register your models here.
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


class profile_fabryAdmin(ImportExportModelAdmin):
    pass


class demographic_fabryAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_fabry, profile_fabryAdmin),
admin.site.register(demographic_fabry, demographic_fabryAdmin),
