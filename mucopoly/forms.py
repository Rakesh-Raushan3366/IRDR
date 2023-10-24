from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfileMGForm(ModelForm):
    class Meta:
        model = profile_mucopolysaccharidosis
        fields = '__all__'
        widgets = {
            'muco_mother_father_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'muco_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'muco_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'muco_date_of_records': DateInput(attrs={'type': 'date', }),
            'muco_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'muco_date_of_birth': DateInput(attrs={'type': 'date', }),
            'muco_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'muco_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'muco_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDataSheetMGForm(ModelForm):
    class Meta:
        model = demographic_mucopolysaccharidosis
        fields = '__all__'
        widgets = {
            'Date_of_initiation': DateInput(attrs={'type': 'date', }),
            'date': DateInput(attrs={'type': 'date', }),
            'mg_date_created': DateInput(attrs={'type': 'date', }),
            'mg_filled_date' : DateInput(attrs={'type': 'date', }),
        }






class QAMGForm(ModelForm):
    class Meta:
        model = profile_mucopolysaccharidosis
        fields = ['qa_user','qa_register','quality_result','quality_reason']
        exclude = '__all__'
        widgets = {
            'muco_mother_father_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'muco_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'muco_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'muco_date_of_records': DateInput(attrs={'type': 'date', }),
            'muco_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'muco_date_of_birth': DateInput(attrs={'type': 'date', }),
            'muco_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
        }