# Create your models here.

# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator

class profile_pid(models.Model):
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
    pid_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_date_of_record = models.DateField(blank=True, null=True)
    pid_clinical_exam_date = models.DateField(blank=True, null=True)
    pid_date_of_birth = models.DateField( null=True)
    pid_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    pid_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    pid_paitent_id = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    pid_paitent_id_list = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    pid_patient_id_no = models.CharField(max_length=100, unique=True,blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_father_mother_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    pid_father_mother_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    pid_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    pid_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    pid_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    pid_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_mother_mobile_no = models.PositiveBigIntegerField(null=True, unique=True)
    pid_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    pid_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    pid_email = models.EmailField(max_length=300, blank=True, null=True)

    pid_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    pid_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    pid_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    pid_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    pid_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    pid_consent_given = models.CharField(max_length=10, null=True, choices=fb_status_sel)
    pid_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, validators=[FileExtensionValidator(['pdf'])])
    pid_assent_given = models.CharField(max_length=10, null=True,  choices=fb_status_sel)
    pid_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    pid_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_pid', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_pid', on_delete=models.CASCADE)

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
            super(profile_pid, self).save(*args, **kwargs)
            self.pid_icmr_unique_no = str('PID/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_pid, self).save(*args, **kwargs)



class demopraphic_pid(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_pid, null=True,related_name='profile_pid', blank=True, on_delete=models.CASCADE)
    known_unknown = [('Known ', 'Known '), ('Unknown', 'Unknown')]
    yes_no = [('Yes', 'Yes'), ('No', 'No')]


    pid_has_hiv_been_excluded = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_date_onset_symptoms = models.CharField(max_length=100, null=True, blank=True, choices=known_unknown)
    pid_onset_date = models.DateField(null=True, blank=True)
    age_onset_symptoms_years = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    age_onset_symptoms_months = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])

    pid_HIV_excluded = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    yes_no_unknown = [('Yes', 'Yes'), ('No', 'No'), ('Not Known', 'Not Known')]
    pid_infections = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_infections_Site_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])
    pid_infections_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    pid_infections_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                    validators=[MaxLengthValidator(100)])

    pid_Meningitis_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    pid_Meningitis_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                    validators=[MaxLengthValidator(100)])

    sino_sel = [('Otitis media', 'Otitis media'), ('Tonsillitis ', 'Tonsillitis '), ('Sinusitis ', 'Sinusitis '),
                ('Pneumonia/Bronchiectasis ', 'Pneumonia/Bronchiectasis ')]
    # pid_Sino_pulmonary  = models.CharField(max_length=100, null=True, blank=True, choices=sino_sel)
    Otitis_media = models.CharField(max_length=100, blank=True, null=True)
    Tonsillitis = models.CharField(max_length=100, blank=True, null=True)
    Sinusitis = models.CharField(max_length=100, blank=True, null=True)
    Pneumonia_Bronchiectasis = models.CharField(max_length=100, blank=True, null=True)

    Otitis_media_last = models.CharField(max_length=100, blank=True, null=True)
    Tonsillitis_last = models.CharField(max_length=100, blank=True, null=True)
    Sinusitis_last = models.CharField(max_length=100, blank=True, null=True)
    Pneumonia_Bronchiectasis_last = models.CharField(max_length=100, blank=True, null=True)

    pid_Sino_pulmonary_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                              validators=[MaxLengthValidator(100)])
    pid_Sino_pulmonary_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                        validators=[MaxLengthValidator(100)])

    pid_Gastroenteritis_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    pid_Gastroenteritis_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                         validators=[MaxLengthValidator(100)])
    pid_Urinary_tract_infections = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    pid_Urinary_tract_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    pid_Urinary_tract_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                       validators=[MaxLengthValidator(100)])

    # sino_sel = [('Soft tissue infections', 'Soft tissue infections'), ('Liver abscess ', 'Liver abscess '), ('Splenic abscess ', 'Splenic abscess ')]

    # pid_Soft_tissue_infections = models.CharField(max_length=100, blank=True, null=True,
    #                                              validators=[MaxLengthValidator(100)])
    # pid_Liver_abscess = models.CharField(max_length=100, blank=True, null=True,
    #                                     validators=[MaxLengthValidator(100)])
    # pid_Splenic_abscess = models.CharField(max_length=100, blank=True, null=True,
    #                                      validators=[MaxLengthValidator(100)])
    pid_Deep_seated = models.CharField(max_length=100, null=True, blank=True, choices=sino_sel)
    tissue_infections = models.CharField(max_length=100, null=True, blank=True)
    tissue_infections_last = models.CharField(max_length=100, null=True, blank=True)
    Liver_abscess = models.CharField(max_length=100, null=True, blank=True)
    Liver_abscess_last = models.CharField(max_length=100, null=True, blank=True)
    Splenic_abscess = models.CharField(max_length=100, null=True, blank=True)
    Splenic_abscess_last = models.CharField(max_length=100, null=True, blank=True)

    pid_Deep_seated_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                           validators=[MaxLengthValidator(100)])
    pid_Deep_seated_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                     validators=[MaxLengthValidator(100)])

    pid_Septicemias_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                           validators=[MaxLengthValidator(100)])
    pid_Septicemias_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                     validators=[MaxLengthValidator(100)])

    pid_Thrush_or_fungal_number_of_infection = models.CharField(max_length=100, blank=True, null=True,
                                                                validators=[MaxLengthValidator(100)])
    pid_Thrush_or_fungal_number_of_infection_last_year = models.CharField(max_length=100, blank=True, null=True,
                                                                          validators=[MaxLengthValidator(100)])
    pid_Vaccine_associated_complications = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_bcg = models.BooleanField(default=False)
    pid_opv = models.BooleanField(default=False)
    pid_Rubella = models.BooleanField(default=False)
    pid_Measles = models.BooleanField(default=False)
    bcg_sel = [('BCG adenitis', 'BCG adenitis'), ('BCG-osis', 'BCG-osis ')]
    pid_Vaccine_associated_complications_BCG_adenitis_age_onset = models.CharField(max_length=100, blank=True,
                                                                                   null=True,
                                                                                   validators=[MaxLengthValidator(100)])
    pid_bcg_options = models.CharField(max_length=100, null=True, blank=True, choices=bcg_sel)

    pid_Vaccine_associated_complications_BCG_adenitis_Axillary = models.CharField(max_length=100, null=True, blank=True,
                                                                                  choices=yes_no)
    pid_Vaccine_associated_adenitis_Multiple_sites_yes_no = models.CharField(max_length=100,
                                                                                               null=True, blank=True,
                                                                                               choices=yes_no)

    pid_Vaccine_associated_complications_BCG_adenitis_Cervical = models.CharField(max_length=100, null=True, blank=True,
                                                                                  choices=yes_no)
    limph_node_sel = [('Single', 'Single'), ('Multiple', 'Multiple')]
    pid_Vaccine_associated_Multiple_sites = models.CharField(max_length=100, blank=True,
                                                                                        null=True,
                                                                                        choices=limph_node_sel)
    pid_Vaccine_associated_complications_BCG_osis = models.CharField(max_length=100, blank=True,
                                                                     null=True,
                                                                     validators=[MaxLengthValidator(100)])

    pid_OPV_Date_Dose = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    pid_OPV_Flaccid_paralysis = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_OPV_Poliovirus_isolation = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_Rubella_Date_Vaccination = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    pid_Rubella_Symptoms_sel = [('Fever', 'Fever'),
                                ('Enlarged lymph nodes', 'Enlarged lymph nodes'),
                                ('Measles-like rash', 'Measles-like rash')]
    pid_Rubella_Symptoms_Fever = models.BooleanField(default=False)
    pid_Rubella_Symptoms_Enlarged_lymph_nodes = models.BooleanField(default=False)
    pid_Rubella_Symptoms_Measles_like_rash = models.BooleanField(default=False)

    pid_Measles_Date_Vaccination = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    pid_Measles_Symptoms_sel = [('Fever', 'Fever'),
                                ('Enlarged lymph nodes', 'Enlarged lymph nodes'),
                                ('Measles-like rash', 'Measles-like rash')]
    pid_Measles_fever = models.BooleanField(default=False)
    pid_Measles_EnlargedLymphNodes = models.BooleanField(default=False)
    pid_Measles_MeaslesLikeRash = models.BooleanField(default=False)
    # pid_Measles_Symptoms = models.CharField(max_length=100, blank=True, null=True, choices=pid_Rubella_Symptoms_sel)
    pid_Failure_to_gain_weight = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_no_times_hospitalised = models.CharField(max_length=100, blank=True,
                                                                                      null=True,
                                                                                      validators=[
                                                                                          MaxLengthValidator(100)])
    pid_autoimmunity_autoinflammation = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_unknown)
    pid_autoimmunity_autoinflammation_type_symptoms_fever = models.CharField(max_length=100, null=True, blank=True,
                                                                             choices=yes_no)
    pid_autoimmunity_autoinflammation_type_symptoms_fever_temp = models.CharField(max_length=100, blank=True,
                                                                                  null=True,
                                                                                  validators=[MaxLengthValidator(100)])
    pid_autoimmunity_autoinflammation_type_symptoms_fever_duration = models.CharField(max_length=100, blank=True,
                                                                                      null=True,
                                                                                      validators=[
                                                                                          MaxLengthValidator(100)])
    pid_autoimmunity_Precipitated_cold = models.CharField(max_length=100,
                                                          null=True, blank=True,
                                                          choices=yes_no_unknown)
    pid_autoimmunity_Precipitated_cold_frequency = models.CharField(max_length=100,
                                                                    blank=True,
                                                                    null=True,
                                                                    validators=[
                                                                        MaxLengthValidator(
                                                                            100)])

    pid_autoimmunity_AssociatedLymphadenopathy = models.CharField(max_length=100,
                                                                  null=True,
                                                                  blank=True,
                                                                  choices=yes_no)

    pid_autoimmunity_AbdominalSymptoms = models.CharField(max_length=100,
                                                          null=True, blank=True,
                                                          choices=yes_no)
    pid_autoimmunity_AbdominalSymptoms_1 = models.BooleanField(default=False)
    pid_autoimmunity_AbdominalSymptoms_2 = models.BooleanField(default=False)
    pid_autoimmunity_AbdominalSymptoms_3 = models.BooleanField(default=False)
    pid_autoimmunity_AbdominalSymptoms_4 = models.BooleanField(default=False)
    pid_autoimmunity_AbdominalSymptoms_5 = models.BooleanField(default=False)
    pid_autoimmunity_MusculoskeletalSymptoms = models.CharField(max_length=100,
                                                                null=True,
                                                                blank=True,
                                                                choices=yes_no)
    pid_autoimmunity_MusculoskeletalSymptoms_1 = models.BooleanField(default=False)
    pid_autoimmunity_MusculoskeletalSymptoms_2 = models.BooleanField(default=False)
    pid_autoimmunity_MusculoskeletalSymptoms_3 = models.BooleanField(default=False)
    pid_autoimmunity_MusculoskeletalSymptoms_3_numberJoints = models.CharField(
        max_length=100, blank=True,
        null=True,
        validators=[MaxLengthValidator(100)])
    pid_autoimmunity_MusculoskeletalSymptoms_3_jointDeformity = models.CharField(
        max_length=100, null=True, blank=True, choices=yes_no)
    pid_autoimmunity_MusculoskeletalSymptoms_3_Contractures = models.CharField(
        max_length=100, null=True, blank=True, choices=yes_no)
    pid_autoimmunity_Osteomyelitis = models.CharField(max_length=100, null=True,
                                                      blank=True, choices=yes_no)
    pid_autoimmunity_CNS_Ear_Eye = models.CharField(max_length=100, null=True,
                                                    blank=True, choices=yes_no)
    pid_autoimmunity_CNS_Ear_Eye_1 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye_2 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye3 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye_4 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye_5 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye_6 = models.BooleanField(default=False)
    pid_autoimmunity_CNS_Ear_Eye_7 = models.BooleanField(default=False)
    # pid_autoimmunity_CNS_Ear_Eye_8 = models.BooleanField(default=False)
    pid_Skin_Mucosal = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_Skin_Mucosal_1 = models.BooleanField(default=False)
    pid_Skin_Mucosal_2 = models.BooleanField(default=False)
    pid_Skin_Mucosal_3 = models.BooleanField(default=False)
    pid_Skin_Mucosal_4 = models.BooleanField(default=False)
    pid_Skin_Mucosal_5 = models.BooleanField(default=False)
    pid_Skin_Mucosal_6 = models.BooleanField(default=False)
    pid_Skin_Mucosal_7 = models.BooleanField(default=False)
    pid_Skin_Mucosal_8 = models.BooleanField(default=False)
    pid_autoimmunity_autoinflammation_type_symptoms_fever_other = models.CharField(max_length=100, blank=True,
                                                                                   null=True,
                                                                                   validators=[MaxLengthValidator(100)])
    pid_ALLERGY_ATOPY = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_unknown)
    food_allergy_sel = [('FOOD', 'FOOD'),
                        ('DRUG', 'DRUG'),
                        ('ENVIRONMENTAL', 'ENVIRONMENTAL'),
                        ('OTHERS', 'OTHERS'),
                        ('UNKNOWN', 'UNKNOWN'), ]
    pid_ALLERGY_ATOPY_opn = models.CharField(max_length=100, null=True, blank=True, choices=food_allergy_sel)
    pid_ALLERGY_ATOPY_other_specify = models.CharField(max_length=100, blank=True,
                                                       null=True,
                                                       validators=[MaxLengthValidator(100)])
    pid_MALIGNANCY = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_unknown)

    pid_MALIGNANCY_diagnosis = models.CharField(max_length=100, blank=True,
                                                null=True,
                                                validators=[MaxLengthValidator(100)])
    pid_MALIGNANCY_diagnosis_present_before_diagnosis = models.CharField(max_length=100, null=True, blank=True,
                                                                         choices=yes_no)
    diagnosis_sel = [('Surgery', 'Surgery'),
                     ('Radiation', 'Radiation'),
                     ('Chemo', 'Chemo'),
                     ('Biologic ', 'Biologic '),
                     ('OTHER', 'OTHER'),
                     ('UNKNOWN', 'UNKNOWN'), ]
    pid_MALIGNANCY_diagnosis_options = models.CharField(max_length=100, null=True, blank=True, choices=diagnosis_sel)
    pid_MALIGNANCY_diagnosis_Biologic = models.CharField(max_length=100, blank=True,
                                                         null=True,
                                                         validators=[MaxLengthValidator(100)])
    pid_ORGANISM_ISOLATED_viral = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    viral_sel = [('Cytomegalovirus', 'Cytomegalovirus'),
                 ('Epstein Barr virus', 'Epstein Barr virus'),
                 ('Herpes simplex virus', 'Herpes simplex virus'),
                 ('Adenovirus ', 'Adenovirus '),
                 ('Varicella zoster virus', 'Varicella zoster virus'),
                 ('Parvovirus B19', 'Parvovirus B19'),
                 ('Coronavirus', 'Coronavirus'),
                 ('Dengue', 'Dengue'),
                 ('Other Flavivirus', 'Other Flavivirus'),
                 ('Chikungunya', 'Chikungunya'),
                 ('Parvo virus', 'Parvo virus'),
                 ('Influenza', 'Influenza'),
                 ('Parainfluenza', 'Parainfluenza'),
                 ('Others', 'Others'),
                 ]
    pid_ORGANISM_ISOLATED_viral_1 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_2 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_3 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_4 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_5 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_6 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_7 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_8 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_9 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_10 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_11 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_12 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_13 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_14 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_viral_14_specify = models.CharField(max_length=100, blank=True,
                                                              null=True,
                                                              validators=[MaxLengthValidator(100)])
    pid_ORGANISM_ISOLATED_viral_options = models.CharField(max_length=100, null=True, blank=True, choices=viral_sel)
    pid_ORGANISM_ISOLATED_viral_other_specify = models.CharField(max_length=100, blank=True,
                                                                 null=True,
                                                                 validators=[MaxLengthValidator(100)])
    pid_ORGANISM_ISOLATED_Bacterial = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)

    pid_ORGANISM_ISOLATED_Bacterial_1 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_2 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_3 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_4 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_5 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_6 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_7 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_8 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_9 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_10 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_11 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_12 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_13 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_Bacterial_14 = models.BooleanField(default=False)
    pid_ORGANISM_ISOLATED_bacterial_14_specify = models.CharField(max_length=100, blank=True,
                                                                  null=True,
                                                                  validators=[MaxLengthValidator(100)])
    pid_Fungal = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)

    pid_Fungal_1 = models.BooleanField(default=False)
    pid_Fungal_2 = models.BooleanField(default=False)
    pid_Fungal_3 = models.BooleanField(default=False)
    pid_Fungal_4 = models.BooleanField(default=False)
    pid_Fungal_5 = models.BooleanField(default=False)
    pid_Fungal_6 = models.BooleanField(default=False)

    pid_Fungal_6_specify = models.CharField(max_length=100, blank=True,
                                            null=True,
                                            validators=[MaxLengthValidator(100)])
    pid_Mycobacterial = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)

    pid_Mycobacterial_1 = models.BooleanField(default=False)
    pid_Mycobacterial_2 = models.BooleanField(default=False)
    pid_Mycobacterial_3 = models.BooleanField(default=False)
    pid_FamilyHistory_Consanguinity = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_unknown)
    pid_FamilyHistory_Consanguinity_degree = models.CharField(max_length=50, null=True, blank=True)
    pid_FamilyHistory_HistoryYoung_Children = models.CharField(max_length=100, null=True, blank=True,
                                                               choices=yes_no_unknown)
    pid_FamilyHistory_HistoryYoung_Children_numberSiblingDeaths = models.CharField(max_length=100, blank=True,
                                                                                   null=True,
                                                                                   validators=[MaxLengthValidator(100)])
    death_cause_sel = [('Infection', 'Infection'),
                       ('Malignancy', 'Malignancy'),
                       ('Other', 'Other'),
                       ]
    pid_FamilyHistory_death_cause = models.CharField(max_length=100, null=True, blank=True,
                                                     choices=death_cause_sel)
    pid_FamilyHistory_deaths_male_member = models.CharField(max_length=100, null=True, blank=True,
                                                            choices=yes_no_unknown)
    relation_sel = [('Brother', 'Brother'),
                    ('Maternal uncle', 'Maternal uncle'),
                    ('Other)', 'Other'),
                    ]
    pid_FamilyHistory_deaths_male_member_relations = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=relation_sel)
    pid_FamilyHistory_deaths_male_member_diagnosed_PID = models.CharField(max_length=100, null=True, blank=True,
                                                                          choices=yes_no)
    pid_FamilyHistory_deaths_male_member_diagnosed_PID_diagnosis = models.CharField(max_length=100, blank=True,
                                                                                    null=True,
                                                                                    validators=[
                                                                                        MaxLengthValidator(100)])
    pid_FamilyHistory_deaths_male_member_diagnosed_PID_relation = models.CharField(max_length=100, blank=True,
                                                                                   null=True,
                                                                                   validators=[MaxLengthValidator(100)])
    pid_FamilyHistory_diagnosed_PID_listed_registry = models.CharField(max_length=100, null=True,
                                                                       blank=True, choices=yes_no)
    pid_FamilyHistory_reason_pid_evaluation = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_clinical_exam = models.BooleanField(default=False)
    pid_clinical_exam_Anthropometry_wieght = models.CharField(max_length=100, blank=True,
                                                              null=True,
                                                              validators=[MaxLengthValidator(100)])
    pid_clinical_exam_Anthropometry_Height = models.CharField(max_length=100, blank=True,
                                                              null=True,
                                                              validators=[MaxLengthValidator(100)])
    pid_clinical_exam_Anthropometry_HeadCircumference = models.CharField(max_length=100, blank=True,
                                                                         null=True,
                                                                         validators=[MaxLengthValidator(100)])
    pid_DistinctivePhenotypeaDysmorphicFacies = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_DistinctivePhenotypeaaHypoPigmentedHair = models.CharField(max_length=100, null=True, blank=True,
                                                                   choices=yes_no)
    pid_DistinctivePhenotypeabTeethAbnormalities = models.CharField(max_length=100, null=True, blank=True,
                                                                    choices=yes_no)
    pid_DistinctivePhenotypeacAbsentTonsil = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_DistinctivePhenotypeadOralUlcers = models.CharField(max_length=100, null=True, blank=True, choices=yes_no)
    pid_DistinctivePhenotypeadeSkinHypopigmentation = models.CharField(max_length=100, null=True, blank=True,
                                                                       choices=yes_no)
    pid_DistinctivePhenotypeadefLymphAdenopathy = models.CharField(max_length=100, null=True, blank=True,
                                                                   choices=yes_no)
    lymph_sel = [('Localized single LN', 'Localized single LN'),
                 ('Localized multiple LN', 'Localized multiple LN'),
                 ('•    Generalized)', '•   Generalized'),
                 ]
    pid_DistinctivePhenotypeadefLymphAdenopathy_options = models.CharField(max_length=100, null=True, blank=True,
                                                                           choices=lymph_sel)
    pid_DistinctivePhenotypegHepatosplenomegaly = models.CharField(max_length=100, null=True, blank=True,
                                                                   choices=yes_no)
    pid_DistinctivePhenotypeSkeletalSystemAbnormalities = models.CharField(max_length=100, null=True, blank=True,
                                                                           choices=yes_no)
    present_absent_sel = [('Present', 'Present'),
                          ('Absent', 'Absent'),
                          ]
    pid_DistinctivePhenotypeBCG_Scar = models.CharField(max_length=100, null=True, blank=True,
                                                        choices=present_absent_sel)
    pid_DistinctivePhenotyFindingaRespiratory = models.CharField(max_length=100, blank=True,
                                                                 null=True,
                                                                 validators=[MaxLengthValidator(100)])
    pid_DistinctivePhenotyFindingCardiovascular = models.CharField(max_length=100, blank=True,
                                                                   null=True,
                                                                   validators=[MaxLengthValidator(100)])
    pid_DistinctivePhenotyFindingcAbdominal = models.CharField(max_length=100, blank=True,
                                                               null=True,
                                                               validators=[MaxLengthValidator(100)])
    pid_DistinctivePhenotyFindingdCNS = models.CharField(max_length=100, blank=True,
                                                         null=True,
                                                         validators=[MaxLengthValidator(100)])
    yes_no_sel = [('Present', 'Present'),
                  ('Absent', 'Absent'),
                  ]
    immunodeficiencyaffecting_sel = [('Severe Combined Immune Deficiency', 'Severe Combined Immune Deficiency'),
                                     ('Omenn’s Syndrome', 'Omenn’s Syndrome'),
                                     ('MHC Class II deficiency', 'MHC Class II deficiency'),
                                     ('DOCK8 deficiency', 'DOCK8 deficiency'),
                                     ('Hyper IgM Syndrome', 'Hyper IgM Syndrome'),
                                     ('Others', 'Others'),
                                     ('Unclassified', 'Unclassified'),
                                     ]
    pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                                  choices=yes_no_sel)
    pid_BroadDiagnosisCategoryImmunodeficiencyAffecting = models.CharField(max_length=100, null=True, blank=True,
                                                                           choices=immunodeficiencyaffecting_sel)
    pid_ImmunodeficiencyAffecting_other_specify = models.CharField(max_length=100, blank=True,
                                                                   null=True,
                                                                   validators=[MaxLengthValidator(100)])
    CID_sel = [('Hyper IgE Syndrome', 'Hyper IgE Syndrome'),
               ('Wiskott- Aldrich Syndrome', 'Wiskott- Aldrich Syndrome'),
               ('Ataxia Telangiectasia', 'Ataxia Telangiectasia'),
               ('Di George Syndrome', 'Di George Syndrome'),
               ('Others', 'Others'),
               ('Unclassified', 'Unclassified'),
               ]
    pid_BroadDiagnosisCategoryCIDAssociated_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=yes_no_sel)
    pid_BroadDiagnosisCategoryCIDAssociated = models.CharField(max_length=100, null=True, blank=True,
                                                               choices=CID_sel)
    pid_BroadDiagnosisCategoryCIDAssociated_Other_Specify = models.CharField(max_length=100, blank=True,
                                                                             null=True,
                                                                             validators=[MaxLengthValidator(100)])

    Predominant_sel = [('XLA', 'XLA'),
                       ('CVID', 'CVID'),
                       ('Others', 'Others'),
                       ('Unclassified', 'Unclassified'),
                       ]
    pid_BroadDiagnosisCategoryPredominantAntibody_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                            choices=yes_no_sel)
    pid_BroadDiagnosisCategoryPredominantAntibody = models.CharField(max_length=100, null=True, blank=True,
                                                                     choices=Predominant_sel)
    pid_BroadDiagnosisCategoryPredominantAntibody_other_specify = models.CharField(max_length=100, blank=True,
                                                                                   null=True,
                                                                                   validators=[MaxLengthValidator(100)])

    Diseases_immune_sel = [
        ('Familial Hemophagocytic Lymphohistiocytosis  ', 'Familial Hemophagocytic Lymphohistiocytosis  '),
        ('Autoimmune Lymphoproliferative Syndrome', 'Autoimmune Lymphoproliferative Syndrome '),
        ('Chediak Higashi Syndrome', 'Chediak Higashi Syndrome'),
        ('Griscelli Syndrome', 'Griscelli Syndrome'),
        ('Others', 'Others'),
        ]
    pid_BroadDiagnosisCategoryDiseasesImmune_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                       choices=yes_no_sel)
    pid_BroadDiagnosisCategoryDiseasesImmune = models.CharField(max_length=100, null=True, blank=True,
                                                                choices=Diseases_immune_sel)
    pid_BroadDiagnosisCategoryDiseasesImmune_other_specify = models.CharField(max_length=100, blank=True,
                                                                              null=True,
                                                                              validators=[MaxLengthValidator(100)])
    CongenitalDefects_sel = [('Chronic Granulomatous Disease', 'Chronic Granulomatous Disease'),
                             ('Leucocyte Adhesion Defect', 'Leucocyte Adhesion Defect'),
                             ('Severe Congenital Neutropenia', 'Severe Congenital Neutropenia'),
                             ('Cystic Fibrosis', 'Cystic Fibrosis'),
                             ('Others', 'Others'),
                             ('Unclassified', 'Unclassified'),
                             ]
    pid_BroadDiagnosisCategoryCongenitalDefects_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                          choices=yes_no_sel)
    pid_BroadDiagnosisCategoryCongenitalDefects = models.CharField(max_length=100, null=True, blank=True,
                                                                   choices=CongenitalDefects_sel)
    pid_BroadDiagnosisCategoryCongenitalDefects_other_specify = models.CharField(max_length=100, blank=True,
                                                                                 null=True,
                                                                                 validators=[MaxLengthValidator(100)])
    Defects_intrinsic_sel = [('IRAK4/MyD88 deficiency', 'IRAK4/MyD88 deficiency'),
                             ('Mendelian Susceptibility to Mycobacterial diseases (MSMD)',
                              'Mendelian Susceptibility to Mycobacterial diseases (MSMD)'),
                             ('STAT1 GOF', 'STAT1 GOF'),
                             ('Others', 'Others'),
                             ('Unclassified', 'Unclassified'),
                             ]
    pid_BroadDiagnosisCategoryDefectsIntrinsic_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                         choices=yes_no_sel)
    pid_BroadDiagnosisCategoryDefectsIntrinsic = models.CharField(max_length=100, null=True, blank=True,
                                                                  choices=Defects_intrinsic_sel)
    pid_BroadDiagnosisCategoryDefectsIntrinsic_other_specify = models.CharField(max_length=100, blank=True,
                                                                                null=True,
                                                                                validators=[MaxLengthValidator(100)])

    Autoinflammatory_sel = [('Type I interferonopathies', 'Type I interferonopathies'),
                            ('Familial Mediterranean fever',
                             'Familial Mediterranean fever'),
                            ('Hyper IgD Syndrome', 'Hyper IgD Syndrome'),
                            ('Cryopyrin-associated periodic fever syndromes (CAPS)',
                             'Cryopyrin-associated periodic fever syndromes (CAPS)'),
                            ('Tumor necrosis factor receptor-associated periodic syndrome(TRAPS)',
                             'Tumor necrosis factor receptor-associated periodic syndrome(TRAPS)'),
                            ('Others', 'Others'),
                            ('Unclassified', 'Unclassified'),
                            ]
    pid_BroadDiagnosisCategoryAutoinflammatory_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                         choices=yes_no_sel)
    pid_BroadDiagnosisCategoryAutoinflammatory = models.CharField(max_length=100, null=True, blank=True,
                                                                  choices=Autoinflammatory_sel)
    pid_BroadDiagnosisCategoryAutoinflammatory_other_specify = models.CharField(max_length=100, blank=True,
                                                                                null=True,
                                                                                validators=[MaxLengthValidator(100)])
    Complement_sel = [('C1 esterase inhibitor deficiency', 'C1 esterase inhibitor deficiency'),
                      ('Early complement deficiency (C1q, C2, C3, C4)',
                       'Early complement deficiency (C1q, C2, C3, C4)'),
                      ('Late complement component deficiency (C5 to C9)',
                       'Late complement component deficiency (C5 to C9)'),

                      ]
    pid_BroadDiagnosisCategoryComplementDeficiency_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                             choices=yes_no_sel)
    pid_BroadDiagnosisCategoryComplementDeficiency = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=Complement_sel)
    # pid_BroadDiagnosisCategoryComplementDeficiency_other_specify = models.CharField(max_length=100, blank=True,
    #                                                                           null=True,
    #                                                                          validators=[MaxLengthValidator(100)])
    Marrow_failure_sel = [('Fanconi anemia', 'Fanconi anemia'),
                          ('DKC',
                           'DKC'),
                          ('Others', 'Others'),

                          ]
    pid_BroadDiagnosisCategoryMarrowFailure_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                      choices=yes_no_sel)
    pid_BroadDiagnosisCategoryMarrowFailure = models.CharField(max_length=100, null=True, blank=True,
                                                               choices=Marrow_failure_sel)
    pid_BroadDiagnosisCategoryMarrowFailure_other_specify = models.CharField(max_length=100, blank=True,
                                                                             null=True,
                                                                             validators=[MaxLengthValidator(100)])

    Phenocopies_sel = [('Chronic mucocutaneous candidiasis(associated with autoantibodies)',
                        'Chronic mucocutaneous candidiasis(associated with autoantibodies)'),
                       ('RAS- associated leukoproliferative disease',
                        'RAS- associated leukoproliferative disease'),
                       ('Others', 'Others'),
                       ('Unclassified', 'Unclassified'),

                       ]
    pid_BroadDiagnosisCategoryPhenocopies_yes_no = models.CharField(max_length=100, null=True, blank=True,
                                                                    choices=yes_no_sel)
    pid_BroadDiagnosisCategoryPhenocopies = models.CharField(max_length=100, null=True, blank=True,
                                                             choices=Phenocopies_sel)
    pid_BroadDiagnosisCategoryPhenocopies_other_specify = models.CharField(max_length=100, blank=True,
                                                                           null=True,
                                                                           validators=[MaxLengthValidator(100)])
    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    variant_sel = [('Pathogenic', 'Pathogenic'), ('VUS', 'VUS')]
    yes_no_notknown_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not Known', 'Not Known')]
    zygosity_sel = [('Homozygous', 'Homozygous'), ('Heterozygous', 'Heterozygous'), ('Hemizygous', 'Hemizygous')]
    level_sel = [('High', 'High'), ('Low', 'Low'), ('Normal', 'Normal')]
    absent_low = [('SCID', 'SCID'), ('MHC Class II deficiency', 'MHC Class II deficiency'),
                  ('DOCK8 deficiency', 'DOCK8 deficiency'), ('Hyper IgM Syndrome', 'Hyper IgM Syndrome'),
                  ('Hyper IgE Syndrome', 'Hyper IgE Syndrome'),
                  ('Wiskott Aldrich Syndrome', 'Wiskott Aldrich Syndrome'),
                  ('Ataxia Telangiectasia', 'Ataxia Telangiectasia'), ('Di George Syndrome', 'Di George Syndrome'),
                  ('XLA', 'XLA'), ('CVID', 'CVID'), ('HLH', 'HLH'), ('ALPS', 'ALPS'),
                  ('Chediak Higashi Syndrome', 'Chediak Higashi Syndrome'),
                  ('Griscelli Syndrome', 'Griscelli Syndrome'),
                  ('Chronic Granulomatous Disease', 'Chronic Granulomatous Disease'),
                  ('Leukocyte adhesion Disease', 'Leukocyte adhesion Disease'),
                  ('Severe Congenital Neutropenia', 'Severe Congenital Neutropenia'),
                  ('Cystic Fibrosis', 'Cystic Fibrosis'), ('MSMD', 'MSMD'), ('CMC', 'CMC'),
                  ('IRAK4 deficiency', 'IRAK4 deficiency'), ('Myd88 deficiency', 'Myd88 deficiency'),
                  ('Other,', 'Other')]
    gene_name_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal')]
    mutation_type_sel = [('Complex', 'Complex'), ('Deletion', 'Deletion'),
                         ('Deletion/insertion(Indel)', 'Deletion/insertion(Indel)'), ('Duplication', 'Duplication'),
                         ('Insertion', 'Insertion'), ('Inversion', 'Inversion'), ('Substitution', 'Substitution')]
    gene_name1_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal'), ('Not Done', 'Not Done')]
    gene_name2_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High')]
    tcr_sel = [('Normal', 'Normal'), ('skewed', 'skewed')]
    expression_sel = [('HLH', 'HLH'), ('MSMD', 'MSMD'), ('LAD', 'LAD'),
                      ('XLA', 'XLA'), ('HIGM', 'HIGM'), ('WAS', 'WAS'), ('HIGE', 'HIGE')]
    pid_CBC_Date = models.DateField(null=True, blank=True)
    pid_CBC_Date1 = models.DateField(null=True, blank=True)
    pid_CBC_Date2 = models.DateField(null=True, blank=True)
    pid_CBC_Date3 = models.DateField(null=True, blank=True)
    pid_CBC_Hb = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc1_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_Lymphcytes = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets3 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets1 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets2 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets3 = models.CharField(max_length=50, null=True, blank=True)
    # pid_Lymphocyte_Phenotype =
    pid_phenotype_Absolute_Lymphocyte_count = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_Absolute_Lymphocyte_count_level = models.CharField(max_length=50, null=True, blank=True,
                                                                     choices=level_sel)
    pid_phenotype_CD3_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD3_T_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_CD4_Helper_T = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_Helper_T_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD8_Cytotoxic_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD8_Cytotoxic_T_cells_level = models.CharField(max_length=50, null=True, blank=True,
                                                                 choices=level_sel)
    pid_phenotype_CD19_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD19_B_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD20_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD20_B_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD56CD16_NK_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD56CD16_NK_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD25 = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD25_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_Double_negative_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_Double_negative_T_cells_level = models.CharField(max_length=50, null=True, blank=True,
                                                                   choices=level_sel)
    Gamma_delta_T_cells = models.CharField(max_length=50, null=True, blank=True)
    Gamma_delta_T_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)

    pid_CD4_subset_panel_naive_cd4 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_subset_panel_naive_cd4_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CD4_subset_panel_Total_Memory_CD4 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_subset_panel_Total_Memory_CD4_level = models.CharField(max_length=20, blank=True, null=True,
                                                                   choices=level_sel)
    CD4_CD45RA = models.CharField(max_length=100, blank=True, null=True)
    CD4_CD45RA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    CD4_CD45RO = models.CharField(max_length=100, blank=True, null=True)
    CD4_CD45RO_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_CD8_subset_panel_naive_cd8 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD8_subset_panel_naive_cd8_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CD8_subset_panel_Total_Memory_CD8 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD8_subset_panel_Total_Memory_CD8_level = models.CharField(max_length=20, blank=True, null=True,
                                                                   choices=level_sel)
    CD8_CD45RA = models.CharField(max_length=100, blank=True, null=True)
    CD8_CD45RO = models.CharField(max_length=100, blank=True, null=True)
    CD8_CD45RA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    CD8_CD45RO_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_T_regulatory_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_T_regulatory_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Naive_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Naive_B_cells_Transitional_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_Transitional_B_cells_level = models.CharField(max_length=20, blank=True, null=True,
                                                                    choices=level_sel)
    pid_Naive_B_cells_Memory_B_cell_phenotype = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_Memory_B_cell_phenotype_level = models.CharField(max_length=20, blank=True, null=True,
                                                                       choices=level_sel)
    cd27_B_cells = models.CharField(max_length=50, null=True, blank=True)
    cd27_B_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    cd27_igm_Bcells = models.CharField(max_length=50, null=True, blank=True)
    cd27_igm_Bcells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    cd27_igD_Bcells = models.CharField(max_length=50, null=True, blank=True)
    cd27_igD_Bcells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Immunoglobulin_IgG = models.CharField(max_length=20, blank=True, null=True)
    pid_Immunoglobulin_IgG1 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG4 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgA = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgM = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgE = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgD = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG1_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG4_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgM_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgE_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgD_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Immunoglobulin_IgG2 = models.CharField(max_length=20, blank=True, null=True)
    pid_Immunoglobulin_IgG21 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG22 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG23 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG24 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgA2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgM2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgE2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgD2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG21_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG22_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG23_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG24_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgA2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgM2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgE2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgD2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Immunoglobulin_IgG3 = models.CharField(max_length=20, blank=True, null=True)
    pid_Immunoglobulin_IgG31 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG32 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG33 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG34 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgA3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgM3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgE3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgD3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG31_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG32_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG33_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG34_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgA3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgM3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgE3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgD3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Vaccine_responses_tested = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Vaccine_responses_tested_Protein = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    diphtheria = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    tetanus = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    protien_conjugated_hib = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Polysaccharide = models.CharField(max_length=100, blank=True, null=True,
                                                                   choices=yes_no_sel)
    Polysaccharide_hib = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    salmonella_typhi = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    PHI_174antigen = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Iso_hemagglutinin = models.CharField(max_length=100, blank=True, null=True,
                                                                      choices=yes_no_sel)
    Iso_hemagglutinin_antiA = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Iso_hemagglutinin_antiB = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_TREC_tested = models.CharField(max_length=100, blank=True, null=True,
                                                                choices=yes_no_sel)
    if_yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Lymphocyte_functional_tests = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=yes_no_sel)
    pha = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    anti_cd = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    others = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Expression_studies = models.CharField(max_length=100, blank=True, null=True,
                                                                       choices=yes_no_sel)
    pid_eexpression_studies = models.CharField(max_length=100, blank=True, null=True,
                                               choices=yes_no_sel)
    pid_scid = models.BooleanField(default=False)
    pid_hlh = models.BooleanField(default=False)
    pid_mxc2 = models.BooleanField(default=False)
    pid_foxp3 = models.BooleanField(default=False)
    pid_lad = models.BooleanField(default=False)
    pid_xla = models.BooleanField(default=False)
    pid_msmd = models.BooleanField(default=False)
    pid_higm = models.BooleanField(default=False)
    pid_was = models.BooleanField(default=False)
    pid_hige = models.BooleanField(default=False)
    pid_Expression_studies_HLH_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)

    pid_Expression_Perforin_expression = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD107a_on_NK_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD107a_on_CD8_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD123 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_th1_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name1_sel)
    pid_Expression_hda_hr_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name2_sel)

    pid_Vaccine_responses_tested_MSMD_workup = models.CharField(max_length=100, blank=True, null=True,
                                                                choices=yes_no_sel)
    pid_cd212_lymphocytes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_cd119_monocytes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_ifn_gama_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_stati_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_stat4_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_LAD_workup_on_neutrophils = models.CharField(max_length=100, blank=True, null=True,
                                                                       choices=yes_no_sel)
    cd18 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    cd11 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    btk = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    xla = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Hyper_IgM_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    cd154 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    cd40 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    wasp = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Hyper_IgE_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    DOCK8 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    STAT3 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    TH17 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Complement_function = models.CharField(max_length=100, blank=True, null=True,
                                                                 choices=yes_no_sel)
    C2 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    C3 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    C4 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Cq = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    CH50 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    AH50 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorD = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorH = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorI = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Properdin = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Beta_Repertoire_analysis = models.CharField(max_length=100, blank=True, null=True,
                                                                      choices=yes_no_sel)
    pid_Vaccine_responses_Beta_yesRepertoire_analysis = models.CharField(max_length=100, blank=True, null=True,
                                                                         choices=tcr_sel)
    pid_Vaccine_responses_Auto_antibodies = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    ANA = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_neutrophil_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_platelet_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_C1q_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_C1_esterase_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    ada_enzyme = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pnp_enzyme = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    NBT = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    # pid_Vaccine_responses_Beta_Repertoire_analysis = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Vaccine_responses_DHR = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Flow_cytometric_expression_b558 = models.CharField(max_length=100, blank=True, null=True,
                                                                             choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression1 = models.CharField(max_length=100, blank=True, null=True,
                                                                         choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p67phox = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p40phox = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p22 = models.CharField(max_length=100, blank=True, null=True,
                                                                            choices=gene_name_sel)
    Maternal_engraftment = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Alfa_feto_protein = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Alfa_feto_protein_yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Karyotype = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Karyotype_finding = models.CharField(max_length=100, blank=True, null=True)
    Chromosomal = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Chromosomal_finding = models.CharField(max_length=100, blank=True, null=True)
    Radiological_investigation = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Radiological_investigation_finding = models.CharField(max_length=100, blank=True, null=True)
    FISH = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    FISH_finding = models.CharField(max_length=100, blank=True, null=True)
    any_other = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    any_other_finding = models.CharField(max_length=100, blank=True, null=True)

    pid_Vaccine_responses_Molecular_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                 choices=yes_no_sel)

    # pid_gene_name = models.CharField(max_length=32, blank=True, null=True, choices=gene_name_sel)

    tb_Nscid_sel = [('ADA', 'ADA'), ('AK2', 'AK2'), ('RAC2', 'RAC2'), ('DCLRE1C', 'DCLRE1C'), ('PRKDC', 'PRKDC'),
                    ('RAG1', 'RAG1'), ('RAG2', 'RAG2'), ('LIG4', 'LIG4'), ('NHEJ1', 'NHEJ1'),
                    ('Other/novel(specify)', 'Other/novel(specify)')]
    tb_Pscid_sel = [('IL2RG', 'IL2RG'), ('JAK3', 'JAK3'), ('IL7R', 'IL7R'), ('PTPRC', 'PTPRC'), ('CD3D', 'CD3D'),
                    ('CD3E', 'CD3E'), ('CD3Z', 'CD3Z'), ('CORO1A', 'CORO1A'), ('LAT', 'LAT'),
                    ('Other/novel(specify)', 'Other/novel(specify)')]

    tb_Nscid = models.CharField(max_length=100, blank=True, null=True, choices=tb_Nscid_sel)
    tb_Pscid = models.CharField(max_length=100, blank=True, null=True, choices=tb_Pscid_sel)

    # pid_malignancy_mhc = models.CharField(max_length=100, blank=True, null=True, choices=mhc_sel)
    pid_malignancy_CIITA = models.BooleanField(default=False)
    pid_malignancy_RFXANK = models.BooleanField(default=False)
    pid_malignancy_RFX5 = models.BooleanField(default=False)
    pid_malignancy_RFXAP = models.BooleanField(default=False)
    pid_malignancy_DOCK8 = models.BooleanField(default=False)
    pid_malignancy_CD40 = models.BooleanField(default=False)
    pid_malignancy_CD40L = models.BooleanField(default=False)
    pid_malignancy_STAT3 = models.BooleanField(default=False)
    pid_malignancy_PGM3 = models.BooleanField(default=False)
    pid_malignancy_SPJNKS = models.BooleanField(default=False)
    pid_malignancy_WAS = models.BooleanField(default=False)
    pid_malignancy_ATM = models.BooleanField(default=False)
    pid_malignancy_LDC22 = models.BooleanField(default=False)
    pid_malignancy_BtK = models.BooleanField(default=False)
    pid_malignancy_CVID = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_PRF1 = models.BooleanField(default=False)
    pid_malignancy_STX11 = models.BooleanField(default=False)
    pid_malignancy_UNC13D = models.BooleanField(default=False)
    pid_malignancy_STXBP2 = models.BooleanField(default=False)
    pid_malignancy_FAAP24 = models.BooleanField(default=False)
    pid_hlh_others = models.BooleanField(default=False)
    pid_hlh_other = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_SLC7A7 = models.BooleanField(default=False)
    pid_malignancy_TNFRSF6 = models.BooleanField(default=False)
    pid_malignancy_TNFSF6 = models.BooleanField(default=False)
    pid_malignancy_CASP8 = models.BooleanField(default=False)
    pid_malignancy_CASP10 = models.BooleanField(default=False)
    pid_malignancy_FADD = models.BooleanField(default=False)
    pid_malignancy_LYST = models.BooleanField(default=False)
    pid_malignancy_RAB27A = models.BooleanField(default=False)
    pid_malignancy_CYBB = models.BooleanField(default=False)
    pid_malignancy_NCF1 = models.BooleanField(default=False)
    pid_malignancy_CYBA = models.BooleanField(default=False)
    pid_malignancy_NCF2 = models.BooleanField(default=False)
    pid_malignancy_NCF4 = models.BooleanField(default=False)
    pid_malignancy_CYBC1 = models.BooleanField(default=False)
    pid_malignancy_G6PD = models.BooleanField(default=False)
    pid_malignancy_ITGB2 = models.BooleanField(default=False)
    pid_malignancy_SLC35C1 = models.BooleanField(default=False)
    pid_malignancy_FERMT3 = models.BooleanField(default=False)
    pid_malignancy_ELANE = models.BooleanField(default=False)
    pid_malignancy_HAX1 = models.BooleanField(default=False)
    pid_malignancy_G6PC3 = models.BooleanField(default=False)
    pid_malignancy_GFI1 = models.BooleanField(default=False)
    pid_malignancy_VPS45 = models.BooleanField(default=False)
    pid_malignancy_CFTR = models.BooleanField(default=False)
    pid_malignancy_IFNGR1 = models.BooleanField(default=False)
    pid_malignancy_IFNGR2 = models.BooleanField(default=False)
    pid_malignancy_IL12RB1 = models.BooleanField(default=False)
    pid_malignancy_STAT1 = models.BooleanField(default=False)
    pid_malignancy_TYK2 = models.BooleanField(default=False)
    pid_malignancy_IRF8 = models.BooleanField(default=False)
    pid_malignancy_RORC = models.BooleanField(default=False)
    pid_malignancy_ISG15 = models.BooleanField(default=False)
    pid_malignancy_IL12B = models.BooleanField(default=False)
    pid_malignancy_IL12RB2 = models.BooleanField(default=False)
    pid_malignancy_IL23 = models.BooleanField(default=False)
    pid_malignancy_SPPL2A = models.BooleanField(default=False)
    pid_malignancy_JAK1 = models.BooleanField(default=False)
    pid_malignancy_STAT1GOF = models.BooleanField(default=False)
    pid_malignancy_IL17F = models.BooleanField(default=False)
    pid_malignancy_IL17RA = models.BooleanField(default=False)
    pid_malignancy_IL17RC = models.BooleanField(default=False)
    pid_malignancy_IRAK4 = models.BooleanField(default=False)
    pid_malignancy_Myd88 = models.BooleanField(default=False)

    pid_malignancy_Others_specify = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])

    tb_Nscid1 = models.CharField(max_length=100, blank=True, null=True, choices=tb_Nscid_sel)
    tb_Pscid1 = models.CharField(max_length=100, blank=True, null=True, choices=tb_Pscid_sel)

    # pid_malignancy_mhc = models.CharField(max_length=100, blank=True, null=True, choices=mhc_sel)
    pid_malignancy_CIITA1 = models.BooleanField(default=False)
    pid_malignancy_RFXANK1 = models.BooleanField(default=False)
    pid_malignancy_RFX5_1 = models.BooleanField(default=False)
    pid_malignancy_RFXAP1 = models.BooleanField(default=False)
    pid_malignancy_DOCK8_1 = models.BooleanField(default=False)
    pid_malignancy_CD40_1 = models.BooleanField(default=False)
    pid_malignancy_CD40L_1 = models.BooleanField(default=False)
    pid_malignancy_STAT3_1 = models.BooleanField(default=False)
    pid_malignancy_PGM3_1 = models.BooleanField(default=False)
    pid_malignancy_SPJNKS1 = models.BooleanField(default=False)
    pid_malignancy_WAS1 = models.BooleanField(default=False)
    pid_malignancy_ATM1 = models.BooleanField(default=False)
    pid_malignancy_LDC22_1 = models.BooleanField(default=False)
    pid_malignancy_BtK1 = models.BooleanField(default=False)
    pid_malignancy_CVID1 = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_PRF1_1 = models.BooleanField(default=False)
    pid_malignancy_STX11_1 = models.BooleanField(default=False)
    pid_malignancy_UNC13D1 = models.BooleanField(default=False)
    pid_malignancy_STXBP21 = models.BooleanField(default=False)
    pid_malignancy_FAAP24_1 = models.BooleanField(default=False)
    pid_hlh_others_1 = models.BooleanField(default=False)
    pid_hlh_other_1 = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_SLC7A7_1 = models.BooleanField(default=False)
    pid_malignancy_TNFRSF6_1 = models.BooleanField(default=False)
    pid_malignancy_TNFSF6_1 = models.BooleanField(default=False)
    pid_malignancy_CASP8_1 = models.BooleanField(default=False)
    pid_malignancy_CASP10_1 = models.BooleanField(default=False)
    pid_malignancy_FADD1 = models.BooleanField(default=False)
    pid_malignancy_LYST1 = models.BooleanField(default=False)
    pid_malignancy_RAB27A1 = models.BooleanField(default=False)
    pid_malignancy_CYBB1 = models.BooleanField(default=False)
    pid_malignancy_NCF1_1 = models.BooleanField(default=False)
    pid_malignancy_CYBA1 = models.BooleanField(default=False)
    pid_malignancy_NCF2_1 = models.BooleanField(default=False)
    pid_malignancy_NCF4_1 = models.BooleanField(default=False)
    pid_malignancy_CYBC1_1 = models.BooleanField(default=False)
    pid_malignancy_G6PD1 = models.BooleanField(default=False)
    pid_malignancy_ITGB2_1 = models.BooleanField(default=False)
    pid_malignancy_SLC35C1_1 = models.BooleanField(default=False)
    pid_malignancy_FERMT3_1 = models.BooleanField(default=False)
    pid_malignancy_ELANE1 = models.BooleanField(default=False)
    pid_malignancy_HAX1_1 = models.BooleanField(default=False)
    pid_malignancy_G6PC3_1 = models.BooleanField(default=False)
    pid_malignancy_GFI1_1 = models.BooleanField(default=False)
    pid_malignancy_VPS45_1 = models.BooleanField(default=False)
    pid_malignancy_CFTR1 = models.BooleanField(default=False)
    pid_malignancy_IFNGR1_1 = models.BooleanField(default=False)
    pid_malignancy_IFNGR2_1 = models.BooleanField(default=False)
    pid_malignancy_IL12RB1_1 = models.BooleanField(default=False)
    pid_malignancy_STAT1_1 = models.BooleanField(default=False)
    pid_malignancy_TYK2_1 = models.BooleanField(default=False)
    pid_malignancy_IRF8_1 = models.BooleanField(default=False)
    pid_malignancy_RORC1 = models.BooleanField(default=False)
    pid_malignancy_ISG15_1 = models.BooleanField(default=False)
    pid_malignancy_IL12B1 = models.BooleanField(default=False)
    pid_malignancy_IL12RB2_1 = models.BooleanField(default=False)
    pid_malignancy_IL23_1 = models.BooleanField(default=False)
    pid_malignancy_SPPL2A1 = models.BooleanField(default=False)
    pid_malignancy_JAK1_1 = models.BooleanField(default=False)
    pid_malignancy_STAT1GOF1 = models.BooleanField(default=False)
    pid_malignancy_IL17F1 = models.BooleanField(default=False)
    pid_malignancy_IL17RA1 = models.BooleanField(default=False)
    pid_malignancy_IL17RC1 = models.BooleanField(default=False)
    pid_malignancy_IRAK4_1 = models.BooleanField(default=False)
    pid_malignancy_Myd88_1 = models.BooleanField(default=False)

    pid_malignancy_Others_specify1 = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])

    tb_Nscid2 = models.CharField(max_length=100, blank=True, null=True, choices=tb_Nscid_sel)
    tb_Pscid2 = models.CharField(max_length=100, blank=True, null=True, choices=tb_Pscid_sel)

    # pid_malignancy_mhc = models.CharField(max_length=100, blank=True, null=True, choices=mhc_sel)
    pid_malignancy_CIITA2 = models.BooleanField(default=False)
    pid_malignancy_RFXANK2 = models.BooleanField(default=False)
    pid_malignancy_RFX5_2 = models.BooleanField(default=False)
    pid_malignancy_RFXAP2 = models.BooleanField(default=False)
    pid_malignancy_DOCK8_2 = models.BooleanField(default=False)
    pid_malignancy_CD40_2 = models.BooleanField(default=False)
    pid_malignancy_CD40L2 = models.BooleanField(default=False)
    pid_malignancy_STAT3_2 = models.BooleanField(default=False)
    pid_malignancy_PGM3_2 = models.BooleanField(default=False)
    pid_malignancy_SPJNKS2 = models.BooleanField(default=False)
    pid_malignancy_WAS2 = models.BooleanField(default=False)
    pid_malignancy_ATM2 = models.BooleanField(default=False)
    pid_malignancy_LDC22_2 = models.BooleanField(default=False)
    pid_malignancy_BtK2 = models.BooleanField(default=False)
    pid_malignancy_CVID2 = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_PRF1_2 = models.BooleanField(default=False)
    pid_malignancy_STX11_2 = models.BooleanField(default=False)
    pid_malignancy_UNC13D2 = models.BooleanField(default=False)
    pid_malignancy_STXBP2_2 = models.BooleanField(default=False)
    pid_malignancy_FAAP24_2 = models.BooleanField(default=False)
    pid_hlh_others2 = models.BooleanField(default=False)
    pid_hlh_other2 = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_SLC7A7_2 = models.BooleanField(default=False)
    pid_malignancy_TNFRSF6_2 = models.BooleanField(default=False)
    pid_malignancy_TNFSF6_2 = models.BooleanField(default=False)
    pid_malignancy_CASP8_2 = models.BooleanField(default=False)
    pid_malignancy_CASP10_2 = models.BooleanField(default=False)
    pid_malignancy_FADD2 = models.BooleanField(default=False)
    pid_malignancy_LYST2 = models.BooleanField(default=False)
    pid_malignancy_RAB27A_2 = models.BooleanField(default=False)
    pid_malignancy_CYBB2 = models.BooleanField(default=False)
    pid_malignancy_NCF1_2 = models.BooleanField(default=False)
    pid_malignancy_CYBA2 = models.BooleanField(default=False)
    pid_malignancy_NCF2_2 = models.BooleanField(default=False)
    pid_malignancy_NCF4_2 = models.BooleanField(default=False)
    pid_malignancy_CYBC1_2 = models.BooleanField(default=False)
    pid_malignancy_G6PD2 = models.BooleanField(default=False)
    pid_malignancy_ITGB2_2 = models.BooleanField(default=False)
    pid_malignancy_SLC35C1_2 = models.BooleanField(default=False)
    pid_malignancy_FERMT3_2 = models.BooleanField(default=False)
    pid_malignancy_ELANE2 = models.BooleanField(default=False)
    pid_malignancy_HAX1_2 = models.BooleanField(default=False)
    pid_malignancy_G6PC3_2 = models.BooleanField(default=False)
    pid_malignancy_GFI1_2 = models.BooleanField(default=False)
    pid_malignancy_VPS45_2 = models.BooleanField(default=False)
    pid_malignancy_CFTR2 = models.BooleanField(default=False)
    pid_malignancy_IFNGR1_2 = models.BooleanField(default=False)
    pid_malignancy_IFNGR2_2 = models.BooleanField(default=False)
    pid_malignancy_IL12RB1_2 = models.BooleanField(default=False)
    pid_malignancy_STAT1_2 = models.BooleanField(default=False)
    pid_malignancy_TYK2_2 = models.BooleanField(default=False)
    pid_malignancy_IRF8_2 = models.BooleanField(default=False)
    pid_malignancy_RORC2 = models.BooleanField(default=False)
    pid_malignancy_ISG15_2 = models.BooleanField(default=False)
    pid_malignancy_IL12B2 = models.BooleanField(default=False)
    pid_malignancy_IL12RB2_2 = models.BooleanField(default=False)
    pid_malignancy_IL23_2 = models.BooleanField(default=False)
    pid_malignancy_SPPL2A2 = models.BooleanField(default=False)
    pid_malignancy_JAK1_2 = models.BooleanField(default=False)
    pid_malignancy_STAT1GOF2 = models.BooleanField(default=False)
    pid_malignancy_IL17F2 = models.BooleanField(default=False)
    pid_malignancy_IL17RA2 = models.BooleanField(default=False)
    pid_malignancy_IL17RC2 = models.BooleanField(default=False)
    pid_malignancy_IRAK4_2 = models.BooleanField(default=False)
    pid_malignancy_Myd88_2 = models.BooleanField(default=False)

    pid_malignancy_Others_specify2 = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])

    pid_mutation_type = models.CharField(max_length=100, blank=True, null=True, choices=mutation_type_sel)
    pid_type_of_variant = models.CharField(max_length=100, blank=True, null=True, choices=variant_sel)
    pid_zygosity = models.CharField(max_length=100, blank=True, null=True, choices=zygosity_sel)
    pid_DNA_change = models.CharField(max_length=100, blank=True, null=True)
    pid_Protein_expressed_checked = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Protein_expressed = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_notknown_sel)

    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    variant_sel = [('Pathogenic', 'Pathogenic'), ('VUS', 'VUS')]
    yes_no_notknown_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not Known', 'Not Known')]
    zygosity_sel = [('Homozygous', 'Homozygous'), ('Heterozygous', 'Heterozygous'), ('Hemizygous', 'Hemizygous')]
    level_sel = [('High', 'High'), ('Low', 'Low'), ('Normal', 'Normal')]
    absent_low = [('SCID', 'SCID'), ('MHC Class II deficiency', 'MHC Class II deficiency'),
                  ('DOCK8 deficiency', 'DOCK8 deficiency'), ('Hyper IgM Syndrome', 'Hyper IgM Syndrome'),
                  ('Hyper IgE Syndrome', 'Hyper IgE Syndrome'),
                  ('Wiskott Aldrich Syndrome', 'Wiskott Aldrich Syndrome'),
                  ('Ataxia Telangiectasia', 'Ataxia Telangiectasia'), ('Di George Syndrome', 'Di George Syndrome'),
                  ('XLA', 'XLA'), ('CVID', 'CVID'), ('HLH', 'HLH'), ('ALPS', 'ALPS'),
                  ('Chediak Higashi Syndrome', 'Chediak Higashi Syndrome'),
                  ('Griscelli Syndrome', 'Griscelli Syndrome'),
                  ('Chronic Granulomatous Disease', 'Chronic Granulomatous Disease'),
                  ('Leukocyte adhesion Disease', 'Leukocyte adhesion Disease'),
                  ('Severe Congenital Neutropenia', 'Severe Congenital Neutropenia'),
                  ('Cystic Fibrosis', 'Cystic Fibrosis'), ('MSMD', 'MSMD'), ('CMC', 'CMC'),
                  ('IRAK4 deficiency', 'IRAK4 deficiency'), ('Myd88 deficiency', 'Myd88 deficiency'),
                  ('Other,', 'Other')]
    gene_name_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal')]
    mutation_type_sel = [('Complex', 'Complex'), ('Deletion', 'Deletion'),
                         ('Deletion/insertion(Indel)', 'Deletion/insertion(Indel)'), ('Duplication', 'Duplication'),
                         ('Insertion', 'Insertion'), ('Inversion', 'Inversion'), ('Substitution', 'Substitution')]
    gene_name1_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal'), ('Not Done', 'Not Done')]
    gene_name2_sel = [('Absent', 'Absent'), ('Low', 'Low'), ('Normal', 'Normal'), ('High', 'High')]
    tcr_sel = [('Normal', 'Normal'), ('skewed', 'skewed')]
    expression_sel = [('HLH', 'HLH'), ('MSMD', 'MSMD'), ('LAD', 'LAD'),
                      ('XLA', 'XLA'), ('HIGM', 'HIGM'), ('WAS', 'WAS'), ('HIGE', 'HIGE')]
    pid_CBC_Date = models.DateField(null=True, blank=True)
    pid_CBC_Date1 = models.DateField(null=True, blank=True)
    pid_CBC_Date2 = models.DateField(null=True, blank=True)
    pid_CBC_Date3 = models.DateField(null=True, blank=True)
    pid_CBC_Hb = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Hb3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_wbc_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc1_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_wbc3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CBC_Lymphcytes = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Lymphcytes3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_PMN3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Eosinophils3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Basophils3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Monocytes3 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets1 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets2 = models.CharField(max_length=50, null=True, blank=True)
    pid_CBC_Platelets3 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets1 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets2 = models.CharField(max_length=50, null=True, blank=True)
    pid_M_Platelets3 = models.CharField(max_length=50, null=True, blank=True)
    # pid_Lymphocyte_Phenotype =
    pid_phenotype_Absolute_Lymphocyte_count = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_Absolute_Lymphocyte_count_level = models.CharField(max_length=50, null=True, blank=True,
                                                                     choices=level_sel)
    pid_phenotype_CD3_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD3_T_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_CD4_Helper_T = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_Helper_T_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD8_Cytotoxic_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD8_Cytotoxic_T_cells_level = models.CharField(max_length=50, null=True, blank=True,
                                                                 choices=level_sel)
    pid_phenotype_CD19_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD19_B_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD20_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD20_B_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD56CD16_NK_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD56CD16_NK_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_CD25 = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_CD25_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)
    pid_phenotype_Double_negative_T_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_phenotype_Double_negative_T_cells_level = models.CharField(max_length=50, null=True, blank=True,
                                                                   choices=level_sel)
    Gamma_delta_T_cells = models.CharField(max_length=50, null=True, blank=True)
    Gamma_delta_T_cells_level = models.CharField(max_length=50, null=True, blank=True, choices=level_sel)

    pid_CD4_subset_panel_naive_cd4 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_subset_panel_naive_cd4_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CD4_subset_panel_Total_Memory_CD4 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD4_subset_panel_Total_Memory_CD4_level = models.CharField(max_length=20, blank=True, null=True,
                                                                   choices=level_sel)
    CD4_CD45RA = models.CharField(max_length=100, blank=True, null=True)
    CD4_CD45RA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    CD4_CD45RO = models.CharField(max_length=100, blank=True, null=True)
    CD4_CD45RO_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_CD8_subset_panel_naive_cd8 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD8_subset_panel_naive_cd8_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_CD8_subset_panel_Total_Memory_CD8 = models.CharField(max_length=50, null=True, blank=True)
    pid_CD8_subset_panel_Total_Memory_CD8_level = models.CharField(max_length=20, blank=True, null=True,
                                                                   choices=level_sel)
    CD8_CD45RA = models.CharField(max_length=100, blank=True, null=True)
    CD8_CD45RO = models.CharField(max_length=100, blank=True, null=True)
    CD8_CD45RA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    CD8_CD45RO_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_T_regulatory_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_T_regulatory_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Naive_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Naive_B_cells_Transitional_B_cells = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_Transitional_B_cells_level = models.CharField(max_length=20, blank=True, null=True,
                                                                    choices=level_sel)
    pid_Naive_B_cells_Memory_B_cell_phenotype = models.CharField(max_length=50, null=True, blank=True)
    pid_Naive_B_cells_Memory_B_cell_phenotype_level = models.CharField(max_length=20, blank=True, null=True,
                                                                       choices=level_sel)
    cd27_B_cells = models.CharField(max_length=50, null=True, blank=True)
    cd27_B_cells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    cd27_igm_Bcells = models.CharField(max_length=50, null=True, blank=True)
    cd27_igm_Bcells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    cd27_igD_Bcells = models.CharField(max_length=50, null=True, blank=True)
    cd27_igD_Bcells_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Immunoglobulin_IgG = models.CharField(max_length=20, blank=True, null=True)
    pid_Immunoglobulin_IgG1 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG2 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG3 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG4 = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgA = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgM = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgE = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgD = models.CharField(max_length=50, null=True, blank=True)
    pid_Immunoglobulin_IgG_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG1_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG2_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG3_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgG4_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgA_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgM_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgE_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)
    pid_Immunoglobulin_IgD_level = models.CharField(max_length=20, blank=True, null=True, choices=level_sel)

    pid_Vaccine_responses_tested = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Vaccine_responses_tested_Protein = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    diphtheria = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    tetanus = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    protien_conjugated_hib = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Polysaccharide = models.CharField(max_length=100, blank=True, null=True,
                                                                   choices=yes_no_sel)
    Polysaccharide_hib = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    salmonella_typhi = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    PHI_174antigen = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Iso_hemagglutinin = models.CharField(max_length=100, blank=True, null=True,
                                                                      choices=yes_no_sel)
    Iso_hemagglutinin_antiA = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Iso_hemagglutinin_antiB = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_TREC_tested = models.CharField(max_length=100, blank=True, null=True,
                                                                choices=yes_no_sel)
    if_yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Lymphocyte_functional_tests = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=yes_no_sel)
    pha = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    anti_cd = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    others = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_tested_Expression_studies = models.CharField(max_length=100, blank=True, null=True,
                                                                       choices=yes_no_sel)
    pid_eexpression_studies = models.CharField(max_length=100, blank=True, null=True,
                                               choices=yes_no_sel)
    pid_scid = models.BooleanField(default=False)
    pid_hlh = models.BooleanField(default=False)
    pid_mxc2 = models.BooleanField(default=False)
    pid_foxp3 = models.BooleanField(default=False)
    pid_lad = models.BooleanField(default=False)
    pid_xla = models.BooleanField(default=False)
    pid_msmd = models.BooleanField(default=False)
    pid_higm = models.BooleanField(default=False)
    pid_was = models.BooleanField(default=False)
    pid_hige = models.BooleanField(default=False)
    pid_Expression_studies_HLH_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)

    pid_Expression_Perforin_expression = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD107a_on_NK_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD107a_on_CD8_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_CD123 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_Expression_th1_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name1_sel)
    pid_Expression_hda_hr_cells = models.CharField(max_length=100, blank=True, null=True, choices=gene_name2_sel)

    pid_Vaccine_responses_tested_MSMD_workup = models.CharField(max_length=100, blank=True, null=True,
                                                                choices=yes_no_sel)
    pid_cd212_lymphocytes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_cd119_monocytes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_ifn_gama_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_stati_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pid_stat4_monocyte = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_LAD_workup_on_neutrophils = models.CharField(max_length=100, blank=True, null=True,
                                                                       choices=yes_no_sel)
    cd18 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    cd11 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    btk = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    xla = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Hyper_IgM_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    cd154 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    cd40 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    wasp = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Hyper_IgE_workup = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    DOCK8 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    STAT3 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    TH17 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Complement_function = models.CharField(max_length=100, blank=True, null=True,
                                                                 choices=yes_no_sel)
    C2 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    C3 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    C4 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Cq = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    CH50 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    AH50 = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorD = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorH = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    factorI = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Properdin = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Beta_Repertoire_analysis = models.CharField(max_length=100, blank=True, null=True,
                                                                      choices=yes_no_sel)
    pid_Vaccine_responses_Beta_yesRepertoire_analysis = models.CharField(max_length=100, blank=True, null=True,
                                                                         choices=tcr_sel)
    pid_Vaccine_responses_Auto_antibodies = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    ANA = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_neutrophil_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_platelet_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_C1q_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Anti_C1_esterase_antibody = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    ada_enzyme = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    pnp_enzyme = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    NBT = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    # pid_Vaccine_responses_Beta_Repertoire_analysis = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Vaccine_responses_DHR = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)

    pid_Vaccine_responses_Flow_cytometric_expression_b558 = models.CharField(max_length=100, blank=True, null=True,
                                                                             choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression1 = models.CharField(max_length=100, blank=True, null=True,
                                                                         choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p67phox = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p40phox = models.CharField(max_length=100, blank=True, null=True,
                                                                                choices=gene_name_sel)
    pid_Vaccine_responses_Flow_cytometric_expression_p22 = models.CharField(max_length=100, blank=True, null=True,
                                                                            choices=gene_name_sel)
    Maternal_engraftment = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Alfa_feto_protein = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Alfa_feto_protein_yes = models.CharField(max_length=100, blank=True, null=True, choices=gene_name_sel)
    Karyotype = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Karyotype_finding = models.CharField(max_length=100, blank=True, null=True)
    Chromosomal = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Chromosomal_finding = models.CharField(max_length=100, blank=True, null=True)
    Radiological_investigation = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Radiological_investigation_finding = models.CharField(max_length=100, blank=True, null=True)
    FISH = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    FISH_finding = models.CharField(max_length=100, blank=True, null=True)
    any_other = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    any_other_finding = models.CharField(max_length=100, blank=True, null=True)

    pid_Vaccine_responses_Molecular_diagnosis = models.CharField(max_length=100, blank=True, null=True,
                                                                 choices=yes_no_sel)

    # pid_gene_name = models.CharField(max_length=32, blank=True, null=True, choices=gene_name_sel)

    tb_Nscid_sel = [('ADA', 'ADA'), ('AK2', 'AK2'), ('RAC2', 'RAC2'), ('DCLRE1C', 'DCLRE1C'), ('PRKDC', 'PRKDC'),
                    ('RAG1', 'RAG1'), ('RAG2', 'RAG2'), ('LIG4', 'LIG4'), ('NHEJ1', 'NHEJ1'),
                    ('Other/novel(specify)', 'Other/novel(specify)')]
    tb_Pscid_sel = [('IL2RG', 'IL2RG'), ('JAK3', 'JAK3'), ('IL7R', 'IL7R'), ('PTPRC', 'PTPRC'), ('CD3D', 'CD3D'),
                    ('CD3E', 'CD3E'), ('CD3Z', 'CD3Z'), ('CORO1A', 'CORO1A'), ('LAT', 'LAT'),
                    ('Other/novel(specify)', 'Other/novel(specify)')]

    tb_Nscid = models.CharField(max_length=100, blank=True, null=True, choices=tb_Nscid_sel)
    tb_Pscid = models.CharField(max_length=100, blank=True, null=True, choices=tb_Pscid_sel)

    # pid_malignancy_mhc = models.CharField(max_length=100, blank=True, null=True, choices=mhc_sel)
    pid_malignancy_CIITA = models.BooleanField(default=False)
    pid_malignancy_RFXANK = models.BooleanField(default=False)
    pid_malignancy_RFX5 = models.BooleanField(default=False)
    pid_malignancy_RFXAP = models.BooleanField(default=False)
    pid_malignancy_DOCK8 = models.BooleanField(default=False)
    pid_malignancy_CD40 = models.BooleanField(default=False)
    pid_malignancy_CD40L = models.BooleanField(default=False)
    pid_malignancy_STAT3 = models.BooleanField(default=False)
    pid_malignancy_PGM3 = models.BooleanField(default=False)
    pid_malignancy_SPJNKS = models.BooleanField(default=False)
    pid_malignancy_WAS = models.BooleanField(default=False)
    pid_malignancy_ATM = models.BooleanField(default=False)
    pid_malignancy_LDC22 = models.BooleanField(default=False)
    pid_malignancy_BtK = models.BooleanField(default=False)
    pid_malignancy_CVID = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_PRF1 = models.BooleanField(default=False)
    pid_malignancy_STX11 = models.BooleanField(default=False)
    pid_malignancy_UNC13D = models.BooleanField(default=False)
    pid_malignancy_STXBP2 = models.BooleanField(default=False)
    pid_malignancy_FAAP24 = models.BooleanField(default=False)
    pid_hlh_others = models.BooleanField(default=False)
    pid_hlh_other = models.CharField(max_length=100, blank=True, null=True, )
    pid_malignancy_SLC7A7 = models.BooleanField(default=False)
    pid_malignancy_TNFRSF6 = models.BooleanField(default=False)
    pid_malignancy_TNFSF6 = models.BooleanField(default=False)
    pid_malignancy_CASP8 = models.BooleanField(default=False)
    pid_malignancy_CASP10 = models.BooleanField(default=False)
    pid_malignancy_FADD = models.BooleanField(default=False)
    pid_malignancy_LYST = models.BooleanField(default=False)
    pid_malignancy_RAB27A = models.BooleanField(default=False)
    pid_malignancy_CYBB = models.BooleanField(default=False)
    pid_malignancy_NCF1 = models.BooleanField(default=False)
    pid_malignancy_CYBA = models.BooleanField(default=False)
    pid_malignancy_NCF2 = models.BooleanField(default=False)
    pid_malignancy_NCF4 = models.BooleanField(default=False)
    pid_malignancy_CYBC1 = models.BooleanField(default=False)
    pid_malignancy_G6PD = models.BooleanField(default=False)
    pid_malignancy_ITGB2 = models.BooleanField(default=False)
    pid_malignancy_SLC35C1 = models.BooleanField(default=False)
    pid_malignancy_FERMT3 = models.BooleanField(default=False)
    pid_malignancy_ELANE = models.BooleanField(default=False)
    pid_malignancy_HAX1 = models.BooleanField(default=False)
    pid_malignancy_G6PC3 = models.BooleanField(default=False)
    pid_malignancy_GFI1 = models.BooleanField(default=False)
    pid_malignancy_VPS45 = models.BooleanField(default=False)
    pid_malignancy_CFTR = models.BooleanField(default=False)
    pid_malignancy_IFNGR1 = models.BooleanField(default=False)
    pid_malignancy_IFNGR2 = models.BooleanField(default=False)
    pid_malignancy_IL12RB1 = models.BooleanField(default=False)
    pid_malignancy_STAT1 = models.BooleanField(default=False)
    pid_malignancy_TYK2 = models.BooleanField(default=False)
    pid_malignancy_IRF8 = models.BooleanField(default=False)
    pid_malignancy_RORC = models.BooleanField(default=False)
    pid_malignancy_ISG15 = models.BooleanField(default=False)
    pid_malignancy_IL12B = models.BooleanField(default=False)
    pid_malignancy_IL12RB2 = models.BooleanField(default=False)
    pid_malignancy_IL23 = models.BooleanField(default=False)
    pid_malignancy_SPPL2A = models.BooleanField(default=False)
    pid_malignancy_JAK1 = models.BooleanField(default=False)
    pid_malignancy_STAT1GOF = models.BooleanField(default=False)
    pid_malignancy_IL17F = models.BooleanField(default=False)
    pid_malignancy_IL17RA = models.BooleanField(default=False)
    pid_malignancy_IL17RC = models.BooleanField(default=False)
    pid_malignancy_IRAK4 = models.BooleanField(default=False)
    pid_malignancy_Myd88 = models.BooleanField(default=False)

    pid_malignancy_Others_specify = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    pid_mutation_type = models.CharField(max_length=100, blank=True, null=True, choices=mutation_type_sel)
    pid_type_of_variant = models.CharField(max_length=100, blank=True, null=True, choices=variant_sel)
    pid_zygosity = models.CharField(max_length=100, blank=True, null=True, choices=zygosity_sel)
    pid_DNA_change = models.CharField(max_length=100, blank=True, null=True)
    pid_Protein_expressed_checked = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Protein_expressed = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_notknown_sel)
    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    drug_route_sel = [('IV', 'IV'), ('Oral', 'Oral')]
    yes_no_notknown_sel = [('Yes', 'Yes'), ('No', 'No'), ('Not Known', 'Not Known')]
    death_cause_sel = [('Infection', 'Infection'), ('Malignancy', 'Malignancy'), ('Other, specify', 'Other, specify')]
    course_sel = [('Continuous', 'Continuous'), ('Intermittent', 'Intermittent'), ('rotating', 'rotating')]
    reaction_sel = [('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')]
    course_number = [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('greater than 3', 'greater than 3')]
    indication_sel = [('Treat disease', 'Treat disease'), ('Prophylaxis', 'Prophylaxis'),
                      ('pre transplant', 'pre transplant'), ('post transplant', 'post transplant'),
                      ('unknown', 'unknown')]
    imm_indication_sel = [('Prophylaxis', 'Prophylaxis'), ('acute infection', 'acute infection'),
                          ('chronic infection', 'chronic infection'), ('unknown', 'unknown')]
    type_of_transplant_sel = [('Sibling – partial match', 'Sibling – partial match'),
                              ('•Sibling – full match', '•Sibling – full match'),
                              ('Haploidentical – parental donor', 'Haploidentical – parental donor'),
                              ('Other related – full match', 'Other related – full match'),
                              ('Other related – partial match', 'Other related – partial match'),
                              ('Unrelated- full match', 'Unrelated- full match'),
                              ('Unrelated – partial match', 'Unrelated – partial match')]
    route_sel = [('IV', 'IV'), ('IM', 'IM'), ('SC', 'SC'), ('Unknown', 'Unknown')]
    tretment_sel = [('Ayurvedic', 'Ayurvedic'), ('acupuncture', 'acupuncture'), ('herbal remedies', 'herbal remedies'),
                    ('homopathic', 'homopathic'), ('other', 'other')]
    trasplant_sel = [('Sibling – full match', 'Sibling – full match'),
                     ('Sibling – partial match', 'Sibling – partial match'),
                     ('Haploidentical – parental donor', 'Haploidentical – parental donor'),
                     ('Other related – full match ', 'Other related – full match'),
                     ('Other related – partial match', 'Other related – partial match'),
                     ('Unrelated- full match', 'Unrelated- full match'),
                     ('Unrelated – partial match', 'Unrelated – partial match')]
    pid_has_patient_received_replacement_therapy = models.CharField(max_length=100, blank=True, null=True,
                                                                    choices=yes_no_notknown_sel)
    pid_is_patient_currently_replacement_therapy = models.CharField(max_length=100, blank=True, null=True,
                                                                    choices=yes_no_sel)
    pid_Date_of_initiation_of_therapy_1 = models.DateTimeField(null=True, blank=True)
    pid_age1 = models.CharField(max_length=100, blank=True, null=True)
    pid_Date_of_termination_of_therapy_2 = models.DateTimeField(null=True, blank=True)
    pid_dose = models.CharField(max_length=50, null=True, blank=True)
    pid_route11 = models.CharField(max_length=100, blank=True, null=True, choices=route_sel)
    pid_frequency = models.CharField(max_length=50, null=True, blank=True)
    pid_reaction = models.CharField(max_length=100, blank=True, null=True, choices=reaction_sel)
    pid_Has_patient_used_anti_infective_medication = models.CharField(max_length=100, blank=True, null=True,
                                                                      choices=yes_no_sel)
    pid_courses_of_antibiotic_treatment_has_the_patient = models.CharField(max_length=100, blank=True, null=True,
                                                                           choices=course_number)
    pid_drug_name = models.CharField(max_length=1000, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_indication = models.CharField(max_length=100, blank=True, null=True, choices=imm_indication_sel)
    pid_route = models.CharField(max_length=100, blank=True, null=True, choices=drug_route_sel)
    pid_course = models.CharField(max_length=100, blank=True, null=True, choices=course_sel)
    pid_adverse_reaction = models.CharField(max_length=1000, blank=True, null=True,
                                            validators=[MaxLengthValidator(100)])

    pid_drug_name1 = models.CharField(max_length=1000, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_indication1 = models.CharField(max_length=100, blank=True, null=True, choices=imm_indication_sel)
    pid_route1 = models.CharField(max_length=100, blank=True, null=True, choices=drug_route_sel)
    pid_course1 = models.CharField(max_length=100, blank=True, null=True, choices=course_sel)
    pid_adverse_reaction1 = models.CharField(max_length=1000, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    pid_drug_name2 = models.CharField(max_length=1000, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_indication2 = models.CharField(max_length=100, blank=True, null=True, choices=imm_indication_sel)
    pid_route2 = models.CharField(max_length=100, blank=True, null=True, choices=drug_route_sel)
    pid_course2 = models.CharField(max_length=100, blank=True, null=True, choices=course_sel)
    pid_adverse_reaction2 = models.CharField(max_length=1000, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    pid_drug_name3 = models.CharField(max_length=1000, blank=True, null=True, validators=[MaxLengthValidator(100)])
    pid_indication3 = models.CharField(max_length=100, blank=True, null=True, choices=imm_indication_sel)
    pid_route3 = models.CharField(max_length=100, blank=True, null=True, choices=drug_route_sel)
    pid_course3 = models.CharField(max_length=100, blank=True, null=True, choices=course_sel)
    pid_adverse_reaction3 = models.CharField(max_length=1000, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    pid_drug_name4 = models.CharField(max_length=1000, null=True, blank=True, validators=[MaxLengthValidator(100)])
    pid_indication4 = models.CharField(max_length=100, blank=True, null=True, choices=imm_indication_sel)
    pid_route4 = models.CharField(max_length=100, blank=True, null=True, choices=drug_route_sel)
    pid_course4 = models.CharField(max_length=100, blank=True, null=True, choices=course_sel)
    pid_adverse_reaction4 = models.CharField(max_length=1000, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    pid_Immuno_modulator_medication_drug_name = models.CharField(max_length=1000, blank=True, null=True,
                                                                 validators=[MaxLengthValidator(100)])
    pid_imm_indication = models.CharField(max_length=100, blank=True, null=True, choices=indication_sel)
    pid_imm_improvement = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_imm_adverse_reaction = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)

    pid_Immuno_modulator_medication_drug_name1 = models.CharField(max_length=1000, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    pid_imm_indication1 = models.CharField(max_length=100, blank=True, null=True, choices=indication_sel)
    pid_imm_improvement1 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_imm_adverse_reaction1 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Immuno_modulator_medication_drug_name2 = models.CharField(max_length=1000, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    pid_imm_indication2 = models.CharField(max_length=100, blank=True, null=True, choices=indication_sel)
    pid_imm_improvement2 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_imm_adverse_reaction2 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Immuno_modulator_medication_drug_name3 = models.CharField(max_length=1000, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    pid_imm_indication3 = models.CharField(max_length=100, blank=True, null=True, choices=indication_sel)
    pid_imm_improvement3 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_imm_adverse_reaction3 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_Immuno_modulator_medication_drug_name4 = models.CharField(max_length=1000, blank=True, null=True,
                                                                  validators=[MaxLengthValidator(100)])
    pid_imm_indication4 = models.CharField(max_length=100, blank=True, null=True, choices=indication_sel)
    pid_imm_improvement4 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_imm_adverse_reaction4 = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_surgeries = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    Other_treatment = models.CharField(max_length=100, blank=True, null=True, choices=tretment_sel)
    pid_Ayurvedic = models.BooleanField(default=False)
    pid_acupuncture = models.BooleanField(default=False)
    pid_herbal_remedies = models.BooleanField(default=False)
    pid_homeopathic = models.BooleanField(default=False)
    pid_Others = models.BooleanField(default=False)
    pid_Others_specify = models.BooleanField(default=False)

    pid_Has_patient_undergone_HSCT = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_type_of_transplant = models.CharField(max_length=100, blank=True, null=True, choices=trasplant_sel)
    pid_outcome_alive = models.CharField(max_length=100, blank=True, null=True, choices=yes_no_sel)
    pid_outcome_alive_no_date = models.DateTimeField(null=True, blank=True)
    pid_outcome_alive_no_cause = models.CharField(max_length=100, blank=True, null=True, choices=death_cause_sel)
    pid_outcome_alive_no_cause_others_specify = models.CharField(max_length=1000, blank=True, null=True,
                                                                 validators=[MaxLengthValidator(100)])
    def __str__(self):
        return str(self.pk)
