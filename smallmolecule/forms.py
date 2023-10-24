from django.forms import RadioSelect
from django.forms import FileInput
from .models import *


class ProfileSMForm(ModelForm):
    class Meta:
        model = profile_smallmolecule
        fields = '__all__'
        widgets = {
            'small_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter patient id number'}),
            'small_father_mother_no': TextInput(
                attrs={'placeholder': 'Please enter  id number'}),
            'small_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'small_date_of_records': DateInput(attrs={'type': 'date', }),
            'small_date_of_clinical_exam': DateInput(attrs={'type': 'date', }),
            'small_date_of_birth': DateInput(attrs={'type': 'date', }),
            'small_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'small_consent_upload': FileInput(attrs={'accept': '.pdf'}),
            'small_assent_upload': FileInput(attrs={'accept': '.pdf'}),
            }


class FirstSymptomDataSheetSMForm(ModelForm):
    class Meta:
        model = demographic_smallmolecule
        fields = '__all__'
        widgets = {
            'developmental_delay': RadioSelect(),
            'vomiting': RadioSelect(),
            'loose_stools': RadioSelect(),
            'pneumonia': RadioSelect(),
            'fever': RadioSelect(),
            'lethargy': RadioSelect(),
            'seizures': RadioSelect(),
            'abdominal_distention': RadioSelect(),
            'history_admission': RadioSelect(),
            'any_surgery': RadioSelect(),
            'aversion_sweet_protein': RadioSelect(),
            'encephalopathy': RadioSelect(),
            'deafness': RadioSelect(),
            'extra_pyramidal_symp': RadioSelect(),
            'hypotonia': RadioSelect(),
            'hypertonia': RadioSelect(),
            'facial_dysmorphism': RadioSelect(),
            'congential_heart_disease': RadioSelect(),
            'cardiomyopathy': RadioSelect(),
            'hepatomegaly': RadioSelect(),
            'splenomegaly': RadioSelect(),
            'pigmentary': RadioSelect(),
            'deranged_LFT': RadioSelect(),
            'deranged_RFT': RadioSelect(),
            'hypoglycemia': RadioSelect(),
            'metabolic_acidosis': RadioSelect(),
            'metabolic_alkalosis': RadioSelect(),
            'hyper_ammonia': RadioSelect(),
            'high_lactate': RadioSelect(),
            'urine_ketones': RadioSelect(),
            'cherry_red_spot': RadioSelect(),
            'retinitis_pigmentosa': RadioSelect(),
            'optic_atrophy': RadioSelect(),
            'mechanical_ventilation': RadioSelect(),
            'dialysis': RadioSelect(),

            'tms =models': RadioSelect(),
            'regression': RadioSelect(),
            'distonia_abnormal_movement': RadioSelect(),
            'high_cpk': RadioSelect(),
            'dna_storage': RadioSelect(),
            'generic_analysis': RadioSelect(),
            'final_dagnosis': RadioSelect(),
            'tms': RadioSelect(),
            'other_info': RadioSelect(),

            'CT_brain_date': DateInput(attrs={'type': 'date', }),
            'mri_brain_date': DateInput(attrs={'type': 'date', }),
            'mrs_brain_date': DateInput(attrs={'type': 'date', }),
            'other_info_date': DateInput(attrs={'type': 'date', }),
            'tms_date': DateInput(attrs={'type': 'date', }),
            'ms_date': DateInput(attrs={'type': 'date', }),
            'gcms_date': DateInput(attrs={'type': 'date', }),
            'enzyme_assay_date': DateInput(attrs={'type': 'date', }),
            'quantitative_plasma_date': DateInput(attrs={'type': 'date', }),
            'quantitative_csf_date': DateInput(attrs={'type': 'date', }),
            'muscle_biopsy_date': DateInput(attrs={'type': 'date', }),
            'ncv_date': DateInput(attrs={'type': 'date', }),
            'ief_cdg_date': DateInput(attrs={'type': 'date', }),
            'glycine_date': DateInput(attrs={'type': 'date', }),
            'molecular_studies_date': DateInput(attrs={'type': 'date', }),
            'sm_date_created': DateInput(attrs={'type': 'date', }),

            'molecular_studies': RadioSelect(),

            }


class QAsmallForm(ModelForm):
    class Meta:
        model = profile_smallmolecule
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
