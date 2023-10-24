from .models import *
from django.forms import FileInput

class ProfilebleedingdisorderForm(ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = profile_bleeding
        fields = '__all__'
        widgets = {
            'bd_patient_id_no': TextInput(
                attrs={'placeholder': 'Please enter number'}),
            'bd_mother_father_id_no': TextInput(
                attrs={'placeholder': 'Please enter id number'}),

            'bd_permanent_addr': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'bd_date_of_record': DateInput(attrs={'type': 'date'}),
            'bd_date_of_clinical_exam': DateInput(attrs={'type': 'date'}),
            'bd_referred_by_desc': TextInput(
                attrs={'placeholder': 'Please specify'}),
            'bd_date_of_birth': DateInput(attrs={'type': 'date', }),
            'bd_consent_upload':FileInput(attrs={'accept': '.pdf'}),
            'bd_assent_upload':FileInput(attrs={'accept': '.pdf'}),
            }


class SocioDemographicDetailsFormbd(ModelForm):
    class Meta:
        model = demographic_bleeding
        fields = '__all__'
        widgets = {
            'bd_carr_any_other_details': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'bd_ante_other_info_1': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'bd_ante_other_info_2': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'bd_carr_female_1_dob': DateInput(attrs={'type': 'date'}),
            'bd_carr_female_1_dos': DateInput(attrs={'type': 'date'}),
            'bd_carr_female_2_dob': DateInput(attrs={'type': 'date'}),
            'bd_carr_female_2_dos': DateInput(attrs={'type': 'date'}),
            'bd_ante_female_1_dob': DateInput(attrs={'type': 'date'}),
            'bd_ante_female_1_dos': DateInput(attrs={'type': 'date'}),
            'bd_ante_female_2_dob': DateInput(attrs={'type': 'date'}),
            'bd_ante_female_2_dos': DateInput(attrs={'type': 'date'}),
            'bd_other_info': Textarea(attrs={'rows': '3', 'cols': '250', }),
            'bd_start_date': DateInput(attrs={'type': 'date'}),
            'bd_end_date': DateInput(attrs={'type': 'date'}),
            'bd_surgery_date1': DateInput(attrs={'type': 'date'}),
            'bd_surgery_date2': DateInput(attrs={'type': 'date'}),
            'bd_surgery_date3': DateInput(attrs={'type': 'date'}),

            }


class QAbleedingForm(ModelForm):
    class Meta:
        model = profile_bleeding
        fields = ['qa_user', 'qa_register', 'quality_result', 'quality_reason']
        exclude = '__all__'
