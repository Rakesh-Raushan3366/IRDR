# Create your models here.

# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator


class profile_smallmolecule(models.Model):
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
    small_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_date_of_records = models.DateField(blank=True, null=True)
    small_date_of_clinical_exam = models.DateField(blank=True, null=True)
    small_date_of_birth = models.DateField( null=True)
    small_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    small_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'), ('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id')]
    small_paitent_id_yes_no = models.CharField(max_length=100,  null=True, choices=fb_status_sel)
    small_paitent_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    small_patient_id_no = models.CharField(max_length=100,unique=True, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_father_mother_id = models.CharField(max_length=100,  null=True, blank=True,choices=id_sel)
    small_father_mother_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    small_mother_adhaar_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    small_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    small_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    small_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    small_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    small_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    small_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    small_email = models.EmailField(max_length=300, blank=True, null=True)

    small_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    small_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    small_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    small_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    small_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    small_consent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    small_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    small_assent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    small_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    small_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    small_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_small', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_small', on_delete=models.CASCADE)

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
            super(profile_smallmolecule, self).save(*args, **kwargs)
            self.small_icmr_unique_no = str('SM/') + str(self.register.institute_code) + str('/') + str(self.pk)

        super(profile_smallmolecule, self).save(*args, **kwargs)


class demographic_smallmolecule(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_smallmolecule, related_name='patient_small', null=True, blank=True,
                                on_delete=models.CASCADE)
    # education_status = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School')
    #     , ('Secondary Level', 'Secondary Level'), ('College and above', 'College and above')]
    #
    # occupation_status = [('Employed (organised sector)', 'Employed (organised sector)'),
    #                      ('Employed (Unorganised sector) ', 'Employed (Unorganised sector)')
    #     , ('Others', 'Others')]
    #
    # yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no = [('Yes', 'Yes'), ('No', 'No')]
    # yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    # religion_list = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'),
    #                  ('Sikh', 'Sikh'), ('Others', 'Others')]
    malformation_list = [('limb', 'limb'), ('clift lip', 'clift lip'), ('palate', 'palate'), ('others', 'others')]
    #
    # referred_from_another_facility_list = [('General Practitioner', 'General Practitioner'), ('Physician', 'Physician')
    #     , ('Neurologist', 'Neurologist'), ('Any Other', 'Any Other')]
    visual_list = [('blindness', 'blindness'), ('cataract', 'cataract'),
                   ('retinitis pigmentosa', 'retinitis pigmentosa'),
                   ('coloboma', 'coloboma'), ('optic atrophy', 'optic atrophy'), ('cherry red pot', 'cherry red pot')]

    # hospital_name = models.CharField(max_length=100, null=True, blank=True,
    #                                  validators=[MaxLengthValidator(100)])
    # hospital_reg_number = models.CharField(max_length=100, null=True, blank=True,
    #                                        validators=[MaxLengthValidator(100)])
    # icmr_unique_id_number = models.CharField(max_length=100, null=True, blank=True,
    #                                          validators=[MaxLengthValidator(100)])
    # report_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    # due_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )

    head_circumference = models.CharField(max_length=200, null=True, blank=True)
    # age_at_first_symptom1 = models.DateField(null=True, blank=True)
    age_at_first_symptom = models.CharField(max_length=50, blank=True, null=True)
    visual_problem = models.CharField(max_length=200, null=True, blank=True, choices=visual_list)
    any_malformation = models.CharField(max_length=200, null=True, blank=True, choices=malformation_list)

    developmental_delay = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    developmental_findings = models.CharField(max_length=50, blank=True, null=True, )
    vomiting = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    vomiting_finding = models.CharField(max_length=50, blank=True, null=True)
    loose_stools = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    stools_findings = models.CharField(max_length=50, blank=True, null=True)
    pneumonia = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    pneumonia_findings = models.CharField(max_length=50, blank=True, null=True)
    fever = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    fever_findings = models.CharField(max_length=50, blank=True, null=True)
    lethargy = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    lethargy_findings = models.CharField(max_length=50, blank=True, null=True)
    seizures = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    seizures_findings = models.CharField(max_length=50, blank=True, null=True)
    abdominal_distention = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    abdominal_distention_findings = models.CharField(max_length=50, blank=True, null=True)
    history_admission = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    history_findings = models.CharField(max_length=50, blank=True, null=True)
    any_surgery = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    surgery_findings = models.CharField(max_length=50, blank=True, null=True)
    aversion_sweet_protein = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    sweet_protein_findings = models.CharField(max_length=50, blank=True, null=True)

    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal'), ('Not Done', 'Not Done')]
    reflex_sel = [('Absent', 'Absent'), ('Diminished', 'Diminished'), ('Brisk', 'Brisk'), ('Normal', 'Normal')]
    photo_sel = [('Patient', 'Patient'), ('X Ray', 'X Ray'), ('MRI', 'MRI')]
    # Cardiomegaly / Cardiomyopathy / Normal/abnormal /Not done
    #
    encephalopathy = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    encephalopathy_findings = models.CharField(max_length=100, blank=True, null=True)
    deafness = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    deafness_findings = models.CharField(max_length=100, blank=True, null=True)
    extra_pyramidal_symp = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    extra_pyramidal_symp_findings = models.CharField(max_length=100, blank=True, null=True)
    hypotonia = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    hypotonia_findings = models.CharField(max_length=100, blank=True, null=True)
    reflexes = models.CharField(max_length=100, blank=True, null=True, choices=reflex_sel)
    reflexes_findings = models.CharField(max_length=100, blank=True, null=True)
    hypertonia = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    hypertonia_findings = models.CharField(max_length=100, blank=True, null=True)
    facial_dysmorphism = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    facial_dysmorphism_findings = models.CharField(max_length=100, blank=True, null=True)
    congential_heart_disease = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    congential_heart_disease_findings = models.CharField(max_length=100, blank=True, null=True)
    cardiomyopathy = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    cardiomyopathy_findings = models.CharField(max_length=100, blank=True, null=True)
    hepatomegaly = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    hepatomegaly_findings = models.CharField(max_length=100, blank=True, null=True)
    splenomegaly = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    splenomegaly_findings = models.CharField(max_length=100, blank=True, null=True)
    pigmentary = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    pigmentary_findings = models.CharField(max_length=100, blank=True, null=True)
    deranged_LFT = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    deranged_LFT_findings = models.CharField(max_length=100, blank=True, null=True)
    deranged_RFT = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    deranged_RFT_findings = models.CharField(max_length=100, blank=True, null=True)
    hypoglycemia = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    hypoglycemia_findings = models.CharField(max_length=100, blank=True, null=True)
    metabolic_acidosis = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    metabolic_acidosis_findings = models.CharField(max_length=100, blank=True, null=True)
    metabolic_alkalosis = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    metabolic_alkalosis_findings = models.CharField(max_length=100, blank=True, null=True)
    hyper_ammonia = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    hyper_ammonia_findings = models.CharField(max_length=100, blank=True, null=True)
    high_lactate = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    high_lactate_findings = models.CharField(max_length=100, blank=True, null=True)
    urine_ketones = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    urine_ketones_findings = models.CharField(max_length=100, blank=True, null=True)
    cherry_red_spot = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    cherry_red_spot_findings = models.CharField(max_length=100, blank=True, null=True)
    retinitis_pigmentosa = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    retinitis_pigmentosa_findings = models.CharField(max_length=100, blank=True, null=True)
    optic_atrophy = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    optic_atrophy_findings = models.CharField(max_length=100, blank=True, null=True)
    mechanical_ventilation = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    mechanical_ventilation_findings = models.CharField(max_length=100, blank=True, null=True)
    dialysis = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    dialysis_findings = models.CharField(max_length=100, blank=True, null=True)
    CT_brain = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    CT_brain_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    CT_brain_age = models.CharField(max_length=100, blank=True, null=True)
    mri_brain = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    mri_brain_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    mri_brain_age = models.CharField(max_length=100, blank=True, null=True)
    mrs_brain = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    mrs_brain_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    mrs_brain_age = models.CharField(max_length=100, blank=True, null=True)

    other_info = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    other_info_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    other_info_age = models.CharField(max_length=100, blank=True, null=True)
    tms = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    tms_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    tms_age = models.CharField(max_length=100, blank=True, null=True)
    regression = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    regression_findings = models.CharField(max_length=100, blank=True, null=True)
    distonia_abnormal_movement = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    distonia_abnormal_findings = models.CharField(max_length=100, blank=True, null=True)
    high_cpk = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    high_cpk_findings = models.CharField(max_length=100, blank=True, null=True)
    ms_ms = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    ms_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    ms_age = models.CharField(max_length=100, blank=True, null=True)
    gcms = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    gcms_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    gcms_age = models.CharField(max_length=100, blank=True, null=True)
    enzyme_assay = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    enzyme_assay_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    enzyme_assay_age = models.CharField(max_length=100, blank=True, null=True)
    dna_storage = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    dna_storage_findings = models.CharField(max_length=100, blank=True, null=True)
    photos = models.CharField(max_length=100, blank=True, null=True, choices=photo_sel)
    photos_specify = models.CharField(max_length=100, blank=True, null=True)
    generic_analysis = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    generic_analysis_findings = models.CharField(max_length=100, blank=True, null=True)
    final_dagnosis = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    final_dagnosis_findings = models.CharField(max_length=100, blank=True, null=True)
    quantitative_plasma = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    quantitative_plasma_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    quantitative_plasma_age = models.CharField(max_length=100, blank=True, null=True)
    quantitative_csf = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    quantitative_csf_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    quantitative_csf_age = models.CharField(max_length=100, blank=True, null=True)
    muscle_biopsy = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    muscle_biopsy_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    muscle_biopsy_age = models.CharField(max_length=100, blank=True, null=True)
    ncv = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    ncv_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    ncv_age = models.CharField(max_length=100, blank=True, null=True)
    ief_cdg = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    ief_cdg_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    ief_cdg_age = models.CharField(max_length=100, blank=True, null=True)
    glycine = models.CharField(max_length=100, blank=True, null=True, choices=normal_abnormal_sel)
    glycine_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    glycine_age = models.CharField(max_length=100, blank=True, null=True)

    Ultrasonography_sel = [('normal', 'normal'), ('abnormal', 'abnormal'), ('not done', 'not done')]
    final_sel = [('Death', 'Death'), ('Alive', 'Alive'), ('Follow up required', 'Follow up required'), ('Lost to follow up', 'Lost to follow up'), ('Unknown', 'Unknown')]

    # Molecular studies
    molecular_studies = models.CharField(max_length=50, default='No', null=True, choices=yes_no)
    molecular_studies_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False, )
    molecular_studies_place = models.CharField(max_length=50, blank=True, null=True)
    upload_studies = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)

    # Final Outcome
    Final_Outcome = models.CharField(max_length=50, blank=True, null=True, choices=final_sel)
    death_cause = models.CharField(max_length=50, blank=True, null=True)
    age_timedeath = models.CharField(max_length=50, blank=True, null=True)
    sm_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

