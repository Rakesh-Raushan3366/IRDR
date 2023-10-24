from django.db import models

# Create your models here.
from uuid import uuid4
from django.core.validators import FileExtensionValidator
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
from account.models import *


# Create your models here.


class profile_pompe(models.Model):
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

    pmp_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_date_of_records = models.DateField(blank=True, null=True)
    pmp_date_of_clinical_exam = models.DateField(blank=True, null=True)
    pmp_date_of_birth = models.DateField( null=True)
    pmp_patient_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    pmp_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'), ('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id')]
    pmp_paitent_id_yes_no = models.CharField(max_length=100, null=True, choices=fb_status_sel)
    pmp_paitent_id = models.CharField(max_length=100, blank=True,null=True, choices=id_sel)
    pmp_patient_id_no = models.CharField(max_length=100, unique=True,blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_father_mother_id = models.CharField(max_length=100,blank=True, null=True, choices=id_sel)
    pmp_father_mother_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    # pmp_mother_adhaar_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    pmp_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    pmp_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    pmp_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    pmp_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_mother_mobile_no = models.PositiveBigIntegerField(null=True, unique=True)
    pmp_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    pmp_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    pmp_email = models.EmailField(max_length=300, blank=True, null=True)

    pmp_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    pmp_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    pmp_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    pmp_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    pmp_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    pmp_consent_given = models.CharField(max_length=10, null=True, choices=fb_status_sel)
    pmp_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    pmp_assent_given = models.CharField(max_length=10, null=True, choices=fb_status_sel)
    pmp_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    pmp_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pmp_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_pompe', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_pompe', on_delete=models.CASCADE)

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
            super(profile_pompe, self).save(*args, **kwargs)
            self.pmp_icmr_unique_no = str('Pompe/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_pompe, self).save(*args, **kwargs)


class demographic_pompe(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_pompe, null=True,related_name='patient_pompe', blank=True, on_delete=models.CASCADE)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    yes_no123 = [('1', 'Yes'), ('0', 'No')]
    Patient_edu_sel = [('No formal education', 'No formal education'),
                       ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                       ('Secondary school', 'Secondary school'),
                       ('College/Pre-university', 'College/Pre-university'),
                       ('Post graduate degree ', 'Post graduate degree ')]
    pd_Patient_education = models.CharField(max_length=100, null=True, blank=True, choices=Patient_edu_sel)
    Patient_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                              ('Private Service', 'Private Service'),
                              ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                              ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    pd_Patient_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Patient_occupation_sel)
    Father_edu_sel = [('No formal education', 'No formal education'),
                      ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                      ('Secondary school', 'Secondary school'),
                      ('College/Pre-university', 'College/Pre-university'),
                      ('Post graduate degree ', 'Post graduate degree ')]
    pd_Father_education = models.CharField(max_length=100, null=True, blank=True, choices=Father_edu_sel)
    Father_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                             ('Private Service', 'Private Service'), 
                             ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                             ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    pd_Father_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Father_occupation_sel)
    Mother_edu_sel = [('No formal education', 'No formal education'),
                      ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                      ('Secondary school', 'Secondary school'),
                      ('College/Pre-university', 'College/Pre-university'),
                      ('Post graduate degree ', 'Post graduate degree ')]
    pd_Mother_education = models.CharField(max_length=100, null=True, blank=True, choices=Mother_edu_sel)
    Mother_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                             ('Private Service', 'Private Service'), ('Housewife', 'Housewife'),
                             ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                             ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    pd_Mother_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Mother_occupation_sel)
    Monthly_family_income_sel = [('> 126,360', '> 126,360)'),
                                 ('63,182 â€“ 126,356)', '63,182 â€“ 126,356)'),
                                 ('47,266 â€“ 63,178', '47,266 â€“ 63,178'),
                                 ('31,591 - 47,262', '31,591 - 47,262'),
                                 ('18,953 - 31,589', '18,953 - 31,589'),
                                 ('6,327 - 18,949', '6,327 - 18,949'),
                                 ('< 6,323', '< 6,323')]
    pd_Monthly_family_income = models.CharField(max_length=200, null=True, blank=True,
                                                choices=Monthly_family_income_sel)
    pd_weight_patient = models.CharField(max_length=200, null=True, blank=True)
    pd_weight_percentile =  models.CharField(max_length=200, null=True, blank=True)
    pd_weight_SD =  models.CharField(max_length=200, null=True, blank=True)
    pd_height_patient =  models.CharField(max_length=200, null=True, blank=True)
    pd_height_percentile =  models.CharField(max_length=200, null=True, blank=True)
    pd_height_SD = models.CharField(max_length=200, null=True, blank=True)
    pd_Head_circumference_patient =  models.CharField(max_length=200, null=True, blank=True)
    pd_Head_circumference_percentile =  models.CharField(max_length=200, null=True, blank=True)
    pd_Head_circumference_sd =  models.CharField(max_length=200, null=True, blank=True)
    pd_Age_at_onset_of_symptoms_year = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_onset_of_symptoms_month = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_onset_of_symptoms_day = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_onset_of_symptoms_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    pd_Age_at_presentation_year = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_presentation_month = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_presentation_day = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_presentation_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    pd_Age_at_diagnosis_year = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_diagnosis_month = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_diagnosis_day = models.PositiveSmallIntegerField(blank=True, null=True)
    pd_Age_at_diagnosis_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    pd_Pedigree_to_be_uploaded = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, )
    pd_positive_family_history = models.CharField(max_length=100, null=True, blank=True,
                                                  choices=yes_no, )
    pd_family_history_specify = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    pd_Consanguinity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no, )
    pd_Consanguinity_specify = models.CharField(max_length=200, null=True, blank=True, )
    pd_Ultrasound_findings = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    pd_Polyhydramnios = models.CharField(max_length=100, null=True, blank=True,
                                         choices=yes_no, )
    pd_Fetal_echocardiography_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    pd_Fetal_echocardiography = models.CharField(max_length=100, null=True, blank=True,
                                                 choices=pd_Fetal_echocardiography_sel)
    pd_Fetal_echocardiography_specify = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    pd_Natal_History_sel = [('caesarean', 'caesarean'), ('Vaginal', 'Vaginal')]
    pd_Natal_History_Type_of_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                         choices=pd_Natal_History_sel)
    pd_Natal_History_Baby_cried_immediately_after_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                                              choices=yes_no)
    pd_Natal_History_Resuscitation_required = models.CharField(max_length=100, null=True, blank=True,
                                                               choices=yes_no)
    pd_Natal_History_o_2_Cpap = models.CharField(max_length=100, null=True, blank=True,
                                                 choices=yes_no)
    pd_Natal_History_ventilater = models.CharField(max_length=100, null=True, blank=True,
                                                   choices=yes_no)
    pd_Natal_History_Nursery_stay = models.CharField(max_length=100, null=True, blank=True,
                                                     choices=yes_no)
    pd_Birth_weight = models.FloatField(blank=True, null=True)
    pd_Milestone_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    pd_Development_milestones = models.CharField(max_length=100, null=True, blank=True, choices=pd_Milestone_sel)
    pd_if_delayed_Motor = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_if_delayed_Global = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_if_delayed_Cognitive = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)

    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    # pd_head_sel = [('Anterior fontanelle', 'Anterior fontanelle'),
    #                ('Posterior fontanelle', 'Posterior fontanelle')]
    pd_head = models.CharField(max_length=200, null=True, blank=True)
    # pd_face_sel = [('Normal', 'Normal'),
    #                ('Abnormal', 'Abnormal')]
    pd_face = models.CharField(max_length=200, null=True, blank=True)
    pd_Eyes_Ptosis = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Large_tongue = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Others_specify = models.CharField(max_length=100, null=True, blank=True,
                                         validators=[MaxLengthValidator(100)])
    pd_Ever_had_respiratory_distress = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_No_of_episode_sel = [('2', '2'),
                            ('>2', '>2')]
    pd_No_of_episode = models.CharField(max_length=200, null=True, blank=True, choices=pd_No_of_episode_sel)
    pd_Ventilator_or_other_respiratory_support = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Mode_of_ventilation_sel = [('Room-air', 'Room-air'),
                                  ('CPAP', 'CPAP'),
                                  ('INVASIVE VENTILATION', 'INVASIVE VENTILATION'),
                                  ('NON-INVASIVE VEANTILATION', 'NON-INVASIVE VEANTILATION')]
    pd_Mode_of_ventilation = models.CharField(max_length=200, null=True, blank=True, choices=pd_Mode_of_ventilation_sel)
    pd_Age_at_ventilator = models.CharField(max_length=100, null=True, blank=True,
                                            validators=[MaxLengthValidator(100)])
    pd_Tracheostomy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Was_weaning_off_from_ventilator_possible = models.CharField(max_length=100, null=True, blank=True,
                                                                   choices=yes_no)
    pd_Feeding_difficulties = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Feeding_sel = [('NG tube', 'NG tube'),
                      ('OG tube feeding', 'OG tube feeding'),
                      ('Gastrostomy', 'Gastrostomy')]
    pd_Feeding = models.CharField(max_length=200, null=True, blank=True, choices=pd_Feeding_sel)
    pd_date_started = models.CharField(max_length=20, null=True, blank=True)
    pd_Protuberantabdomen = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Hepatomegaly = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Size_BCM = models.CharField(max_length=100, null=True, blank=True,
                                   validators=[MaxLengthValidator(100)])
    pd_Span = models.CharField(max_length=100, null=True, blank=True,
                               validators=[MaxLengthValidator(100)])
    pd_Hernia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Others = models.CharField(max_length=20, null=True, blank=True)
    pd_Hernia_Others_specify = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    pd_Edema = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Cyanosis = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Cardiac_medications_date_started = models.DateField(blank=True, null=True)
    pd_Cardiac_medications_dose = models.CharField(max_length=100, null=True, blank=True,
                                                   validators=[MaxLengthValidator(100)])
    pd_Heart_rate = models.CharField(max_length=100, null=True, blank=True,
                                     validators=[MaxLengthValidator(100)])
    pd_Gallop = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_arrythmia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Cardiac_medications = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Cardiac_medications_specify = models.CharField(max_length=100, null=True, blank=True,
                                                         validators=[MaxLengthValidator(100)])
    pd_Muscle_weakness = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Age_at_Onset_of_weakness = models.CharField(max_length=100, null=True, blank=True,
                                                   validators=[MaxLengthValidator(100)])
    pd_Onset_of_weakness_sel = [('Upper Limbs', 'Upper Limbs'),
                                ('Lower Limbs', 'Lower Limbs'),
                                ('Both', 'Both')]
    pd_Onset_of_weakness = models.CharField(max_length=200, null=True, blank=True, choices=pd_Onset_of_weakness_sel)
    pd_Difficulty_in_sitting_from_lying_position = models.CharField(max_length=100, null=True, blank=True,
                                                                    choices=yes_no)
    pd_Difficulty_in_standing_from_standing_position = models.CharField(max_length=100, null=True, blank=True,
                                                                        choices=yes_no)
    pd_Wheelchair_bound_sel = [('Ambulatory', 'Ambulatory'),
                            ('Wheelchair bound', 'Wheelchair bound'),
                               ('Bedridden', 'Bedridden'),
                               ('Other motor assisted devices', 'Other motor assisted devices'),
                               ('Not yet attained ambulation', 'Not yet attained ambulation')]
    pd_Wheelchair_bound = models.CharField(max_length=200, null=True, blank=True, choices=pd_Wheelchair_bound_sel)
    pd_Age_at_Wheelchair_bound = models.CharField(max_length=100, null=True, blank=True,
                                                  validators=[MaxLengthValidator(100)])
    pd_Sleep_disturbances_apnea = models.CharField(max_length=100, null=True, blank=True,
                                                   choices=yes_no)
    pd_Hypotonia = models.CharField(max_length=100, null=True, blank=True,
                                    choices=yes_no)
    pd_Proximal_muscle_weakness_in_upper_extremities = models.CharField(max_length=100, null=True, blank=True,
                                                                        choices=yes_no)
    pd_Distal_muscle_weakness_in_upper_extremities = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=yes_no)
    pd_Proximal_muscle_weakness_in_lower_extremities = models.CharField(max_length=100, null=True, blank=True,
                                                                        choices=yes_no)
    pd_Distal_muscle_weakness_in_lower_extremities = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=yes_no)
    pd_Neck_muscle_weakness = models.CharField(max_length=100, null=True, blank=True,
                                               choices=yes_no)
    pd_Muscle_weakness_in_trunk = models.CharField(max_length=100, null=True, blank=True,
                                                   choices=yes_no)
    pd_Reflexes_sel = [('Present', 'Present'),
                       ('Absent', 'Absent')]
    pd_Reflexes = models.CharField(max_length=200, null=True, blank=True, choices=pd_Reflexes_sel)
    pd_Gower_positive = models.CharField(max_length=100, null=True, blank=True,
                                         choices=yes_no)
    pd_Contractures = models.CharField(max_length=100, null=True, blank=True,
                                       choices=yes_no)
    pd_Abnormal_Gait = models.CharField(max_length=100, null=True, blank=True,
                                        choices=yes_no)
    pd_Muscles_of_respiration_involved = models.CharField(max_length=100, null=True, blank=True,
                                                          choices=yes_no)
    pd_bulbar_and_lingual_weakness = models.CharField(max_length=100, null=True, blank=True,
                                                      choices=yes_no)
    pd_if_yes_bulbar_sel = [('dysarthria', 'dysarthria'),
                            ('dysphagia', 'dysphagia')]
    pd_if_yes = models.CharField(max_length=200, null=True, blank=True, choices=pd_if_yes_bulbar_sel)
    pd_Rigid_spine = models.CharField(max_length=100, null=True, blank=True,
                                      choices=yes_no)
    pd_Higher_mental_functions_sel = [('Normal', 'Normal'),
                                      ('Abnormal', 'Abnormal')]
    pd_Higher_mental_functions = models.CharField(max_length=200, null=True, blank=True,
                                                  choices=pd_Higher_mental_functions_sel)
    pd_Cranial_nerve_involvement = models.CharField(max_length=100, null=True, blank=True,
                                                    choices=yes_no)
    pd_Altered_or_reduced_visual_acuity = models.CharField(max_length=100, null=True, blank=True,
                                                           choices=yes_no)
    pd_Hearing_loss = models.CharField(max_length=100, null=True, blank=True,
                                       choices=yes_no)
    pd_Foot_drop = models.CharField(max_length=100, null=True, blank=True,
                                    choices=yes_no)

    # yes_no = [('Yes', 'Yes'), ('No', 'No')]
    pd_Radiography_of_chest_to_assess_for_cardiomegaly_sel = [('Cardiomegaly Present', 'Cardiomegaly Present'),
                                                          ('Cardiomegaly Absent', 'Cardiomegaly Absent'),
                                                              ('Not done', 'Not done')]
    pd_Radiography_of_chest_to_assess_for_cardiomegaly = models.CharField(max_length=100, null=True, blank=True,
                                                                          choices=pd_Radiography_of_chest_to_assess_for_cardiomegaly_sel)
    pd_ECG_sel = [('Normal', 'Normal'),
                  ('abnormal', 'abnormal')]
    pd_ECG = models.CharField(max_length=200, null=True, blank=True, choices=pd_ECG_sel)
    pd_Short_PR = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Tall_broad_QRS = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_ECHO_date = models.DateField(blank=True, null=True)
    pd_ECHO_sel = [('Normal', 'Normal'),
                   ('Abnormal', 'Abnormal')]
    pd_ECHO = models.CharField(max_length=200, null=True, blank=True, choices=pd_ECHO_sel)
    pd_ECHO_specify = models.CharField(max_length=100, null=True, blank=True,
                                      validators=[MaxLengthValidator(100)])
    pd_PFT_date = models.DateField(blank=True, null=True)
    pd_PFT_sel = [('Normal', 'Normal'),('abnormal', 'abnormal'),
                  ('Not Done', 'Not Done')]
    pd_PFT = models.CharField(max_length=200, null=True, blank=True, choices=pd_PFT_sel)
    # pd_PFT_if_done_sel = [('Normal', 'Normal'),
    #                       ('Abnormal', 'Abnormal')]
    # pd_PFT_if_done = models.CharField(max_length=200, null=True, blank=True, choices=pd_PFT_if_done_sel)
    pd_PFT_Supine_FVC = models.CharField(max_length=100, null=True, blank=True,
                                         validators=[MaxLengthValidator(100)])
    pd_PFT_Sitting_FVC = models.CharField(max_length=100, null=True, blank=True,
                                          validators=[MaxLengthValidator(100)])
    pd_PFT_Supine_FEV1 = models.CharField(max_length=100, null=True, blank=True,
                                          validators=[MaxLengthValidator(100)])
    pd_PFT_Sitting_FEV1 = models.CharField(max_length=100, null=True, blank=True,
                                           validators=[MaxLengthValidator(100)])
    pd_PFT_Mean_Inspiratory_Pressure = models.CharField(max_length=100, null=True, blank=True,
                                                        validators=[MaxLengthValidator(100)])
    pd_PFT_Mean_Expiratory_Pressure = models.CharField(max_length=100, null=True, blank=True,
                                                       validators=[MaxLengthValidator(100)])
    pd_Swallow_study_sel = [('Normal', 'Normal'),
                            ('Abnormal', 'Abnormal'),
                            ('Not Done', 'Not Done')]
    pd_Swallow_study = models.CharField(max_length=200, null=True, blank=True, choices=pd_Swallow_study_sel)
    pd_Swallow_study_specify = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    pd_Biochemical_testing_date = models.DateField(blank=True, null=True)
    pd_CK = models.CharField(max_length=100, null=True, blank=True,
                             validators=[MaxLengthValidator(100)])
    pd_CK_MB = models.CharField(max_length=100, null=True, blank=True,
                                validators=[MaxLengthValidator(100)])
    pd_AST = models.CharField(max_length=100, null=True, blank=True,
                              validators=[MaxLengthValidator(100)])
    pd_ALT = models.CharField(max_length=100, null=True, blank=True,
                              validators=[MaxLengthValidator(100)])
    pd_LDH = models.CharField(max_length=100, null=True, blank=True,
                              validators=[MaxLengthValidator(100)])

    pd_Enzyme_analysis_uploaded = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True, )
    pd_Sample_sel = [('DBS', 'DBS'),
                     ('Blood', 'Blood')]
    pd_Enzyme_analysis_done = models.CharField(max_length=200, null=True, blank=True, choices=pd_Sample_sel)
    pd_Sample_date_done = models.DateField(blank=True, null=True)
    pd_patien = models.CharField(max_length=200, null=True, blank=True,)
    pd_contro = models.CharField(max_length=200, null=True, blank=True, )
    pd_nor_ran = models.CharField(max_length=200, null=True, blank=True, )
    pd_CRIM_sel = [('Negative', 'Negative'),
                   ('Positive', 'Positive'),
                   ('Not Done', 'Not Done')]
    pd_CRIM_Status = models.CharField(max_length=200, null=True, blank=True, choices=pd_CRIM_sel)

    #	Molecular Diagnostics
    pd_Causative_DNA_sequence_variation = [('done', 'done'), ('not done', 'not done')]
    pd_Causative_DNA_sequence_variat = models.CharField(max_length=20, blank=True, null=True, choices=yes_no)
    # If_done =
    pd_molecular_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    pd_Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    pd_Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    pd_trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    pd_mul_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_mul_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_mul_var_sel = [('Novel', 'Novel '),
                   ('Reported', 'Reported')]
    pd_mul_var1 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_var_sel)
    pd_mul_zyg_sel = [('Homozygous', 'Homozygous '),
                    ('Heterozygous', 'Heterozygous'),
                      ('Hemizygous', 'Hemizygous')]
    pd_mul_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_zyg_sel)
    pd_mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                    ('Likely Pathogenic', 'Likely Pathogenic'),
                    ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    pd_mul_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_vari_sel)
    pd_mul_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_mul_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_mul_var_sel = [('Novel', 'Novel '),
                      ('Reported', 'Reported')]
    pd_mul_var2 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_var_sel)
    pd_mul_zygo_sel = [('Homozygous', 'Homozygous '),
                       ('Heterozygous', 'Heterozygous'),
                       ('Hemizygous', 'Hemizygous')
                       ]
    pd_mul_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_zygo_sel)
    pd_mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                       ('Likely Pathogenic', 'Likely Pathogenic'),
                       ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    pd_mul_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=pd_mul_vari_sel)
    pd_mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pd_father = models.CharField(max_length=100, blank=True, null=True)
    pd_mother = models.CharField(max_length=100, blank=True, null=True)
    pd_ERT = models.CharField(max_length=30, null=True, blank=True, choices=yes_no)
    pd_name_of_com = models.CharField(max_length=30, null=True, blank=True, choices=yes_no)
    pd_ERT_enz = models.CharField(max_length=30, null=True, blank=True)
    pd_Date_Initiation = models.DateField(blank=True, null=True)
    pd_Age_of_Start = models.CharField(max_length=100, null=True, blank=True,
                                       validators=[MaxLengthValidator(100)])
    pd_Dosage = models.CharField(max_length=100, null=True, blank=True,
                                 validators=[MaxLengthValidator(100)])
    pd_Duration = models.CharField(max_length=100, null=True, blank=True,
                                   validators=[MaxLengthValidator(100)])
    pd_Adverse_events = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Adverse_events_specify = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])

    pd_Response = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Immunomodulation = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    pd_Immunomodulation_methotrexate = models.BooleanField(default=False)
    pd_Immunomodulation_rituximab = models.BooleanField(default=False)
    pd_Immunomodulation_ivig = models.BooleanField(default=False)
    pd_Current_ERT_Status = models.CharField(max_length=100, null=True, blank=True,
                                             validators=[MaxLengthValidator(100)])
    pd_Ongoing = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)

    pd_Any_interruption = models.CharField(max_length=100, null=True, blank=True,
                                           validators=[MaxLengthValidator(100)])
    pd_Reason_for_interruption = models.CharField(max_length=100, null=True, blank=True,
                                                  validators=[MaxLengthValidator(100)])
    pd_Duration_of_interruption = models.CharField(max_length=100, null=True, blank=True,
                                                   validators=[MaxLengthValidator(100)])
    pd_moto_ass = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pd_moto_sca = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_moto_qmft = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_moto_gsgc = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_moto_wlk_ts = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_Physiotherapy_date = models.DateField(blank=True, null=True)
    pd_filed_by_DEO_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pd_clinician_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    pd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pd_filled_date = models.DateField(null=True, blank=True)
    pd_Finaldiagnosis_sel = [('Late Onset Pompe Diesase', 'Late Onset Pompe Diesase'),
                             ('Infantile Onset Pompe Diesase', 'Infantile Onset Pompe Diesase')]
    pd_Finaldiagnosis = models.CharField(max_length=100, null=True, blank=True, choices=pd_Finaldiagnosis_sel)
    pd_Finaloutcomes_sel = [('Death', 'Death'),
                            ('Alive', 'Alive'),
                            ('Followup required', 'Followup required'),
                            ('Unknown', 'Unknown'), ]
    pd_Finaloutcomes = models.CharField(max_length=100, null=True, blank=True, choices=pd_Finaloutcomes_sel)

    def __str__(self):
        return str(self.pk)
