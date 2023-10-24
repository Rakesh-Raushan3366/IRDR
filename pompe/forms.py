from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *



class PompeRegistrationForm(ModelForm):
    class Meta:
        model = profile_pompe
        fields = '__all__'
        widgets = {
            'pmp_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'pmp_father_mother_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'pmp_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pmp_date_of_records': DateInput(attrs={'type': 'date', }),
            'pmp_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'pmp_date_of_birth': DateInput(attrs={'type': 'date', }),
            'pmp_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'pmp_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'pmp_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class PompeSocioDemographicDetailsForm(ModelForm):
    class Meta:
        model = demographic_pompe
        fields = '__all__'
        widgets = {
            'pd_if_yes_date_started': DateInput(attrs={'type': 'date', }),
            'pd_Cardiac_medications_date_started': DateInput(attrs={'type': 'date', }),
            'pd_ECHO_date': DateInput(attrs={'type': 'date', }),
            'pd_PFT_date': DateInput(attrs={'type': 'date', }),
            'pd_Biochemical_testing_date': DateInput(attrs={'type': 'date', }),
            'pd_Sample_date_done': DateInput(attrs={'type': 'date', }),
            'pd_Date_Initiation': DateInput(attrs={'type': 'date', }),
            'pd_Physiotherapy_date': DateInput(attrs={'type': 'date', }),
            'pd_filled_date': DateInput(attrs={'type': 'date', }),

        }



class QApompeForm(ModelForm):
    class Meta:
        model = profile_pompe
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
