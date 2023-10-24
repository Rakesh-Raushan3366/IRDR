from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin import (widgets, site as admin_site1)
from django.contrib.admin.widgets import FilteredSelectMultiple, AdminDateWidget, RelatedFieldWidgetWrapper
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import SelectMultiple, TextInput, Select, DateInput, CheckboxSelectMultiple, CheckboxInput
from django.forms import modelformset_factory
from django.forms import Textarea
from multiselectfield import MultiSelectField
from django.db import models

from account.models import *

# Create your models here.


class profile_fabry(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    fb_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    fb_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    fb_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    fb_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    fb_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    fb_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_date_of_record = models.DateField(blank=True, null=True)
    fb_clinical_exam_date = models.DateField(blank=True, null=True)
    fb_date_of_birth = models.DateField( null=True)
    fb_patient_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    fb_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id')]
    fb_paitent_id = models.CharField(max_length=100,  null=True, choices=fb_status_sel)
    fb_paitent_id_list = models.CharField(max_length=100,  blank=True,null=True, choices=id_sel)
    fb_patient_id_no = models.CharField(max_length=100,unique=True, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # fb_patient_adhaar_no = models.IntegerField(blank=True, null=True)
    fb_father_mother_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    fb_father_mother_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    fb_mother_adhaar_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    fb_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    fb_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    fb_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE, verbose_name=' district')
    fb_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    fb_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    fb_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    fb_email = models.EmailField(max_length=300, blank=True, null=True)
    fb_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    fb_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    fb_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    fb_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    fb_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    fb_consent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    fb_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, validators=[FileExtensionValidator(['pdf'])])
    fb_assent_given = models.CharField(max_length=10,  null=True,  choices=fb_status_sel)
    fb_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    fb_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    fb_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_fabry', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_fabry', on_delete=models.CASCADE)

    quality_result = models.CharField(max_length=10, blank=True, null=True, choices=quality_score)
    quality_reason = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    uniqueId = models.CharField(null=True, blank=True, max_length=500)
    yes_no_na = [('Yes', 'Yes'), ('No', 'No'), ('Na', 'Na')]
    complete = models.CharField(max_length=10,  blank=True, null=True, default='No', choices=yes_no_na)
    update_profile =models.CharField(max_length=10, blank=True, null=True, choices=yes_no_na)
    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4())
            count1 = State.objects.count()
            count2 = 0
            count2 += count1
            super(profile_fabry, self).save(*args, **kwargs)
            self.fb_icmr_unique_no = str('Fabry/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_fabry, self).save(*args, **kwargs)


class demographic_fabry(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_fabry, null=True, blank=True, related_name='patient_fabry',
                                on_delete=models.CASCADE)
    fb_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    fb_status_sel123 = [('1', 'Yes'), ('0', 'No')]
    fb_patient_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                          ('Secondary '
                           'level',
                           'Secondary '
                           'level'),
                          ('College and above', 'College and above')]
    fb_patient_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                           ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    fb_father_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    fb_father_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    fb_mother_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    fb_mother_occu_sel = [('Home maker', 'Home maker)'),
                          ('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    fb_monthly_income_sel = [('> 126,360', '> 126,360)'),
                             ('63,182 – 126,356)', '63,182 – 126,356)'),
                             ('47,266 – 63,178', '47,266 – 63,178'),
                             ('31,591 - 47,262', '31,591 - 47,262'),
                             ('18,953 - 31,589', '18,953 - 31,589'),
                             ('6,327 - 18,949', '6,327 - 18,949'),
                             ('< 6,323', '< 6,323')]

    fb_patient_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=fb_patient_edu_sel)
    fb_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=fb_patient_occu_sel)
    fb_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=fb_father_edu_sel)
    fb_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=fb_father_occu_sel)
    fb_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=fb_mother_edu_sel)
    fb_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=fb_mother_occu_sel)
    fb_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=fb_monthly_income_sel)
    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_given_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not known', 'Not known')]

    antenatal_ultra_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    pres_abs_sel = [('Present', 'Present'), ('Absent', 'Absent')]
    delivery_sel = [('Caesarean', 'Caesarean'), ('Vaginal', 'Vaginal')]
    resc_req_sel = [('Ventilation', 'Ventilation'), ('NICU Stay days', 'NICU Stay days')]
    time_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    fb_anth_wght_pat = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_wght_per = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_wght_sd = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_height_pat = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_height_per = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_height_sd = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_head_cir_pat = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_head_cir_perc = models.CharField(max_length=50,blank=True, null=True)
    fb_anth_head_cir_sd = models.CharField(max_length=50,blank=True, null=True)

    fb_presenting_complaints_years = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_months = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_day = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=fb_status_sel123)
    fb_presenting_complaints_age_presentation_years = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_presentation_months = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_presentation_day = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_presentation_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=fb_status_sel123)
    fb_presenting_complaints_age_diagnosis_years = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_diagnosis_months = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_diagnosis_day = models.IntegerField(blank=True, null=True)
    fb_presenting_complaints_age_diagnosis_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=fb_status_sel123)

    fb_onset_age = models.DateField(blank=True, null=True)
    #fb_present_age = models.DateField(blank=True, null=True)
    #fb_diag_age = models.DateField(blank=True, null=True)
    fb_pedigree_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    fb_fam_hist_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_fam_hist_descr = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_cons_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_cons_degree_specify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_fever = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_gi_symtoms = models.CharField(max_length=10, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_abdominal_pain = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_diarrhea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_constipation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_nausea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_vomiting = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_irritable_bowel = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_acroparesthesia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_neuronopathic_pain = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    hand_feet_sel = [('Hand', 'Hand'), ('Feet', 'Feet'), ('Both', 'Both')]
    fb_hand = models.BooleanField(default=False)
    fb_feet = models.BooleanField(default=False)
    fb_both = models.BooleanField(default=False)
    treatment_sel = [('Self', 'Self'), ('Insurance', 'Insurance'), ('Compassionate Access', 'Compassionate Access'),
                    ('Reimbursement', 'Reimbursement'), ('Under Rare Disease Policy', 'Under Rare Disease Policy')]
    fb_treatment = models.CharField(max_length=200, blank=True, null=True, choices=treatment_sel)
    fb_medication_Morphine = models.BooleanField(default=False)
    fb_medication_CBZ = models.BooleanField(default=False)
    fb_medication_Phenytoin = models.BooleanField(default=False)
    fb_improvement_after_ert = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_given_sel)
    fb_improvement_after_medication = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_given_sel)
    fb_improvement_after_medication_specify = models.CharField(max_length=50, blank=True, null=True,
                                                               validators=[MaxLengthValidator(50)])

    fb_medication_effect = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    # fb_medication_pain_effect_desc = models.CharField(max_length=50, blank=True, null=True,
    #                                                validators=[MaxLengthValidator(50)])
    fb_angiokeratoma = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_angiok_onset_age = models.CharField(max_length=10, blank=True, null=True,)
    fb_hypohidrosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_inter_physical_act = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_hydro_impro_after_ert = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_given_sel)
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    ecg_sel = [('PR intervalShort/Prolonged', 'PR intervalShort/Prolonged'),
               ('QRS durationShort/Prolonged', 'QRS durationShort/Prolonged')]
    neuropsy_symp_sel = [('Depression', 'Depression'), ('Neuropsychological deficits', 'Neuropsychological deficits')]
    trans_isch_sel = [('Ischemic', 'Ischemic'), ('Hemorrhagic', 'Hemorrhagic')]
    sensory_type_sel = [('Sensorineural', 'Sensorineural'), ('Conductive', 'Conductive')]
    norm_abnorm_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    fb_cardiac_symtoms = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_myocardial_infarction = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_unstable_angina = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_hypertension = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_echo = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_echo_date = models.DateField(blank=True, null=True)
    fb_left_vent_diastolic_dia = models.FloatField(blank=True, null=True)
    fb_left_vent_diastolic_dia_date = models.DateField(blank=True, null=True)
    fb_pwt_septum_lvm = models.FloatField(blank=True, null=True)
    fb_co = models.FloatField(blank=True, null=True)
    fb_co_date = models.DateField(blank=True, null=True)
    fb_ef_per = models.FloatField(blank=True, null=True)
    fb_ef_per_date = models.DateField(blank=True, null=True)
    fb_lvh = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_lvh_date = models.DateField(blank=True, null=True)
    fb_mr_tr = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_mr_tr_date = models.DateField(blank=True, null=True)
    fb_lvmi = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_cardiomyopathy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_cardiomyopathy_date = models.DateField(blank=True, null=True)
    fb_cardiomyopathy_specify = models.CharField(max_length=50, blank=True, null=True,
                                                 validators=[MaxLengthValidator(50)])

    fb_ecg = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    fb_ecg_date = models.DateField(blank=True, null=True)
    # fb_ecg_abnormal = models.CharField(max_length=50, blank=True, null=True, choices=ecg_sel)
    ecg_sel = [('Short', 'Short'),
               ('Prolonged', 'Prolonged')]
    fb_ecg_abnormal_pr_select = models.CharField(max_length=50, blank=True, null=True, choices=ecg_sel)
    # fb_ecg_specify = models.CharField(max_length=50, blank=True, null=True,
    #                                              validators=[MaxLengthValidator(50)])
    fb_any_rhythm_abnormality = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_any_rhythm_abnormality_specify = models.CharField(max_length=50, blank=True, null=True,
                                                         validators=[MaxLengthValidator(50)])
    fb_neropsychiatric_symp = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_neuropsychiatric_types = models.CharField(max_length=50, blank=True, null=True, choices=neuropsy_symp_sel)
    fb_depression_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    # fb_neuro_deficits_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_stroke = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_stroke_age = models.FloatField(blank=True, null=True)
    fb_rec_stroke = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_trans_isch_attack = models.CharField(max_length=50, blank=True, null=True, choices=trans_isch_sel)
    fb_visual_prob = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_cornea_vertic = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_corneal_opacity = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_hearing_loss = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_sensory_type = models.CharField(max_length=50, blank=True, null=True, choices=sensory_type_sel)
    fb_proteinuria = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_proteinuria_age_onset = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    fb_microalbuminuri = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_microalbuminuri_date = models.DateField(blank=True, null=True)
    fb_microalbuminuri_value = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    fb_albumin_creatinine = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_albumin_creatinine_date = models.DateField(blank=True, null=True)
    fb_albumin_creatinine_val = models.FloatField(blank=True, null=True)
    fb_renal_biops = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_renal_biops_status = models.CharField(max_length=10, blank=True, null=True, choices=norm_abnorm_sel)
    fb_renal_biops_abnorm_specify = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    fb_renal_transplant = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_renal_transplant_specify = models.CharField(max_length=50, blank=True, null=True,
                                                   validators=[MaxLengthValidator(50)])
    fb_dialysis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_gfr = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_urea_base_line_value = models.FloatField(blank=True, null=True)
    fb_urea_date = models.DateField(blank=True, null=True)
    fb_creatinine_base_value = models.FloatField(blank=True, null=True)
    fb_creatinine_date = models.DateField(blank=True, null=True)
    yes_no_not_done_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not done', 'Not done')]
    hepatomegaly_sel = [('Size (cm) BCM', 'Size (cm) BCM'), ('Span', 'Span'),
                        ('Left lobe enlargement', 'Left lobe enlargement'),
                        ('Consistency', 'Consistency'), ('Margins', 'Margins')]
    done_not_done_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    normal_delayed_sel = [('Normal', 'Normal'), ('Delayed', 'Delayed')]
    curr_ert_status_sel = [('Ongoing', 'Ongoing'), ('Stopped', 'Stopped')]
    fb_plasma_gl_3_date = models.DateField(blank=True, null=True)
    fb_plasma_gl_3_value = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_plasma_gl_3_lab_name = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    fb_urine_gl_3_date = models.DateField(blank=True, null=True)
    fb_urine_gl_3_lab_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_urine_gl_3_lab_value = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    fb_mri_brain = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    fb_mri_brain_abnormal_spcify = models.CharField(max_length=50, blank=True, null=True,
                                                    validators=[MaxLengthValidator(50)])
    fb_enzyme_assy_ref_range = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    fb_enzyme_assy_lab_name = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    fb_enzyme_assy_upload_report = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    fb_enzyme_assy_sel = [('Homozygous', 'Homozygous '),
                    ('Heterozygous', 'Heterozygous'),
                          ('Hemizygous', 'Hemizygous')]
    fb_enzyme_assy1 = models.CharField(max_length=50, blank=True, null=True, choices=fb_enzyme_assy_sel)
    fb_gene_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_transcript_id = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_cDNA_change1 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_protein_change1 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    variant_sel = normal_delayed_sel = [('Novel', 'Novel'), ('Report', 'Report')]
    fb_variant1 = models.CharField(max_length=50, blank=True, null=True, choices=variant_sel)
    fb_variant_class_sel = [('Pathogenic ', 'Pathogenic '),
                            ('Likely Pathogenic', 'Likely Pathogenic'),
                            ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    fb_variant_class1 = models.CharField(max_length=50, blank=True, null=True, choices=fb_variant_class_sel)
    fb_enzyme_assy_sel = [('Homozygous', 'Homozygous '),
                          ('Heterozygous', 'Heterozygous'),
                          ('Hemizygous', 'Hemizygous')]
    fb_enzyme_assy2 = models.CharField(max_length=50, blank=True, null=True, choices=fb_enzyme_assy_sel)
    fb_cDNA_change2 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_protein_change2 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    variant_sel = normal_delayed_sel = [('Novel', 'Novel'), ('Report', 'Report')]
    fb_variant2 = models.CharField(max_length=50, blank=True, null=True, choices=variant_sel)
    fb_variant_class_sel = [('Pathogenic ', 'Pathogenic '),
                            ('Likely Pathogenic', 'Likely Pathogenic'),
                            ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    fb_variant_class2 = models.CharField(max_length=50, blank=True, null=True, choices=fb_variant_class_sel)
    fb_mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_sel)
    fb_father = models.CharField(max_length=100, blank=True, null=True)
    fb_mother = models.CharField(max_length=100, blank=True, null=True)

    fb_segregation_parents = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_not_done_sel)
    fb_enzyme_assy_report_details = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    fb_enzyme_assy_cont = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    fb_mutaion_rep_lab_name = models.CharField(max_length=50, blank=True, null=True,
                                               choices=yes_no_sel)
    fb_mutaion_rep_datails = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_mutaion_rep_upload_report = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    fb_ert_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_ert_initial_date = models.DateField(blank=True, null=True)
    fb_ert_start_age = models.FloatField(blank=True, null=True)
    fb_ert_dosage = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_ert_duration = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_adverse_events = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_adverse_events_specify = models.CharField(max_length=50, blank=True, null=True,
                                                 validators=[MaxLengthValidator(50)])
    fb_curr_ert_status = models.CharField(max_length=10, blank=True, null=True, choices=curr_ert_status_sel)
    fb_any_interuption = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_reseason_interrupt = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_dur_interrupt = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_fabri_disease_pain_score = models.FloatField(blank=True, null=True)
    fb_drugs_recieved = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_pain_killers = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_pain_medication_name = models.CharField(max_length=10, blank=True, null=True, )
    fb_pain_killers_spcify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_ace_inhibitors = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fb_ace_inhibitors_name =  models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_ace_inhibitors_dose = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    # fb_ace_inhibitors_specify = models.CharField(max_length=50, blank=True, null=True, validators=[
    # MaxLengthValidator(50)])
    fb_any_other = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_filled_by_deo_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_clinicial_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    fb_date = models.DateField(blank=True, null=True)
    fb_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    fb_Finaloutcomes_sel = [('Death', 'Death'),('Alive', 'Alive'),('Followup Required', 'Followup Required'),
                           ('Unknown', 'Unknown')]
    fb_Finaloutcomes = models.CharField(max_length=1000, blank=True, null=True, choices=fb_Finaloutcomes_sel)

    def __str__(self):
        return str(self.pk)