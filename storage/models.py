# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator
# Create your models here.



class profile_storage(models.Model):
    status_sel = [('Yes', 'Yes'), ('No', 'No')]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    sd_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sd_date_of_records = models.DateField(blank=True, null=True)
    sd_date_of_clinical_exam = models.DateField(blank=True, null=True)
    sd_date_of_birth = models.DateField( null=True)
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'), ('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    sd_paitent_id_yes_no = models.CharField(max_length=100,  null=True, choices=status_sel)
    sd_paitent_id = models.CharField(max_length=100,blank=True,  null=True, choices=id_sel)
    sd_patient_id_no = models.CharField(max_length=100, unique=True,blank=True, null=True, validators=[MaxLengthValidator(100)])
    sd_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sd_Patient_name = models.CharField(max_length=100, null=True, blank=True,validators=[MaxLengthValidator(100)])
    sd_Father_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Mother_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    #sd_Patient_aadhaar_num = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(20)])
    sd_Father_mother_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    sd_Father_mother_id_no =models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    #sd_Mother_aadhaar_num = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(20)])
    sd_permanent_addr = models.CharField(max_length=500, null=True, blank=True, validators=[MaxLengthValidator(500)])
    sd_state = models.ForeignKey(State, null=True,  on_delete=models.CASCADE)
    sd_district = models.ForeignKey(District, null=True,  on_delete=models.CASCADE)
    sd_city_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_country_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_dob = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    sd_age = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(10)])
    sd_Patient_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    sd_Father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    sd_Mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    sd_land_line_number = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(10)])
    sd_email = models.EmailField(max_length=300, blank=True, null=True)
    religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                    ('Others', 'Others')]
    sd_religion = models.CharField(max_length=100, null=True, blank=True, choices=religion_sel)
    religion_other = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    cast_sel = [('ST', 'ST'), ('SC', 'SC'), ('OBC', 'OBC'), ('General', 'General'), ('Others', 'Others')]
    sd_cast = models.CharField(max_length=100, null=True, blank=True, choices=cast_sel)
    cast_other = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    referred_status_sel = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                           ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    sd_referred_status = models.CharField(max_length=100, null=True, blank=True, choices=referred_status_sel)
    sd_referred_by = models.CharField(max_length=100, null=True, blank=True, )
    sd_referred_by_desc = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    sd_gender = models.CharField(max_length=100, null=True, blank=True, choices=gender_sel)

    sd_consent_given = models.CharField(max_length=10, null=True,  choices=status_sel)
    sd_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    sd_assent_given = models.CharField(max_length=10,  null=True,  choices=status_sel)
    sd_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    sd_hospital_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_hospital_reg_no = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_storage', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_storage', on_delete=models.CASCADE)

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
            super(profile_storage, self).save(*args, **kwargs)
            self.sd_icmr_unique_no = str('Storage/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_storage, self).save(*args, **kwargs)


class demographic_storage(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_storage, null=True, related_name='patient_storage',blank=True, on_delete=models.CASCADE)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    yes_no123 = [('1', 'Yes'), ('0', 'No')]
    Patient_edu_sel = [('No formal education', 'No formal education'),
                       ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                       ('Secondary school', 'Secondary school'),
                       ('College/Pre-university', 'College/Pre-university'),
                       ('Post graduate degree ', 'Post graduate degree ')]
    sd_Patient_education = models.CharField(max_length=100, null=True, blank=True, choices=Patient_edu_sel)
    Patient_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                              ('Private Service', 'Private Service'), ('Housewife', 'Housewife'),
                              ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                              ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    sd_Patient_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Patient_occupation_sel)
    Father_edu_sel = [('No formal education', 'No formal education'),
                      ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                      ('Secondary school', 'Secondary school'),
                      ('College/Pre-university', 'College/Pre-university'),
                      ('Post graduate degree ', 'Post graduate degree ')]
    sd_Father_education = models.CharField(max_length=100, null=True, blank=True, choices=Father_edu_sel)
    Father_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                             ('Private Service', 'Private Service'), ('Housewife', 'Housewife'),
                             ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                             ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    sd_Father_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Father_occupation_sel)
    Mother_edu_sel = [('No formal education', 'No formal education'),
                      ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                      ('Secondary school', 'Secondary school'),
                      ('College/Pre-university', 'College/Pre-university'),
                      ('Post graduate degree ', 'Post graduate degree ')]
    sd_Mother_education = models.CharField(max_length=100, null=True, blank=True, choices=Mother_edu_sel)
    Mother_occupation_sel = [('Unemployed', 'Unemployed'), ('Government Service', 'Government Service'),
                             ('Private Service', 'Private Service'), ('Housewife', 'Housewife'),
                             ('Agriculture', 'Agriculture'), ('Business', 'Business'), ('Daily labor', 'Daily labor'),
                             ('Student', 'Student'), ('Others (Specify)', 'Others (Specify)'), ]
    sd_Mother_occupation = models.CharField(max_length=200, null=True, blank=True, choices=Mother_occupation_sel)
    Monthly_family_income_sel = [('> 126,360', '> 126,360)'),
                                 ('63,182 â€“ 126,356)', '63,182 â€“ 126,356)'),
                                 ('47,266 â€“ 63,178', '47,266 â€“ 63,178'),
                                 ('31,591 - 47,262', '31,591 - 47,262'),
                                 ('18,953 - 31,589', '18,953 - 31,589'),
                                 ('6,327 - 18,949', '6,327 - 18,949'),
                                 ('< 6,323', '< 6,323')]
    sd_Monthly_family_income = models.CharField(max_length=200, null=True, blank=True,
                                                choices=Monthly_family_income_sel)
    sd_weight_patient = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_weight_percentile = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_weight_SD = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_height_patient = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_height_percentile = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_height_SD = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_Head_circumference_patient = models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_Head_circumference_percentile =models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_Head_circumference_sd =models.CharField(max_length=50, null=True, validators=[MaxLengthValidator(50)])
    sd_Age_at_onset_of_symptoms_year = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_onset_of_symptoms_month = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_onset_of_symptoms_day = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_onset_of_symptoms_Intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=yes_no123)
    sd_Age_at_presentation_year = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_presentation_month = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_presentation_day = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_presentation_Intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=yes_no123)
    sd_Age_at_diagnosis_year = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_diagnosis_month = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_diagnosis_day = models.PositiveSmallIntegerField(blank=True, null=True)
    sd_Age_at_diagnosis_Intrauterine = models.CharField(max_length=10, blank=True, null=True, choices=yes_no123)
    sd_Pedigree_to_be_uploaded = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True, blank=True, )
    sd_positive_family_history = models.CharField(max_length=100, null=True, blank=True,
                                                  choices=yes_no, )
    sd_family_history_specify = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    sd_Consanguinity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no, )
    sd_Consanguinity_specify = models.CharField(max_length=200, null=True, blank=True, )
    Antenatal_Ultrasound_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    sd_Antenatal_Ultrasound = models.CharField(max_length=100, null=True, blank=True,
                                               choices=Antenatal_Ultrasound_sel)
    sd_if_other_specify = models.CharField(max_length=200, null=True, blank=True, )
    Antenatal_Polyhydramnios_Ultrasound_sel = [('Present', 'Present'), ('Absent', 'Absent')]
    sd_Polyhydramnios = models.CharField(max_length=100, null=True, blank=True,
                                         choices=Antenatal_Polyhydramnios_Ultrasound_sel)
    Antenatal_Hydrops_sel = [('Present', 'Present'), ('Absent', 'Absent'),  ]
    sd_Hydrops = models.CharField(max_length=100, null=True, blank=True,
                                  choices=Antenatal_Hydrops_sel)
    sd_Hydrops_specify = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    Delivery_sel = [('cesarean', 'cesarean'), ('Vaginal', 'Vaginal')]
    sd_Type_of_delivery = models.CharField(max_length=100, null=True, blank=True,
                                           choices=Delivery_sel)
    sd_Baby_cried_immediately_after_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                                choices=yes_no)
    sd_Resuscitation_required = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Resuscitation_specify = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Resuscitation_ventilation = models.CharField(max_length=100, null=True, blank=True,
                                                    choices=yes_no)
    sd_NICU_stay = models.CharField(max_length=100, null=True, blank=True,
                                    choices=yes_no)
    sd_NICU_specify = models.CharField(max_length=200, null=True, blank=True, )
    sd_NICU_stay_other = models.CharField(max_length=200, null=True, blank=True, )
    sd_Birth_weight = models.FloatField(blank=True, null=True)
    Milestone_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    sd_Development_milestones = models.CharField(max_length=100, null=True, blank=True, choices=Milestone_sel)
    sd_delayed_Motor = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_delayed_Global = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_delayed_Cognitive = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Abdominal_distentesion = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Increasing_pallor = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Bleeding = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Developmental_Delay = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Neuroregression = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Behavioral_problems = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hyperactivity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Psychomotor_arrest = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Seizures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Seizures_sel = [('GTCS', 'GTCS'),
                    ('Partial', 'Partial'), ('Myoclonic', 'Myoclonic'),
                    ('Complex partial ', 'Complex partial ')]
    sd_Seizures_specify = models.CharField(max_length=100, null=True, blank=True, choices=Seizures_sel)
    sd_On_some_antiepileptics_drugs = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    antiepileptics_drugs_sel = [('Phenobarb', 'Phenobarb'),
                                ('Phenytoin', 'Phenytoin'), ('Levetiracetam', 'Levetiracetam'),
                                ('valproic acid', 'valproic acid'),
                                ('other specify', 'other specify')]
    sd_antiepileptics_specify = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])
    sd_Decreased_attention_span = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Stiffness = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Poor_feeding = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Choking = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Loss_of_Vision = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hearing_loss = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Recurrent_persistent_upper_respiratory_symptoms = models.CharField(max_length=100, null=True, blank=True,
                                                                          choices=yes_no)
    sd_Fractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Gait_disturbances = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Speech_disturbances = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Any_surgery = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Any_surgery_sel = [('Splenectomy', 'Splenectomy'),
                       ('Hernia', 'Hernia'),
                       ('other', 'other')]
    sd_Surgery = models.CharField(max_length=200, null=True, blank=True, choices=Any_surgery_sel)
    sd_Surgery_age_history= models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])
    sd_Surgery_other_specify= models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])
    status_sel = [('Ambulatory', 'Ambulatory'),
                  ('Wheel chair Bound', 'Wheel chair Bound'), ('Bed ridden', 'Bed ridden'),
                  ('Assisted motor device','Assisted motor device')]
    sd_Functional_status = models.CharField(max_length=200, null=True, blank=True, choices=status_sel)

    sd_Head_shape_Abnormal = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Mongolian_spots_at_back = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Ichthyosis = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Stiff_Thick_skin = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Telangiectasia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Edema = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hydrops1 = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Angiokeratomas = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Exaggerated_startle_reflex = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hypotonia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hypertonia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Brisk_reflexes = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hyporeflexia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Gait_abnormalities = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Opisthotonus = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Dystonia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Signs_of_raised_ICT = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)

    sd_IQ_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    sd_IQ_done = models.CharField(max_length=100, null=True, blank=True, choices=sd_IQ_sel)
    sd_IQ_done_value = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])
    sd_DQ_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    sd_DQ_done = models.CharField(max_length=100, null=True, blank=True, choices=sd_DQ_sel)
    sd_DQ_done_value = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])

    sd_Oculomotor_apraxia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Saccades = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Corneal_clouding_opacity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Glaucoma = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Optic_Nerve_atrophy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Retinal_degeneration_pigmentation = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Cataract = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Squint = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Nystagmus = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Supranuclear_gaze_palsy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Fundus_abnormal = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Cherry_Red_Spot = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    sd_Pigmentary_changes = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    sd_Cardiovascular_Congestive_Heart_Failure = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Cardiovascular_Cor_Pulomonale = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Respiratory_Enlarged_tonsils = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Respiratory_Sleep_apnea = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Respiratory_Reactive_Airway_Disease = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Respiratory_Dyspnea = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Gastrointestinal_Hepatomegaly = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hepatomegaly = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    # Hepatomegaly_sel = [('Size BCM', 'Size BCM'),
    #                     ('Span (cm)', 'Span (cm)')]
    sd_if_yes_size_bcm = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_if_yes_span=models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Consistency = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Consistency_sel = [('Soft', 'Soft'),
                       ('Hard', 'Hard'),
                       ('Firm', 'Firm')]
    surface_sel=[('Smooth','Smooth'),('Nodular','Nodular'),('Granular','Granular')]
    margin_sel=[('Sharp','Sharp'),('Rounded','Rounded')]
    sd_if_yes_Consistency = models.CharField(max_length=200, null=True, blank=True, choices=Consistency_sel)
    sd_if_yes_surface = models.CharField(max_length=200, null=True, blank=True, choices=surface_sel)
    sd_if_yes_margin = models.CharField(max_length=200, null=True, blank=True, choices=margin_sel)
    sd_Splenomegaly = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    # Splenomegaly_sel = [('Size BCM', 'Size BCM'),
    #                     ('Span (cm)', 'Span (cm)')]
    sd_if_Splenomegaly = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(100)])

    sd_Joint_stiffness = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Scoliosis = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Kyphosis_Gibbus = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Genu_valgum = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Pes_Cavus = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Toe_Walking = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Hb = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_WBC_Total_Count = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Platelet_Count = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_WBC_Differnetial = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Absolute_neutrophil_counts = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    sd_PT_sec = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_APTT_sec = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_S_calcium_mg_dl = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_S_Phosphorus_mg_dl = models.CharField(max_length=100, null=True, blank=True,
                                             validators=[MaxLengthValidator(100)])
    sd_S_alkaline_phosphatise_IU = models.CharField(max_length=100, null=True, blank=True,
                                                    validators=[MaxLengthValidator(100)])
    sd_S_Acid_phosphatise_IU = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    sd_S_Total_protein_g_dl = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])
    sd_S_Serum_albumin_g_dl = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])
    sd_SGPT_IU = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_SGOT_IU = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_GGT = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_IRON_mg_dl = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_TIBC_mg_dl = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Vit_B12_pg_ml = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Vit_D_ng_ml = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_PTH_ng_ml = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_Radiological_Ultrasonography = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Ultrasonography_sel = [('Normal', 'Normal'),
                           ('Abnormal', 'Abnormal'),
                           ('Not Done', 'Not Done')]
    sd_rad_ultrasonography = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_rad_ultrasono_type = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    sd_rad_ultra_finding_ab_specify = models.CharField(max_length=50, blank=True, null=True,
                                                       validators=[MaxLengthValidator(50)])
    sd_rad_liversize = models.FloatField(blank=True, null=True)
    sd_rad_liverEchotexture = models.CharField(max_length=10, blank=True, null=True, )
    sd_rad_Kidney = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_rad_hepatic = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_rad_kidney_size = models.IntegerField(blank=True, null=True)
    sd_rad_spleen_size = models.FloatField(blank=True, null=True)
    sd_rad_Echotexture = models.FloatField(blank=True, null=True)
    sd_rad_lymphnodes_size = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_rad_portal_vien_dia = models.IntegerField(blank=True, null=True)
    sd_rad_adenoma = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_renal_par_pathalogy = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_renal_par_pathalogy_specify = models.CharField(max_length=50, blank=True, null=True,
                                                      validators=[MaxLengthValidator(50)])
    sd_nephrocalcinosis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_pancreatitis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_cholethiasis = models.CharField(max_length=10, blank=True, null=True, choices=yes_no)
    sd_xray_bone_age = models.CharField(max_length=50, blank=True, null=True,
                                                      validators=[MaxLengthValidator(50)])

    Echotexture_sel = [('Normal', 'Normal'), ('coarse', 'coarse')]
    sd_Echotexture = models.CharField(max_length=200, null=True, blank=True, choices=Echotexture_sel)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_Lymph_nodes_enlarged = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Portal_vein_diameter_sel = [('> 10 mm', '> 10 mm)'),
                                ('< 10 mm', '< 10 mm')]
    sd_Portal_vein_diameter = models.CharField(max_length=200, null=True, blank=True, choices=Portal_vein_diameter_sel)
    sd_Any_adrenal_calcifications = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_Skeletal_survey = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Erlenmeyer_flask_deformity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Osteopenia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Skeletal_Scoliosis = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Dysostosis_multiplex = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Dexa_Z_Score = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    sd_Neuroimaging_CT_scan = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    CT_scan_sel = [('Normal', 'Normal'),
                   ('Abnormal', 'Abnormal')]
    sd_CT_scan = models.CharField(max_length=200, null=True, blank=True, choices=CT_scan_sel)
    sd_CT_scan_specify=models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    MRI_Brain_sel = [('Normal', 'Normal'),
                     ('Abnormal', 'Abnormal')]
    sd_MRI_Brain = models.CharField(max_length=200, null=True, blank=True, choices=MRI_Brain_sel)
    if_abnormal_sel = [('cerebral atrophy', 'cerebral atrophy'),
                       ('hydrocephalus', 'hydrocephalus'),
                       ('basal ganglia hypo', 'basal ganglia hypo'),
                       ('hyperintensity', 'hyperintensity'),
                       ('thalamic', 'thalamic'),
                       ('dysmyelination', 'dysmyelination'),
                       ('Any other ', 'Any other ')]
    cerebral_atrophy=models.BooleanField(default=False)
    hydrocephalus=models.BooleanField(default=False)
    basal_ganglia_hypo=models.BooleanField(default=False)
    hyperintensity=models.BooleanField(default=False)
    thalamic=models.BooleanField(default=False)
    dysmyelination=models.BooleanField(default=False)
    Any_other_MRI=models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    sd_abnormal = models.CharField(max_length=200, null=True, blank=True, choices=if_abnormal_sel)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_MRI_abdomen = models.CharField(max_length=20, null=True, blank=True, choices=sd_DQ_sel)
    sd_Liver_volume = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Spleen_volume = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Gaucher_related_nodules = models.CharField(max_length=100, null=True, blank=True,
                                                  validators=[MaxLengthValidator(100)])
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_MRI_Spine_limbs_pelvis = models.CharField(max_length=20, null=True, blank=True, choices=sd_DQ_sel)
    sd_Osteonecrosis= models.BooleanField(default=False)
    sd_Compression_spine_deformity_fractures= models.BooleanField(default=False)
    sd_Marrow_infiltration= models.BooleanField(default=False)
    sd_marrow_Any_other= models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    # sd_Osteonecrosis = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    # sd_Compression_spine_deformity_fractures = models.CharField(max_length=100, null=True, blank=True,
    #                                                             validators=[MaxLengthValidator(100)])
    # sd_Marrow_infiltration = models.CharField(max_length=100, null=True, blank=True,
    #                                           validators=[MaxLengthValidator(100)])
    # sd_marrow_Any_other = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    Pulmonary_function_test_sel = [('Normal', 'Normal'),
                                   ('Restrictive', 'Restrictive'),
                                   ('Obstructive', 'Obstructive'),('Not done','Not done')]
    sd_Pulmonary_function_test = models.CharField(max_length=200, null=True, blank=True,
                                                  choices=Pulmonary_function_test_sel)
    sd_sitting_FEV1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_sittingFVC = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Supine_FEV1 = models.CharField(max_length=100, null=True, blank=True,
                                                      validators=[MaxLengthValidator(100)])
    sd_SupineFVC = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    Echocardiography_sel = [('Normal', 'Normal'),
                            ('Abnormal', 'Abnormal'),
                            ('Not done', 'Not done')]
    sd_Echocardiography_test = models.CharField(max_length=200, null=True, blank=True, choices=Echocardiography_sel)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_Specify_findings_Cardiomyopathy = models.CharField(max_length=100, null=True, blank=True,
                                                          validators=[MaxLengthValidator(100)])
    Cardiomyopathy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Cardiomyopathy_sel = [('Dilated', 'Dilated'),
                          ('Hypertrophic', 'Hypertrophic')]
    sd_Cardiomyopathy = models.CharField(max_length=200, null=True, blank=True, choices=Cardiomyopathy_sel)
    sd_Mention_LVMI = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    sd_Valvular_involvement = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Valvular_Stenosis_sel = [('mitral', 'mitral'),
                             ('tricuspid', 'tricuspid'),
                             ('aortic', 'aortic'),
                             ('pulmonary', 'pulmonary')]
    Valvular_Stenosis_mitral=models.BooleanField(default=False)
    Valvular_Stenosis_tricuspid=models.BooleanField(default=False)
    Valvular_Stenosis_aortic=models.BooleanField(default=False)
    Valvular_Stenosis_pulmonary=models.BooleanField(default=False)
    sd_Valvular_Stenosis = models.CharField(max_length=200, null=True, blank=True, choices=Valvular_Stenosis_sel)
    Valvular_Regurgitation_sel = [('mitral', 'mitral'),
                                  ('tricuspid', 'tricuspid'),
                                  ('aortic', 'aortic'),
                                  ('pulmonary', 'pulmonary')]
    sd_Valvular_Regurgitation = models.CharField(max_length=200, null=True, blank=True,
                                                 choices=yes_no)
    Valvular_Regurgitation_mitral = models.BooleanField(default=False)
    Valvular_Regurgitation_tricuspid = models.BooleanField(default=False)
    Valvular_Regurgitation_aortic = models.BooleanField(default=False)
    Valvular_Regurgitation_pulmonary = models.BooleanField(default=False)
    sd_Ejection_fraction = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    EEG_sel = [('Normal', 'Normal'),
               ('Abnormal', 'Abnormal'),
               ('Not done', 'Not done')]
    sd_EEG = models.CharField(max_length=200, null=True, blank=True, choices=EEG_sel)
    sd_EEG_specify_Findings = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])
    Sleep_Studies_sel = [('Normal', 'Normal'),
                         ('Abnormal', 'Abnormal'),
                         ('Not done', 'Not done')]
    sd_Sleep_Studies = models.CharField(max_length=200, null=True, blank=True, choices=Sleep_Studies_sel)
    sd_Sleep_Studies_Findings = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    sd_SLIT_lamp_examination = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])


    Opthalmological_Examination_sel = [('Normal', 'Normal'),
                                       ('Abnormal', 'Abnormal'),
                                       ('Not done', 'Not done')]
    slit_sel=[('Present','Present'),('Absent','Absent')]
    sd_VEP = models.CharField(max_length=20, null=True, blank=True, choices=Opthalmological_Examination_sel)
    sd_ved_specify=models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    sd_Opthalmological_Examination = models.CharField(max_length=200, null=True, blank=True,
                                                      choices=Opthalmological_Examination_sel)
    sd_Describe_if_abnormal = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])

    sd_SLIT_Lamp = models.CharField(max_length=20, null=True, blank=True, choices=slit_sel)
    BERA_Audiogram_sel = [('Conductive Hearing loss', 'Conductive Hearing loss'),
                          ('Sensorineural Hearing loss', 'Sensorineural Hearing loss'),('Normal Hearing','Normal Hearing')]
    sd_BERA_Audiogram = models.CharField(max_length=200, null=True, blank=True, choices=BERA_Audiogram_sel)
    sd_BERA_Describe_if_abnormal = models.CharField(max_length=100, null=True, blank=True,
                                                    validators=[MaxLengthValidator(100)])

    Servirity_sel = [('Mild', 'Mild'),
                     ('Mod', 'Mod'),
                     ('Severe', 'Severe'),
                     ('Profound', 'Profound')]
    sd_Servirity = models.CharField(max_length=200, null=True, blank=True, choices=Servirity_sel)
    Unilat_bilat_sel = [('Unilateral', 'Unilateral'),
                        ('Bilateral', 'Bilateral')]
    sd_Unilat_bilat = models.CharField(max_length=200, null=True, blank=True, choices=Unilat_bilat_sel)

    Nerve_Conduction_Study_sel = [('Normal', 'Normal'),
                                  ('Abnormal', 'Abnormal'),
                                  ('Not done', 'Not done')]
    sd_Nerve_Conduction_Study = models.CharField(max_length=200, null=True, blank=True,
                                                 choices=Nerve_Conduction_Study_sel)
    sd_Nerve_Describe_if_abnormal = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    Chitrotriosidase_sel = [('Normal', 'Normal'),
                            ('Abnormal', 'Abnormal'),
                            ('Not done', 'Not done')]
    sd_Chitrotriosidase_Study = models.CharField(max_length=200, null=True, blank=True, choices=Chitrotriosidase_sel)
    sd_Chitrotriosidase_if_abnormal = models.CharField(max_length=100, null=True, blank=True,
                                                       validators=[MaxLengthValidator(100)])
    Any_Other_Biomarker_sel = [('Done', 'Done'),
                               ('Not done', 'Not done')]
    Any_Other_Biomarker = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    Any_Other_Biomarker2 = models.CharField(max_length=100, null=True, blank=True,
                                           choices=Any_Other_Biomarker_sel)
    sd_Biomarker_if_abnormal = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])

    sd_Enzyme_assay = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Sample_sel = [('Whole blood','Whole blood'),('Serum', 'Serum'),
                  ('Plasma', 'Plasma'),
                  ('Leucocyte', ' Leucocyte'),
                  ('Dried Blood Spot', 'Dried Blood Spot'),
                  ('Fibroblast','Fibroblast')]
    sd_Sample_used = models.CharField(max_length=200, null=True, blank=True, choices=Sample_sel)
    enzyme_sel = [('Glucocerebrosidase', 'Glucocerebrosidase'),
                  ('Sphingomyelinase', 'Sphingomyelinase'),
                  ('Beta-galactosidase-1', 'Beta-galactosidase-1'),
                  ('Beta-hexosaminidase A', 'Beta-hexosaminidase A'),
                  ('Beta-hexosaminidase A&B', 'Beta-hexosaminidase A&B'),
                  ('Palmitoyl-Protein thioesterase (PPT)', 'Palmitoyl-Protein thioesterase (PPT)'),
                  ('Tripeptidyl amino peptidase-1 (TPP)', 'Tripeptidyl amino peptidase-1 (TPP)'),
                  ('Arylsulfatase A (ARSA)', 'Arylsulfatase A (ARSA)'),
                  ('Galactosylceramidase', 'Galactosylceramidase'),
                  ('Other','Other')]
    sd_Enzyme = models.CharField(max_length=200, null=True, blank=True, choices=enzyme_sel)
    sd_Enzyme_other=models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mt_enzyme_patient_control = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mt_enzyme_normal_range = models.CharField(max_length=100, blank=True, null=True,
                                                       validators=[MaxLengthValidator(100)])
    mt_enzyme_control_range = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    sd_Enzyme_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

    #	Molecular Diagnostics
    sd_Causative_DNA_sequence_variation = [('done', 'done'), ('not done', 'not done')]
    sd_Causative_DNA_sequence_variat = models.CharField(max_length=20, blank=True, null=True, choices=yes_no)
    # If_done =
    sd_molecular_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    sd_Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    sd_Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    sd_trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    sd_mul_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_mul_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_mul_var_sel = [('Novel', 'Novel '),
                      ('Reported', 'Reported')]
    sd_mul_var1 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_var_sel)
    sd_mul_zygo_sel = [('Homozygous', 'Homozygous '),
                       ('Heterozygous', 'Heterozygous'),
                       ('Hemizygous','Hemizygous')]
    sd_mul_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_zygo_sel)
    sd_mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                       ('Likely Pathogenic', 'Likely Pathogenic'),
                       ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    sd_mul_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_vari_sel)
    sd_mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    sd_mul_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_mul_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_mul_var2 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_var_sel)
    sd_mul_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_vari_sel)
    sd_mul_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=sd_mul_zygo_sel)
    sd_father = models.CharField(max_length=100, blank=True, null=True)
    sd_mother = models.CharField(max_length=100, blank=True, null=True)

    sd_ERT = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Date_of_initiation = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    sd_age_of_start = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(10)])
    sd_Dosage = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Duration = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Adverse_events = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Adverse_events_specify = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    ERT_sel = [(' Ongoing', 'Ongoing'),
               ('Stopped', 'Stopped')]
    sd_ERT_Status = models.CharField(max_length=200, null=True, blank=True, choices=ERT_sel)
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    sd_Response_to_therapy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Any_interruption = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Reason_interruption = models.CharField(max_length=100, null=True, blank=True,
                                              validators=[MaxLengthValidator(100)])
    sd_Duration_interruption = models.CharField(max_length=100, null=True, blank=True,
                                                validators=[MaxLengthValidator(100)])
    sd_Bone_Marrow_Transplantation = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Bone_Marrow_Date = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    Donor_sel = [('Related', 'Related'), ('Unrelated', 'Unrelated')]
    sd_Donor = models.CharField(max_length=100, null=True, blank=True, choices=Donor_sel)
    sd_Hospital = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    sd_Response = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Surgery1 = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    Surgery_sel = [('Splenectomy', 'Splenectomy'),
                   ('Hernia', 'Hernia'),
                   ('others', 'others')]
    Surgery_status = models.CharField(max_length=200, null=True, blank=True, choices=Surgery_sel)
    Surgery_Splenectomy=models.BooleanField(default=False)
    Surgery_Hernia=models.BooleanField(default=False)
    Surgery_others=models.BooleanField(default=False)
    Surgery_others_text= models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Surgery_age = models.CharField(max_length=10, null=True, blank=True, validators=[MaxLengthValidator(10)])

    sd_Calcium_and_multivitamin_supplements = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Regular_Physiotherapy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Antiepileptics = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_Blood_Transfusion = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_BL_freq= models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_BL_Trans =  models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_Platlet_Transfusion = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sd_PL_freq= models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sd_PL_Trans =  models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    PL_Any_other = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    other_information = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])

    # GAUCHERM mSST SCORE
    gaucherm_msst_sel=[('Gaze palsy','Gaze palsy'),('Ophthalmology','Ophthalmology'),
                         ('Epilepsy','Epilepsy'),('Age at first seizure','Age at first seizure'),
                         ('Development/ Cognitive ability)','Development/ Cognitive ability)'),
                         ('Ataxia of gait ','Ataxia of gait '),('Cerebellar tremor','Cerebellar tremor'),('Pyramidal','Pyramidal'),
                         ('Extrapyramidal','Extrapyramidal'),('Swallowing difficulties/ Oral bulbar function','Swallowing difficulties/ Oral bulbar function'),
                         ('Speech','Speech'),('Spinal alignement','Spinal alignement')]
    sd_msst_diagnosis=models.CharField(max_length=100, null=True, blank=True,choices=gaucherm_msst_sel)


    sd_gaze_palsy_sel = [(0.0, "Normal (although not likely in diagnosis)(0) "),
                         (0.5, 'Horizontal saccades absent, vertical saccades present (0.5)'),
                         (1.0, 'Horizontal saccades absent, vertical saccades present (1)')]
    sd_gaze_palsy = models.FloatField(null=True, blank=True, choices=sd_gaze_palsy_sel)
    sd_Ophthalmology_sel = [(0.0, "Normal (although not likely in diagnosis) (0) "),
                            (1.0, 'Cranial nerve palsy (previously corrected or not) (1)'),
                            (2.0, 'Cranial nerve palsy (reappearing despite surgical correction) (2) ')]
    sd_Ophthalmology = models.FloatField(null=True, blank=True, choices=sd_Ophthalmology_sel)
    Epilepsy_sel = [(0.0, "No seizures  (0)"),
                    (3.0, 'Seizures not requiring anticonvulsants(3) '),
                    (4.0, 'Seizures controlled with anticonvulsants (4)'),
                    (5.0, 'Seizures requiring combination therapy or resistant to anticonvulsants (5)')]
    sd_Epilepsy = models.FloatField(null=True, blank=True, choices=Epilepsy_sel)
    Age_seizure_sel = [(3.0, "Younger than 5 years (3)"),
                       (2.0, '5-10 years (2)'),
                       (1.0, '10-15 years (1)'),
                       (0.0, '16 years or over, or seizure free (0)')]
    sd_Age_seizure = models.FloatField(null=True, blank=True, choices=Age_seizure_sel)
    Development_Cognitive_ability_sel = [(0.0, "Normal (0)"),
                                         (1.0, 'Mildly impaired (IQ less than 85 or equivalent) (1)'),
                                         (2.0, 'Moderate (IQ 50-57 or equivalent (2)'),
                                         (3.0, 'Severe (more than half their chronological age (3)')]
    sd_Development_Cognitive_ability = models.FloatField(null=True, blank=True,
                                                         choices=Development_Cognitive_ability_sel)
    Ataxia_of_gait_sel = [(0.0, "Normal, apparent only on tandem walking (0)"),
                          (1.0, 'Ataxia on straight gait, able to walk without assistance (1)'),
                          (2.0, 'Able to walk only with assistance (2) '),
                          (3.0, 'Unable to walk (3)')]
    sd_Ataxia_of_gait = models.FloatField(null=True, blank=True, choices=Ataxia_of_gait_sel)
    Cerebellar_tremor_sel = [(0.0, "No intention tremor (0)"),
                             (0.5, 'Intention tremor not affecting function (0.5)'),
                             (1.0, 'Intention tremor with marked impact on function (1)')]
    sd_Cerebellar_tremor = models.FloatField(null=True, blank=True, choices=Cerebellar_tremor_sel)
    Pyramidal_sel = [(0.0, "No intention tremor (0)"),
                     (2.0, 'Mildly to moderately increased tone and reflexes (2)'),
                     (3.0, 'Increased tone and reflexes with clonus, whether unsustained or sustained (3) '),
                     (5.0, 'Severe spasticity with inability to walk (5)')]
    sd_Pyramidal = models.FloatField(null=True, blank=True, choices=Pyramidal_sel)
    Extrapyramidal_sel = [(0.0, "Normal (0)"),
                          (1.0, 'Variable tone and posturing not impairing function, with or without therapy (1)'),
                          (2.0, 'Variable tone and posturing impairing function, despite therapy (2)'),
                          (3.0, 'Significant rigidity with no/minimal benefit from therapy (3)')]
    sd_Extrapyramidal = models.FloatField(null=True, blank=True, choices=Extrapyramidal_sel)
    Swallowing_difficulties_Oral_bulbar_function_sel = [(0.0, "Normal (0)"),
                                                        (1.0, 'Mild dysphagia (excess drooling) (1)'),
                                                        (2.0, 'Moderate dysphagia (risk of aspiration, modification to diet required)(2)'),
                                                        (3.0, 'Severe dysphagia (requiring non-oral feeding) (3)')]
    sd_Swallowing_difficulties_Oral_bulbar_function = models.FloatField(null=True, blank=True,
                                                                        choices=Swallowing_difficulties_Oral_bulbar_function_sel)
    Speech_sel = [(0.0, "Normal (and those too young yet to speak) (0) "),
                  (1.0, 'Mild to moderate dysarthia impairing intelligibility to unfamiliar listener (1)'),
                  (2.0, 'Severe dysarthia with most speech unintelligible to familiar and unfamiliar liste (2)'),
                  (3.0, 'Anarthria (3)')]
    sd_Speech = models.FloatField(null=True, blank=True, choices=Speech_sel)
    Spinal_alignement_sel = [(0.0, "Normal"),
                             (1.0, 'Mild kyphosisâ€“but flexible and not requiring bracing (1)'),
                             (2.0, 'Moderate kyphosisâ€“partially corrected by bracing (2) '),
                             (3.0, 'Severe kyphosisâ€“not corrected by bracing or requiring surgery (3)')]
    sd_Spinal_alignement = models.FloatField(null=True, blank=True, choices=Spinal_alignement_sel)
    sd_final_score=models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    sd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #final diagnosis

    sd_final_diagnosis_sel=[('Gaucher Disease type I','Gaucher Disease type I'),('Gaucher Disease type II','Gaucher Disease type II'),('Gaucher Disease type III','Gaucher Disease type III'),
                        ('Niemann Pick Disease A','Niemann Pick Disease A'),('Niemann Pick Disease B','Niemann Pick Disease B'),('Niemann Pick Disease C','Niemann Pick Disease C'),
                        ('GM1 gangliosidosis','GM1 gangliosidosis'),('GM2 gangliosidosis(Tay Sachs)','GM2 gangliosidosis(Tay Sachs)'),('GM2 gangliosidosis(Sandhoff)','GM2 gangliosidosis(Sandhoff)'),('Metachromatic Leukodystrophy','Metachromatic Leukodystrophy'),('Krabbe Disease','Krabbe Disease'),
                        ('Farber Disease','Farber Disease'),('Other','Other')]

    sd_final_diagnosis=models.CharField(max_length=100, blank=True, null=True,
                                             choices=sd_final_diagnosis_sel)
    sd_final_diagnosis_other = models.CharField(max_length=100, blank=True, null=True,
                                          validators=[MaxLengthValidator(100)])



    # Final Outcome
    sd_final_sel = [('Death', 'Death'), ('Alive', 'Alive'), ('Follow up required', 'Follow up required'),
                    ('Unknown', 'Unknown')]
    sd_filed_by_DEO_name = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])

    sd_clinician_name = models.CharField(max_length=100, blank=True, null=True,
                                         validators=[MaxLengthValidator(100)])
    sd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    sd_filled_date = models.DateField(null=True, blank=True)

    sd_Final_Outcome = models.CharField(max_length=50, blank=True, null=True, choices=sd_final_sel)
    sd_death_cause = models.CharField(max_length=50, blank=True, null=True)
    sd_age_timedeath = models.CharField(max_length=50, blank=True, null=True)







    def __str__(self):
        return str(self.pk)
