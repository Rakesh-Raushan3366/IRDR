from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfileNMDForm(ModelForm):
    class Meta:
        model = profile_nmd
        fields = '__all__'
        widgets = {
            'nmd_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'nmd_mother_father_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),
            'nmd_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'nmd_date_of_records': DateInput(attrs={'type': 'date', }),
            'nmd_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'nmd_date_of_birth': DateInput(attrs={'type': 'date', }),
            'nmd_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'nmd_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'nmd_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class SocioDemographicDetailsNMDForm(ModelForm):
    class Meta:
        model = demographic_nmd
        fields = '__all__'


class DYSTOPHINOPATHYDetailsNMDForm(ModelForm):
    class Meta:
        model = dsystophinopathy_nmd
        fields = '__all__'
        widgets = {

            'functional_status_WheelchairBound_age': DateInput(attrs={'type': 'date', }),
            'functional_status_BedBound_age': DateInput(attrs={'type': 'date', }),
            'current_past_treatment_Steroids_starting_age': DateInput(attrs={'type': 'date', }),
            'Tendon_lengthening_surgery_if_yes_age': DateInput(attrs={'type': 'date', }),
            'Surgicalcorrectionscoliosis_if_yes_age': DateInput(attrs={'type': 'date', }),
            'last_follow_up_if_yes_age': DateInput(attrs={'type': 'date', }),
            'outcome_age': DateInput(attrs={'type': 'date', }),

        }


class SpinalMuscularAtrophyDetailsNMDForm(ModelForm):
    class Meta:
        model = spinal_nmd
        fields = '__all__'
        widgets = {

            'currentMotor_WheelchairBound_if_yes_age': DateInput(attrs={'type': 'date', }),
            'finalOutcome_if_dead_age': DateInput(attrs={'type': 'date', }),

        }


class LimbGirdleMuscularDystrophyDetailsNMDForm(ModelForm):
    class Meta:
        model = limb_gridle_nmd
        fields = '__all__'
        widgets = {


            'RespiratoryAssistance_BiPAP_age': DateInput(attrs={'type': 'date', }),
            'RespiratoryAssistance_Ventilator_age': DateInput(attrs={'type': 'date', }),
            'Final_Outcome_last_followup_Date': DateInput(attrs={'type': 'date', }),


        }




class QAnmdForm(ModelForm):
    class Meta:
        model = profile_nmd
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'