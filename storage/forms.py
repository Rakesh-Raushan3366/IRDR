from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class StorageRegistrationForm(ModelForm):
    class Meta:
        model = profile_storage
        fields = '__all__'
        widgets = {
            'sd_Father_mother_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'sd_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'sd_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'sd_date_of_records': DateInput(attrs={'type': 'date', }),
            'sd_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'sd_date_of_birth': DateInput(attrs={'type': 'date', }),
            'sd_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'sd_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'sd_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class StorageSocioDemographicDetailsForm(ModelForm):
    class Meta:
        model = demographic_storage
        fields = '__all__'
        widgets = {
            'sd_Date_of_initiation': DateInput(attrs={'type': 'date', }),
            'sd_Bone_Marrow_Date': DateInput(attrs={'type': 'date', }),
            'sd_filled_date': DateInput(attrs={'type': 'date', }),
        }





class QAstorageForm(ModelForm):
    class Meta:
        model = profile_storage
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
