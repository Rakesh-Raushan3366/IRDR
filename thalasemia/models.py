# Create your models here.

# Create your models here.

# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator

class profile_thalassemia(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)

    th_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    th_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    th_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    th_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    th_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_given_sel = [('Yes', 'Yes'), ('No', 'No'), ('Unable to assent', 'Unable to assent')]
    th_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_date_record = models.DateField(blank=True, null=True)
    date_clinical_examination = models.DateField(blank=True, null=True)
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    th_paitent_id = models.CharField(max_length=100, null=True, blank=True, choices=id_sel)
    th_patient_id_no = models.CharField(max_length=100, unique=True, blank=True, null=True,
                                        validators=[MaxLengthValidator(100)])
    th_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_patient_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    th_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_patient_adhaar_no = models.CharField(max_length=10, null=True, choices=th_status_sel)
    th_patient_adhaar_no_specify = models.CharField(max_length=100, unique=True, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    th_father_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    th_father_id_no = models.CharField(max_length=100, unique=True, blank=True, null=True,
                                       validators=[MaxLengthValidator(100)])
    th_father_adhaar_no = models.CharField(max_length=10, null=True, blank=True, choices=th_status_sel)
    th_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    th_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE, verbose_name=' state')
    th_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE, verbose_name=' district')
    th_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_mother_mobile_no = models.PositiveBigIntegerField(null=True, unique=True)
    th_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    th_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    th_email = models.EmailField(max_length=300, blank=True, null=True)
    th_religion = models.CharField(max_length=100, blank=True, null=True, choices=th_religion_sel)
    th_religion_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                                 validators=[MaxLengthValidator(100)])
    th_caste = models.CharField(max_length=100, blank=True, null=True, choices=th_caste_sel)
    th_caste_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                              validators=[MaxLengthValidator(100)])
    th_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=th_referred_by)
    th_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_gender = models.CharField(max_length=100, blank=True, null=True, choices=th_gender_sel)
    th_consent_given = models.CharField(max_length=10, null=True, choices=th_status_sel)
    th_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    th_assent_given = models.CharField(max_length=30,  null=True, choices=yes_no_given_sel)
    th_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    th_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_date_of_birth = models.DateField( null=True)
    th_nationality = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    th_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    diseases = [('Thalassemia', 'Thalassemia'), ('Glycogen', 'Glycogen'), ('Fabridisease', 'Fabridisease'),
                ('BleedingDisorder', 'BleedingDisorder')]
    th_icmr_disease = models.CharField(max_length=100, blank=True, null=True, choices=diseases)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    uniqueId = models.CharField(null=True, blank=True, max_length=500, validators=[MaxLengthValidator(500)])

    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_thalasemia', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_thalasemia', on_delete=models.CASCADE)
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    quality_result = models.CharField(max_length=10, blank=True, null=True, choices=quality_score)
    quality_reason = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
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
            super(profile_thalassemia, self).save(*args, **kwargs)
            self.th_icmr_unique_no = str('Thalassemia/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_thalassemia, self).save(*args, **kwargs)


class demographic_thalassemia(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_thalassemia, null=True, related_name='patient_thalassemia', blank=True, on_delete=models.CASCADE)

    th_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_na = [('Yes', 'Yes'), ('No', 'No'), ('NA', 'NA')]
    yes_no_notdone = [('Yes', 'Yes'), ('No', 'No'), ('Not done', 'Not done')]
    th_patient_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                          ('Secondary '
                           'level',
                           'Secondary '
                           'level'),
                          ('College and above', 'College and above')]
    th_patient_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                           ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    th_father_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    th_father_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    th_mother_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                         ('Secondary '
                          'level',
                          'Secondary '
                          'level'),
                         ('College and above', 'College and above')]
    th_mother_occu_sel = [('Home maker', 'Home maker)'),
                          ('Employed (organised sector)', 'Employed (organised sector)'),
                          ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    th_monthly_income_sel = [('> 126,360', '> 126,360)'),
                             ('63,182 – 126,356)', '63,182 – 126,356)'),
                             ('47,266 – 63,178', '47,266 – 63,178'),
                             ('31,591 - 47,262', '31,591 - 47,262'),
                             ('18,953 - 31,589', '18,953 - 31,589'),
                             ('6,327 - 18,949', '6,327 - 18,949'),
                             ('< 6,323', '< 6,323')]

    th_nontribal_sel = [('Sindhi', 'Sindhi'), ('Lohana', 'Lohana'), ('Bhanushali ', 'Bhanushali '),
                        ('Khatri', 'Khatri'), ('Arora', 'Arora'), ('Jain ', 'Jain '), ('Others', 'Others')]
    th_patient_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=th_patient_edu_sel)
    th_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=th_patient_occu_sel)
    th_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=th_father_edu_sel)
    th_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=th_father_occu_sel)
    th_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=th_mother_edu_sel)
    th_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=th_mother_occu_sel)
    th_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=th_monthly_income_sel)
    th_tribal = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_non_tribal_caste = models.CharField(max_length=50, blank=True, null=True, choices=th_nontribal_sel)

    diagnosis_sel = [('Beta Thalassemia ', 'Beta Thalassemia '), ('Sickle cell anemia ', 'Sickle cell anemia'),
                     ('Sickle Beta thalassemia', 'Sickle Beta thalassemia'),
                     ('Sickle – Hemoglobin C disease', 'Sickle – Hemoglobin C disease'),
                     ('Hemoglobin E – beta thalassemia', 'Hemoglobin E – beta thalassemia'),
                     ('Hemoglobin D – beta thalassemia', 'Hemoglobin D – beta thalassemia'),
                     ('Alpha thalassemia [Hb H disease', 'Alpha thalassemia [Hb H disease'),
                     ('Any other', 'Any other')]
    th_diagnosis_type = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_sel)
    th_diagonosis_other_specify = models.CharField(max_length=50, blank=True, null=True,
                                                   validators=[MaxLengthValidator(50)])
    th_presentation_age = models.CharField(max_length=50, blank=True, null=True,
                                           validators=[MaxLengthValidator(50)])
    th_diagnosis_age = models.CharField(max_length=50, blank=True, null=True,
                                        validators=[MaxLengthValidator(50)])
    th_pres_feature = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_pallor = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_yellowness = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_rec_fever = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_dist_abd = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_lethargy = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pres_fatigue = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_curr_child_age = models.CharField(max_length=50, blank=True, null=True,
                                         validators=[MaxLengthValidator(50)])

    neuro_ab_sel = [('Stroke', 'Stroke'),
                    ('Transient ischemic attack [TIA]', 'Transient ischemic attack [TIA]'),
                    ('Neuropathic pain', 'Neuropathic pain'),
                    ('Other', 'Other'),
                    ]
    renal_inv_sel = [('Facial puffiness', 'Facial puffiness'),
                     ('Decreased urine output', 'Decreased urine output'),
                     ('Other', 'Other'), ]
    iron_overload_sel = [('Cardiac', 'Cardiac'), ('Endocrine', 'Endocrine'), ('Growth ', 'Growth')]
    hist_infection_sel = [('Pneumonia', 'Pneumonia'), ('Sepsis', 'Sepsis'), ('Osteomyelitis ', 'Osteomyelitis'),
                          ('Other', 'Other')]
    th_consanguinity = models.CharField(max_length=100, blank=True, null=True,
                                        validators=[MaxLengthValidator(100)])
    th_sibling_aff = models.CharField(max_length=100, blank=True, null=True,
                                      validators=[MaxLengthValidator(100)])
    th_other_family_mem = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_other_family_mem_details = models.CharField(max_length=100, blank=True, null=True,
                                                   validators=[MaxLengthValidator(100)])
    th_pedigree_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    th_f_fatigue = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_dyspnoea = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_rec_fever = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_abdominal_pain = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_chest_pain = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_bone_joint_pain = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_any_other = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_f_any_other_specify = models.CharField(max_length=50, blank=True, null=True,
                                              validators=[MaxLengthValidator(50)])
    th_f_past_hist = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_crisis_num = models.IntegerField(blank=True, null=True)
    th_crisis_num_last_12 = models.IntegerField(blank=True, null=True)
    th_acute_chest_syndrome = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_crisis_hyperhemolyitc = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_crisis_pain_pr_yr_before_hydoxyurea = models.IntegerField(blank=True, null=True)
    th_crisis_pain_pr_yr_after_hydoxyurea = models.IntegerField(blank=True, null=True)
    th_other_illness = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_other_illness_name = models.CharField(max_length=50, blank=True, null=True,
                                             validators=[MaxLengthValidator(50)])
    th_other_illness_age = models.CharField(max_length=50, blank=True, null=True,
                                            validators=[MaxLengthValidator(50)])
    th_other_illness_dur = models.CharField(max_length=50, blank=True, null=True,
                                            validators=[MaxLengthValidator(50)])
    th_height = models.FloatField(blank=True, null=True)
    th_height_z_score = models.FloatField(blank=True, null=True)
    th_weight = models.FloatField(blank=True, null=True)
    th_weight_z_score = models.FloatField(blank=True, null=True)
    th_hemolytic_facies = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_pallor = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_jaundice = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_edema = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_leg_ulcers = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_hepatomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_notdone)
    th_splenomegaly = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_notdone)
    th_any_systematic_anom = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_any_sys_ab_specify = models.CharField(max_length=50, blank=True, null=True,
                                             validators=[MaxLengthValidator(50)])
    th_neurological_abnor = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_neurological_abnor_option = models.CharField(max_length=32, blank=True, null=True, choices=neuro_ab_sel)
    th_neurological_abnor_option_other = models.CharField(max_length=50, blank=True, null=True,
                                                          validators=[MaxLengthValidator(50)])
    th_renal_involvement = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_renal_involvement_opts = models.CharField(max_length=50, blank=True, null=True, choices=renal_inv_sel)
    th_renal_involvement_opts_other = models.CharField(max_length=50, blank=True, null=True,
                                                       validators=[MaxLengthValidator(50)])
    th_feet_swelling = models.CharField(max_length=32, blank=True, null=True, choices=th_status_sel)
    th_clin_leg_ulcers = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_clin_gallstones = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_clin_gallstones_specify = models.CharField(max_length=50, blank=True, null=True,
                                                  validators=[MaxLengthValidator(50)])
    th_iron_overload = models.CharField(max_length=10, blank=True, null=True, choices=iron_overload_sel)
    th_iron_overload_specify = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_iron_overload_yes_no = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_iron_overload_cardiac = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_iron_overload_Endocrine = models.CharField(max_length=50, blank=True, null=True,
                                                  validators=[MaxLengthValidator(50)])
    th_iron_overload_Growth = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])

    th_hist_infection = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_hist_infection_opt = models.CharField(max_length=50, blank=True, null=True, choices=hist_infection_sel)
    th_hist_infection_opt_other_specify = models.CharField(max_length=50, blank=True, null=True,
                                                           validators=[MaxLengthValidator(50)])

    red_morph_sel = (
        ('Hypochromic', 'Hypochromic'),
        ('Microcytic ', 'Microcytic '),
        ('Anisocytosis', 'anisocytosis'),
        ('poikilocytosis', 'poikilocytosis'),
        ('Target Cells', 'Target Cells'),
        ('Other', 'Other'),
    )
    alpha_thal_sel = (
        ('αα/αα ', 'αα/αα'),
        ('αα/-α^3.7', 'αα/-α^3.7'),
        ('-α^3.7/-α^3.7', '-α^3.7/-α^3.7'),
        ('-α^4.2/-α^4.2', '-α^4.2/-α^4.2'),
        ('αα/--SA', 'αα/--SA'),
        ('αα/--SEA', 'αα/--SEA'),
        ('αα/--MED', 'αα/--MED')

    )

    hbh_sel = [('-α^3.7/--SEA', '-α^3.7/--SEA'), ('-α^4.2 /--SA', '-α^4.2 /--SA'), ('Other', 'Other')]
    inter_pret_sel = (
        ('Heterozygote', 'Heterozygote'),
        ('Homozygote', 'Homozygote'),
        ('Compound Heterozygote', 'Compound Heterozygote')
    )
    pos_neg_sel = [('+', '+'), ('-', '-')]
    th_haem_wbc = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_hb = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_mcv = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_mch = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_mchc = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_rbc_count = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_rdw_per = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_plts = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_retic_count = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_red_cell_morphology = models.CharField(max_length=30, blank=True, null=True, choices=th_status_sel)
    th_red_cell_morphology_1 = models.BooleanField(default=False)
    th_red_cell_morphology_2 = models.BooleanField(default=False)
    th_red_cell_morphology_3 = models.BooleanField(default=False)
    th_red_cell_morphology_4 = models.BooleanField(default=False)
    th_red_cell_morphology_5 = models.BooleanField(default=False)
    th_red_cell_morphology_other = models.BooleanField(default=False)

    th_red_cell_morphology_other_specify = models.CharField(max_length=100, blank=True, null=True,
                                                            validators=[MaxLengthValidator(100)])
    th_haem_hba = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_hbf = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_hba2 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_var_hb = models.CharField(max_length=30, blank=True, null=True, choices=th_status_sel)
    th_haem_var_hb_hbs = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_var_hb_hbe = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_var_hb_hbd = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_haem_var_hb_other_per = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_haem_var_hb_retention_time = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    th_haem_hpcl_det = models.CharField(max_length=30, blank=True, null=True, choices=th_status_sel)
    th_haem_hbh_incl = models.CharField(max_length=30, blank=True, null=True, choices=th_status_sel)
    th_haem_unstable_haem = models.CharField(max_length=30, blank=True, null=True, choices=th_status_sel)
    th_haem_mol_incl = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_mol_alpha_thal = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_notdone)
    th_mol_alpha_thal_opt = models.CharField(max_length=32, blank=True, null=True, choices=alpha_thal_sel)
    th_mol_hbh_thal_opt = models.CharField(max_length=32, blank=True, null=True, choices=hbh_sel)
    th_mol_alpha_thal_opt_other = models.CharField(max_length=50, blank=True, null=True,
                                                   validators=[MaxLengthValidator(50)])
    th_mol_beta_thal = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    # th_mol_beta_thal_opt = models.CharField(max_length=32, blank=True, null=True, choices=beta_thal_sel)
    th_mol_beta_thal_opt_1 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_2 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_3 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_4 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_5 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_6 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_7 = models.BooleanField(default=False)
    th_mol_beta_thal_opt_8 = models.BooleanField(default=False)
    th_mol_beta_thal_other_spec = models.CharField(max_length=50, blank=True, null=True,
                                                   validators=[MaxLengthValidator(50)])
    interpretation_sel = [('Heterozygote', 'Heterozygote'), ('Homozygote', 'Homozygote'),
                          ('Compound Heterozygote', 'Compound Heterozygote')]
    th_mol_interpretaion = models.CharField(max_length=50, blank=True, null=True, choices=interpretation_sel)
    th_HPFH_test = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_HPFH_test_result = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_mol_alpha_beta_test = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_mol_alpha_beta_test_result = models.CharField(max_length=50, blank=True, null=True,
                                                     validators=[MaxLengthValidator(50)])
    th_upload_report = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    th_curr_invest_date = models.DateField(blank=True, null=True)
    th_curr_pretasnsfusion = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_curr_post_transfusion = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_curr_hiv = models.CharField(max_length=15, blank=True, null=True, choices=pos_neg_sel)
    th_curr_hbsag = models.CharField(max_length=15, blank=True, null=True, choices=pos_neg_sel)
    th_curr_hcv = models.CharField(max_length=15, blank=True, null=True, choices=pos_neg_sel)
    th_treat_recieved = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_bio_serum_ferritin = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_serum_dehyd = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_vitamin_b12 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_folate_levels = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])

    th_bio_ser_bilirubin = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_alan_amino = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_ser_alkline = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_alkaline_phas = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_ser_calc = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_ser_calc_ionized = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    th_bio_ser_phosp = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_s_creatinine = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_t4 = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_tsh = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_bio_s_cortisol_early = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    th_bio_s_cortisol_stimulates = models.CharField(max_length=50, blank=True, null=True,
                                                    validators=[MaxLengthValidator(50)])
    th_bio_blood_sugar_fast = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    th_bio_blood_sugar_post_meal = models.CharField(max_length=50, blank=True, null=True,
                                                    validators=[MaxLengthValidator(50)])
    th_ecg = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_ECHOcardiography = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_Any_other = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])

    bone_marrow_sel = [('Done', 'Done'), ('planned', 'planned'),
                       ('No HLA matched donor', 'No HLA matched donor'),
                       ('Not considered', 'Not considered'),
                       ('under consideration', 'under consideration')]
    bmt_outcome_sel = [('Cured', 'Cured'), (' No engraftment', ' No engraftment')]
    management_sel = [('Well managed', 'Well managed'),
                      ('Sub-optimally managed', 'Sub-optimally managed'),
                      ('Poorly managed', 'Poorly managed')]
    f_diagnosis_sel = [('Beta thalassemia major', 'Beta thalassemia major'),
                       ('Non transfusion dependent beta thalassemia [Homozygous beta thalassemia]',
                        'Non transfusion dependent beta thalassemia [Homozygous beta thalassemia]'),
                       ('Non transfusion dependent beta thalassemia [Heterozygous beta thalassemia]',
                        'Non transfusion dependent beta thalassemia [Heterozygous beta thalassemia]'),
                       ('Beta thalassemia – Hb variant', 'Beta thalassemia – Hb variant'),
                       ('Sickle cell disease', 'Sickle cell disease'),
                       ('Hb H disease', 'Hb H disease'),
                       ('Any other', 'Any other')]
    chelation_sel = [('Deferoxamine (Desferal)', 'Deferoxamine (Desferal)'),
                     ('Deferasirox (Exjade)', 'Deferasirox (Exjade)'),
                     ('Deferiprone (L1)', 'Deferiprone (L1)'), ('Other', 'Other')]
    th_bone_marrow_treat = models.CharField(max_length=30, blank=True, null=True, choices=bone_marrow_sel)
    th_bmt_done = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_bmt_done_outcome = models.CharField(max_length=30, blank=True, null=True, choices=bmt_outcome_sel)
    th_hyper_trans_therapy = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_inter_transfusion = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_splenectomy = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_splenectomy_age = models.FloatField(blank=True, null=True)
    th_diagnosis_age1 = models.CharField(max_length=50, blank=True, null=True,
                                         validators=[MaxLengthValidator(50)])
    th_transfusion = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_na)
    th_transfusion_age = models.CharField(max_length=50, blank=True, null=True,
                                          validators=[MaxLengthValidator(50)])
    th_transfusion_frequency = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_hydroxyurea = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_notdone)
    th_hydroxyurea_dose = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_hydroxyurea_duration = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    th_pre_hydroxyurea_hb = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_post_hydroxyurea_hb = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_pre_hydroxyurea_trans = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_post_hydroxyurea_trans = models.CharField(max_length=50, blank=True, null=True,
                                                 validators=[MaxLengthValidator(50)])
    th_hydroxyurea_pain = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_any_other_disease = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_any_other_disease_detail = models.CharField(max_length=50, blank=True, null=True,
                                                   validators=[MaxLengthValidator(50)])
    th_chelation_status = models.CharField(max_length=10, blank=True, null=True, choices=yes_no_notdone)
    th_deferoxamine_dose = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_deferasirox_dose = models.CharField(max_length=50, blank=True, null=True, choices=chelation_sel)
    th_deferasirox_dose_other_specify = models.CharField(max_length=50, blank=True, null=True,
                                                         validators=[MaxLengthValidator(50)])
    th_deferiprone_dose = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_other_dose = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_any_other_disease_dur = models.CharField(max_length=50, blank=True, null=True,
                                                validators=[MaxLengthValidator(50)])
    th_other_medication = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    th_final_diagnosis = models.CharField(max_length=75, blank=True, null=True, choices=f_diagnosis_sel)
    th_f_diag_other_specify = models.CharField(max_length=50, blank=True, null=True,
                                               validators=[MaxLengthValidator(50)])
    th_comp_iron_overload = models.CharField(max_length=10, blank=True, null=True, choices=th_status_sel)
    th_comp_iron_overload_detail = models.CharField(max_length=100, blank=True, null=True,
                                                    validators=[MaxLengthValidator(100)])
    th_comp_iron_overload_beta_thalassemia_detail = models.CharField(max_length=100, blank=True, null=True,
                                                                     validators=[MaxLengthValidator(100)])
    th_impr_mngt = models.CharField(max_length=30, blank=True, null=True, choices=management_sel)
    th_filled_by_deo_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_filled_by_name = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    th_filled_date = models.DateField(blank=True, null=True)
    th_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)
