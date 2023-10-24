from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin

# Register your models here.

class profile_nmdAdmin(ImportExportModelAdmin):
    pass


class demographic_nmdAdmin(ImportExportModelAdmin):
    pass


class spinal_nmdAdmin(ImportExportModelAdmin):
    pass


class dsystophinopathy_nmdAdmin(ImportExportModelAdmin):
    pass


class limb_gridle_nmdAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_nmd, profile_nmdAdmin),
admin.site.register(demographic_nmd, demographic_nmdAdmin),
admin.site.register(spinal_nmd, spinal_nmdAdmin),
admin.site.register(dsystophinopathy_nmd, dsystophinopathy_nmdAdmin),
admin.site.register(limb_gridle_nmd, limb_gridle_nmdAdmin),