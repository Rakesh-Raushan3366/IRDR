# Create your models here.


from account.models import *
from django.core.validators import FileExtensionValidator
# Create your models here.

class profile_skeletal(models.Model):
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
    sk_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_date_of_records = models.DateField(blank=True, null=True)
    sk_date_of_clinical_exam = models.DateField(blank=True, null=True)
    sk_date_of_birth = models.DateField( null=True)
    sk_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    sk_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    sk_paitent_id_yes_no = models.CharField(max_length=100,  null=True, choices=fb_status_sel)
    sk_paitent_id = models.CharField(max_length=100,  blank=True,null=True, choices=id_sel)
    sk_patient_id_no = models.CharField(max_length=100,blank=True, unique=True, null=True, validators=[MaxLengthValidator(100)])
    sk_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_father_mother_id =  models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    sk_father_mother_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    #sk_mother_adhaar_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    sk_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    sk_state = models.ForeignKey(State, null=True,  on_delete=models.CASCADE, verbose_name=' state')
    sk_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    sk_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    sk_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    sk_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    sk_email = models.EmailField(max_length=300, blank=True, null=True)

    sk_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    sk_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    sk_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    sk_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    sk_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    sk_consent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    sk_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    sk_assent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    sk_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True,  null=True, validators=[FileExtensionValidator(['pdf'])])
    sk_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    sk_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_skeletal', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_skeletal', on_delete=models.CASCADE)

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
            super(profile_skeletal, self).save(*args, **kwargs)
            self.sk_icmr_unique_no = str('Skeletal/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_skeletal, self).save(*args, **kwargs)


class demographic_skeletal(models.Model):
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    yes_no123 = [('1', 'Yes'), ('0', 'No')]
    sk_Patient_edu_sel = [('Illiterate', 'Illiterate'),
                          ('Primary', 'Primary'), ('High school', 'High school'),
                          ('Secondary level', 'Secondary level'),
                          ('College and above', 'College and above'),
                          ('Other', 'Other')]
    sk_Patient_education = models.CharField(max_length=100, null=True, blank=True, choices=sk_Patient_edu_sel)
    sk_Patient_occupation_sel = [('Employed(organised sector)', 'Employed(organised sector)'),
                                 ('Employed(unorganised sector)', 'Employed(unorganised sector)'),
                                 ('Others', 'Others'), ]
    sk_Patient_occupation = models.CharField(max_length=200, null=True, blank=True, choices=sk_Patient_occupation_sel)
    sk_Father_edu_sel = [('No formal education', 'No formal education'),
                         ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                         ('Secondary school', 'Secondary school'),
                         ('College/Pre-university', 'College/Pre-university'),
                         ('Post graduate degree ', 'Post graduate degree ')]
    sk_Father_education = models.CharField(max_length=100, null=True, blank=True, choices=sk_Patient_edu_sel)
    sk_Father_occupation_sel = [('Employed(organised sector)', 'Employed(organised sector)'),
                                 ('Employed(unorganised sector)', 'Employed(unorganised sector)'),
                                 ('Home maker', 'Home maker'),
                                 ('Others', 'Others'), ]
    sk_Father_occupation = models.CharField(max_length=200, null=True, blank=True, choices=sk_Father_occupation_sel)
    sk_Mother_edu_sel = [('No formal education', 'No formal education'),
                         ('Less than primary school', 'Less than primary school'), ('High school', 'High school'),
                         ('Secondary school', 'Secondary school'),
                         ('College/Pre-university', 'College/Pre-university'),
                         ('Post graduate degree ', 'Post graduate degree ')]
    sk_Mother_education = models.CharField(max_length=100, null=True, blank=True, choices=sk_Patient_edu_sel)
    sk_Mother_occupation_sel = [ ('Home maker', 'Home maker'),
                                ('Employed(organised sector)', 'Employed(organised sector)'),
                                 ('Employed(unorganised sector)', 'Employed(unorganised sector)'),
                                 ('Others', 'Others'), ]
    sk_Mother_occupation = models.CharField(max_length=200, null=True, blank=True, choices=sk_Mother_occupation_sel)
    sk_Monthly_family_income_sel = [('> 126,360', '> 126,360)'),
                                    ('63,182 – 126,356)', '63,182 – 126,356)'),
                                    ('47,266 – 63,178', '47,266 – 63,178'),
                                    ('31,591 - 47,262', '31,591 - 47,262'),
                                    ('18,953 - 31,589', '18,953 - 31,589'),
                                    ('6,327 - 18,949', '6,327 - 18,949'),
                                    ('< 6,323', '< 6,323')]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_skeletal, null=True, related_name='patient_skeletal', blank=True,
                                on_delete=models.CASCADE)
    sk_Monthly_family_income = models.CharField(max_length=200, null=True, blank=True,
                                                choices=sk_Monthly_family_income_sel)
    sk_weight_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_weight_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_weight_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_height_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_height_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_height_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_Lower_segment_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_Lower_segment_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_Lower_segment_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_US_LS_Ratio_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_US_LS_Ratio_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_US_LS_Ratio_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_Head_circumference_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_Head_circumference_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_Head_circumference_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_Arm_span_patient = models.CharField(max_length=200, null=True, blank=True)
    sk_Arm_span_percentile = models.CharField(max_length=200, null=True, blank=True)
    sk_Arm_span_sd = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_onset_of_symptoms_year = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_onset_of_symptoms_month = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_onset_of_symptoms_day = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_onset_of_symptoms_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    sk_Age_at_presentation_year = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_presentation_month = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_presentation_day = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_presentation_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    sk_Age_at_diagnosis_year = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_diagnosis_month = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_diagnosis_day = models.CharField(max_length=200, null=True, blank=True)
    sk_Age_at_diagnosis_Intrauterine = models.CharField(max_length=20, null=True, blank=True, choices=yes_no123)
    sk_Pedigree_to_be_uploaded = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True, blank=True, )
    sk_positive_family_history = models.CharField(max_length=100, null=True, blank=True,
                                                  choices=yes_no, )
    sk_Family_history_specify = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    sk_Consanguinity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no, )
    sk_Consanguinity_specify = models.CharField(max_length=200, null=True, blank=True, )

    sk_Ultrasound_findings_sel = [('Present', 'Present'), ('Absent', 'Absent')]
    sk_Ultrasound_Polyhydramnios = models.CharField(max_length=100, null=True, blank=True,
                                                    choices=sk_Ultrasound_findings_sel)
    sk_Ultrasound_Any_other_antenatal_investigations = models.CharField(max_length=100, null=True, blank=True,
                                                                        validators=[MaxLengthValidator(100)])

    sk_Ultrasound_Short_long_Bones_Bending = models.CharField(max_length=100, null=True, blank=True,
                                                              choices=yes_no, )
    sk_Ultrasound_Short_long_Bones_Bending_gestation_period = models.CharField(max_length=100, null=True, blank=True,
                                                                               validators=[MaxLengthValidator(100)])
    sk_Ultrasound_Hydrops = models.CharField(max_length=100, null=True, blank=True,
                                             choices=sk_Ultrasound_findings_sel)
    sk_Natal_History_sel = [('caesarean', 'caesarean'), ('Vaginal', 'Vaginal')]
    sk_Natal_History_Type_of_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                         choices=sk_Natal_History_sel)
    sk_Natal_History_Baby_cried_immediately_after_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                                              choices=yes_no)
    sk_Natal_History_Resuscitation_required = models.CharField(max_length=100, null=True, blank=True,
                                                               choices=yes_no)
    sk_Natal_History_Resuscitation_specify = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(9999999999)],
        null=True, blank=True,
    )
    sk_Natal_History_o_2 = models.CharField(max_length=100, null=True, blank=True,
                                            choices=yes_no)
    sk_Natal_History_ventilation = models.CharField(max_length=100, null=True, blank=True,
                                                    choices=yes_no)
    sk_Natal_History_NICU_stay = models.CharField(max_length=100, null=True, blank=True,
                                                  choices=yes_no)
    sk_Natal_History_NICU_stay_specify = models.CharField(max_length=100, null=True, blank=True,
                                                          validators=[MaxLengthValidator(100)])
    sk_Natal_History_NICU_stay_other = models.CharField(max_length=100, null=True, blank=True,
                                                        validators=[MaxLengthValidator(100)])
    sk_Other_Birth_weight = models.FloatField(blank=True, null=True)
    sk_Other_Birth_length = models.FloatField(blank=True, null=True)
    sk_Other_Birth_head_circumference =models.FloatField(blank=True, null=True)
    sk_Other_Short_Bones = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Other_Any_other_malformation = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Other_joint_contractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Other_Fractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Milestone_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    sk_Development_milestones = models.CharField(max_length=100, null=True, blank=True, choices=sk_Milestone_sel)
    sk_if_delayed_Motor = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_if_delayed_Global = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_if_delayed_Cognitive = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_history = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Any_Fractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Any_Fractures_number = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])
    sk_Natal_History_NICU_stay_Gestation_at_delivery = models.CharField(max_length=100, null=True, blank=True,
                                                        validators=[MaxLengthValidator(100)])
    sk_Any_hearing_impairment = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Any_visual_problems = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Any_surgical_intervation = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Any_surgical_intervation_specify = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Development_delay = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_IQ_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    sk_IQ_done = models.CharField(max_length=100, null=True, blank=True, choices=sk_IQ_sel)
    sk_IQ_done_value = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])
    sk_DQ_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    sk_DQ_done = models.CharField(max_length=100, null=True, blank=True, choices=sk_DQ_sel)
    sk_DQ_done_value = models.CharField(max_length=200, null=True, blank=True, validators=[MaxLengthValidator(200)])

    sk_Upper_limb_Rhizomelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Rhizomelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                 validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Rhizomelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Mesomelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Mesomelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Mesomelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                               validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Acromelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Acromelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Acromelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                               validators=[MaxLengthValidator(200)])
    sk_Upper_limb_hypoplastic_radius = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_hypoplastic_radius_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Upper_limb_hypoplastic_radius_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Upper_limb_hypoplastic_ulna = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_hypoplastic_ulna_right = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Upper_limb_hypoplastic_ulna_left = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Polydactyly_hand_Preaxial = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Polydactyly_hand_Preaxial_right = models.CharField(max_length=200, null=True, blank=True,
                                                                     validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Polydactyly_hand_Preaxial_left = models.CharField(max_length=200, null=True, blank=True,
                                                                    validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Ectrodactyly = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Ectrodactyly_right_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Ectrodactyly_left = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Brachydactyly_hand = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Brachydactyly_hand_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Brachydactyly_hand_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Trident_hand = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Trident_hand_right = models.CharField(max_length=200, null=True, blank=True,
                                                        validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Trident_hand_left = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Oligodactyly_hand = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Oligodactyly_hand_right = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Oligodactyly_hand_left = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Hypoplastic_thumb = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Hypoplastic_thumb_right = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Hypoplastic_thumb_left = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Syndactyly_Skin = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Syndactyly_Skin_right = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Syndactyly_Skin_left = models.CharField(max_length=200, null=True, blank=True,
                                                          validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Joint_laxity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Joint_laxity_right = models.CharField(max_length=200, null=True, blank=True,
                                                        validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Joint_laxity_left = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Joint_contractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Joint_contractures_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Joint_contractures_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Deformities = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Upper_limb_Deformities_right = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Deformities_left = models.CharField(max_length=200, null=True, blank=True,
                                                      validators=[MaxLengthValidator(200)])
    sk_Upper_limb_Any_other = models.CharField(max_length=200, null=True, blank=True,
                                               validators=[MaxLengthValidator(200)])

    sk_Lower_limb_Rhizomelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Rhizomelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                 validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Rhizomelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Mesomelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Mesomelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Mesomelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                               validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Acromelic_shortening = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Acromelic_shortening_right = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Acromelic_shortening_left = models.CharField(max_length=200, null=True, blank=True,
                                                               validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_fibula = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_hypoplastic_fibula_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_fibula_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_tibula = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_hypoplastic_tibula_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_tibula_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_femur = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_hypoplastic_femur_right = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_hypoplastic_femur_left = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Polydactyly_foot = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Polydactyly_foot_right = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Polydactyly_foot_left = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Oligodactyly_foot = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Oligodactyly_foot_right = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Oligodactyly_foot_left = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Brachydactyly_foot = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Brachydactyly_foot_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Brachydactyly_foot_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Ectrodactyly_foot = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Ectrodactyly_foot_right = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Ectrodactyly_foot_left = models.CharField(max_length=200, null=True, blank=True,
                                                            validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Hypoplastic_great_toe = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Hypoplastic_great_toe_right = models.CharField(max_length=200, null=True, blank=True,
                                                                 validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Hypoplastic_great_toe_left = models.CharField(max_length=200, null=True, blank=True,
                                                                validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Hallux_vagus = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Hallux_vagus_right = models.CharField(max_length=200, null=True, blank=True,
                                                        validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Hallux_vagus_left = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Broad_great_toe = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Broad_great_toe_right = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Broad_great_toe_left = models.CharField(max_length=200, null=True, blank=True,
                                                          validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Deviated_great_toe = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Deviated_great_toe_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Deviated_great_toe_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Syndactyly_Skin = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Syndactyly_Skin_right = models.CharField(max_length=200, null=True, blank=True,
                                                           validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Syndactyly_Skin_left = models.CharField(max_length=200, null=True, blank=True,
                                                          validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Joint_laxity = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Joint_laxity_right = models.CharField(max_length=200, null=True, blank=True,
                                                        validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Joint_laxity_left = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Joint_contractures = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Joint_contractures_right = models.CharField(max_length=200, null=True, blank=True,
                                                              validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Joint_contractures_left = models.CharField(max_length=200, null=True, blank=True,
                                                             validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Deformities = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Lower_limb_Deformities_right = models.CharField(max_length=200, null=True, blank=True,
                                                       validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Deformities_left = models.CharField(max_length=200, null=True, blank=True,
                                                      validators=[MaxLengthValidator(200)])
    sk_Lower_limb_Any_other = models.CharField(max_length=200, null=True, blank=True,
                                               validators=[MaxLengthValidator(200)])
    sk_Face_upload_photograph = models.FileField(null=True, blank=True, upload_to='uploads/%Y/%m/%d/')
    sk_Frenula = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Cleft_lip_palate = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Cleft_lip_palate_right = models.CharField(max_length=200, null=True, blank=True,
                                                 validators=[MaxLengthValidator(200)])
    sk_Cleft_lip_palate_left = models.CharField(max_length=200, null=True, blank=True,
                                                validators=[MaxLengthValidator(200)])
    sk_Dysmorphism = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Dysmorphism_specify = models.CharField(max_length=200, null=True, blank=True,
                                              validators=[MaxLengthValidator(200)])
    sk_high_prominent_forehead_Midface_hypoplasia = models.CharField(max_length=100, null=True, blank=True,
                                                                     choices=yes_no)
    sk_Abnormal_Hair = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Abnormal_Hair_specify = models.CharField(max_length=200, null=True, blank=True,
                                                validators=[MaxLengthValidator(200)])
    sk_Ear_abnormality = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Blue_sclera = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Dentition = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Thorax_Narrow = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Thorax_Carinatum = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Thorax_Excavatum = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Spine_sel =     [('Normal ', 'Normal '),
                        ('Abnormal ', 'Abormal')]
    sk_Genitalia_sel = [('Normal male', 'Normal male'),
                        ('Normal female', 'Normal female'),
                        ('Ambiguous', 'Ambiguous'),
                        ('other', 'other')]
    sk_Spine = models.CharField(max_length=100, null=True, blank=True, choices=sk_Spine_sel)
    sk_Spine_abnormal = models.CharField(max_length=100, null=True, blank=True, )
    sk_Genitalia = models.CharField(max_length=100, null=True, blank=True, choices=sk_Genitalia_sel)
    sk_Skin_pigmentary_abnormalities = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Skin_pigmentary_specify = models.CharField(max_length=100, null=True, blank=True, )
    sk_Nail_hypoplasia = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_Eye_pigmentary_or_any_other_ocular_abnormality = models.CharField(max_length=100, null=True, blank=True,
                                                                         choices=yes_no)
    sk_Eye_pigmentary_specify = models.CharField(max_length=100, null=True, blank=True, )

    sk_Invetigation_Date = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    sk_Bone_health_assessment = models.CharField(max_length=100, null=True, blank=True,
                                                 validators=[MaxLengthValidator(100)])
    sk_S_Cal = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_Po4 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_SAP = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_Vit_D = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_PTH = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_DEXA_Scan_Z_score = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_x_ray_findings_Date = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    sk_skull_ap = models.CharField(max_length=100, null=True, blank=True, )
    sk_Dorso_lumbar_Spine_AP = models.CharField(max_length=100, null=True, blank=True, )
    sk_Hands_with_wrist_AP = models.CharField(max_length=100, null=True, blank=True, )
    sk_Chest_PA = models.CharField(max_length=100, null=True, blank=True, )
    sk_Pelvis_with_both_hip_joints = models.CharField(max_length=100, null=True, blank=True, )
    sk_Long_bones_AP = models.CharField(max_length=100, null=True, blank=True, )
    sk_X_ray_cervical_spine_in_extension_and_flexion_AP = models.CharField(max_length=100, null=True, blank=True, )
    sk_Any_other = models.CharField(max_length=100, null=True, blank=True, )
    sk_CT_Scan_MRI_Brain = models.DateField(auto_now=False, null=True, blank=True, auto_now_add=False, )
    sk_CT_Scan2 = models.CharField(max_length=100, null=True, blank=True, )
    sk_any_other_investigation_date = models.DateField(blank=True, null=True)
    sk_BERA_Audiogram = models.CharField(max_length=100, null=True, blank=True, )
    sk_VEP = models.CharField(max_length=100, null=True, blank=True, )
    sk_Ocular = models.CharField(max_length=100, null=True, blank=True, )
    sk_Thyroid = models.CharField(max_length=100, null=True, blank=True, )
    sk_ECHO = models.CharField(max_length=100, null=True, blank=True, )
    sk_USG_abdomen = models.CharField(max_length=100, null=True, blank=True, )
    sk_genetic_analysis_performed = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_genetic_analysis_performed_report = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True, blank=True, )

    sk_gene = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_tran = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_dna = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_pro = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_var_sel =     [('Novel ', 'Novel '),
                        ('Reported ', 'Reported')]
    sk_var = models.CharField(max_length=100, null=True, blank=True, choices=sk_var_sel)
    sk_vari_sel =     [('Pathogenic ', 'Pathogenic '),
                        ('Likely Pathogenic', 'Likely Pathogenic'),
                        ('Variant of uncertain Significance ', 'Variant of uncertain Significance')]
    sk_var_cla = models.CharField(max_length=100, null=True, blank=True, choices=sk_vari_sel)
    sk_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    sk_Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    sk_Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    sk_trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    sk_mul_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_mul_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_mul_var_sel = [('Novel', 'Novel '),
                      ('Reported', 'Reported')]
    sk_mul_var1 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_var_sel)
    sk_mul_zyg_sel = [('Homozygous', 'Homozygous '),
                       ('Heterozygous', 'Heterozygous'),
                      ('Hemizygous', 'Hemizygous')
                      ]
    sk_mul_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_zyg_sel)
    sk_mul_var_sel = [('Pathogenic ', 'Pathogenic '),
                       ('Likely Pathogenic', 'Likely Pathogenic'),
                       ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    sk_mul_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_var_sel)

    sk_mul_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_mul_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_mul_vari_sel = [('Novel', 'Novel '),
                      ('Reported', 'Reported')]
    sk_mul_var2 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_vari_sel)
    sk_mul_zygo_sel = [('Homozygous', 'Homozygous '),
                       ('Heterozygous', 'Heterozygous'),
                       ('Hemizygous', 'Hemizygous')]
    sk_mul_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_zygo_sel)
    sk_mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                       ('Likely Pathogenic', 'Likely Pathogenic'),
                       ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    sk_mul_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=sk_mul_vari_sel)
    sk_mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    sk_father = models.CharField(max_length=100, blank=True, null=True)
    sk_mother = models.CharField(max_length=100, blank=True, null=True)
    sk_diagnosis = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_mention_novel_findings = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_Treatment_Bisphosphonates = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    
    sk_Bisphosphonates_Pamidronate = models.BooleanField(default=False)
    sk_Bisphosphona_Zolendronate = models.BooleanField(default=False)
    sk_Bisphosphonate_Alendronate = models.BooleanField(default=False)
    sk_Bisphosphon_Other = models.BooleanField(default=False)
    sk_date_of_inititation = models.DateField(null=True, blank=True, )
    sk_bisphosphonates_dose = models.CharField(max_length=100, null=True, blank=True,
                                               validators=[MaxLengthValidator(100)])
    sk_bisphosphonates_duration = models.CharField(max_length=100, null=True, blank=True,
                                                   validators=[MaxLengthValidator(100)])
    sk_Treatment_Response = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    # sk_Response_sel = [('Decrease  of fractures', 'Decrease  of fractures'),
    #                    ('Improvement in Z score (DEXA)', 'Improvement in Z score (DEXA)'),
    #                    ('Improved QOL (subjective)', 'Improved QOL (subjective)'),
    #                    ('other', 'other')]
    # sk_Response = models.CharField(max_length=100, null=True, blank=True, choices=sk_Response_sel)
    sk_Response_Decrease = models.BooleanField(default=False)
    sk_Response_Improvement = models.BooleanField(default=False)
    sk_Response_Improved = models.BooleanField(default=False)
    sk_Response_other = models.BooleanField(default=False)
    sk_Treatment_Any_Surgical_Procedure = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    # sk_Any_Surgical_Procedure_Sel = [('Limb lengthening', 'Limb lengthening'),
    #                                  ('Hydrocephalus surgery', 'Hydrocephalus surgery'),
    #                                  ('Craniosynostosis surgery', 'Craniosynostosis surgery'),
    #                                  ('surgery for fractures', 'surgery for fractures'),
    #                                  ('surgery for fractures', 'surgery for fractures'),
    #                                  ('joint replacement', 'joint replacement'),
    #                                  ('other', 'other')]
    #
    # sk_Any_Surgical_Procedure = models.CharField(max_length=100, null=True, blank=True,
    #                                              choices=sk_Any_Surgical_Procedure_Sel)
    sk_Any_Surgical_Procedure_Limb = models.BooleanField(default=False)
    sk_Any_Surgical_Procedure_Hydrocephalus = models.BooleanField(default=False)
    sk_Any_Surgical_Procedure_Craniosynostosis = models.BooleanField(default=False)
    sk_Any_Surgical_Procedure_surgery = models.BooleanField(default=False)
    sk_Any_Surgical_Procedure_joint = models.BooleanField(default=False)
    sk_Any_Surgical_Procedure_other = models.BooleanField(default=False)


    sk_other_surgical_information = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    sk_Any_other_therapy = models.CharField(max_length=20, null=True, blank=True, choices=yes_no)
    sk_other_information = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_filed_by_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_clinician_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    sk_filled_date = models.DateField(null=True, blank=True)
    sk_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    sk_Final_outcome_sel = [('Death', 'Death'),
                              ('Alive', 'Alive'),
                              ('Followup reqired', 'Followup reqired'),
                              ('Unknown', 'Unknown')]
    sk_Final_outcome = models.CharField(max_length=100, null=True, blank=True, choices=sk_Final_outcome_sel)
    sk_Final_diagnosis_sel = [('Osteogenesis Imperfecta', 'Osteogenesis Imperfecta'),
                              ('Achodroplasia', 'Achodroplasia'),
                              ('Sclerosing bone dysplasia ', 'Sclerosing bone dysplasia'),
                              ('other', 'other')]
    sk_Final_diagnosis = models.CharField(max_length=100, null=True, blank=True, choices=sk_Final_diagnosis_sel)
    sk_diagno_other = models.CharField(max_length=100, null=True, blank=True,
                                                     validators=[MaxLengthValidator(100)])
    def __str__(self):
        return str(self.pk)
