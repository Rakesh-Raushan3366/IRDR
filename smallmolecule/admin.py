from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *


class profile_smallmoleculeAdmin(ImportExportModelAdmin):
    pass


class demographic_smallmoleculeAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_smallmolecule, profile_smallmoleculeAdmin),
admin.site.register(demographic_smallmolecule, demographic_smallmoleculeAdmin),
from django.contrib import admin

# Register your models here.
