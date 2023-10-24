from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin


class StateAdmin(ImportExportModelAdmin):
    pass


class DistrictAdmin(ImportExportModelAdmin):
    pass


class RegisterAdmin(ImportExportModelAdmin):
    pass


admin.site.register(State, StateAdmin),
admin.site.register(District, DistrictAdmin),
admin.site.register(Register, RegisterAdmin),
admin.site.register(Opd_attendance,),
