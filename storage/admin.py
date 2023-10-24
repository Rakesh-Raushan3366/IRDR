from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin

# Register your models here.
class profile_storageAdmin(ImportExportModelAdmin):
    pass


class demographic_storageAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_storage, profile_storageAdmin),
admin.site.register(demographic_storage, demographic_storageAdmin),