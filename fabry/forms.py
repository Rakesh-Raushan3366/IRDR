from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfilefabridiseaseForm(ModelForm):
    class Meta:
        model = profile_fabry
        fields = '__all__'
        widgets = {
            'fb_father_mother_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'fb_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'fb_date_of_record': DateInput(attrs={'type': 'date', }),
            'fb_clinical_exam_date': DateInput(attrs={'type': 'date', }),
            'fb_date_of_birth': DateInput(attrs={'type': 'date', }),
            'fb_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'fb_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'fb_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'fb_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDetailsFormfb(ModelForm):
    class Meta:
        model = demographic_fabry
        fields = '__all__'
        widgets = {
            'gl_other_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'gl_other_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'fb_any_other': Textarea(attrs={'rows': '4', 'cols': '250', }),
            'gl_inv_biotinidase_if_abnormal': TextInput(attrs={'placeholder': 'Please specify'}),
            'gl_inv_tms_if_abnormal_value': TextInput(attrs={'placeholder': 'Please specify'}),
            'gl_echo_abnormal_volvular_spcify': TextInput(attrs={'placeholder': 'Please specify'}),
            'fb_enzyme_assy_report_details': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'gl_any_other_info': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'gl_any_surgery_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'gl_any_organ_transplantation_specify': TextInput(attrs={'placeholder': 'Please specify'}),
            'fb_improvement_after_medication_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),

            'fb_onset_age': DateInput(attrs={'type': 'date', }),
            'fb_present_age': DateInput(attrs={'type': 'date', }),
            'fb_diag_age': DateInput(attrs={'type': 'date', }),
            # 'fb_angiok_onset_age': DateInput(attrs={'type': 'date', }),
            'fb_echo_date': DateInput(attrs={'type': 'date', }),
            'fb_left_vent_diastolic_dia_date': DateInput(attrs={'type': 'date', }),
            'fb_co_date': DateInput(attrs={'type': 'date', }),
            'fb_ef_per_date': DateInput(attrs={'type': 'date', }),
            'fb_lvh_date': DateInput(attrs={'type': 'date', }),
            'fb_mr_tr_date': DateInput(attrs={'type': 'date', }),
            'fb_cardiomyopathy_date': DateInput(attrs={'type': 'date', }),
            'fb_ecg_date': DateInput(attrs={'type': 'date', }),
            'fb_microalbuminuri_date': DateInput(attrs={'type': 'date', }),
            'fb_albumin_creatinine_date': DateInput(attrs={'type': 'date', }),
            'fb_urea_date': DateInput(attrs={'type': 'date', }),
            'fb_creatinine_date': DateInput(attrs={'type': 'date', }),
            'fb_plasma_gl_3_date': DateInput(attrs={'type': 'date', }),
            'fb_urine_gl_3_date': DateInput(attrs={'type': 'date', }),
            'fb_ert_initial_date': DateInput(attrs={'type': 'date', }),
            # 'fb_ace_inhibitors_name': DateInput(attrs={'type': 'date', }),
            'fb_date': DateInput(attrs={'type': 'date', }),

        }






class QAfabryForm(ModelForm):
    class Meta:
        model = profile_fabry
        fields = ['qa_user','qa_register','quality_result','quality_reason']
        exclude = '__all__'