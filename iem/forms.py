from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfilemetabolismForm(ModelForm):
    class Meta:
        model = profile_metabolism
        fields = '__all__'
        widgets = {
            'mt_date_of_records': DateInput(attrs={'type': 'date', }),
            'mt_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'mt_date_of_birth': DateInput(attrs={'type': 'date', }),
            'mt_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'mt_religion_other_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'mt_caste_other_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'mt_referred_by_desc': TextInput(attrs={'placeholder': 'Please specify'}),
            'mt_patient_id_no': TextInput(attrs={'placeholder': 'Please enter id number'}),
            'mt_mother_father_id_no': TextInput(attrs={'placeholder': 'Please enter id number'}),
            'mt_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'mt_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDetailsmetaForm(ModelForm):
    class Meta:
        model = demographic_matabolism
        fields = '__all__'
        widgets = {
            'mt_anthropometry_date': DateInput(attrs={'type': 'date', }),
            'mt_Any_other_findings': Textarea(attrs={'rows': '2', 'cols': '250', }),
            'mt_Any_other_investigations': Textarea(attrs={'rows': '2', 'cols': '250', }),
            'mt_enzyme_analusis_sample_dbs_blood_date': DateInput(attrs={'type': 'date', }),
            'mt_csf_other': TextInput(attrs={'placeholder': 'Please specify'}),
            'mt_any_other_specify': Textarea(attrs={'rows': '2', 'cols': '250', }),
            'mt_any_other_special_drug_specify': Textarea(attrs={'rows': '2', 'cols': '250', }),
            'mt_death_cause': TextInput(attrs={'placeholder': 'Please enter NA if not applicable'}),
            'mt_date': DateInput(attrs={'type': 'date', }),
            'mt_date_filled': DateInput(attrs={'type': 'date', }),
        }




class QAmetabolismForm(ModelForm):
    class Meta:
        model = profile_metabolism
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
