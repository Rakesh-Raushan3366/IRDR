# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator

class profile_bleeding(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    bd_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    bd_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    bd_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    bd_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    bd_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    bd_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_date_of_record = models.DateField(blank=True, null=True)
    bd_date_of_birth = models.DateField( null=True)
    bd_date_of_clinical_exam = models.DateField(blank=True, null=True)
    bd_patient_name = models.CharField(max_length=100, null=True, validators=[MaxLengthValidator(100)])
    bd_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id')]
    bd_paitent_id_yes_no = models.CharField(max_length=100, null=True, choices=bd_status_sel)
    bd_paitent_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    bd_patient_id_no = models.CharField(max_length=100, blank=True, unique=True, null=True, validators=[MaxLengthValidator(100)])
    bd_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    # bd_patient_adhaar_no = models.BigIntegerField(blank=True, null=True)
    bd_mother_father_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    bd_mother_father_id_no = models.PositiveBigIntegerField(blank=True, null=True)
    bd_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    bd_state = models.ForeignKey(State, null=True, on_delete=models.CASCADE)
    bd_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE)
    bd_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_mother_mobile_no = models.PositiveBigIntegerField(null=True, unique=True)
    bd_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    bd_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    bd_email = models.EmailField(max_length=300, blank=True, null=True)
    bd_religion = models.CharField(max_length=100, blank=True, null=True, choices=bd_religion_sel)
    bd_caste = models.CharField(max_length=100, blank=True, null=True, choices=bd_caste_sel)
    bd_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=bd_status_sel)
    bd_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=bd_referred_by)
    bd_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_gender = models.CharField(max_length=100, blank=True, null=True, choices=bd_gender_sel)
    bd_consent_given = models.CharField(max_length=10, null=True, choices=bd_status_sel)
    bd_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, validators=[FileExtensionValidator(['pdf'])])
    bd_assent_given = models.CharField(max_length=10,  null=True, choices=bd_status_sel)
    bd_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    bd_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'),('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]

    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_bleeding', on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_bleeding', on_delete=models.CASCADE)

    quality_result = models.CharField(max_length=20, blank=True, null=True, choices=quality_score)
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    quality_reason = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    uniqueId = models.CharField(null=True, blank=True, max_length=500)
    yes_no_na = [('Yes','Yes'), ('No','No'), ('Na','Na')]
    complete = models.CharField(max_length=10, blank=True, null=True,default='No', choices=yes_no_na)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.uniqueId is None:
            self.uniqueId = str(uuid4())
            count1 = State.objects.count()
            count2 = 0
            count2 += count1
            super(profile_bleeding, self).save(*args, **kwargs)
            self.bd_icmr_unique_no = str('Bleeding/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_bleeding, self).save(*args, **kwargs)


class demographic_bleeding(models.Model):
    patient = models.ForeignKey(profile_bleeding, null=True, blank=True,related_name='patient_bleeding', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)

    curr_study_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_na = [('Yes', 'Yes'), ('No', 'No'), ('NA', 'NA')]
    yes_no_notdone = [('Yes', 'Yes'), ('No', 'No'), ('Not done', 'Not done')]
    patient_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                       ('Secondary '
                        'level',
                        'Secondary '
                        'level'),
                       ('College and above', 'College and above')]
    patient_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
                        ('Employed (Unorganised sector)', 'Employed (Unorganised sector)'), ('Others', 'Others')]
    father_edu_sel = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School'),
                      ('Secondary '
                       'level',
                       'Secondary '
                       'level'),
                      ('College and above', 'College and above')]
    father_occu_sel = [('Employed (organised sector)', 'Employed (organised sector)'),
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

    bd_patient_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=patient_edu_sel)
    bd_patient_occupation = models.CharField(max_length=50, blank=True, null=True, choices=patient_occu_sel)
    bd_father_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=father_edu_sel)
    bd_father_occupation = models.CharField(max_length=50, blank=True, null=True, choices=father_occu_sel)
    bd_mother_edu_status = models.CharField(max_length=50, blank=True, null=True, choices=mother_edu_sel)
    bd_mother_occupation = models.CharField(max_length=50, blank=True, null=True, choices=mother_occu_sel)
    bd_monthly_income_status = models.CharField(max_length=50, blank=True, null=True, choices=monthly_income_sel)

    diagnosis_sel = [('Hemophilia A', 'Hemophilia A'), ('Hemophilia B', 'Hemophilia B'),
                     ('Von Willebranddisease', 'Von Willebranddisease'), ('Any other', 'Any other')]
    diagnosis_age_sel = [('Prenatal', 'Prenatal'), ('At birth', 'At birth'),
                         ('Less than 1 year', 'Less than 1 year'), ('1-2 years', '1-2 years'),('2-5 years', '2-5 years'),
                         ('5-12 years', '5-12 years'), ('12-18 years', '12-18 years'),
                         ('more than 18 years', 'more than 18 years'), ('unknown', 'unknown')]
    blood_pressure_sel = [('Hypertensive', 'Hypertensive'), ('Normotensive', 'Normotensive')]
    status_sel = [('Yes', 'Yes'), ('No', 'No')]
    diagnosis_method_sel = [('Coagulation tests Specify', 'Coagulation tests Specify'),
                            ('Genotypic', 'Genotypic'), ('Both', 'Both')]
    blood_group_sel = [('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'),
                       ('O+', 'O+'), ('O-', 'O-'), ('Others', 'Others')]
    status_sel_2 = [('Positive', 'Positive'), ('Negative', 'Negative'), ('Unknown', 'Unknown')]
    factory_deficiency_sel = [('FVIII', 'FVIII'), ('FIX', 'FIX'), ('NA', 'NA'), ('Others', 'Others')]
    severity_sel = [('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe'), ('NA', 'NA'),]
    vwf_method_sel = [('Immunoelectrophoresis', 'Immunoelectrophoresis'), ('ELISA', 'ELISA'), ('LIA', 'LIA')]
    screen_test_sel = [('Positive', 'Positive'), ('Negative', 'Negative'), ('Ambiguous', 'Ambiguous')]
    inhibitor_method_sel = [('Classical Bethesda', 'Classical Bethesda'), ('NBA', 'NBA'), ('ELISA', 'ELISA')]
    platelet_aggr_sel = [('Ristocetin low dose (%)', 'Ristocetin low dose (%)'),
                         ('Ristocetin high dose (%)', 'Ristocetin high dose (%)'), ('ADP (%)', 'ADP (%)'),
                         ('Collagen (%)', 'Collagen (%)'), ('Epinephrine (%)', 'Epinephrine (%)'),
                         ('Arachidonic acid (%)', 'Arachidonic acid (%)'), ('Others (%)', 'Others (%)')]
    platelet_rec_sel = [('Gb1b (%)', 'Gb1b (%)'), ('GPV (%)', 'GPV (%)'), ('GPIX (%)', 'GPIX (%)'),
                        ('GP1b/IX(%)', 'GP1b/IX(%)'), ('GPIIb(%)', 'GPIIb(%)'),
                        ('GPIIIa (%)', 'GPIIIa (%)'), ('GPIIb/IIIa(%)', 'GPIIb/IIIa(%)'),
                        ('Fibrinogen(%)', 'Fibrinogen(%)'), ('Collagen(%)', 'Collagen(%)'),
                        ('Others(%)', 'Others(%)')]
    final_diag_sel = [('Hemophilia A', 'Hemophilia A'), ('Hemophilia B', 'Hemophilia B'),
                      ('VWD', 'VWD'), ('Other Rare Disorders', 'Other Rare Disorders')]
    female_status_sel = [('Carrier', 'Carrier'), ('Non Carrier', 'Non Carrier'), ('Unknown', 'Unknown')]
    ant_fem_status_sel = [('Chorionic Villus Sampling', 'Chorionic Villus Sampling'),
                          ('Amniocentesis', 'Amniocentesis'), ('Cordocentesis', 'Cordocentesis')]
    ant_result_sel = [('Affected', 'Affected'), ('Unaffected', 'Unaffected')]
    stud_sel = [('1', '1'), ('2', '2')]

    bd_diagnosis_type_1 = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_sel)
    bd_diagnosis_type_other = models.CharField(max_length=100, blank=True, null=True,
                                               validators=[MaxLengthValidator(100)])
    bd_anthr_weight = models.FloatField(blank=True, null=True)
    bd_anthr_height = models.FloatField(blank=True, null=True)
    bd_anthr_head_circum = models.FloatField(blank=True, null=True)
    bd_diagnosis_age = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_age_sel)
    bd_first_bleed_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_bleeding_site = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_blood_pressure_type = models.CharField(max_length=50, blank=True, null=True, choices=blood_pressure_sel)
    bd_blooding_fam_hist = models.CharField(max_length=10, blank=True, null=True, choices=status_sel)
    bd_fam_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_fam_reln = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_fam_daignosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_test_center_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_diagnosis_method = models.CharField(max_length=50, blank=True, null=True, choices=diagnosis_method_sel)
    bd_blood_group = models.CharField(max_length=10, blank=True, null=True, choices=blood_group_sel)
    bd_hiv_status = models.CharField(max_length=15, blank=True, null=True, choices=status_sel_2)
    bd_hbv_status = models.CharField(max_length=15, blank=True, null=True, choices=status_sel_2)
    bd_hcv_status = models.CharField(max_length=15, blank=True, null=True, choices=status_sel_2)
    bd_factory_deficiency = models.CharField(max_length=15, blank=True, null=True, choices=factory_deficiency_sel)
    bd_factory_deficiency_other = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_factory_level_per = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_factory_severity = models.CharField(max_length=15, blank=True, null=True, choices=severity_sel)
    bd_vwf_antigen_per = models.FloatField(blank=True, null=True)
    bd_vwf_method = models.CharField(max_length=30, blank=True, null=True, choices=vwf_method_sel)
    bd_vwf_ris_cofactor = models.FloatField(blank=True, null=True)
    bd_screening_test = models.CharField(max_length=30, blank=True, null=True, choices=screen_test_sel)
    bd_quant_assay = models.CharField(max_length=30, blank=True, null=True, choices=status_sel)
    bd_inhibitor_method = models.CharField(max_length=30, blank=True, null=True, choices=inhibitor_method_sel)
    bd_inhibitor_titer = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_count = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_agregatin = models.CharField(max_length=30, blank=True, null=True, choices=platelet_aggr_sel)
    bd_platelet_agregatin_Ristocetin_low_dose = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # bd_platelet_agregatin_Ristocetin_low_dose = models.CharField(max_length=100, blank=True, null=True,
    #                                                            validators=[MaxLengthValidator(100)])
    bd_platelet_agregatin_Ristocetin_high_dose = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_agregatin_ADP = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_agregatin_Collagen = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    bd_platelet_agregatin_Epinephrine = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    bd_platelet_agregatin_Arachidonic_acid = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    bd_platelet_agregatin_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_agregatin_per_value = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # bd_platelet_receptors = models.CharField(max_length=30, blank=True, null=True, choices=platelet_rec_sel)
    bd_platelet_receptors_1 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_2 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_3 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_4 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_5 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_6 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_7 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_8 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_9 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_platelet_receptors_perc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_mutation_identified = models.CharField(max_length=30, blank=True, null=True, choices=status_sel)
    bd_mutation_type = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_final_diagnosis = models.CharField(max_length=30, blank=True, null=True, choices=final_diag_sel)
    bd_fam_pedigree = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    bd_diag_invest_report = models.FileField(max_length=50, blank=True, null=True)
    bd_carrier_studies = models.CharField(max_length=100, blank=True, null=True, choices=stud_sel)
    bd_carr_female_1_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_carr_female_1_adhaar = models.IntegerField(blank=True, null=True)
    bd_carr_female_1_dob = models.DateField(blank=True, null=True)
    bd_carr_female_1_age = models.IntegerField(blank=True, null=True)
    bd_carr_female_1_rel_index = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_carr_female_1_status = models.CharField(max_length=30, blank=True, null=True, choices=female_status_sel)
    bd_carr_female_1_dos = models.DateField(blank=True, null=True)
    bd_carr_female_2_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_carr_female_2_adhaar = models.IntegerField(blank=True, null=True)
    bd_carr_female_2_dob = models.DateField(blank=True, null=True)
    bd_carr_female_2_age = models.IntegerField(blank=True, null=True)
    bd_carr_female_2_rel_index = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_carr_female_2_status = models.CharField(max_length=30, blank=True, null=True, choices=female_status_sel)
    bd_carr_female_2_dos = models.DateField(blank=True, null=True)
    bd_carr_any_other_details = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_studies = models.IntegerField(blank=True, null=True, choices=stud_sel)
    bd_ante_female_1_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_1_adhaar = models.IntegerField(blank=True, null=True)
    bd_ante_female_1_dob = models.DateField(blank=True, null=True)
    bd_ante_female_1_age = models.IntegerField(blank=True, null=True)
    bd_ante_female_1_rel_index = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_1_proc = models.CharField(max_length=30, blank=True, null=True, choices=ant_fem_status_sel)
    bd_ante_female_1_per_by = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_1_dos = models.DateField(blank=True, null=True)
    bd_ante_female_1_res = models.CharField(max_length=30, blank=True, null=True, choices=ant_result_sel)
    bd_ante_other_info_1 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_2_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_2_adhaar = models.IntegerField(blank=True, null=True)
    bd_ante_female_2_dob = models.DateField(blank=True, null=True)
    bd_ante_female_2_age = models.IntegerField(blank=True, null=True)
    bd_ante_female_2_rel_index = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_2_proc = models.CharField(max_length=30, blank=True, null=True, choices=ant_fem_status_sel)
    bd_ante_female_2_per_by = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_ante_female_2_dos = models.DateField(blank=True, null=True)
    bd_ante_female_2_res = models.CharField(max_length=30, blank=True, null=True, choices=ant_result_sel)
    bd_ante_other_info_2 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])

    exposure_days_sel = [('<20', '<20'), ('>20', '>20'), ('>50', '>50'), ('Others', 'Others')]
    ondemand_sel = (
        ('On demand', 'On demand'),
        ('Prophylaxis', 'Prophylaxis'),
        ('ITI', 'ITI')
        )
    source_funding_sel = [('Self', 'Self'), ('Employer', 'Employer'), ('Government support', 'Government support'),
                          ('ESIS', 'ESIS'),
                          ('Personal grant from PM/CM fund', 'Personal grant from PM/CM fund'),
                          ('Other', 'Other')]
    status_sel = [('Yes', 'Yes'), ('No', 'No')]
    inhibitor_sel = [('Positive', 'Positive'), ('Negative', 'Negative')]
    transfusion_sel = [('Factor', 'Factor'), ('FEIBA replacement', 'FEIBA replacement'), ('Others', 'Others')]
    physical_dis_sel = (
        ('No disability', 'No disability'),
        ('Can walk with difficulty', 'Can walk with difficulty'),
        ('Walk with support', 'Walk with support'),
        ('Wheelchair bound', 'Wheelchair bound')
        )
    surgery_sel = [('Surgery 1', 'Surgery 1'), ('Surgery 2', 'Surgery 2'), ('Surgery 3', 'Surgery 3')]
    transfusion_mul_sel = [
        ('Whole Blood', 'Whole Blood'),
        ('Cryoprecipitate', 'Cryoprecipitate'),
        ('FFP', 'FFP'), ('Plasma derived Factor', 'Plasma derived Factor'),
        ('Recombinant factor', 'Recombinant factor'),
        ('Anti-inhibitor coagulant complex', 'Anti-inhibitor coagulant complex'),
        ('Activated recombinant coagulation factor VII', 'Activated recombinant coagulation factor VII'),
        ('Others', 'Others')
        ]
    # Pregnancy Details
    bd_bleed_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_bleed_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_spontaneous_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_spontaneous_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_traumatic_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_traumatic_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_haemorrhages_past_12 =models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_haemorrhages_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_cns_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_cns_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_muscle_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_muscle_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_mucosal_past_12 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_mucosal_life_time = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_chronic_def = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_bleeds_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_first_fact_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_birth_exposure_days = models.CharField(max_length=30, blank=True, null=True, choices=exposure_days_sel)
    bd_transfusion_product = MultiSelectField(null=True, blank=True, max_length=500, choices=transfusion_mul_sel)
    bd_transfusion_product_others = models.CharField(max_length=200, blank=True, null=True, validators=[MaxLengthValidator(200)])
    bd_curr_mode_treatment = models.CharField(max_length=30, blank=True, null=True, choices=ondemand_sel)
    bd_demand_bd_episodes = models.IntegerField(blank=True, null=True)
    bd_demand_bd_duration = models.IntegerField(blank=True, null=True)
    bd_funding_source = models.CharField(max_length=50, blank=True, null=True, choices=source_funding_sel)
    bd_funding_source_other = models.CharField(max_length=50, blank=True, null=True, validators=[MaxLengthValidator(50)])
    bd_dose = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_frequency = models.IntegerField(blank=True, null=True)
    bd_start_date = models.DateField(blank=True, null=True)
    bd_end_date = models.DateField(blank=True, null=True)
    bd_ongoing_status = models.CharField(max_length=10, blank=True, null=True, choices=status_sel)
    bd_duration = models.IntegerField(blank=True, null=True)
    bd_infusion_skill = models.CharField(max_length=10, blank=True, null=True, choices=status_sel)
    bd_inhibitor_status = models.CharField(max_length=10, blank=True, null=True, choices=inhibitor_sel)
    bd_any_other_info = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_num = models.CharField(max_length=10, blank=True, null=True, choices=surgery_sel)
    bd_surgery_date1 = models.DateField(blank=True, null=True)
    bd_surgery_1 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_1_transfusin = models.CharField(max_length=50, blank=True, null=True, choices=transfusion_sel)
    bd_surgery_1_transfusin_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_date2 = models.DateField(blank=True, null=True)
    bd_surgery_2 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_2_transfusin = models.CharField(max_length=50, blank=True, null=True, choices=transfusion_sel)
    bd_surgery_2_transfusin_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_date3 = models.DateField(blank=True, null=True)
    bd_surgery_3 = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_surgery_3_transfusin = models.CharField(max_length=50, blank=True, null=True, choices=transfusion_sel)
    bd_surgery_3_transfusin_others = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_physical_dis_status = models.CharField(max_length=50, blank=True, null=True, choices=physical_dis_sel)
    bd_cronic_anthr = models.CharField(max_length=10, blank=True, null=True, choices=status_sel)
    bd_joint = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_target_joint = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_other_info = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    bd_doctor_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    bd_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)
