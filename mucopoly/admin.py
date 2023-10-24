from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *
from django.contrib import admin


# Register your models here.


class profile_mucopolysaccharidosisAdmin(ImportExportModelAdmin):
    pass


class demographic_mucopolysaccharidosisAdmin(ImportExportModelAdmin):
    pass


admin.site.register(profile_mucopolysaccharidosis, profile_mucopolysaccharidosisAdmin),
admin.site.register(demographic_mucopolysaccharidosis, demographic_mucopolysaccharidosisAdmin),
