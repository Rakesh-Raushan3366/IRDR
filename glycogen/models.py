from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.
from django.db import models

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



class profile_glycogen(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)

    gl_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    gl_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    gl_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    gl_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    gl_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    gl_final_dignosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_date_of_record = models.DateField(null=True, blank=True)
    gl_clinical_exam_date = models.DateField(null=True, blank=True)
    gl_date_of_birth = models.DateField(null=True,)
    gl_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    gl_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    gl_paitent_id = models.CharField(max_length=100,  null=True, choices=gl_status_sel)
    gl_paitent_id_list = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    gl_patient_id_no = models.CharField(max_length=100,unique=True,blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # gl_patient_adhaar_no = models.IntegerField(blank=True, null=True)
    gl_mother_father_id = models.CharField(max_length=100,  blank=True,null=True, choices=id_sel)
    gl_mother_father_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    gl_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    gl_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    gl_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE, verbose_name=' district')
    # gl_state = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # gl_district = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_mother_mobile_no = models.PositiveBigIntegerField( null=True)
    gl_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    gl_land_line_no = models.IntegerField(blank=True, null=True)
    gl_email = models.EmailField(max_length=300,blank=True, null=True)
    gl_religion = models.CharField(max_length=100, blank=True, null=True, choices=gl_religion_sel)
    gl_caste = models.CharField(max_length=100, blank=True, null=True, choices=gl_caste_sel)
    gl_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=gl_status_sel)
    gl_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=gl_referred_by)
    gl_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_gender = models.CharField(max_length=100, blank=True, null=True, choices=gl_gender_sel)
    gl_consent_given = models.CharField(max_length=10,  null=True, choices=gl_status_sel)
    gl_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, validators=[FileExtensionValidator(['pdf'])])
    gl_assent_given = models.CharField(max_length=10,  null=True,  choices=gl_status_sel)
    gl_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    gl_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gl_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_glycogen', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_glycogen', on_delete=models.CASCADE)

    quality_result = models.CharField(max_length=10, blank=True, null=True, choices=quality_score)
    quality_reason = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    uniqueId = models.CharField(null=True, blank=True, max_length=500)
    yes_no_na = [('Yes', 'Yes'), ('No', 'No'), ('Na', 'Na')]
    complete = models.CharField(max_length=10, blank=True, null=True,default='No', choices=yes_no_na)
    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4())
            count1 = State.objects.count()
            count2 = 0
            count2 += count1
            super(profile_glycogen, self).save(*args, **kwargs)
            self.gl_icmr_unique_no = str('Glycogen/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_glycogen, self).save(*args, **kwargs)


class demographic_glycogen(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_glycogen, null=True, blank=True, related_name='patient_glycogen',
                                on_delete=models.CASCADE)
    gl_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    gl_status_sel123 = [('1', 'Yes'), ('0', 'No')]
    gl_patient_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                          ('Secondary '
                           'level',
                           'Secondary '
                           'level'),
                          ('College and above', 'College and above')]
    gl_patient_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                           ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    gl_father_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    gl_father_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    gl_mother_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    gl_mother_occu_sel = [('Home maker', 'Home maker)'),
                          ('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    gl_monthly_income_sel = [('> 126,360', '> 126,360)'),
                             ('63,182 – 126,356)', '63,182 – 126,356)'),
                             ('47,266 – 63,178', '47,266 – 63,178'),
                             ('31,591 - 47,262', '31,591 - 47,262'),
                             ('18,953 - 31,589', '18,953 - 31,589'),
                             ('6,327 - 18,949', '6,327 - 18,949'),
                             ('< 6,323', '< 6,323')]

    gl_patient_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=gl_patient_edu_sel)
    gl_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=gl_patient_occu_sel)
    gl_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=gl_father_edu_sel)
    gl_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=gl_father_occu_sel)
    gl_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=gl_mother_edu_sel)
    gl_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=gl_mother_occu_sel)
    gl_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=gl_monthly_income_sel)
    antenatal_ultra_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    pres_abs_sel = [('Present', 'Present'), ('Absent', 'Absent')]
    delivery_sel = [('Caesarean', 'Caesarean'), ('Vaginal', 'Vaginal')]
    resc_req_sel = [('Ventilation', 'Ventilation'), ('NICU Stay days', 'NICU Stay days')]
    time_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    gl_presenting_complaints_specify = models.CharField(max_length=200, blank=True, null=True,)
    gl_anth_wght_pat = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_wght_per = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_wght_sd = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_height_pat = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_height_per = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_height_sd = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_head_cir_pat = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_head_cir_perc = models.CharField(max_length=50, blank=True, null=True,)
    gl_anth_head_cir_sd = models.CharField(max_length=50, blank=True, null=True,)
    gl_presenting_complaints_years = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_months = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_day = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=gl_status_sel123)
    gl_presenting_complaints_age_presentation_years = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_presentation_months = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_presentation_day = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_presentation_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=gl_status_sel123)
    gl_presenting_complaints_age_diagnosis_years = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_diagnosis_months = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_diagnosis_day = models.IntegerField(blank=True, null=True)
    gl_presenting_complaints_age_diagnosis_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=gl_status_sel123)

    gl_onset_age = models.DateField(blank=True, null=True)
    gl_present_age = models.DateField(blank=True, null=True)
    gl_diag_age = models.DateField(blank=True, null=True)
    gl_pedigree_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    gl_fam_hist_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_fam_hist_descr = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_cons_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_cons_degree_specify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_anti_natal_altra = models.CharField(max_length=10, blank=True, null=True, choices=antenatal_ultra_sel)
    antenatal_ultra_sell = [('Polyhydramnios', 'Polyhydramnios'), ('Hydrops', 'Hydrops'), ('Other', 'Other')]
    antenatal_ultrasound_if_abnormal = models.CharField(max_length=100, blank=True, null=True,
                                                        choices=antenatal_ultra_sell)
    gl_antenatal_ultrasound_status = models.CharField(max_length=10, blank=True, null=True, choices=pres_abs_sel)
    gl_other_specify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_delivery_type = models.CharField(max_length=10, blank=True, null=True, choices=delivery_sel)
    gl_baby_cried_after_del = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    resusciation_sel = [('Ventilation', 'Ventilation'), ('O2 Support', 'O2 Support'),('CPAP', 'CPAP'), ('Other', 'Other')]
    gl_nicu_stay=models.CharField(max_length=10, blank=True, null=True,)
    gl_resusciation_yes_no = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_resusciation_req = models.CharField(max_length=50, blank=True, null=True, choices=resusciation_sel)
    gl_resusciation_req_other = models.CharField(max_length=50, blank=True, null=True,)
    gl_birth_weight = models.FloatField(blank=True, null=True)
    gl_dev_milestone = models.CharField(max_length=15, blank=True, null=True, choices=time_sel)
    gl_dev_motor_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_dev_global_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_dev_cognitive_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    rec_infec_sel = [('Diarrhoea', 'Diarrhoea'), ('Respiratory', 'Respiratory'), ('skin', 'skin'), ('Other', 'Other')]
    site_bleeding_sel = [('epistaxis', 'epistaxis'), ('hemetemesis', 'hemetemesis'), ('Per rectum', 'Per rectum')]
    gl_morn_leth_seiz = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_dev_delay = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_irritability = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_tremors = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_muscle_weak_floppy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_exerc_cramping = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_abdominal_dist = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_jaundice = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_over_hunger = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_vomiting = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_diarrhia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_weight_gain_fail = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_oral_ulcers = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_perianal_ulcar = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rec_infections = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rec_infections_type = models.CharField(max_length=15, blank=True, null=True, choices=rec_infec_sel)
    gl_rec_infections_type_other = models.CharField(max_length=15, blank=True, null=True, )
    gl_bony_deforminty = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_site_bleeding = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_site_bleeding_type = models.CharField(max_length=15, blank=True, null=True, choices=site_bleeding_sel)
    gl_polyurea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_puberty_delay = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_joint_pain = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_exertion_dyspnoea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    hepatomegaly_sel = [('Size (cm) BCM', 'Size (cm) BCM'), ('Span', 'Span'),
                        ('Left lobe enlargement', 'Left lobe enlargement'),
                        ('Consistency', 'Consistency'), ('Margins', 'Margins')]
    done_not_done_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    normal_delayed_sel = [('Normal', 'Normal'), ('Delayed', 'Delayed')]
    hepatomegalySize=models.FloatField(max_length=10, blank=True, null=True, )
    hepatomegalySpan=models.CharField(max_length=10, blank=True, null=True, )
    hepatomegalyLeftLobe=models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    hepatomegalyConsistency= [('Firm', 'Firm'), ('Soft', 'Soft'), ('Hard', 'Hard')]
    hepatomegalyConsistencyChoice=models.CharField(max_length=10, blank=True, null=True, choices=hepatomegalyConsistency)
    hepatomegalysurface=[ ('Smooth', 'Smooth'),('Nodular', 'Nodular'),('Granular', 'Granular')]
    hepatomegalysurfaceChoice=models.CharField(max_length=10, blank=True, null=True, choices=hepatomegalysurface)
    hepatomegalyMargin=[('Sharp', 'Sharp'), ('Rounded', 'Rounded')]
    hepatomegalyMarginChoice=models.CharField(max_length=10, blank=True, null=True, choices=hepatomegalyMargin)




    gl_doll_like_face = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_hepatomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_hepatomegaly_type = models.CharField(max_length=32, blank=True, null=True, choices=hepatomegaly_sel)
    gl_hepatomegaly_left_lobe_enlargement = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    consistency_sel = [('Soft', 'Soft'), ('Firm', 'Firm'), ('Firm', 'Firm')]
    gl_hepatomegaly_consistency = models.CharField(max_length=10, blank=True, null=True, choices=consistency_sel)
    margin_sel = [('Round', 'Round'), ('Sharp', 'Sharp')]
    gl_hepatomegaly_margin = models.CharField(max_length=10, blank=True, null=True, choices=margin_sel)
    gl_splenomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_splenomegaly_size = models.FloatField(blank=True, null=True)
    gl_renal_enlargement = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rachitic_changes = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_hypotonia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    iq_dq_sel = [('Perform', 'Perform'), ('Not perform', 'Not perform')]
    IQDQSel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    IIQChoice = models.CharField(max_length=10, blank=True, null=True, choices=IQDQSel)
    DQChoice = models.CharField(max_length=10, blank=True, null=True, choices=IQDQSel)
    IQValue= models.CharField(max_length=20, blank=True, null=True,)
    DQValue = models.CharField(max_length=20, blank=True, null=True,)

    gl_iq_status = models.CharField(max_length=50, blank=True, null=True, choices=iq_dq_sel)
    gl_iq_value = models.FloatField(blank=True, null=True)
    # gl_dq_status = models.CharField(max_length=10, blank=True, null=True, choices=done_not_done_sel)
    # gl_dq_value = models.FloatField(blank=True, null=True)
    gl_any_other_findings = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_cong_heart_fail = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_core_pulomonable = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_hypertension = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_inv_hb = models.FloatField(blank=True, null=True)
    gl_inv_wbc = models.FloatField(blank=True, null=True)
    gl_inv_platelet_count = models.FloatField(blank=True, null=True)
    gl_inv_anc = models.FloatField(blank=True, null=True)
    gl_inv_abs_neutrophil_count = models.FloatField(blank=True, null=True)
    gl_inv_pt_sec = models.FloatField(blank=True, null=True)
    gl_inv_aptt_sec = models.FloatField(blank=True, null=True)
    gl_inv_ph = models.FloatField(blank=True, null=True)
    gl_inv_hco_3 = models.FloatField(blank=True, null=True)
    gl_inv_lactate = models.FloatField(blank=True, null=True)
    gl_inv_anion_gap = models.FloatField(blank=True, null=True)
    gl_inv_fasting_sugar = models.FloatField(blank=True, null=True)
    gl_inv_s_cal = models.FloatField(blank=True, null=True)
    gl_inv_s_phosphorous = models.FloatField(blank=True, null=True)
    gl_inv_s_alkaline = models.FloatField(blank=True, null=True)
    gl_inv_total_bilirubin = models.FloatField(blank=True, null=True)
    gl_inv_direct_bilirubin = models.FloatField(blank=True, null=True)
    gl_inv_total_protien = models.FloatField(blank=True, null=True)
    gl_inv_serum_albumin = models.FloatField(blank=True, null=True)
    gl_inv_sgpt = models.FloatField(blank=True, null=True)
    gl_inv_sgot = models.FloatField(blank=True, null=True)
    gl_inv_ggt = models.FloatField(blank=True, null=True)
    gl_inv_serum_urea = models.FloatField(blank=True, null=True)
    gl_inv_serum_creatinine = models.FloatField(blank=True, null=True)
    gl_inv_micro_alb =models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gl_inv_proteinuria = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gl_inv_hypercal = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    # gl_Microalbuminuria=models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    # gl_Proterinuria=models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gl_Hypercalciuria=models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gi_Hypocitrauria=models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gl_inv_hypercitrauria = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    gl_inv_bld = models.FloatField(blank=True, null=True)
    gl_inv_tg = models.FloatField(blank=True, null=True)
    gl_inv_tc = models.FloatField(blank=True, null=True)
    gl_inv_vldl = models.FloatField(blank=True, null=True)
    gl_inv_hdl = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_ldl = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_iron = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_tibc = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_vit_d = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_pth = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_s_uric_acid = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_s_cpk = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_inv_s_afp = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    gl_inv_biotinidase = models.CharField(max_length=50, blank=True, null=True, choices=normal_abnormal_sel)
    gl_inv_biotinidase_if_abnormal = models.CharField(max_length=50, blank=True, null=True,
                                                      validators=[MaxLengthValidator(50)])
    gl_inv_tms = models.CharField(max_length=50, blank=True, null=True, choices=normal_abnormal_sel)
    gl_inv_tms_if_abnormal_value = models.CharField(max_length=50, blank=True, null=True,
                                                    validators=[MaxLengthValidator(50)])
    gl_theroid_function_test = models.CharField(max_length=50, blank=True, null=True, choices=normal_abnormal_sel)
    gl_inv_t_3 =  models.CharField(max_length=50, blank=True, null=True, )
    gl_inv_t_4 =models.CharField(max_length=50, blank=True, null=True, )
    gl_inv_tsh = models.CharField(max_length=50, blank=True, null=True, )
    gl_inv_urine = models.IntegerField(blank=True, null=True)
    gl_ketosis = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Gl_urine_ketone = [('0', '0'), ('1+', '1+'), ('2+', '2+'), ('3+', '3+'), ('4+', '4+')]
    urine_ketosis = models.CharField(max_length=50, blank=True, null=True, choices=Gl_urine_ketone)
    done_not_done_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    normal_delayed_sel = [('Normal', 'Normal'), ('Delayed', 'Delayed')]
    echocardiography_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    volvular_sel = [('mitral', 'mitral'), ('tricuspid', ' tricuspid'), ('aortic', 'aortic'), ('pulmonary', 'pulmonary')]
    gl_rad_ultrasonography = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rad_ultrasono_type = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    gl_rad_ultra_finding_ab_specify = models.CharField(max_length=50, blank=True, null=True,
                                                       validators=[MaxLengthValidator(50)])
    gl_rad_liversize =  models.FloatField(blank=True, null=True)
    gl_rad_liverEchotexture = models.CharField(max_length=10, blank=True, null=True, )
    gl_rad_Kidney= models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rad_hepatic = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rad_kidney_size = models.IntegerField(blank=True, null=True)
    gl_rad_spleen_size = models.FloatField(blank=True, null=True)
    gl_rad_Echotexture = models.FloatField(blank=True, null=True)
    gl_rad_lymphnodes_size = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_rad_portal_vien_dia = models.IntegerField(blank=True, null=True)
    gl_rad_adenoma = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_renal_par_pathalogy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_renal_par_pathalogy_specify = models.CharField(max_length=50, blank=True, null=True,
                                                      validators=[MaxLengthValidator(50)])
    gl_nephrocalcinosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_pancreatitis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_cholethiasis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_xray_bone_age = models.CharField(max_length=10, blank=True, null=True, choices=normal_delayed_sel)
    gl_echocardiography_status = models.CharField(max_length=20, blank=True, null=True, choices=echocardiography_sel)
    # gl_echocard_abnormal_findings = models.CharField(max_length=50, blank=True, null=True,
    #                                             validators=[MaxLengthValidator(50)])
    gl_echo_abnormal_cardio = models.BooleanField(default=False)
    gl_echo_abnormal_mention_lvmi = models.CharField(max_length=20, blank=True, null=True, )
    # gl_echo_abnormal_volvular = models.CharField(max_length=10, blank=True, null=True, validators=[MaxLengthValidator(10)])
    gl_echo_abnormal_volvular_spcify = models.CharField(max_length=10, blank=True, null=True,
                                                        validators=[MaxLengthValidator(10)])
    gl_volvular_stenosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_volvular_mitral1= models.BooleanField(default=False)
    gl_volvular_tricuspid1 = models.BooleanField(default=False)
    gl_volvular_aortic1 = models.BooleanField(default=False)
    gl_volvular_pulmonary1 = models.BooleanField(default=False)
    gl_volvular_mitral2 = models.BooleanField(default=False)
    gl_volvular_tricuspid2 = models.BooleanField(default=False)
    gl_volvular_aortic2 = models.BooleanField(default=False)
    gl_volvular_pulmonary2 = models.BooleanField(default=False)
    gl_volvular_stenosis_options = models.CharField(max_length=20, blank=True, null=True, choices=volvular_sel)
    gl_volvular_regurgitation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_volvular_regurgitation_options = models.CharField(max_length=20, blank=True, null=True, choices=volvular_sel)
    gl_ejection_fraction = models.CharField(max_length=20, blank=True, null=True, )
    gl_liver_muscle = models.CharField(max_length=20, blank=True, null=True, choices=done_not_done_sel)
    gl_live_histopathology = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    gl_live_histopathology_val = models.CharField(max_length=20, blank=True, null=True,)
    gl_Muscule_histopathology = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    gl_Muscule_histopathology_val = models.CharField(max_length=20, blank=True, null=True, )
    gl_liver_muscle_findings_specify = models.CharField(max_length=50, blank=True, null=True,
                                                        validators=[MaxLengthValidator(50)])
    echocardiography_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    assay_sel = [('Serum', 'Serum'), ('Plasma', 'Plasma'), ('Leucocyte', 'Leucocyte'), ('RBC', 'RBC'),
                 ('Liver', 'Liver'), ('Muscle', 'Muscle'),('DBS','DBS'),('whole blood','whole blood')]
    gl_enzyme_assay = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_enzyme_assay_report = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    gl_enzyme_assay_type = models.CharField(max_length=20, blank=True, null=True, choices=assay_sel)
    gl_patient_value = models.FloatField(blank=True, null=True)
    gl_normal_control = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_normal_range = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_mol_diagnosis_desc_gene_seq = models.CharField(max_length=50, blank=True, null=True,
                                                      validators=[MaxLengthValidator(50)])
    gl_mol_diagnosis_report = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    gl_dna_seq = models.CharField(max_length=20, blank=True, null=True, choices=echocardiography_sel)
    gl_abormal_patient = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_abormal_father = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_abormal_mother = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_treat_diet_alone =  models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_treat_diet_anti_lipic =  models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_treat_diet_anti_lipic_hypouricemia =  models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_treat_diet_anti_hypouricemia =  models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_supportive_therapy = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_any_surgery = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_any_surgery_specify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_any_organ_transplantation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    gl_any_organ_transplantation_specify = models.CharField(max_length=50, blank=True, null=True,
                                                            validators=[MaxLengthValidator(50)])
    gl_any_other_info = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    gl_filled_by_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_clinical_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    gl_date = models.DateField(blank=True, null=True)
    gl_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #	Molecular Diagnostics
    Causative_DNA_sequence_variation_sel = [('done', 'done'), ('not done', 'not done')]
    Causative_DNA_sequence_variation = models.CharField(max_length=20,  null=True, choices=yes_no_sel)
    # If_done =
    molecular_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    gl_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    gl_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    gl_var_sel = [('Novel', 'Novel '),
                   ('Reported', 'Reported')]
    gl_var1 = models.CharField(max_length=100, null=True, blank=True, choices=gl_var_sel)
    gl_zygo_sel = [('Homozygous', 'Homozygous '),
                    ('Heterozygous', 'Heterozygous'),
                   ('Hemizygous', 'Hemizygous')]
    gl_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=gl_zygo_sel)
    gl_vari_sel = [('Pathogenic ', 'Pathogenic '),
                    ('Likely Pathogenic', 'Likely Pathogenic'),
                    ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    gl_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=gl_vari_sel)

    gl_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    gl_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    gl_var_sel = [('Novel', 'Novel '),
                  ('Reported', 'Reported')]
    gl_var2 = models.CharField(max_length=100, null=True, blank=True, choices=gl_var_sel)
    gl_zygo_sel = [('Homozygous', 'Homozygous '),
                   ('Heterozygous', 'Heterozygous'),
                   ('Hemizygous', 'Hemizygous')]
    gl_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=gl_zygo_sel)
    gl_vari_sel = [('Pathogenic ', 'Pathogenic '),
                   ('Likely Pathogenic', 'Likely Pathogenic'),
                   ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    gl_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=gl_vari_sel)
    gl_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_sel)
    father = models.CharField(max_length=100, blank=True, null=True)
    mother = models.CharField(max_length=100, blank=True, null=True)

    gl_Finaldiagnosis_sel = [('Glyogen storage disorder Type Ia(Von Gierke)', 'Glyogen storage disorder Type Ia(Von Gierke)'),
                             ('Glyogen storage disorder Type Ib', 'Glyogen storage disorder Type Ib'),
                             ('Glyogen storage disorder Type IIIa(Cori/Forbes)', 'Glyogen storage disorder Type IIIa(Cori/Forbes)'),
                             ('Glyogen storage disorder Type IIIb', 'Glyogen storage disorder Type IIIb'),
                             ('Glyogen storage disorder Type IVa(Anderson)', 'Glyogen storage disorder Type IVa(Anderson)'),

                             ('Glyogen storage disorder Type VI(Hers)', 'Glyogen storage disorder Type VI(Hers)'),

                             ('Glyogen storage disorder Type XIa(Phosphorylase kinase deficiency)', 'Glyogen storage disorder Type XIa(Phosphorylase kinase deficiency)'),

                             ('Glyogen storage disorder Type0(Glycogen synthases deficiency)', 'Glyogen storage disorder Type0(Glycogen synthases deficiency'),
                             ('Glyogen storage disorder TypeXI(Fanconi-Bickel Syndrome)', 'Glyogen storage disorder TypeXI(Fanconi-Bickel Syndrome)'),

                             ('Other', 'Other')]
    gl_Finaldiagnosis_other= models.CharField(max_length=100, null=True, blank=True,)
    gl_Finaldiagnosis = models.CharField(max_length=100, null=True,  choices=gl_Finaldiagnosis_sel)

    gl_Finaloutcomes_sel = [('Death', 'Death'),
                            ('Alive', 'Alive'),
                            ('Followup required', 'Followup required'),
                            ('Unknown', 'Unknown'), ]
    gl_Finaloutcomes = models.CharField(max_length=100, null=True,  choices=gl_Finaloutcomes_sel)

    def __str__(self):
        return str(self.pk)