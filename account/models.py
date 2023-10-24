from django.db import models

# Create your models here.
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin import (widgets, site as admin_site1)
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminDateWidget, RelatedFieldWidgetWrapper
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import SelectMultiple, TextInput, Select, DateInput, CheckboxSelectMultiple, CheckboxInput
from django.forms import modelformset_factory
from django.forms import Textarea
from multiselectfield import MultiSelectField


class State(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Register(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=200, null=True, validators=[MaxLengthValidator(200)])
    address = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    email = models.EmailField(max_length=300, blank=True, null=True)
    investigator_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    access_sel = [('Super User', 'Super User'), ('Admin', 'Admin'), ('Nodal', 'Nodal'), ('User', 'User')]
    access = models.CharField(max_length=100, null=True, blank=True, default="User", choices=access_sel)
    disable_sel = [('Activated', 'Activated'), ('Deactivated', 'Deactivated')]
    disable = models.CharField(max_length=100, null=True, blank=True, default="Activated", choices=disable_sel)
    deactivate_reason = models.CharField(max_length=100, null=True, blank=True)
    institute_code = models.CharField(max_length=100, null=True, )
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    cytogenetic = models.BooleanField(default=False)
    dna_sequencer = models.BooleanField(default=False)
    mi_seq = models.BooleanField(default=False)
    next_seq = models.BooleanField(default=False)
    real_time_pcr = models.BooleanField(default=False)
    high_throughput_rna_dna = models.BooleanField(default=False)
    quality_check = models.BooleanField(default=False)
    chromosomal_micro = models.BooleanField(default=False)
    newborn_screening = models.BooleanField(default=False)
    antenatal_screening = models.BooleanField(default=False)
    eonis_tm_system = models.BooleanField(default=False)
    capillary_electrophoresis = models.BooleanField(default=False)
    multimode_reader = models.BooleanField(default=False)
    liquid_chromatography = models.BooleanField(default=False)
    hplc = models.BooleanField(default=False)
    gcms = models.BooleanField(default=False)
    microfluidics_platform = models.BooleanField(default=False)
    any_other_facility = models.CharField(max_length=100, null=True, blank=True)
    # opd_attendance = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.institute_name)

class Opd_attendance(models.Model):
        user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
        date = models.CharField( null=True, max_length = 50)
        # name_of_rd = models.CharField(max_length=100, null=True, blank=True)
        name_of_rd = [('Fabry Disease', 'Fabry Disease'),('Thalassemia', 'Thalassemia'),
                      ('Glycogen Storage Disorder', 'Glycogen Storage Disorder'),
                      ('Bleeding Disorder', 'Bleeding Disorder'),
                      ('IEM', 'IEM'),
                      ('Pompe Disease', 'Pompe Disease'),
                      ('Sphingo Lipidosis', 'Sphingo Lipidosis'),
                      ('Skeletal Dysplasia', 'Skeletal Dysplasia'),
                      ('NMD', 'NMD'),
                      ('Mucopolysaccharidosis Group', 'Mucopolysaccharidosis Group'),
                      # ('Small molecule samples', 'Small molecule samples'),
                      ('PID', 'PID')
                      ]
        name_of_rdei = models.CharField(max_length=1000, null=True, choices=name_of_rd)
        no_of_cases = models.PositiveBigIntegerField( null=True)
        no_of_opd_cases = models.PositiveBigIntegerField( null=True)
        no_of_new_adminission = models.PositiveBigIntegerField( null=True)
        pre_opd_att = models.FloatField(blank=True, null=True)
        pre_new_admi = models.FloatField(blank=True, null=True)
        pre_total = models.FloatField(blank=True, null=True)

        def __str__(self):
            return str(self.pk)




