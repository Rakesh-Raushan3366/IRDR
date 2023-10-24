from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


# Register your models here.
class profile_glycogenAdmin(ImportExportModelAdmin):
    pass


class demographic_glycogenAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_glycogen, profile_glycogenAdmin),
admin.site.register(demographic_glycogen, demographic_glycogenAdmin),
