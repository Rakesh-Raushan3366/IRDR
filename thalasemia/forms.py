from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfilethalasemiaForm(ModelForm):
    class Meta:
        model = profile_thalassemia
        fields = '__all__'
        widgets = {
            'th_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter number'}),
            'th_date_of_birth': DateInput(attrs={'type': 'date', }),
            'th_date_record': DateInput(attrs={'type': 'date', }),
            'date_clinical_examination': DateInput(attrs={'type': 'date', }),
            'th_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'th_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_religion_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_caste_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_patient_adhaar_no_specify': TextInput(
                attrs={'placeholder': 'Please enter 14 degit aadhar no.'}),
            'th_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'th_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDetailsthForm(ModelForm):
    class Meta:
        model = demographic_thalassemia
        fields = '__all__'
        widgets = {


            'th_red_cell_morphology_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_mol_beta_thal_other_spec': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_neurological_abnor_option_other': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_renal_involvement_opts_other': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_mol_alpha_thal_opt_other': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'th_curr_invest_date': DateInput(attrs={'type': 'date', }),
            'th_transfusion_age': TextInput(
                attrs={'placeholder': 'Please specify age'}),
            'th_other_medication': Textarea(attrs={'rows': '2', 'cols': '250', }),
            'th_filled_date': DateInput(attrs={'type': 'date', }),
            'th_f_diag_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),

            'th_deferasirox_dose_other_specify': TextInput(
                attrs={'placeholder': 'Please specify '}),
            'th_comp_iron_overload_detail': TextInput(
                attrs={'placeholder': 'Please specify'}),

            'th_comp_iron_overload_beta_thalassemia_detail': TextInput(
                attrs={'placeholder': 'Please specify'}),
        }






class QATHForm(ModelForm):
    class Meta:
        model = profile_thalassemia
        fields = ['qa_user','qa_register','quality_result','quality_reason']
        exclude = '__all__'
