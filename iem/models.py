# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator

class profile_metabolism(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    mt_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    mt_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    mt_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    mt_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    mt_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    mt_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_date_of_records = models.DateField(blank=True, null=True)
    mt_date_of_clinical_exam = models.DateField(blank=True, null=True)
    mt_date_of_birth = models.DateField( null=True)
    mt_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    mt_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'), ('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id')]
    mt_paitent_id_yes_no = models.CharField(max_length=100,  null=True, choices=mt_status_sel)
    mt_paitent_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    mt_patient_id_no = models.CharField(max_length=100,blank=True, unique=True, null=True, validators=[MaxLengthValidator(100)])
    mt_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_patient_adhaar_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    mt_father_mother_id = models.CharField(max_length=100,blank=True,  null=True, choices=id_sel)
    mt_mother_father_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    mt_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    mt_state = models.ForeignKey(State, null=True,  on_delete=models.CASCADE, verbose_name=' state')
    mt_district = models.ForeignKey(District, null=True,  on_delete=models.CASCADE, verbose_name=' district')
    mt_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    mt_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    mt_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    mt_email = models.EmailField(max_length=300, blank=True, null=True)
    mt_religion = models.CharField(max_length=100, blank=True, null=True, choices=mt_religion_sel)
    mt_religion_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    mt_caste = models.CharField(max_length=100, blank=True, null=True, choices=mt_caste_sel)
    mt_caste_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    mt_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=mt_status_sel)
    mt_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=mt_referred_by)
    mt_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_gender = models.CharField(max_length=100, blank=True, null=True, choices=mt_gender_sel)
    mt_consent_given = models.CharField(max_length=10,  null=True, choices=mt_status_sel)
    mt_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, validators=[FileExtensionValidator(['pdf'])])
    mt_assent_given = models.CharField(max_length=10,  null=True, choices=mt_status_sel)
    mt_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    mt_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mt_date = models.DateField( null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_iem', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_iem', on_delete=models.CASCADE)

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
            super(profile_metabolism, self).save(*args, **kwargs)
            self.mt_icmr_unique_no = str('Metabolism/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_metabolism, self).save(*args, **kwargs)


class demographic_matabolism(models.Model):

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_metabolism, null=True,related_name='patient_metabolism', blank=True, on_delete=models.CASCADE)
    mt_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    mt_status_sel123 = [('1', 'Yes'), ('0', 'No')]
    mt_patient_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                          ('Secondary '
                           'level',
                           'Secondary '
                           'level'),
                          ('College and above', 'College and above')]
    mt_patient_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                           ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    mt_father_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    mt_father_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    mt_mother_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    mt_mother_occu_sel = [('Home maker', 'Home maker)'),
                          ('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    mt_monthly_income_sel = [('> 126,360', '> 126,360)'),
                             ('63,182 – 126,356)', '63,182 – 126,356)'),
                             ('47,266 – 63,178', '47,266 – 63,178'),
                             ('31,591 - 47,262', '31,591 - 47,262'),
                             ('18,953 - 31,589', '18,953 - 31,589'),
                             ('6,327 - 18,949', '6,327 - 18,949'),
                             ('< 6,323', '< 6,323')]

    mt_patient_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=mt_patient_edu_sel)
    mt_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=mt_patient_occu_sel)
    mt_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=mt_father_edu_sel)
    mt_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=mt_father_occu_sel)
    mt_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=mt_mother_edu_sel)
    mt_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=mt_mother_occu_sel)
    mt_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=mt_monthly_income_sel)

    yes_no_given_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not Given', 'Not Given')]
    mt_anthropometry_date = models.DateField(blank=True, null=True)
    mt_anth_wght_pat = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_wght_per = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_wght_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_height_pat = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_height_per = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_height_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_segment_patient = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_segment_percemtile =models.CharField(max_length=10, blank=True, null=True)
    mt_lower_segment_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_us_ls_patient = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_us_ls_percemtile = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_us_ls_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_arm_spam_patient = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_arm_spam_percemtile = models.CharField(max_length=10, blank=True, null=True)
    mt_lower_arm_spam_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_head_cir_pat = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_head_cir_perc = models.CharField(max_length=10, blank=True, null=True)
    mt_anth_head_cir_sd = models.CharField(max_length=10, blank=True, null=True)
    mt_presenting_complaints_years = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_months = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_day = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=mt_status_sel123)
    mt_presenting_complaints_age_presentation_years = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_presentation_months = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_presentation_day =models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_presentation_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=mt_status_sel123)
    mt_presenting_complaints_age_diagnosis_years = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_diagnosis_months = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_diagnosis_day = models.PositiveSmallIntegerField(blank=True, null=True)
    mt_presenting_complaints_age_diagnosis_intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=mt_status_sel123)

    mt_pedigree_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    mt_fam_hist_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_fam_hist_descr = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    mt_cons_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_cons_degree_specify = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    mt_Inbreeding = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Inbreeding_specify_degree = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_Inbreeding_coefficient_degree = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])

    mt_encephalopathic_presentation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_encephalopathic_presentation_age_presentaion = models.CharField(max_length=100, blank=True, null=True,
                                                                       validators=[MaxLengthValidator(100)])
    mt_encephalopathic_presentation_age_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                     validators=[MaxLengthValidator(100)])
    mt_encephalopathic_presentation_duration = models.CharField(max_length=100, blank=True, null=True,
                                                                validators=[MaxLengthValidator(100)])
    mt_Presentation_neonatal_jaundice = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Presentation_neonatal_jaundice_age_presentation = models.CharField(max_length=100, blank=True, null=True,
                                                                          validators=[MaxLengthValidator(100)])
    mt_Presentation_neonatal_jaundice_ae_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                      validators=[MaxLengthValidator(100)])
    mt_Presentation_neonatal_jaundice_duraions = models.CharField(max_length=100, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    mt_Presentation_cardiac_symptoms = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Presentation_cardiac_symptoms_age_presentation = models.CharField(max_length=100, blank=True, null=True,
                                                                         validators=[MaxLengthValidator(100)])
    mt_Presentation_cardiac_symptoms_age_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                      validators=[MaxLengthValidator(100)])
    mt_Presentation_cardiac_symptoms_duration = models.CharField(max_length=100, blank=True, null=True,
                                                                 validators=[MaxLengthValidator(100)])
    mt_Presentation_refractory_epilepsy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Presentation_refractory_epilepsy_age_presentation = models.CharField(max_length=100, blank=True, null=True,
                                                                            validators=[MaxLengthValidator(100)])
    mt_Presentation_refractory_epilepsy_age_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                         validators=[MaxLengthValidator(100)])
    mt_Presentation_refractory_epilepsy_duration = models.CharField(max_length=100, blank=True, null=True,
                                                                    validators=[MaxLengthValidator(100)])
    mt_symptoms_after_long_normalcy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_symptoms_after_long_normalcy_sugar = models.BooleanField(default=False)
    mt_symptoms_after_long_normalcy_fruit_juice = models.BooleanField(default=False)
    mt_symptoms_after_long_normalcy_fasting = models.BooleanField(default=False)
    mt_symptoms_after_long_normalcy_protein_foods = models.BooleanField(default=False)
    mt_symptoms_after_long_normalcy_febrile_illness = models.BooleanField(default=False)

    mt_mental_retardation_or_dev_delay = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Neuroregression = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    # = models.CharField(max_length=100, blank=True, null=True,
    #                                          validators=[MaxLengthValidator(100)])
    mt_mental_retardation_Motor = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_mental_retardation_Cognitive = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_mental_retardation_Global = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Age_onset_regression = models.FloatField(blank=True, null=True)
    mt_Neuroregression_Motor = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Neuroregression_Cognitive = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Neuroregression_Global = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    loose_pneumonia_sel=[('single episode','single episode'),('recurrent(>3 times /year)','recurrent(>3 times /year)')]
    mt_Behavioral_problems = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Vomiting = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Loose_stools = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Loose_stools_dropdown = models.CharField(max_length=30, blank=True, null=True, choices=loose_pneumonia_sel)
    # mt_Loose_stools_recurrent_pneumonia = models.BooleanField(default=False)
    mt_Pneumonia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Pneumonia_dropdown = models.CharField(max_length=30, blank=True, null=True, choices=loose_pneumonia_sel)
    # mt_Pneumonia_recurrent_pneumonia = models.BooleanField(default=False)
    mt_Fever = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Fever_dropdown = models.CharField(max_length=30, blank=True, null=True, choices=loose_pneumonia_sel)

    # mt_Fever_recurrent = models.BooleanField(default=False)
    fever_type=[('Low grade','Low grade'),('Moderate grade','Moderate grade'),('High grade','High grade')]
    mt_Fever_type= models.CharField(max_length=30, blank=True, null=True, choices=fever_type)

    # mt_Fever_Low_grade = models.BooleanField(default=False)
    # mt_Fever_Moderate_grade = models.BooleanField(default=False)
    # mt_Fever_High_grade = models.BooleanField(default=False)

    mt_Lethargy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_Seizures = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Seizures_Partial = models.BooleanField(default=False)
    mt_Seizures_generalized = models.BooleanField(default=False)
    mt_Seizures_myoclonic = models.BooleanField(default=False)
    mt_Seizures_other = models.BooleanField(default=False)

    mt_Seizures_frequency = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_AntiConvulsant_therapy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AntiConvulsant_Monotherapy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AntiConvulsant_Monotherapy_drug_name = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    mt_AntiConvulsant_Monotherapy_dose = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_AntiConvulsant_Polytherapy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AntiConvulsant_Polytherapy_drug_name = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    mt_AntiConvulsant_Polytherapy_dose = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])

    mt_history_nuroregression= models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_history_nuroregression_text=models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_history_diagnosis= models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_history_diagnosis_text=models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_history_mech_ventilation= models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_history_mech_ventilation_text=models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_history_mech_distention= models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_history_mech_distention_text=models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])


    mt_HistoryPreviousAdmission = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_surgery = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_surgery_specify = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])

    mt_Seizures_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])

    mt_Aversion_sweet_protein = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Excessive_crying = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_Decreased_attention_span = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Speech_disturbances = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Decline_school_performance = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_Clumsiness = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    ultrasound_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not done', 'Not done')]

    mt_Ultrasound = models.CharField(max_length=50, blank=True, null=True, choices=ultrasound_sel)
    mt_Ultrasound_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                                      validators=[MaxLengthValidator(100)])
    mt_History_liver_dysfunction = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_History_liver_dysfunction_trimester_pregnancy = models.CharField(max_length=100, blank=True, null=True,
                                                                        validators=[MaxLengthValidator(100)])
    Polyhydramnios_sel = [('Present', 'Present'), ('Absent', 'Absent')]
    mt_Polyhydramnios = models.CharField(max_length=50, blank=True, null=True, choices=Polyhydramnios_sel)
    mt_Ultrasound_Polyhydramnios = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ultrasound_Oligoamnios = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ultrasound_Skeletal_anomalies = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ultrasound_Hydrops = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_any_other_antenatal_investigation = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])
    delivery_type_sel = [('Cesarean', 'Cesarean'), ('Vaginal', 'Vaginal')]
    mt_Delivery_type = models.CharField(max_length=20, blank=True, null=True, choices=delivery_type_sel)
    mt_Baby_cried_immediately_after_delivery = models.CharField(max_length=10, blank=True, null=True,
                                                                choices=yes_no_sel)
    mt_Resuscitation_required = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Resuscitation_required_specify = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mt_Ventilation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ventilation_CPAP = models.BooleanField(default=False)
    mt_Ventilation_NIV = models.BooleanField(default=False)
    mt_Ventilation_MV = models.BooleanField(default=False)

    mt_NICU_Stay = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Symptomatic_asymptomatic = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Shock = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Shock_catecholamine_sensitive = models.BooleanField(default=False)
    mt_Shock_refractory = models.BooleanField(default=False)
    mt_feeding_issues = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_feeding_issues_Regurgitation_oral_feed = models.BooleanField(default=False)
    mt_feeding_issues_NG_feeding = models.BooleanField(default=False)
    mt_feeding_issues_Parenteral = models.BooleanField(default=False)
    mt_Neonatal_hyperbilurubinemia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Neonatal_hyperbilurubinemia_direct = models.BooleanField(default=False)
    mt_Neonatal_hyperbilurubinemia_indirect = models.BooleanField(default=False)
    mt_Neonatal_hyperbilurubinemia_total_bill_value = models.CharField(max_length=100, blank=True, null=True,
                                                                       validators=[MaxLengthValidator(100)])
    mt_Sepsis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Sepsis_CultureProven = models.BooleanField(default=False)
    mt_Sepsis_Clinical = models.BooleanField(default=False)
    mt_Sepsis_Organism = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_CRRT_PD_required = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    development_milestone_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    mt_EEG_natel = models.CharField(max_length=10, blank=True, null=True, choices=development_milestone_sel)
    mt_EEG_BurstSuppressionPattern_natel = models.BooleanField(blank=True, default=None)
    mt_EEG_Hypsarrythmia_natel = models.BooleanField(blank=True, default=False)
    mt_EEG_GeneralizedSlowing_natel = models.BooleanField(blank=True, default=False)
    mt_EEG_Comb_like_pattern_natel = models.BooleanField(blank=True, default=False)

    mt_facial_dysmorphism = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Facial_dysmorphism_upload_file = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    color_sel = [('Normal', 'Normal'), ('Dark', 'Dark'), ('Blond', 'Blond')]
    mt_Skin_Pigmentation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Skin_Pigmentation_Hypopigmentation_diffuse = models.CharField(max_length=10, blank=True, null=True,
                                                                     choices=yes_no_sel)
    mt_Skin_Pigmentation_Hypopigmentation_patchy = models.CharField(max_length=10, blank=True, null=True,
                                                                    choices=yes_no_sel)
    mt_Skin_Pigmentation_Hypopigmentation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hirsutism = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hirsutism_Facial = models.BooleanField(blank=True, default=None)
    mt_Hirsutism_generalised = models.BooleanField(blank=True, default=None)
    mt_Hemoglobinura = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]

    mt_Hyperpigmentation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    diffus_patchy_sel = [('Diffuse', 'Diffuse'), ('Patchy', 'Patchy')]

    mt_Hypopigmentation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hypopigmentation_type = models.CharField(max_length=10, blank=True, null=True, choices=diffus_patchy_sel)
    mt_Excessive_mongolion_spots = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ichthyosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Telengiectasia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Edema = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hydrops = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Inverted_nipples = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_fat_distribution_Lipodystrophy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Encephalopathy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hypotonia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hypertonia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Brisk_reflexes = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AnyOther_TremorJitteriness = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AnyOther_chorea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_AnyOther_athetosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_Hyporeflexia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Opisthotonus = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Other_Abnormal_Movement = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Tremor_chorea_athetosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Gait_abnormalities = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Optic_Nerve_atrophy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Retinal_degeneration = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Cataract = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Squint = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Nystagmus_oculogyria = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Fundus_Abnormal = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    fundus_abnormal_sel = [('Partial optic atrophy', 'Partial optic atrophy'),
                           ('Complete optic atrophy', 'Complete optic atrophy')]
    mt_Fundus_Abnormal_specify = models.CharField(max_length=50, blank=True, null=True, choices=fundus_abnormal_sel)
    mt_cheery_red_spot=models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_cheery_red_spot_specify=models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Murmur = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Congestive_Heart_Failure = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Cardio_myopathy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hepatomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    Consistency_sel = [ ('soft', 'soft'), ('firm', 'firm'),('hard','hard')]
    surface_sel=[ ('smooth', 'smooth'),('nodular', 'nodular'),('granular','granular')]
    margin_sel=[('sharp','sharp'),('rounded','rounded')]

    mt_Consistency = models.CharField(max_length=10, blank=True, null=True, choices=Consistency_sel)
    mt_surface = models.CharField(max_length=10, blank=True, null=True, choices=surface_sel)
    mt_margin = models.CharField(max_length=10, blank=True, null=True, choices=margin_sel)
    mt_BCM_size = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Span_cm = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Splenomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Splenomegaly_size_cm = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    Done_Not_Done_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    mt_IQ = models.CharField(max_length=10, blank=True, null=True, choices=Done_Not_Done_sel)
    mt_IQ_value = models.IntegerField(blank=True, null=True)
    mt_DQ = models.CharField(max_length=10, blank=True, null=True, choices=Done_Not_Done_sel)
    mt_DQ_value = models.IntegerField(blank=True, null=True)
    mt_Any_other_findings = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])

    mt_Hb_gm_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_wbc_tc_ul = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_wbc_dc_perc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Absolut_Neutrophil_count_mm_3 = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])
    mt_Platelet_count_ul = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Acanthocytes = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_S_calcium_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_S_phosphorous_mg_dl = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    mt_S_alkaline_phosphate_UI = models.CharField(max_length=100, blank=True, null=True,
                                                  validators=[MaxLengthValidator(100)])
    mt_S_acid_phosphatase_U_L = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    mt_CPK_U_L_total = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_MM_MB = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Blood_Urea = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Blood_creatinine_mg_dl = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    mt_Serum_sodium_meq_l = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_Serum_potassium_meq_l = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    mt_Total_protein_g_dl = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_Serum_albumin_g_dl = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_SGPT_IU_L = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_SGOT_IU_L = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_PT_sec = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_APTT_sec = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_TSB_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_DSB_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_IRON_IU_L = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_TIBC_IU_L = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Lactate_mmol_l = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Uric_acid_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Blood_sugar_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_HbA1C_per = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Total_Cholesterol_mg_dl = models.CharField(max_length=100, blank=True, null=True,
                                                  validators=[MaxLengthValidator(100)])
    mt_TGs_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_HDL_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_LDL_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_VLDL_mg_dl = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_Homocysteine_uml_l = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_Prolactin_ng_ml = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not done', 'Not done')]
    mt_Ultrasonography = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    ultrasonography_sel = [('Liver', 'Liver'), ('Kidney', 'Kidney'), ('Spleen', 'Spleen'),
                           ('Any adenoma', 'Any adenoma'), ('Any renal cysts', 'Any renal cysts')]
    mt_Ultrasonography_abnormal_speicfy = models.CharField(max_length=100, null=True, blank=True,
                                                           choices=ultrasonography_sel)
    mt_Ultrasonography_abnormal_Liver = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mt_Ultrasonography_abnormal_Kidney = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_Ultrasonography_abnormal_Spleen = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mt_Ultrasonography_abnormal_AnyAdenoma = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Ultrasonography_abnormal_RenalCysts = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)

    mt_Skeletal_survey = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_Skeletal_survey_Rickets = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Skeletal_survey_DysostosisMultiplex = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Skeletal_survey_ShortLimbs = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Skeletal_survey_SpineAbnormalities = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Skeletal_survey_ChondrodyplasiaPuncta = models.CharField(max_length=10, blank=True, null=True,
                                                                choices=yes_no_sel)

    # mt_Neuroimaging = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_ctc_scan = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_ctc_scan_ThalamusHypointesity = models.BooleanField(default=False)
    mt_ctc_scan_calcification = models.BooleanField(default=False)
    mt_ctc_scan_ventriculomegaly = models.BooleanField(default=False)
    mt_ctc_scan_cerebralAtrophy = models.BooleanField(default=False)
    mt_ctc_scan_infarct = models.BooleanField(default=False)
    mt_ctc_scan_hemorrhage = models.BooleanField(default=False)
    mt_ctc_scan_cerebraledema = models.BooleanField(default=False)
    mt_ctc_scan_cysts = models.BooleanField(default=False)

    # mt_mri_brain = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_mri_brain_status = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_mri_brain_corticalAtrophy = models.BooleanField(default=False)
    mt_mri_brain_cerebellarAtrophy = models.BooleanField(default=False)
    mt_mri_brain_ventriculomegaly = models.BooleanField(default=False)
    mt_mri_brain_basalGangliaHypo = models.BooleanField(default=False)
    mt_mri_brain_hyperintensity = models.BooleanField(default=False)
    mt_mri_brain_deepGrayMatterHyperintensity = models.BooleanField(default=False)
    mt_mri_brain_thalamicHypo = models.BooleanField(default=False)
    mt_mri_brain_demyelinationDysmyelination = models.BooleanField(default=False)
    mt_mri_brain_cerebralEdema = models.BooleanField(default=False)
    mt_mri_brain_cysts = models.BooleanField(default=False)
    mt_mri_brain_infarct = models.BooleanField(default=False)
    mt_mri_brain_hemorrhage = models.BooleanField(default=False)
    mt_mri_brain_other=models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])

    mri_brain_sel = [('cerebral atrophy', 'cerebral atrophy'), ('hydrocephalus', 'hydrocephalus'),
                     ('basal ganglia hypo', 'basal ganglia hypo'),
                     ('hyperintensity', 'hyperintensity'), ('hyperintensity', 'hyperintensity'),
                     ('demyelination or dysmyelination', 'demyelination or dysmyelination'),
                     ('any other', 'any other')]
    # mt_mri_brain_abnormal_specify = models.CharField(max_length=100, null=True, blank=True, choices=mri_brain_sel)
    mt_mrs_done = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_mrs_LactatePeak = models.BooleanField(default=False)
    mt_mrs_NAAPeak = models.BooleanField(default=False)
    mt_mrs_LowCreatininePeak = models.BooleanField(default=False)
    mt_mrs_CholinePeak = models.BooleanField(default=False)
    # mt_mrs_done_status = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)

    mt_echocardiography = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_echocardiography_DialtedCardiomyopathy = models.BooleanField(default=False)
    mt_echocardiography_hypertrophicCardiomyopathy = models.BooleanField(default=False)
    mt_echocardiography_valvularAbnormality = models.BooleanField(default=False)
    mt_echocardiography_structuralDefects = models.BooleanField(default=False)

    mt_echocardiography_SpecifyStructuralDefect = models.CharField(max_length=100, blank=True, null=True,
                                                                   validators=[MaxLengthValidator(100)])
    mt_echocardiography_EjectionFraction = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])

    # mt_echocardiography_status = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)

    mt_eeg = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_eeg_BurstSuppressionPattern = models.BooleanField(blank=True, default=None)
    mt_eeg_Hypsarrythmia = models.BooleanField(blank=True, default=None)
    mt_eeg_GeneralizedSlowing = models.BooleanField(blank=True, default=None)
    mt_eeg_CombLikePattern = models.BooleanField(blank=True, default=None)
    # mt_eeg_status = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_sel)
    mt_eeg_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    mt_ocular_examination_slit = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    normal_abnormal_not_done_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    mt_veps = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_not_done_sel)
    mt_veps_abnormal_latency = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    mt_erg = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_not_done_sel)
    mt_erg_abnormal_specify = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # mt_latency_prolonged = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_OAE_BERA = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_not_done_sel)
    mt_OAE_BERA_Unilateral = models.BooleanField(default=False)
    mt_OAE_BERA_bilateral = models.BooleanField(default=False)
    mt_OAE_BERA_mild = models.BooleanField(default=False)
    mt_OAE_BERA_moderate = models.BooleanField(default=False)
    mt_OAE_BERA_severe = models.BooleanField(default=False)
    mt_OAE_BERA_profoundHearingLoss = models.BooleanField(default=False)

    # mt_beras_audiogram_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
    #                                                 validators=[MaxLengthValidator(100)])
    mt_nerve_conduction_study = models.CharField(max_length=10, blank=True, null=True,
                                                 choices=normal_abnormal_not_done_sel)
    mt_nerve_conduction_study_motor = models.BooleanField(default=False)
    mt_nerve_conduction_study_sensory = models.BooleanField(default=False)
    mt_nerve_conduction_study_mixed = models.BooleanField(default=False)
    mt_nerve_conduction_study_upperLimb = models.BooleanField(default=False)
    mt_nerve_conduction_study_lowerLimb = models.BooleanField(default=False)
    mt_nerve_conduction_study_reducedMUAPAmplitude = models.BooleanField(default=False)
    mt_nerve_conduction_study_shortMUAPDuration = models.BooleanField(default=False)
    mt_nerve_conduction_study_decreasedConductionVelocity = models.BooleanField(default=False)
    mt_nerve_conduction_study_increasedDistalLatency = models.BooleanField(default=False)
    mt_nerve_conduction_study_decreasedSNAP = models.BooleanField(default=False)
    mt_nerve_conduction_study_increasedFwaveLatency = models.BooleanField(default=False)

    mt_Any_other_investigations = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])

    mt_muscle_biopsy = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])

    mt_blood_gas_metabolism_acidosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    blood_gas_metabolism_acidosis_sel = [('PH', 'PH'), ('HCO3', 'HCO3'), ('Anion gap', 'Anion gap')]
    mt_blood_gas_metabolism_acidosis_PH = models.CharField(max_length=100, blank=True, null=True,
                                                           validators=[MaxLengthValidator(100)])
    mt_blood_gas_metabolism_acidosis_HCO_3 = models.CharField(max_length=100, blank=True, null=True,
                                                              validators=[MaxLengthValidator(100)])
    mt_blood_gas_metabolism_acidosis_Anion_gap = models.CharField(max_length=100, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    mt_metabolic_alkalosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hyper_ammonemia = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_Hyper_ammonemia_value = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    mt_Hyper_ammonemia_duration = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    mt_high_lactate = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_high_lactate_csf = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_high_lactate_value = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_high_lactate_csf_value = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    normal_abnormal_not_done_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    mt_ief_transferring_pattern_type = models.CharField(max_length=10, blank=True, null=True,
                                                        choices=normal_abnormal_not_done_sel)
    mt_ief_transferring_pattern_type_tpye1 = models.BooleanField(default=False)
    mt_ief_transferring_pattern_type_tpye2 = models.BooleanField(default=False)
    mt_ief_transferring_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])
    present_absent_sel = [('Present', 'Present'), ('Absent', 'Absent'), ('Not Done', 'Not Done')]
    mt_urine_ketones = models.CharField(max_length=10, blank=True, null=True, choices=present_absent_sel)
    mt_urine_ketones_value = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    mt_plasma_ketones = models.CharField(max_length=10, blank=True, null=True, choices=present_absent_sel)
    mt_plasma_ketones_value = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    mt_plasma_ketones_ffa_ratio = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_plasma_ketones_ffa_ratio_value = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mt_tms_primary_analyte = models.CharField(max_length=10, blank=True, null=True,
                                              choices=normal_abnormal_not_done_sel)
    mt_tms_primary_analyte_specify_anlyte = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    mt_tms_primary_analyte_value = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_hplc = models.CharField(max_length=10, blank=True, null=True,
                                              choices=yes_no_sel)
    mt_hplc_specify = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    mt_hplc_value = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_gcms = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_not_done_sel)
    mt_gcms_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    mt_gcms_abnormal_value = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    mt_orotic_acid = models.CharField(max_length=10, blank=True, null=True, choices=present_absent_sel)
    # mt_orotic_acid_specify = models.CharField(max_length=100, blank=True, null=True,
    #                                         validators=[MaxLengthValidator(100)])
    mt_vlcfa = models.CharField(max_length=10, blank=True, null=True, choices=normal_abnormal_not_done_sel)

    mt_vlcfa_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    csf_sel = [('Amino acids', 'Amino acids'), ('Glucose', 'Glucose'), ('Lactate', 'Lactate'), ('Pterin', 'Pterin'),
               ('Neurotransmitter', 'Neurotransmitter'), ('Porphyrins', 'Porphyrins'), ('Purine', 'Purine'),
               ('Pyrimidines', 'Pyrimidines'), ('Others', 'Others')]
    mt_succinyl_acetone_status = models.CharField(max_length=10, blank=True, null=True,
                                                  choices=normal_abnormal_not_done_sel)
    mt_succinyl_acetone_abnormal_specify = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])

    mt_csf = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    mt_csf_other = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    mt_csf_status = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_not_done_sel)
    mt_csf_abnormal_specify_umol_l = models.CharField(max_length=100, blank=True, null=True,
                                                      validators=[MaxLengthValidator(100)])
    mt_csf_abnormal_specify_mg_dl = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    mt_csf_abnormal_specify_ug_l = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_abnormal_specify_nmol_l = models.CharField(max_length=100, blank=True, null=True,
                                                      validators=[MaxLengthValidator(100)])
    mt_enzyme_analusis_lab_name = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    mt_enzyme_analusis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_enzyme_analusis_ref_range = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_enzyme_analusis_normal_control = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_enzyme_analusis_normal_range = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    # <..................................>

    mt_csf_amino_acid=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_glucose=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_lactose=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_protien=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_nurotransonitres=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_porphyrins=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_purine=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_pyrinidies=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_glycine=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    mt_csf_others=models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])


    enzyme_sample=[('Leukocyte','Leukocyte'),('DBS','DBS'),('Blood','Blood'),('Plasma','Plasma'),('Serum','Serum'),('Skin fibroblast','Skin fibroblast')]
    mt_enzyme_analusis_sample_dbs_blood = models.CharField(max_length=100, blank=True, null=True,
                                                           choices=enzyme_sample)
    mt_enzyme_analusis_value = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])

    mt_enzyme_analusis_sample_dbs_blood_date = models.DateField(blank=True, null=True)
    mt_enzyme_analusis_upload_report = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)


    ##### cDNA SEQUENCING PROFILE

    mt_Causative_DNA_sequence_variation = [('done', 'done'), ('not done', 'not done')]
    mt_Causative_DNA_sequence_variat = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    # If_done =
    mt_molecular_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    mt_Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    mt_Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    mt_trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    mt_mul_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mt_mul_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mt_mul_var_sel = [('Novel', 'Novel '),
                      ('Reported', 'Reported')]
    mt_mul_var1 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_var_sel)
    mt_mul_zygo_sel = [('Homozygous', 'Homozygous '),
                       ('Heterozygous', 'Heterozygous'),
                       ('Hemizygous','Hemizygous')]
    mt_mul_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_zygo_sel)
    mt_mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                       ('Likely Pathogenic', 'Likely Pathogenic'),
                       ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    mt_mul_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_vari_sel)
    mt_mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_sel)
    mt_mul_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mt_mul_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mt_mul_var2 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_var_sel)
    mt_mul_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_vari_sel)
    mt_mul_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=mt_mul_zygo_sel)
    mt_father = models.CharField(max_length=100, blank=True, null=True)
    mt_mother = models.CharField(max_length=100, blank=True, null=True)





    dietery_management_sel = [('0-6 months', '0-6 months'), ('6-12 months', '6-12 months'),
                              ('1-5 years', '1-5 years'), ('>5 years', '>5 years'), ]
    mt_dietary_managment = models.CharField(max_length=30, blank=True, null=True, choices=dietery_management_sel)
    mt_dietary_managment_1 = models.BooleanField(default=False)
    mt_dietary_managment_2 = models.BooleanField(default=False)
    mt_dietary_managment_3 = models.BooleanField(default=False)
    mt_dietary_managment_4 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_1 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_2 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_3 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_4 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_5 = models.BooleanField(default=False)
    mt_dietary_managment_type_of_diet_6 = models.BooleanField(default=False)

    mt_special_diet = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_special_diet_specify = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    mt_liver_transplantation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_kidney_transplantation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_heart_transplantation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_lung_transplantation = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_calcium_multivitamin_supplements = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_regular_physiotherapy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_ocular_medication = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_CPAP_BiPAP_sleep_apnea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_other = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                            validators=[MaxLengthValidator(100)])
    mt_any_other_special_drug = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_sel)
    mt_any_other_special_drug_1 = models.BooleanField(default=False)
    mt_any_other_special_drug_2 = models.BooleanField(default=False)
    mt_any_other_special_drug_3 = models.BooleanField(default=False)
    mt_any_other_special_drug_4 = models.BooleanField(default=False)
    mt_any_other_special_drug_5 = models.BooleanField(default=False)
    mt_any_other_special_drug_6 = models.BooleanField(default=False)
    mt_any_other_special_drug_7 = models.BooleanField(default=False)
    mt_any_other_special_drug_8 = models.BooleanField(default=False)
    mt_any_other_special_drug_9 = models.BooleanField(default=False)
    mt_any_other_special_drug_10 = models.BooleanField(default=False)
    mt_any_other_special_drug_11 = models.BooleanField(default=False)
    mt_any_other_special_drug_12 = models.BooleanField(default=False)
    mt_any_other_special_drug_13 = models.BooleanField(default=False)
    mt_any_other_special_drug_14 = models.BooleanField(default=False)
    mt_any_other_special_drug_specify = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])


    # Final Diagnosis

    mt_final_diagno_sel = [('Organic acidemia', 'Organic acidemia'), ('Aminoacidpathies', 'Aminoacidpathies'), ('Urea cycle defects', 'Urea cycle defects'),('Vitamin/cofactor','Vitamin/cofactor'),
                          ('Fatty acid oxidation defects/Carnitine', 'Fatty acid oxidation defects/Carnitine'), ('Metal related', 'Metal related'), ('Carbohydrate disorders','Carbohydrate disorders'),
                           ('Congenital disorder of glycosylation','Congenital disorder of glycosylation'),('Peroxisomal disorder','Peroxisomal disorder'),('Mitochondrial','Mitochondrial'),('Neurotransmitter defects','Neurotransmitter defects'),
                           ('Others','Others')]

    organic_sel=[('Methylmalonic acidemia','Methylmalonic acidemia'),('Propionic acidemia','Propionic acidemia'),('Isovaleric acidemia','Isovaleric acidemia'),('Glutaric acidemia','Glutaric acidemia'),
                 ('others','others')]
    Aminoacidpathies_sel=[('Maple syrup urine disease','Maple syrup urine disease'),(' Tyrosinemia 1',' Tyrosinemia 1'),('Classical Homocystinuria','Classical Homocystinuria'),('Phenylketonuria','Phenylketonuria'),
                          ('Alkaptonuria','Alkaptonuria'),('Others such as serine, asparagine, BCAA kinase','Others such as serine, asparagine, BCAA kinase'),('Others','Others')]

    urea_sel=[('Citrullinemia 1','Citrullinemia 1'),('Citrullinemia II','Citrullinemia II'),('Ornithine transcarbomylase deficiency','Ornithine transcarbomylase deficiency'),('ASL deficiency','ASL deficiency'),
              ('Others (NAGS, CPS, HHH, OAT, CAVA, LPI, etc)','Others (NAGS, CPS, HHH, OAT, CAVA, LPI, etc)')]
    vitamin_sel=[('Cobalamin disorder','Cobalamin disorder'),('Folate','Folate'),('Biotin','Biotin'),('Pyridoxine','Pyridoxine'),('Others','Others')]

    fatty_sel=[('MCAD','MCAD'),('LCHAD','LCHAD'),('Others','Others')]

    metal_sel=[('Wilson disease','Wilson disease'),('Menke Kinky hair disease','Menke Kinky hair disease'),('Others','Others')]
    Carbohydrate_sel=[('Classical Galactosemia ','Classical Galactosemia '),('Herediatry Fructose intolerance','Herediatry Fructose intolerance'),('Fructose 1,6 bisphosphatase deficiency ','Fructose 1,6 bisphosphatase deficiency '),
                      ('Glycogen storage disorders','Glycogen storage disorders')]
    mitochondrial_sel=[('Nuclear','Nuclear'),('mitochondrial ','mitochondrial'),('Others','Others')]

    Neurotransmitter_sel=[('Pterin disorders','Pterin disorders'),('Tyrosine Hydroxylase Def','Tyrosine Hydroxylase Def'),('Others','Others')]

    Carbohydrate_sub3_sel=[('1a','1a'),('1b','1b'),('III','III'),('IV','IV'),('VI','VI'),('VII','VII'),('IX','IX')]



    mt_Final_Diagnosis = models.CharField(max_length=50, blank=True, null=True, choices=mt_final_diagno_sel)

    organic_cat=models.CharField(max_length=50, blank=True, null=True, choices=organic_sel)
    organic_cat_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    aminoacidpathies_cat=models.CharField(max_length=50, blank=True, null=True, choices=Aminoacidpathies_sel)
    aminoacidpathies_cat_BCAA=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    aminoacidpathies_cat_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    urea_cat=models.CharField(max_length=50, blank=True, null=True, choices=urea_sel)
    urea_cat_NAGS = models.CharField(max_length=100, blank=True, null=True,
                                      validators=[MaxLengthValidator(100)])
    urea_cat_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    vitamin_cat=models.CharField(max_length=50, blank=True, null=True, choices=vitamin_sel)
    vitamin_cobalamin=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    vitamin_folate=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    vitamin_biotin=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    vitamin_pyridoxine=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    vitamin_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    fatty_cat=models.CharField(max_length=50, blank=True, null=True, choices=fatty_sel)
    fatty_cat_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    metal_cat=models.CharField(max_length=50, blank=True, null=True, choices=metal_sel)
    metal_cat_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    carbohydrate_cat=models.CharField(max_length=50, blank=True, null=True, choices=Carbohydrate_sel)
    Carbohydrate_sub3=models.CharField(max_length=50, blank=True, null=True, choices=Carbohydrate_sub3_sel)
    Congenital_disorder= models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    Peroxisomal_disorder_specify=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    mitochondrial_cat=models.CharField(max_length=50, blank=True, null=True, choices=mitochondrial_sel)
    mitochondrial_nuclear=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    mitochondrial_mitochondrial=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    mitochondrial_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    Neurotransmitter_cat=models.CharField(max_length=50, blank=True, null=True, choices=Neurotransmitter_sel)
    Neurotransmitter_pterin=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    Neurotransmitter_tyrosine=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    Neurotransmitter_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])

    mt_diag_other=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])



    # Final Outcome
    mt_final_sel = [('Death', 'Death'), ('Alive', 'Alive'), ('Follow up required', 'Follow up required'),
                    ('Lost to follow up', 'Lost to follow up'), ('Unknown', 'Unknown')]
    mt_filled_by_deo_name = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    mt_clinician_name = models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    mt_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mt_date_filled = models.DateField(null=True, blank=True)

    mt_Final_Outcome = models.CharField(max_length=50, blank=True, null=True, choices=mt_final_sel)
    mt_death_cause = models.CharField(max_length=50, blank=True, null=True)
    mt_age_timedeath = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.pk)

