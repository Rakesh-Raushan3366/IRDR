from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *



class ProfileglycogenForm(ModelForm):
    class Meta:
        model = profile_glycogen
        fields = '__all__'
        widgets = {
            'gl_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter number'}),
            'gl_mother_father_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'gl_date_of_record': DateInput(attrs={'type': 'date', }),
            'gl_clinical_exam_date': DateInput(attrs={'type': 'date', }),
            'gl_date_of_birth': DateInput(attrs={'type': 'date', }),
            'gl_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'gl_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'gl_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'gl_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDetailsFormgl(ModelForm):
    class Meta:
        model = demographic_glycogen
        fields = '__all__'
        widgets = {
            'gl_onset_age': DateInput(attrs={'type': 'date', }),
            'gl_present_age': DateInput(attrs={'type': 'date', }),
            'gl_diag_age': DateInput(attrs={'type': 'date', }),
            'gl_date': DateInput(attrs={'type': 'date', }),
            'gl_any_other_info': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'gl_inv_biotinidase_if_abnormal': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'gl_inv_tms_if_abnormal_value': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'gl_any_surgery_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'gl_any_organ_transplantation_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'gl_echo_abnormal_volvular_spcify': TextInput(
                attrs={'placeholder': 'Please specify'}),

        }





class QAglycogenForm(ModelForm):
    class Meta:
        model = profile_glycogen
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
