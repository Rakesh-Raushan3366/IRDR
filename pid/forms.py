from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from django.forms import FileInput
from .models import *


class ProfilePIDForm(ModelForm):
    class Meta:
        model = profile_pid
        fields = '__all__'

        widgets = {
            'pid_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'pid_father_mother_id_no': TextInput(
                attrs={'placeholder': 'Please enter parent id number'}),
            'pid_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_date_of_record': DateInput(attrs={'type': 'date', }),
            'pid_clinical_exam_date': DateInput(attrs={'type': 'date', }),
            'pid_date_of_birth': DateInput(attrs={'type': 'date', }),
            'pid_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'pid_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'pid_assent_upload': FileInput(attrs={'accept': '.pdf'}),
        }


class ClinicalPresentationPIDForm(ModelForm):
    class Meta:
        model = demopraphic_pid
        fields = '__all__'
        widgets = {

            'pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryCIDAssociated_Other_Specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryPredominantAntibody_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryDiseasesImmune_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryCongenitalDefects_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryDefectsIntrinsic_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryAutoinflammatory_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryMarrowFailure_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_BroadDiagnosisCategoryPhenocopies_other_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_CVID': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_Others_specify': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_CVID1': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_Others_specify1': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_CVID2': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'pid_malignancy_Others_specify2': TextInput(
                attrs={'placeholder': 'Please specify'}),

            # 'pid_date_onset_symptoms': DateInput(attrs={'type': 'date', }),
            'pid_onset_date': DateInput(attrs={'type': 'date', }),
            'pid_OPV_Date_Dose': DateInput(attrs={'type': 'date', }),
            'pid_Rubella_Date_Vaccination': DateInput(attrs={'type': 'date', }),
            'pid_Measles_Date_Vaccination': DateInput(attrs={'type': 'date', }),
            'pid_CBC_Date': DateInput(attrs={'type': 'date', }),
            'pid_CBC_Date1': DateInput(attrs={'type': 'date', }),
            'pid_CBC_Date2': DateInput(attrs={'type': 'date', }),
            'pid_CBC_Date3': DateInput(attrs={'type': 'date', }),
            'pid_Date_of_initiation_of_therapy_1': DateInput(attrs={'type': 'date', }),
            'pid_Date_of_termination_of_therapy_2': DateInput(attrs={'type': 'date', }),
            'pid_outcome_alive_no_date': DateInput(attrs={'type': 'date', }),

        }




class QApidForm(ModelForm):
    class Meta:
        model = profile_pid
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'