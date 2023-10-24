from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


# Register your models here.

class profile_bleedingAdmin(ImportExportModelAdmin):
    pass


class demographic_bleedingAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_bleeding, profile_bleedingAdmin),
admin.site.register(demographic_bleeding, demographic_bleedingAdmin),
