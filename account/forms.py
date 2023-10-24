from django.forms import RadioSelect, DateTimeInput
from .models import *
from django.forms import RadioSelect, DateTimeInput, NumberInput
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class UpdateUserForm(UserUpdationForm):
#     class Meta:
#         model = User
#         fields = ['facility']

class ChangepasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['password1', 'password2']




class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = '__all__'
        # exclude = '__all__'

class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['cytogenetic','dna_sequencer','mi_seq','next_seq','real_time_pcr',
                  'high_throughput_rna_dna','quality_check','chromosomal_micro','newborn_screening',
                  'antenatal_screening','eonis_tm_system','capillary_electrophoresis','multimode_reader',
                  'liquid_chromatography','hplc','gcms','microfluidics_platform','any_other_facility']

          # exclude = '__all__'

class Opd_attendanceForm(ModelForm):
    class Meta:
        model = Opd_attendance
        fields = '__all__'
        widgets = {
           'date': DateInput(attrs={'type': 'week'}),
        }

#