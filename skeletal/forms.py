from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class skeletal_RegistrationForm(ModelForm):
    class Meta:
        model = profile_skeletal
        fields = '__all__'
        widgets = {
            'sk_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'sk_father_mother_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'sk_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'sk_date_of_records': DateInput(attrs={'type': 'date', }),
            'sk_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'sk_date_of_birth': DateInput(attrs={'type': 'date', }),
            'sk_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'sk_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'sk_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class skeletal_SocioDemographicDetailsForm(ModelForm):
    class Meta:
        model = demographic_skeletal
        fields = '__all__'

        widgets = {
            'sk_Invetigation_Date': DateInput(attrs={'type': 'date', }),
            'sk_x_ray_findings_Date': DateInput(attrs={'type': 'date', }),
            'sk_CT_Scan_MRI_Brain': DateInput(attrs={'type': 'date', }),
            'sk_any_other_investigation_date': DateInput(attrs={'type': 'date', }),
            'sk_date_of_inititation': DateInput(attrs={'type': 'date', }),
            'sk_filled_date': DateInput(attrs={'type': 'date', }),
            'sk_Any_other': Textarea(attrs={'rows': '3', 'cols': '250', }),
        }




class QAskeletalForm(ModelForm):
    class Meta:
        model = profile_skeletal
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'