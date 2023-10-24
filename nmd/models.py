# Create your models here.

from django.db import models

from account.models import *

from django.core.validators import FileExtensionValidator
# Create your models here.


class profile_nmd(models.Model):
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
    nmd_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_date_of_records = models.DateField(blank=True, null=True)
    nmd_date_of_clinical_exam = models.DateField(blank=True, null=True)
    nmd_date_of_birth = models.DateField( null=True)
    nmd_patient_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    nmd_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    nmd_paitent_id_yes_no = models.CharField(max_length=100, null=True, choices=fb_status_sel)
    nmd_paitent_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    nmd_patient_id_no = models.CharField(max_length=100, unique=True,  blank=True,null=True, validators=[MaxLengthValidator(100)])
    nmd_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_father_mother_id = models.CharField(max_length=100, null=True,  blank=True,choices=id_sel)
    nmd_mother_father_no = models.CharField(max_length=100, blank=True,unique=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    nmd_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    nmd_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    nmd_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_mother_mobile_no = models.PositiveBigIntegerField(null=True, unique=True)
    nmd_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    nmd_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    nmd_email = models.EmailField(max_length=300, blank=True, null=True)

    nmd_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    nmd_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    nmd_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    nmd_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    nmd_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    nmd_consent_given = models.CharField(max_length=10, null=True, choices=fb_status_sel)
    nmd_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    nmd_assent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    nmd_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    nmd_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    nmd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_nmd', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_nmd', on_delete=models.CASCADE)

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
            super(profile_nmd, self).save(*args, **kwargs)
            self.nmd_icmr_unique_no = str('NMD/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_nmd, self).save(*args, **kwargs)


class demographic_nmd(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_nmd, related_name='demographicnmd', null=True, blank=True, on_delete=models.CASCADE)
    curr_study_sel = [('Yes', 'Yes'), ('No', 'No')]
    edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
               ('Secondary '
                'level',
                'Secondary '
                'level'),
               ('College and above', 'College and above')]

    occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    mother_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                      ('Secondary '
                       'level',
                       'Secondary '
                       'level'),
                      ('College and above', 'College and above')]
    mother_occu_sel = [('Home maker', 'Home maker)'),
                       ('Employed (organised sector)', 'Employed (organised sector)'),
                       ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    monthly_income_sel = [('> 126,360', '> 126,360)'),
                          ('63,182 – 126,356)', '63,182 – 126,356)'),
                          ('47,266 – 63,178', '47,266 – 63,178'),
                          ('31,591 - 47,262', '31,591 - 47,262'),
                          ('18,953 - 31,589', '18,953 - 31,589'),
                          ('6,327 - 18,949', '6,327 - 18,949'),
                          ('< 6,323', '< 6,323')]

    NMD_patient_education = models.CharField(max_length=50, blank=True, null=True, choices=edu_sel)
    NMD_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=occu_sel)
    NMD_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=edu_sel)
    NMD_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=occu_sel)
    NMD_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=edu_sel)
    NMD_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=mother_occu_sel)
    NMD_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=monthly_income_sel)
    nmd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class dsystophinopathy_nmd(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_nmd, related_name='dystonmd', null=True, blank=True, on_delete=models.CASCADE)
    diagnosis_sel = [('Dystrophinopathy ', 'Dystrophinopathy'), ('Spinal Muscular Atrophy', 'Spinal Muscular Atrophy'),
                     ('Limb Girdle Muscular Dystrophy', 'Limb Girdle Muscular Dystrophy')]
    diagnosis_age_sel = [('Prenatal', 'Prenatal'), ('At birth', 'At birth'),
                         ('Not sure', 'Not sure')]
    yes_no_sel = [('yes', 'Yes'), ('No', 'No')]

    NMD_diagnosis_type = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_sel)
    enrollment_sel = [('Enrolled', 'Enrolled'), ('Not Enrolled.', 'Not Enrolled.')]
    NMD_enrollment_status = models.CharField(max_length=50, blank=True, null=True, choices=enrollment_sel)
    diagnosis_age = models.CharField(max_length=100, blank=True, null=True,
                                     validators=[MaxLengthValidator(100)])
    aproximate_age = models.CharField(max_length=100, blank=True, null=True,
                                      validators=[MaxLengthValidator(100)])
    symptoms_age_onset = models.CharField(max_length=100, blank=True, null=True,
                                          validators=[MaxLengthValidator(100)])
    pedigree = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    positive_family_hist = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    family_hist_sel = [('Siblings', 'Siblings'), ('Cousins', 'Cousins'), ('Maternal uncles', 'Maternal uncles'),
                       ('Grand '
                        'maternal uncle', 'Grand maternal uncle'), ('Grand maternal uncle', 'Grand maternal uncle')]
    onset_age = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_age_sel)
    positive_family_siblings = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)

    positive_family_sibling_nubmer_affected = models.IntegerField(blank=True, null=True)
    positive_family_cousins = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)

    positive_family_sCousins_nubmer_affected = models.IntegerField(blank=True, null=True)
    positive_family_Maternal_uncles = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)

    positive_family_Maternal_uncles_nubmer_affected = models.IntegerField(blank=True, null=True)
    positive_family_Grand_materna = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)

    positive_family_Grand_materna_affected = models.IntegerField(blank=True, null=True)
    positive_family_mothers = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)

    symptoms_signs_onset = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    difficulty_running_walking_fast = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    unable_rise_low_chair_floor = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    repeated_false = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    muscle_hypertrophy = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mental_sub_normality = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    learning_disability = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    delayed_motor_milestrones = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    symtoms_signs_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    CEF_anthropometric_wieght = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    CEF_anthropometric_height = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    CEF_anthropometric_head_circumference = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    MP_MRC_grade_upperlimb_proximal_muscles = models.IntegerField(blank=True, null=True)
    MP_MRC_grade_upperlimb_distal_muscles = models.IntegerField(blank=True, null=True)
    MP_MRC_grade_lowerlimb_proximal_muscles = models.IntegerField(blank=True, null=True)
    MP_MRC_grade_lowerlimb_distal_muscles = models.IntegerField(blank=True, null=True)

    functional_status_sel = [('Independently ambulant', 'Independently ambulant'),
                             ('Needs physical assistance', 'Needs physical assistance'),
                             ('Ambulant in home', 'Ambulant in home'),
                             ('Wheelchair bound', 'Wheelchair bound'), ('Bed Bound', 'Bed Bound'),
                             ('Functional score available', 'Functional score available'),
                             ('Brooke Scale for upper extremity', 'Brooke Scale for upper extremity'),
                             ('Vignos Scale for lower extremity', 'Vignos Scale for lower extremity')]
    functional_status_Independently_ambulant = models.BooleanField(default=False)
    functional_status_NeedsPhysicalAssistance = models.BooleanField(default=False)
    functional_status_AmbulantHome = models.BooleanField(default=False)
    functional_status_WheelchairBound = models.BooleanField(default=False)
    functional_status_WheelchairBound_age = models.DateField(blank=True, null=True)
    functional_status_BedBound = models.BooleanField(default=False)
    functional_status_BedBound_age = models.DateField(blank=True, null=True)
    functional_status_FunctionalScoreAvailable = models.BooleanField(default=False)
    functional_status_BrookeScale = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    functional_status_VignosScale = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])

    functional_status_functional_score_available = models.CharField(max_length=50, blank=True, null=True,
                                                                    choices=yes_no_sel)
    intelligent_quotient_tested = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    intelligent_quotient_tested_if_yes = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    autism = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_dmd = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_ankle = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_knee = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_hips = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_elbows = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Scoliosis_dmd = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Kyphosis_dmd = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Respiratory_difficulty = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    LaboratoryInvestigation_serum_ck_lvel = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    LaboratoryInvestigation_Cardiac_Evaluation = models.CharField(max_length=50, blank=True, null=True,
                                                                  choices=yes_no_sel)
    done_notdone_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    LaboratoryInvestigation_ecg_status = models.CharField(max_length=50, blank=True, null=True,
                                                          choices=done_notdone_sel)
    normal_abnormal_sel = [('Normal', 'Normal'), ('Abnormal', 'Abnormal')]
    LaboratoryInvestigation_ecg_normal_abnormal = models.CharField(max_length=50, blank=True, null=True,
                                                                   choices=normal_abnormal_sel)
    ecg_done_abnormal_sel = [('sinus tachycardia', 'sinus tachycardia'),
                             ('Tall R waves in right precordial leads', 'Tall R waves in right precordial leads'),
                             ('right ventricular hypertrophy', 'right ventricular hypertrophy'),
                             ('S-T segment depression', 'S-T segment depression'),
                             ('prolonged QTc', 'prolonged QTc'), ('RBBB', 'RBBB'), ('WPW syndrome', 'WPW syndrome'),
                             ('sinus arrhythmia', 'sinus arrhythmia'),
                             ('sinus pauses', 'sinus pauses'), ('atrial ectopic beats', 'atrial ectopic beats'),
                             ('atrial ectopic rhythm', 'atrial ectopic rhythm'),
                             ('junctional rhythm', 'junctional rhythm'), ('atrial flutter', 'atrial flutter'),
                             ('ventricular premature beats', 'ventricular premature beats'),
                             ('Mobitz type I block', 'Mobitz type I block')]
    # LaboratoryInvestigation_ecg_if_abnormal = models.MultiSelectField(max_length=100, blank=True, null=True,
    #                                                                  choices=ecg_done_abnormal_sel)
    LaboratoryInvestigation_2DECHO_status = models.CharField(max_length=50, blank=True, null=True,
                                                             choices=done_notdone_sel)
    LaboratoryInvestigation_2DECHO_normal_abnormal = models.CharField(max_length=50, blank=True, null=True,
                                                                      choices=normal_abnormal_sel)
    DECHO_done_abnormal_sel = [('Dilated cardiomyopathy', 'Dilated cardiomyopathy'),
                               ('LV systolic dysfunction ', 'LV systolic dysfunction '),
                               ('LV diastolic dysfunction', 'LV diastolic dysfunction'),
                               ('Ejection fraction %', 'Ejection fraction %'),
                               ('LA dysfunction', 'LA dysfunction'),
                               ('Global systolic dysfunction', 'Global systolic dysfunction'),
                               ('LV Hypertrophy', 'LV Hypertrophy'),
                               ('Mitral regurgitation', 'Mitral regurgitation'),
                               ('Mitral valve prolapse', 'Mitral valve prolapse'),
                               ('Tricuspid regurgitation ', 'Tricuspid regurgitation '),
                               ]
    # LaboratoryInvestigation_2DECHO_abnormal = models.MultiSelectFieldMultiSelectField(max_length=100, blank=True, null=True,
    #                                                                  choices=DECHO_done_abnormal_sel)
    pulmonary_function_tests = models.CharField(max_length=50, blank=True, null=True, choices=done_notdone_sel)
    pulmonary_function_tests_normal_abnormal = models.CharField(max_length=50, blank=True, null=True,
                                                                choices=normal_abnormal_sel)
    pulmonary_function_forced_vital_capacity = models.CharField(max_length=100, blank=True, null=True,
                                                                validators=[MaxLengthValidator(100)])
    genetic_diagnosis_sel = [('mPCR', 'mPCR'),
                             ('MLPA', 'MLPA'),
                             ('Micro Array', 'Micro Array'),
                             ('Sanger sequencing', 'Next Generation Sequencing'),
                             ]
    # genetic_diagnosis_confirmed = models.MultiSelectField(max_length=100, blank=True, null=True,
    #                                                      choices=DECHO_done_abnormal_sel)
    genetic_diagnosis_confirmed_mPCR = models.BooleanField(default=False)
    genetic_diagnosis_confirmed_MLPA = models.BooleanField(default=False)
    genetic_diagnosis_confirmed_MicroArray = models.BooleanField(default=False)
    genetic_diagnosis_confirmed_SangerSequencing = models.BooleanField(default=False)
    genetic_diagnosis_confirmed_next_generation = models.BooleanField(default=False)
    genetic_diagnosis_next_generation = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    genetic_diagnosis_next_generation_sel = [('Targeted Panel', 'Targeted Panel'),
                                             ('Clinical exome', 'Clinical exome'),
                                             ('Whole exome sequencing', 'Whole exome sequencing'),
                                             ('Whole genome sequencing', 'Whole genome sequencing'),
                                             ]
    # enetic_diagnosis_next_generation_sequencing = models.MultiSelectField(max_length=100, blank=True, null=True,
    #                                                                       choices=genetic_diagnosis_next_generation_sel)
    enetic_diagnosis_next_generation_TargetedPanel = models.BooleanField(default=False)
    enetic_diagnosis_next_generation_ClinicalExome = models.BooleanField(default=False)
    enetic_diagnosis_next_generation_WholeExomeSequencing = models.BooleanField(default=False)
    enetic_diagnosis_next_generation_WholeGenomeSequencing = models.BooleanField(default=False)
    upload_genetic_report = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    deleted_exons_sel = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')]
    # deleted_exons = models.MultiSelectField(max_length=100, blank=True, null=True, choices=deleted_exons_sel)
    inframe_outframe_sel = [('In-frame ', 'In-frame '), ('Out-of-frame', 'Out-of-frame')]
    inframe_outframe = models.CharField(max_length=50, blank=True, null=True, choices=inframe_outframe_sel)
    list_of_deleted_exons = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    list_of_duplicate_exons = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    mutation_identified_Missense = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Missense_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    mutation_identified_Nonsense = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Nonsense_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    mutation_identified_Mutation = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Mutation_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                             validators=[MaxLengthValidator(100)])
    mutation_identified_Frameshift = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Frameshift_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    mutation_identified_Splicesite = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Splicesite_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    mutation_identified_InframeInsertion = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_InframeInsertion_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                                     validators=[MaxLengthValidator(100)])
    mutation_identified_InframeDeletion = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_InframeDeletion_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                                    validators=[MaxLengthValidator(100)])
    mutation_identified_INDEL = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_INDEL_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mutation_identified_Others = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutation_identified_Others_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                           validators=[MaxLengthValidator(100)])
    gene_location = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gene_variant = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gene_Zygosity = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gene_Disease = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gene_Inheritance = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    gene_classification = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    Muscle_Biopsy = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Muscle_Biopsy_MuscleImmunohistochemistry = models.CharField(max_length=50, blank=True, null=True,
                                                                choices=yes_no_sel)
    MuscleImmunohistochemistry_sel = [('Absent Dystrophin staining ', 'Absent Dystrophin staining '),
                                      ('Reduced Dystrophin staining', 'Reduced Dystrophin staining'),
                                      ('Mosaic pattern', 'Mosaic pattern')]
    Muscle_Biopsy_MuscleImmunohistochemistry_if_yes = models.CharField(max_length=50, blank=True, null=True,
                                                                       choices=MuscleImmunohistochemistry_sel)
    final_diagnosis_sel = [('Duchenne Muscular Dystrophy (DMD) ', 'Duchenne Muscular Dystrophy (DMD) '),
                           ('Becker Muscular Dystrophy (BMD)', 'Becker Muscular Dystrophy (BMD)'),
                           ('Intermediate Muscular Dystrophy (IMD)', 'Intermediate Muscular Dystrophy (IMD)')]
    final_diagnosis = models.CharField(max_length=100, blank=True, null=True, choices=final_diagnosis_sel)
    current_past_treatment_Steroids = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    current_past_treatment_Steroids_starting_age = models.DateField(blank=True, null=True)
    current_past_treatment_Prednisone = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    current_past_treatment_1 = models.FloatField(blank=True, null=True)
    current_past_treatment_2 = models.FloatField(blank=True, null=True)
    current_past_treatment_Deflazacort = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    current_past_treatment_Deflazacort_1 = models.FloatField(blank=True, null=True)
    current_past_treatment_Deflazacort_anyother_specify = models.CharField(max_length=100, blank=True, null=True,
                                                                           validators=[MaxLengthValidator(100)])
    current_past_treatment_Supplements = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    current_past_treatment_Supplements_calcium = models.CharField(max_length=50, blank=True, null=True,
                                                                  choices=yes_no_sel)
    current_past_treatment_Supplements_vit_D = models.CharField(max_length=50, blank=True, null=True,
                                                                choices=yes_no_sel)
    Respiratoryassistance = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Respiratoryassistance_sel = [('BiPAP ', 'BiPAP'), ('Ventilator', 'Ventilator')]
    Respiratoryassistance_BiPAP = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    Respiratoryassistance_Ventilator = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])
    Respiratoryassistance_BiPAP_age = models.CharField(max_length=100, blank=True, null=True,
                                                       validators=[MaxLengthValidator(100)])
    Respiratoryassistance_Ventilator_age = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])
    Tendon_lengthening_surgery = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Tendon_lengthening_surgery_if_yes_age = models.DateField(blank=True, null=True)
    Surgicalcorrectionscoliosis = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Surgicalcorrectionscoliosis_if_yes_age = models.DateField(blank=True, null=True)
    last_follow_up = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    last_follow_up_sel = [('Physical follow-up  ', 'Physical follow-up '),
                          ('Telephonic information ', 'Telephonic information '), ('Letter ', 'Letter ')]
    last_follow_up_if_yes = models.CharField(max_length=50, blank=True, null=True, choices=last_follow_up_sel)
    last_follow_up_if_yes_age = models.DateField(blank=True, null=True)
    known_notknown_sel = [('Known  ', 'Known '), ('Not Known ', 'Not Known')]
    Functionalstatus = models.CharField(max_length=50, blank=True, null=True, choices=known_notknown_sel)
    functional_status_options_sel = [('Independently ambulant  ', 'Independently ambulant '),
                                     ('Needs physical assistance', 'Needs physical assistance'),
                                     ('Ambulant in home', 'Ambulant in home'),
                                     ('Wheelchair bound ', 'Wheelchair bound'), ('Bed Bound', 'Bed Bound')]
    functional_status_options = models.CharField(max_length=100, blank=True, null=True,
                                                 choices=functional_status_options_sel)
    functional_score = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    functional_score_brooks_grade = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    functional_score_vignos_grade = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    outcome_sel = [('Alive', 'Alive'), ('Dead ', 'Dead')]
    outcome = models.CharField(max_length=50, blank=True, null=True, choices=outcome_sel)
    outcome_age = models.DateField(blank=True, null=True)
    oucome_cause_of_death = models.CharField(max_length=50, blank=True, null=True, choices=known_notknown_sel)
    death_cause_sel = [('Cardiac cause ', 'Cardiac cause '), ('Respiratory failure', 'Respiratory failure')]
    outcome_death_cause = models.CharField(max_length=100, blank=True, null=True, choices=death_cause_sel)
    death_place_sel = [('Home ', 'Home '), ('Hospital ', 'Hospital')]
    death_place = models.CharField(max_length=100, blank=True, null=True, choices=death_place_sel)
    mother_carrier_status = models.CharField(max_length=100, blank=True, null=True, choices=done_notdone_sel)
    positive_negative_sel = [('Positive  ', 'Positive  '), ('Negative ', 'Negative')]
    mother_carrier_status_outcome = models.CharField(max_length=100, blank=True, null=True,
                                                     choices=positive_negative_sel)
    sister_carrier_status = models.CharField(max_length=100, blank=True, null=True, choices=done_notdone_sel)
    sister_carrier_status_outcome = models.CharField(max_length=100, blank=True, null=True,
                                                     choices=positive_negative_sel)
    nmd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class spinal_nmd(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_nmd, related_name='spinalnmd', null=True, blank=True, on_delete=models.CASCADE)
    gender_sel = [('Male ', 'Male '), ('Female ', 'Female')]
    yes_no_sel = [('yes', 'Yes'), ('No', 'No')]
    gender = models.CharField(max_length=50, blank=True, null=True, choices=gender_sel)
    born_consanguineous_parents = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    consanguineous_parents_sel = [('Uncle –niece', 'Uncle –niece'), ('First cousins', 'First cousins'),
                                  ('Distant relatives', 'Distant relatives')]
    consanguineous_parents_if_yes = models.CharField(max_length=50, blank=True, null=True,
                                                     choices=consanguineous_parents_sel)
    familyHistory_sibling_affected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    familyHistory_sibling_affected_number = models.IntegerField(blank=True, null=True)
    upload_pedegree = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    age_first_evaluation = models.CharField(max_length=100, blank=True, null=True,
                                            validators=[MaxLengthValidator(100)])
    age_at_onset = models.IntegerField(blank=True, null=True)
    age_onset_sel = [('Prenatal / In-utero', 'Prenatal / In-utero'), ('Birth', 'Birth'),
                     ('< 6 months age', '< 6 months age'),
                     ('6 months to 18 months', '6 months to 18 months'),
                     ('18 mo to 36 months', '18 mo to 36 months'), ('>36 months to 20 years', '>36 months to 20 years'),
                     ('> 20 years', '> 20 years')]
    age_onset_options = models.CharField(max_length=50, blank=True, null=True, choices=age_onset_sel)
    age_onset_options_yes_no = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    ConditionBirth_cry = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    conditionBirth_feedingDifficulty = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    conditionBirth_RespiratoryDistress = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    conditionBirth_ReceivedOxygen = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    conditionBirth_KeptIncubator = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    arthrogryposisBirth = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RecurrentLowerRespiratory = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Scoliosis_sma = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Kyphosis_sma = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    HipDislocation = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Fractures = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MotorSystemExam_Minipolymyoclonus = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MotorSystemExam_TongueFasciculations = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MotorSystemExam_MotorPower_ModifiedMRCgrade = models.CharField(max_length=100, blank=True, null=True,
                                                                   validators=[MaxLengthValidator(100)])
    MotorSystemExam_UpperLimb_ProximalMuscles = models.CharField(max_length=100, blank=True, null=True,
                                                                 validators=[MaxLengthValidator(100)])
    MotorSystemExam_UpperLimb_DistalMuscles = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    MotorSystemExam_lowerLimb_ProximalMuscles = models.CharField(max_length=100, blank=True, null=True,
                                                                 validators=[MaxLengthValidator(100)])
    MotorSystemExam_lowerLimb_DistalMuscles = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])

    LimbWeakness = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    LimbWeakness_if_yes_UpperLimb_ProximalGrade = models.IntegerField(blank=True, null=True)
    LimbWeakness_if_yes_UpperLimb_DistalGrade = models.IntegerField(blank=True, null=True)
    LimbWeakness_if_yes_LowerLimb_ProximalGrade = models.IntegerField(blank=True, null=True)
    LimbWeakness_if_yes_LowerLimb_DistalGrade = models.IntegerField(blank=True, null=True)
    current_motor_sel = [('Able to sit up self / support', 'Able to sit up self / support'),
                         ('Able to stand by self / support', 'Able to stand by self / support'),
                         ('Able to walk by self / support', 'Able to walk by self / support'),
                         ('Normal walking', 'Normal walking'),
                         ('Can run ', 'Can run '), ('Wheelchair bound', 'Wheelchair bound')
                         ]
    currentMotor_ability = models.CharField(max_length=50, blank=True, null=True, choices=current_motor_sel)
    currentMotor_WheelchairBound = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    currentMotor_WheelchairBound_if_yes_age = models.DateField(blank=True, null=True)
    currentMotor_BedBound = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    currentMotor_BedBound_age = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    done_notdone_sel = [('Done', 'Done'), ('Not Done', 'Not Done')]
    HMAS = models.CharField(max_length=50, blank=True, null=True, choices=done_notdone_sel)
    HMAS_score = models.CharField(max_length=100, blank=True, null=True,
                                  validators=[MaxLengthValidator(100)])
    clinicalDiagnosis_SMA0 = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    clinicalDiagnosis_SMA1 = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    clinicalDiagnosis_SMA2 = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    clinicalDiagnosis_SMA3 = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    clinicalDiagnosis_SMA4 = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    LaboratoryInvestigation_CK_Level = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])
    genetic_diagnosis_sel = [('Fluorescent quantitative PCR (FQ-PCR)', 'Fluorescent quantitative PCR (FQ-PCR)'),
                             ('Multiplex ligation-dependent probe amplification (MLPA) ',
                              'Multiplex ligation-dependent probe amplification (MLPA) '),
                             ('PCR-restriction fragment length polymorphism (PCR-RFLP)',
                              'PCR-restriction fragment length polymorphism (PCR-RFLP)'),
                             ('PCR-denaturing high-performance liquid chromatography (PCR-DHPLC)',
                              'PCR-denaturing high-performance liquid chromatography (PCR-DHPLC)'),
                             ('Long-range PCR ', 'Long-range PCR '),
                             ('SMN Gene sequencing ', 'SMN Gene sequencing '),
                             ('Chromosomal Micro-array ', 'Chromosomal Micro-array')
                             ]
    geneticDiagnosis = models.CharField(max_length=100, blank=True, null=True, choices=genetic_diagnosis_sel)
    NAIP_sel = [('Yes', 'YES'), ('No', 'No'), ('Not Done', 'Not Done')]
    NAIP_deletion = models.CharField(max_length=100, blank=True, null=True, choices=NAIP_sel)
    geneticFindings_gene = models.CharField(max_length=100, blank=True, null=True,
                                            validators=[MaxLengthValidator(100)])

    geneticFindings_Location = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    geneticFindings_Variant = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    geneticFindings_Zygosity = models.CharField(max_length=100, blank=True, null=True,
                                                validators=[MaxLengthValidator(100)])
    geneticFindings_Disease = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    geneticFindings_Inheritance = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    classification_sel = [('Pathogenic ', 'Pathogenic '), ('Likely pathogenic ', 'Likely pathogenic '),
                          ('Uncertain significance ', 'Uncertain significance ')]
    geneticFindings_classification = models.CharField(max_length=100, blank=True, null=True, choices=classification_sel)
    genetic_diagnosis2_sel = [('Homozygous deletion of SMN1 exon 7', 'Homozygous deletion of SMN1 exon 7'),
                              ('Homozygous Deletion of EXON 7 and 8',
                               'Homozygous Deletion of EXON 7 and 8'),
                              ('Heterozygous Deletion of EXON 7 and 8 with compound heterozygous point mutation',
                               'Heterozygous Deletion of EXON 7 and 8 with compound heterozygous point mutation'),
                              ('Heterozygous Deletion of EXON 7 and 8 only)',
                               'Heterozygous Deletion of EXON 7 and 8 only')
                              ]
    geneticDiagnosis2 = models.CharField(max_length=100, blank=True, null=True, choices=genetic_diagnosis2_sel)
    final_diagnosis_sel = [("Infant type (SMAI) [OMIM 253300]", "Infant type (SMAI) [OMIM 253300]"),
                           ("Intermediate type (SMAII) [OMIM 253500]",
                            "Intermediate type (SMAII) [OMIM 253500]"),
                           ("Juvenile type (SMAIII) [OMIM 253400]",
                            "Juvenile type (SMAIII) [OMIM 253400]"),
                           ("Adult type (SMAIV) [OMIM 271150])",
                            "Adult type (SMAIV) [OMIM 271150]")
                           ]
    final_diagnosis_1 = models.CharField(max_length=100, blank=True, null=True, choices=final_diagnosis_sel)
    genetic_report_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    Treatment_RespiratorySupport = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Treatment_RespiratorySupport_ifyes_BIPAP = models.CharField(max_length=100, blank=True, null=True,
                                                                validators=[MaxLengthValidator(100)])
    Treatment_RespiratorySupport_ifyes_IPPR = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    Treatment_RespiratorySupport_ifyes_Ventilation = models.CharField(max_length=100, blank=True, null=True,
                                                                      validators=[MaxLengthValidator(100)])
    Feeding_Oral = models.CharField(max_length=100, blank=True, null=True,
                                    validators=[MaxLengthValidator(100)])
    Feeding_Nasogastric = models.CharField(max_length=100, blank=True, null=True,
                                           validators=[MaxLengthValidator(100)])
    Feeding_PEG = models.CharField(max_length=100, blank=True, null=True,
                                   validators=[MaxLengthValidator(100)])
    OperatedScoliosis = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    OperatedScoliosis_ifyes_age = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    CurrentPastTreatment_ReceivedNusinersin = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CurrentPastTreatment_ReceivedNusinersin_if_yes = models.CharField(max_length=100, blank=True, null=True,
                                                                      validators=[MaxLengthValidator(100)])
    CurrentPastTreatment_ReceivedRisdiplam = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CurrentPastTreatment_ReceivedRisdiplam_if_yes_age = models.CharField(max_length=100, blank=True, null=True,
                                                                         validators=[MaxLengthValidator(100)])
    CurrentPastTreatment_ReceivedZolgensma = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CurrentPastTreatment_ReceivedZolgensma_if_yes_age = models.CharField(max_length=100, blank=True, null=True,
                                                                         validators=[MaxLengthValidator(100)])
    outcome_sel = [('Alive ', 'Alive '), ('Dead', 'Dead')]
    finalOutcome = models.CharField(max_length=50, blank=True, null=True, choices=outcome_sel)
    finalOutcome_if_dead_age = models.DateField(blank=True, null=True)
    death_place_sel = [('Hospital  ', 'Hospital  '), ('Home', 'Home')]
    finalOutcome_death_place1 = models.CharField(max_length=50, blank=True, null=True, choices=death_place_sel)
    death_cause_sel = [('known ', 'known '), ('Not known', 'Not known')]
    finalOutcome_deathCause = models.CharField(max_length=50, blank=True, null=True, choices=death_cause_sel)
    death_cause_reason_sel = [('Respiratory failure  ', 'Respiratory failure  '), ('Aspiration', 'Aspiration')]
    finalOutcome_deathCause_known = models.CharField(max_length=50, blank=True, null=True,
                                                     choices=death_cause_reason_sel)
    finalOutcome_death_place2 = models.CharField(max_length=50, blank=True, null=True, choices=death_place_sel)
    carrier_testing_parents = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    prenatal_testing = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    prenatal_sel = [('MLPA ', 'MLPA '), ('QF-PCR ', 'QF-PCR ')]
    prenatal_testing_if_yes = models.CharField(max_length=50, blank=True, null=True, choices=prenatal_sel)
    nmd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class limb_gridle_nmd(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_nmd,related_name='limbnmd',  null=True, blank=True, on_delete=models.CASCADE)
    gender_sel = [('Male', 'Male'), ('Female ', 'Female')]
    limb_gender = models.CharField(max_length=50, blank=True, null=True, choices=gender_sel)
    evaluation_age = models.CharField(max_length=100, blank=True, null=True,
                                      validators=[MaxLengthValidator(100)])
    limb_symptoms_onset_age = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    yes_no_sel = [('yes', 'Yes'), ('No', 'No')]
    limb_born_consanguineous_parents = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    consanguineous_parents_sel = [('Uncle –niece', 'Uncle –niece'), ('First cousins', 'First cousins'),
                                  ('Distant relatives', 'Distant relatives')]
    limb_consanguineous_parents_if_yes = models.CharField(max_length=50, blank=True, null=True,
                                                          choices=consanguineous_parents_sel)
    MuscleHypertrophy = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MuscleWasting = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_3 = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_sel = [('Ankle', 'Ankle'), ('Knee', 'Knee'), ('Hip', 'Hip'), ('Elbow', 'Elbow'), ('Neck ', 'Neck ')]
    Contractures_3_yes = models.CharField(max_length=50, blank=True, null=True, choices=Contractures_sel)
    Contractures_3_ankle = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_3_knee = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_3_hip = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_3_elbow = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Contractures_3_neck = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    limb_weakness = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    limb_weakness_UpperlimbProximal = models.CharField(max_length=100, blank=True, null=True,
                                                       validators=[MaxLengthValidator(100)])
    limb_weakness_UpperlimbDistal = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    limb_weakness_LowerlimbProximal = models.CharField(max_length=100, blank=True, null=True,
                                                       validators=[MaxLengthValidator(100)])
    limb_weakness_lowerlimbDistal = models.CharField(max_length=100, blank=True, null=True,
                                                     validators=[MaxLengthValidator(100)])
    BulbarWeakness = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    bulbar_sel = [('Dysphagia', 'Dysphagia'),
                  ('Dysarthria', 'Dysarthria'),
                  ('Nasal regurgitation', 'Nasal regurgitation'),
                  ('Choking', 'Choking')
                  ]
    BulbarWeakness_if_yes = models.CharField(max_length=50, blank=True, null=True, choices=bulbar_sel)
    CardiacSymptoms = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    cardiac_symptoms_sel = [('Palpitations', 'Palpitations'),
                            ('Exertion induced dyspnoea', 'Exertion induced dyspnoea'),
                            ('Missed beats', 'Missed beats')]
    cardiac_symptoms_options = models.CharField(max_length=50, blank=True, null=True, choices=cardiac_symptoms_sel)
    RespiratorySymptoms = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RespiratorySymptoms_sel = [('Exertion induced dyspnoea', 'Exertion induced dyspnoea'), ('Orthopnoea', 'Orthopnoea'),
                               ('Breathlessness', 'Breathlessness')]
    RespiratorySymptoms_options = models.CharField(max_length=50, blank=True, null=True,
                                                   choices=RespiratorySymptoms_sel)
    Inheritance_sel = [('Autosomal dominant', 'Autosomal dominant'),
                       ('Autosomal recessive', 'Autosomal recessive'),
                       ('X-linked recessive', 'Missed beats'),
                       ('X-linked Dominant', 'X-linked Dominant')
                       ]
    InheritancePattern = models.CharField(max_length=50, blank=True, null=True, choices=Inheritance_sel)
    PositiveFamilyHistory = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_SiblingsAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_SiblingsAffected_number = models.IntegerField(blank=True, null=True)
    PositiveFamilyHistory_MotherAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_FatherAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_GrandmotherAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_GrandFatherAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_CousinsAffected = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_CousinsAffected_number = models.IntegerField(blank=True, null=True)
    PositiveFamilyHistory_AnyOther = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    PositiveFamilyHistory_AnyOther_specify = models.CharField(max_length=100, blank=True, null=True,
                                                              validators=[MaxLengthValidator(100)])
    PositiveFamilyHistory_AnyOther_Specify_names = models.CharField(max_length=100, blank=True, null=True,
                                                                    validators=[MaxLengthValidator(100)])

    PositiveFamilyHistory_upload_pedidegree = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    CurrentMotor_sel = [('Independently ambulant', 'Independently ambulant'),
                        ('. Needs physical assistance', '. Needs physical assistance'),
                        ('. Ambulant in home', '. Ambulant in home'), ('Wheel chair bound', 'Wheel chair bound'),
                        ('Bed Bound', 'Bed Bound')]
    current_motor = models.CharField(max_length=50, blank=True, null=True, choices=CurrentMotor_sel)
    CurrentMotor_yes_no = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CurrentMotor_if_yes_age = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    LaboratoryInvestigations_CK_level = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    NerveConductionStudies = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    NerveConduction_sel = [('Normal', 'Normal'), ('Sensory neuropathy', 'Sensory neuropathy'),
                           ('Sensory-motor neuropathy', 'Sensory-motor neuropathy')]
    NerveConductionStudies_options = models.CharField(max_length=50, blank=True, null=True, choices=NerveConduction_sel)
    CardiacEvaluation = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CardiacEvaluation_ECG = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    normal_abnormal_sel = [('Normal ', 'Normal'), ('Abnormal', 'Abnormal')]
    CardiacEvaluation_ECG_status = models.CharField(max_length=50, blank=True, null=True, choices=normal_abnormal_sel)
    CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia = models.CharField(max_length=50, blank=True, null=True,
                                                                           choices=yes_no_sel)
    Arrhythmia_sel = [('Atrial arrhythmias ', 'Atrial arrhythmias'), ('Conduction disease', 'Conduction disease'),
                      ('Bradycardia', 'Bradycardia'), ('Ventricular arrhythmias', 'Ventricular arrhythmias')]
    CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia_if_yes = models.CharField(max_length=50, blank=True, null=True,
                                                                                  choices=Arrhythmia_sel)
    limb_2DECHO = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    limb_2DECHO_status = models.CharField(max_length=50, blank=True, null=True, choices=normal_abnormal_sel)
    DECHO_sel = [('Dilated cardiomyopathy ', 'Dilated cardiomyopathy'),
                 ('Hypertrophic Cardiomyopathy', 'Hypertrophic Cardiomyopathy'), ('Any other ', 'Any other ')]
    limb_2DECHO_if_abnormal = models.CharField(max_length=50, blank=True, null=True, choices=DECHO_sel)
    limb_2DECHO_yes_no = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    limb_2DECHO_AnyOther = models.CharField(max_length=100, blank=True, null=True,
                                            validators=[MaxLengthValidator(100)])
    MuscleBiopsy = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MuscleBiopsy_Immunohistochemistry = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MuscleBiopsy_sel = [('Absent Dysferlin staining ', 'Absent Dysferlin staining'),
                        ('Absent Sarcoglycan staining', 'Absent Sarcoglycan staining'),
                        ('Absent Alpha-Dystroglycan staining', 'Absent Alpha-Dystroglycan staining'),
                        ('Absent Caveolin staining', 'Absent Caveolin staining')]
    MuscleBiopsy_if_yes = models.CharField(max_length=50, blank=True, null=True, choices=MuscleBiopsy_sel)
    DiagnosisConfirmed_sanger = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    DiagnosisConfirmed_nextGenerationSeq = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    next_generation_sel = [('Clinical Exome', 'Clinical Exome'),
                           ('Targeted panel', 'Targeted panel'),
                           ('Whole exome sequencing', 'Whole exome sequencing'),
                           ('Whole genome sequencing', 'Whole genome sequencing'),
                           ('MLPA', 'MLPA'),
                           ('Exome Array', 'Exome Array'), ]
    DiagnosisConfirmed_nextGenerationSeq_options = models.CharField(max_length=50, blank=True, null=True, choices=next_generation_sel)
    DiagnosisConfirmed_nextGenerationSeq_ClinicalExome = models.BooleanField(blank=True, null=True)
    DiagnosisConfirmed_nextGenerationSeq_TargetedPanel = models.BooleanField(blank=True, null=True)
    DiagnosisConfirmed_nextGenerationSeq_WholeExomeSequencing = models.BooleanField(blank=True, null=True)
    DiagnosisConfirmed_nextGenerationSeq_WholegGenomeSequencing = models.BooleanField(blank=True, null=True)
    DiagnosisConfirmed_nextGenerationSeq_MLPA = models.BooleanField(blank=True, null=True)
    DiagnosisConfirmed_nextGenerationSeq_ExomeArray = models.BooleanField(blank=True, null=True)
    upload_genetic_report = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    limb_mutation = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_Missense = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_Missense_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mutationDetails_Nonsense = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_Nonsense_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    mutationDetails_SpliceSite = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_SpliceSite_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                           validators=[MaxLengthValidator(100)])
    mutationDetails_Insertion = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_Insertion_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mutationDetails_Deletions = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_Deletions_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                          validators=[MaxLengthValidator(100)])
    mutationDetails_AnyOther_specify = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    mutationDetails_AnyOther_mutation = models.CharField(max_length=100, blank=True, null=True,
                                                         validators=[MaxLengthValidator(100)])
    MutationDetected_Homozygous = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MutationDetected_CompoundHeterozygous = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MutationDetected_Heterozygous = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    MutationDetected_VariantUnknownSignificance = models.CharField(max_length=100, blank=True, null=True,
                                                                   validators=[MaxLengthValidator(100)])
    gene_Location1 = models.CharField(max_length=100, blank=True, null=True,
                                     validators=[MaxLengthValidator(100)])
    gene_Variant1 = models.CharField(max_length=100, blank=True, null=True,
                                    validators=[MaxLengthValidator(100)])
    gene_Zygosity1 = models.CharField(max_length=100, blank=True, null=True,
                                     validators=[MaxLengthValidator(100)])
    gene_Disease1 = models.CharField(max_length=100, blank=True, null=True,
                                    validators=[MaxLengthValidator(100)])
    inheritence2_sel = [('AD', 'AD'), ('AR', 'AR'), ('XLD', 'XLD')]
    gene_Inheritance1 = models.CharField(max_length=50, blank=True, null=True, choices=inheritence2_sel)
    classification_sel = [('Pathogenic ', 'Pathogenic'), ('Likely pathogenic ', 'Likely pathogenic '),
                          ('Uncertain significance', 'Uncertain significance')]
    gene_classification1 = models.CharField(max_length=50, blank=True, null=True, choices=classification_sel)
    gene_Location = models.CharField(max_length=100, blank=True, null=True,
                                     validators=[MaxLengthValidator(100)])
    FinalGeneticDiagnosis = models.CharField(max_length=100, blank=True, null=True,
                                             validators=[MaxLengthValidator(100)])
    AR_LGMD_sel = [('LGMD 2A', 'LGMD 2A'), ('LGMD 2B', 'LGMD 2B'), ('LGMD 2C', 'LGMD 2C'), ('. LGMD 2D', '. LGMD 2D'),
                   ('LGMD 2E', 'LGMD 2E'), ('LGMD 2F', 'LGMD 2F'), ('LGMD 2G', 'LGMD 2G'), ('LGMD 2H', 'LGMD 2H'),
                   ('LGMD 2I', 'LGMD 2I'), ('LGMD 2J', 'LGMD 2J'), ('LGMD 2K', 'LGMD 2K'), ('LGMD 2L', 'LGMD 2L'),
                   ('LGMD 2M', 'LGMD 2M'), ('LGMD 2N', 'LGMD 2N'), ('LGMD 2O', 'LGMD 2O'), ('LGMD 2P', 'LGMD 2P'),
                   ('LGMD 2Q', 'LGMD 2Q'),
                   ('LGMD 2R', 'LGMD 2R'), ('LGMD 2S', 'LGMD 2S'), ('LGMD 2T', 'LGMD 2T'), ('LGMD 2U', 'LGMD 2U'),
                   ('LGMD 2V', 'LGMD 2V'), ('LGMD 2W', 'LGMD 2W'), ('LGMD 2X', 'LGMD 2X')]
    AR_LGMD_type = models.CharField(max_length=50, blank=True, null=True, choices=AR_LGMD_sel)
    ADLGMD_sel = [('LGMD 1A', 'LGMD 1A'), ('LGMD 1B', 'LGMD 1B'), ('LGMD 1C', 'LGMD 1C'), ('LGMD 1D', 'LGMD 1D'),
                  ('LGMD 1E', 'LGMD 1E'), ('LGMD 1F', 'LGMD 1F'), ('LGMD 1G', 'LGMD 1G'), ('LGMD 1H', 'LGMD 1H'),
                  ('LGMD 1I', 'LGMD 1I')]
    ADLGMD_type = models.CharField(max_length=50, blank=True, null=True, choices=ADLGMD_sel)
    SegregationPattern_Father = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    SegregationPattern_Mother = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    TreatmentReceived_TendonLengthening = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    TreatmentReceived_TendonLengthening_age = models.CharField(max_length=100, blank=True, null=True,
                                                               validators=[MaxLengthValidator(100)])
    Scoliosis_limb = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Scoliosis_SurgicalCorrection = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Scoliosis_SurgicalCorrection_age = models.CharField(max_length=100, blank=True, null=True,
                                                        validators=[MaxLengthValidator(100)])
    CardiacAbnormalities_pacemaker = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CardiacAbnormalities_Prophylactic = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    CardiacAbnormalities_CardiacTransplant = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RespiratoryAssistance = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RespiratoryAssistance_BiPAP = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RespiratoryAssistance_BiPAP_age = models.DateField(blank=True, null=True)
    RespiratoryAssistance_Ventilator = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    RespiratoryAssistance_Ventilator_age = models.DateField(blank=True, null=True)
    Final_Outcome_last_followup_Date = models.DateField(blank=True, null=True)
    death_status = [('Alive ', 'Alive '), ('Dead', 'Dead')]
    Final_Outcome_status = models.CharField(max_length=50, blank=True, null=True, choices=death_status)
    Final_Outcome_if_death_age = models.CharField(max_length=100, blank=True, null=True,
                                                  validators=[MaxLengthValidator(100)])
    Final_Outcome_death_cause = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    Final_Outcome_Cardiac = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    death_place = [('Death At home  ', 'Death At home  '), ('Hospital', 'Hospital')]
    Final_Outcome_death_place = models.CharField(max_length=50, blank=True, null=True, choices=death_place)
    Final_Outcome_Respiratory = models.CharField(max_length=50, blank=True, null=True, choices=yes_no_sel)
    Final_Outcome_Respiratory_place = models.CharField(max_length=50, blank=True, null=True, choices=death_place)
    nmd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

###################
