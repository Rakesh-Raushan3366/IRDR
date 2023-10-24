# Create your models here.

from account.models import *
from django.core.validators import FileExtensionValidator

# Create your models here.


class profile_mucopolysaccharidosis(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    qa_user = models.ForeignKey(User, null=True, blank=True,related_name='qa_user_muco', on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    qa_register = models.ForeignKey(Register, null=True, blank=True,related_name='qa_register_muco', on_delete=models.CASCADE)
    fb_religion_sel = [('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh'),
                       ('Others', 'Others')]
    fb_caste_sel = [('Scheduled caste', 'Scheduled caste'), ('Scheduled tribe', 'Scheduled tribe'),
                    ('Others', 'Others')]
    fb_gender_sel = [('Male', 'Male'), ('Female', ' Female'), ('Transgender', 'Transgender')]
    fb_referred_by = [('General practitioner', 'General practitioner'), ('Physician', 'Physician'),
                      ('Neurologist', 'Neurologist'), ('Any others', 'Any others')]
    fb_status_sel = [('Yes', 'Yes'), ('No', 'No')]
    quality_score = [('Pass', 'Pass'), ('Fail', 'Fail')]
    quality_status_sel = [('Pending', 'Pending'), ('Resubmitted', 'Resubmitted'), ('Completed', 'Completed')]
    quality_status = models.CharField(max_length=20, blank=True, null=True, choices=quality_status_sel)
    muco_final_diagnosis = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_date_of_records = models.DateField(blank=True, null=True)
    muco_date_of_clinical_exam = models.DateField(blank=True, null=True)
    muco_date_of_birth = models.DateField( null=True)
    muco_patient_name = models.CharField(max_length=100,  null=True, validators=[MaxLengthValidator(100)])
    muco_father_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_mother_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    id_sel = [('Aadhar card', 'Aadhar card'), ('Driving license', 'Driving license'), ('Voter id', 'Voter id'),
              ('Rations card', 'Rations card'), ('PAN card', 'PAN card'), ('BPL card', 'BPL card'),('SECC card', 'SECC card'),('Aabha Id', 'Aabha Id') ]
    muco_paitent_id_yes_no = models.CharField(max_length=100,  null=True, choices=fb_status_sel)
    muco_paitent_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    muco_patient_id_no = models.CharField(max_length=100,unique=True,blank=True,  null=True, validators=[MaxLengthValidator(100)])
    muco_patient_age = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_father_mother_id = models.CharField(max_length=100, blank=True, null=True, choices=id_sel)
    muco_mother_father_id_no = models.PositiveBigIntegerField(blank=True, null=True, unique=True)
    muco_permanent_addr = models.CharField(max_length=500, blank=True, null=True, validators=[MaxLengthValidator(500)])
    muco_state = models.ForeignKey(State, null=True,  on_delete=models.CASCADE, verbose_name=' state')
    muco_district = models.ForeignKey(District, null=True, on_delete=models.CASCADE,
                                     verbose_name=' district')
    muco_city_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_country_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_mother_mobile_no = models.PositiveBigIntegerField( null=True, unique=True)
    muco_father_mobile_no = models.PositiveBigIntegerField(blank=True, null=True)
    muco_land_line_no = models.PositiveBigIntegerField(blank=True, null=True)
    muco_email = models.EmailField(max_length=300, blank=True, null=True)

    muco_religion = models.CharField(max_length=100, blank=True, null=True, choices=fb_religion_sel)
    muco_caste = models.CharField(max_length=100, blank=True, null=True, choices=fb_caste_sel)
    muco_referred_status = models.CharField(max_length=10, blank=True, null=True, choices=fb_status_sel)
    muco_referred_by = models.CharField(max_length=100, blank=True, null=True, choices=fb_referred_by)
    muco_referred_by_desc = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_gender = models.CharField(max_length=100, blank=True, null=True, choices=fb_gender_sel)
    muco_consent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    muco_consent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',  null=True, validators=[FileExtensionValidator(['pdf'])])
    muco_assent_given = models.CharField(max_length=10,  null=True, choices=fb_status_sel)
    muco_assent_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])])
    muco_hospital_name = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_hospital_reg_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_icmr_unique_no = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    muco_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
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
            super(profile_mucopolysaccharidosis, self).save(*args, **kwargs)
            self.muco_icmr_unique_no = str('Mucopolysaccharidosis/') + str(self.register.institute_code) + str('/') + str(self.pk)
            # self.slug = slugify(self.occupation)

        super(profile_mucopolysaccharidosis, self).save(*args, **kwargs)


class demographic_mucopolysaccharidosis(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    register = models.ForeignKey(Register, null=True, blank=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(profile_mucopolysaccharidosis, null=True, related_name='patient_mucopoly', blank=True,
                                on_delete=models.CASCADE)

    education_status = [('Illiterate', 'Illiterate'), ('Primary', 'Primary'), ('High School', 'High School')
        , ('Secondary Level', 'Secondary Level'), ('College and above', 'College and above')]

    occupation_status = [('Employed (organised sector)', 'Employed (organised sector)'),
                         ('Employed (Unorganised sector) ', 'Employed (Unorganised sector)'),
                         ('Home maker', 'Home maker'),
                          ('Others', 'Others')]

    yes_no_sel = [('Yes', 'Yes'), ('No', 'No')]
    yes_no_sel123 = [('1', 'Yes'), ('0', 'No')]

    current_status = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    education_status_of_patient = models.CharField(max_length=50, blank=True, null=True, choices=education_status)

    occupation_of_patient = models.CharField(max_length=50, blank=True, null=True, choices=occupation_status)

    education_status_of_father = models.CharField(max_length=50, blank=True, null=True, choices=education_status)

    occupation_of_father = models.CharField(max_length=50, blank=True, null=True, choices=occupation_status)

    education_status_of_mother = models.CharField(max_length=50, blank=True, null=True, choices=education_status)

    occupation_of_mother = models.CharField(max_length=50, blank=True, null=True, choices=occupation_status)
    family_income_list = [('> 126,360', '> 126,360')
        , ('63,182 – 126,356', '63,182 – 126,356')
        , ('47,266 – 63,178', '47,266 – 63,178')
        , ('31,591 - 47,262', '31,591 - 47,262')
        , ('18,953 - 31,589', '18,953 - 31,589')
        , ('6,327 - 18,949', '6,327 - 18,949')
        , ('< 6,323', '< 6,323')]
    Age_at_Onset_of_symptoms_list = [('< 1year', '< 1year'), ('1 - 2year', '1 - 2year'), ('2 - 5year', '2 - 5year'), ('5 - 12year', '5 - 12year'), ('> 12year', '> 12year')]

    family_income = models.CharField(max_length=50, blank=True, null=True,default='No', choices=family_income_list)
    # anthropometry


    gl_anth_wght_pat = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_wght_exp = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_wght_per = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_wght_sd = models.CharField(max_length=50,blank=True, null=True)

    gl_anth_height_pat = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_height_exp = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_height_per = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_height_sd = models.CharField(max_length=50,blank=True, null=True)

    gl_anth_seg_pat = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_seg_exp = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_seg_per = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_seg_sd = models.CharField(max_length=50,blank=True, null=True)

    gl_anth_ratio_pat = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_ratio_exp = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_ratio_per = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_ratio_sd = models.CharField(max_length=50,blank=True, null=True)

    gl_anth_head_cir_pat = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_head_cir_exp = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_head_cir_per = models.CharField(max_length=50,blank=True, null=True)
    gl_anth_head_cir_sd = models.CharField(max_length=50,blank=True, null=True)

    # head_circumference = models.CharField(max_length=50, blank=True, null=True)
    Age_at_Onset_of_symptoms_years = models.IntegerField(blank=True, null=True)
    Age_at_Onset_of_symptoms_months = models.IntegerField(blank=True, null=True)
    Age_at_Onset_of_symptoms_day = models.IntegerField(blank=True, null=True)
    Age_at_Onset_of_symptoms_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel123)

    Age_at_Presentation_years = models.IntegerField(blank=True, null=True)
    Age_at_Presentation_months = models.IntegerField(blank=True, null=True)
    Age_at_Presentation_day = models.IntegerField(blank=True, null=True)
    Age_at_Presentation_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel123)

    Age_at_diagnosis_years = models.IntegerField(blank=True, null=True)
    Age_at_diagnosis_months = models.IntegerField(blank=True, null=True)
    Age_at_diagnosis_day = models.IntegerField(blank=True, null=True)
    Age_at_diagnosis_intrauterine = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel123)

    # Presenting_Complaints = models.CharField(max_length=50, blank=True, null=True)
    # Age_at_Onset_of_symptoms = models.CharField(max_length=50, blank=True, null=True, choices=Age_at_Onset_of_symptoms_list)
    # Age_at_Presentation = models.CharField(max_length=50, blank=True, null=True)
    # Age_at_diagnosis = models.CharField(max_length=50, blank=True, null=True)
    Pedigree_generation_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)

    # Educational Information
    positive_family_history = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    family_history_specify = models.CharField(max_length=50, blank=True, null=True)
    consanguinity = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    consanguinity_mention_degree = models.CharField(max_length=50, blank=True, null=True)

    # Cardiomegaly / Cardiomyopathy / Normal/abnormal /Not done
    cardiography_sel = [('Cardiomegaly', 'Cardiomegaly'), ('Cardiomyopathy', 'Cardiomyopathy')
        , ('Normal', 'Normal'), ('abnormal', 'abnormal')
        , ('Not done', 'Not done')]
    functional_sel = [('Ambulatory', 'Ambulatory'), ('Wheel chair', 'Wheel chair'), ('bed ridden', 'bed ridden')]
    antenatal_findings_sel = [('normal', 'normal'), ('abnormal', 'abnormal')]
    abnormal_specify_sel = [('polyhydramnios', 'polyhydramnios'), ('hydrops', 'hydrops'), ('other specify', 'other specify')]
    present_absent_sel = [('present', 'present'), ('absent', 'absent')]

    # Antenatal Investigation:
    antenatal_findings = models.CharField(max_length=50, blank=True, null=True, choices=antenatal_findings_sel)
    if_abnormal_specify = models.CharField(max_length=200, null=True, blank=True, choices=abnormal_specify_sel)
    antenatal_present_absent = models.CharField(max_length=200, null=True, blank=True, choices=present_absent_sel)
    # polyhydramnios = models.CharField(max_length=5, blank=True, null=True, choices=antenatal_findings_sel)
    # hydrops = models.CharField(max_length=5, blank=True, null=True, choices=antenatal_findings_sel)
    antenatal_other_specify = models.CharField(max_length=50, blank=True, null=True)

    # Natal History::
    type_of_delivery_seL = [('Caesarean', 'Caesarean'), ('Vaginal', 'Vaginal')]
    resuscitation_sel = [('ventilation', 'ventilation'), ('NICU stay days', 'NICU stay days')]
    type_of_delivery = models.CharField(max_length=50, blank=True, null=True, choices=type_of_delivery_seL)
    baby_cried_immediately_after_delivery = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    resuscitation_required = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    # ventilation = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    # NICU_stay_days = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    yes_specify = models.CharField(max_length=200, null=True, blank=True )
    specify = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    birth_weight = models.CharField(max_length=50, blank=True, null=True)

    developmental_milestones_sel = [('Delayed', 'Delayed'), ('Normal', 'Normal')]
    developmental_milestones = models.CharField(max_length=50, blank=True, null=True,
                                                choices=developmental_milestones_sel)
    # milestone_delayed_sel = [('motor','motor'),('globl','globl'),('cognitive','cognitive')]
    # developmental = models.CharField(max_length=20, blank=True, null=True, choices=milestone_delayed_sel)
    motor = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    cognitive = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    globall = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    # History of
    mental_retardation_Delay = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Neuroregression = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    behavioural_problems = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Hyperactivity = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    On_some_drugs = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Seizures = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    On_some_antiepileptics_drugs = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Symptoms = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Recurrent_diarrheoa = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Recurrent_pneumonia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    persistent_upper_respiratory_symptoms = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Sleep_disturbance = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Snoring = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Visual_problem = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Deafness = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Chronic_otitis_media = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Use_of_hearing_aid = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    PE_ear_tube_placement = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Any_surgery_for_hernia_or_others = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Functional_status = models.CharField(max_length=50, blank=True, null=True, choices=functional_sel)

    # Clinical Examination findings
    face_coarse = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    enlarged_tongue = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    head_shape_sel = [('normal', 'normal'), ('Dolichocephaly', 'Dolichocephaly'),
                      ('Craniosynostosis', 'Craniosynostosis'), ('trigonocephaly', 'trigonocephaly')]
    head_shape = models.CharField(max_length=50, blank=True, null=True, choices=head_shape_sel)

    # Skin
    skin = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    pebbly_MPSII = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    mongolian_spots_at_back = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    ichthyosis = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    stiff_thick_skin = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    telangiectasia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    edema = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    hydrops = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    # Neurological
    tone_sel = [('normal', 'normal'), ('increased', 'increased'), ('decreased', 'decreased')]
    Tone = models.CharField(max_length=50, blank=True, null=True, choices=tone_sel)
    power_sel = [('normal', 'normal'), ('decreased', 'decreased')]
    Power = models.CharField(max_length=50, blank=True, null=True, choices=power_sel)

    upper_list = [('0', '0')
        , ('1', '1')
        , ('2', '2')
        , ('3', '3')
        , ('4', '4')
        , ('5', '5')]

    upper_l = models.CharField(max_length=50, blank=True, null=True, choices=upper_list)
    upper_r = models.CharField(max_length=50, blank=True, null=True, choices=upper_list)
    # upper_1l = models.CharField(max_length=50, blank=True, null=True)
    # upper_1r = models.CharField(max_length=50, blank=True, null=True)
    # upper_2r = models.CharField(max_length=50, blank=True, null=True)
    # upper_2l = models.CharField(max_length=50, blank=True, null=True)
    # upper_3l = models.CharField(max_length=10, blank=True, null=True)
    # upper_3r = models.CharField(max_length=50, blank=True, null=True)
    # upper_4l = models.CharField(max_length=50, blank=True, null=True)
    # upper_4r = models.CharField(max_length=50, blank=True, null=True)
    # upper_5r = models.CharField(max_length=50, blank=True, null=True)
    # upper_5l = models.CharField(max_length=50, blank=True, null=True)

    lower_0r = models.CharField(max_length=50, blank=True, null=True, choices=upper_list)
    lower_0l = models.CharField(max_length=50, blank=True, null=True, choices=upper_list)
    # lower_1r = models.CharField(max_length=50, blank=True, null=True)
    # lower_1l = models.CharField(max_length=50, blank=True, null=True)
    # lower_2r = models.CharField(max_length=50, blank=True, null=True)
    # lower_2l = models.CharField(max_length=50, blank=True, null=True)
    # lower_3r = models.CharField(max_length=10, blank=True, null=True)
    # lower_3l = models.CharField(max_length=50, blank=True, null=True)
    # lower_4r = models.CharField(max_length=50, blank=True, null=True)
    # lower_4l = models.CharField(max_length=50, blank=True, null=True)
    # lower_5r = models.CharField(max_length=50, blank=True, null=True)
    # lower_5l = models.CharField(max_length=50, blank=True, null=True)

    reflexes_sel = [('brisk', 'brisk'), ('normal', 'normal')]
    Reflexes = models.CharField(max_length=50, blank=True, null=True, choices=reflexes_sel)
    ataxia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Signs_of_raised_ICT = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Symptoms_of_CTS = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    iq_sel = [('done', 'done'), ('not done', 'not done')]
    IQ = models.CharField(max_length=50, blank=True, null=True, choices=iq_sel)
    iq_value = models.CharField(max_length=50, blank=True, null=True)
    DQ = models.CharField(max_length=50, blank=True, null=True, choices=iq_sel)
    dq_value = models.CharField(max_length=50, blank=True, null=True)

    # Ophthalmologic
    corneal_clouding = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    papilledema = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    glaucoma = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    optic_nerve_atrophy = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    retinal_degeneration_pigmentation = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    corneal_opacity = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    cataract = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    squint = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    nystagmus = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    any_other_specify = models.CharField(max_length=200, null=True, blank=True)

    # Cardiovascular
    Cardiomyopathy = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Congestive_Heart_failure = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Cor_pulomonale = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Valvular_involvement = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Stenosis_Regurgitation_which_valve_sel = [('mitral', 'mitral'), ('tricuspid', 'tricuspid'), ('aortic', 'aortic'),
                                              ('pulmonary', 'pulmonary')]
    Stenosis_which_valve_mitral = models.BooleanField(default=False)
    Stenosis_which_valv_tricuspid = models.BooleanField(default=False)
    Stenosis_which_val_aortic = models.BooleanField(default=False)
    Stenosis_which_va_pulmonary = models.BooleanField(default=False)                                          
    # Stenosis_which_valve = models.CharField(max_length=10, blank=True, null=True,1
    #                                         choices=Stenosis_Regurgitation_which_valve_sel)
    Regurgitation_which_valve_mitral = models.BooleanField(default=False)
    Regurgitation_which_valv_tricuspid = models.BooleanField(default=False)
    Regurgitation_which_val_aortic = models.BooleanField(default=False)
    Regurgitation_which_va_pulmonary = models.BooleanField(default=False)
    # Regurgitation_which_valve = models.CharField(max_length=10, blank=True, null=True,
    #                                              choices=Stenosis_Regurgitation_which_valve_sel)

    # Respiratory
    Enlarged_tonsils = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Sleep_apnea = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Reactive_Airway_Disease = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Dyspnea = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    # Gastrointestinal

    Gum_hyperplasia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    hepatomegaly = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    size_hepatomegaly = models.CharField(max_length=5, blank=True, null=True)
    span_hepatomegaly = models.CharField(max_length=5, blank=True, null=True)
    Splenomegaly = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    size_splenomegaly = models.CharField(max_length=5, blank=True, null=True)
    span_splenomegaly = models.CharField(max_length=5, blank=True, null=True)
    hernia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    specify_if = models.CharField(max_length=100, blank=True, null=True)
    Umbilical_hernia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Inguinal_hernia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    # Skeletal
    Joint_Contractures = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Joint_arthritis = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Joint_laxity = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Scoliosis = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Kyphosis_Gibbus = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Genu_valgum = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Pes_Cavus = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Toe_Walking = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    Ultrasonography_sel = [('normal', 'normal'), ('abnormal', 'abnormal'), ('not done', 'not done')]

    # Echocardiography
    Echocardiography = models.CharField(max_length=20, blank=True, null=True, choices=Ultrasonography_sel)
    abnormal_finding = models.CharField(max_length=50, blank=True, null=True)
    Ultrasonography = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Liver_Size_volume = models.CharField(max_length=5, blank=True, null=True)
    Spleen_Size_Volume = models.CharField(max_length=5, blank=True, null=True)

    # Skeletal survey
    Skull_J_shaped_sella = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Spine_Beaked_vertebra = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Central_lower_tick = models.CharField(max_length=5, blank=True, null=True)
    Metacarpals_Bullet_shaped = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Ribs_oar_shaped = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Pelvis_Hip_dysplasia = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Dislocation_of_hip = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Flared_iliac_wings = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Long_bones_sel = [('Stippled epiphyses ', 'Stippled epiphyses '),
                      ('metaphyseal dysplasia', 'metaphyseal dysplasia')]
    Long_bones = models.CharField(max_length=32, blank=True, null=True, choices=Long_bones_sel)
    Dexa_Z_score_sel = [('done', 'done'), ('not done', 'not done')]
    Dexa_Z_score = models.CharField(max_length=32, blank=True, null=True, choices=Dexa_Z_score_sel)
    if_done_specify = models.CharField(max_length=100, blank=True, null=True)
    EPS_for_CTS = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    If_abnormal_specify_findings = models.CharField(max_length=100, blank=True, null=True)

    # Pulmonary function test
    Pulmonary_function_test = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    if_yes_sel = [('normal', 'normal'), ('abnormal', 'abnormal')]
    if_yes = models.CharField(max_length=20, blank=True, null=True, choices=if_yes_sel)
    if_abnormal_finding_specify = models.CharField(max_length=200, blank=True, null=True)

    # Neuroimaging
    ct_scan_sel = [('Hydrocephalus', 'Hydrocephalus'), ('Craniosynostosis', 'Craniosynostosis')]
    CT_Scan = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Specify_findings_if_abnormall = models.CharField(max_length=100, blank=True, null=True, choices=ct_scan_sel)

    # MRI Brain
    MRI_Brain = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Specify_findings_if_abnormal_mri = models.CharField(max_length=100, blank=True, null=True)

    # EEG
    EEG = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Specify_findings_if_abnormal_eeg = models.CharField(max_length=100, blank=True, null=True)

    # Ocular Examination
    Corneal_clouding_sel = [('present', 'present'), ('absent', 'absent')]
    Corneal_clouding1 = models.CharField(max_length=10, blank=True, null=True, choices=Corneal_clouding_sel)
    Fundus = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Specify_if_abnormal = models.CharField(max_length=100, blank=True, null=True)
    Glaucoma1 = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)

    # Hearing Assessment
    Hearing_Assessment = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    If_abnormal_sel = [('Unilateral', 'Unilatera'), ('Bilateral', 'Bilateral'), ('Mild', 'Mild'),
                       ('Moderate', 'Moderate'), ('Severe', 'Severe'), ('Profound', 'Profound')]
    If_abnormal_sel_Unilateral = models.BooleanField(default=False)
    If_abnorma_sel_Bilateral = models.BooleanField(default=False)
    If_abnorm_sel_Mild = models.BooleanField(default=False)
    If_abnor_sel_Moderate = models.BooleanField(default=False)
    If_abno_sel_Severe = models.BooleanField(default=False)
    If_abn_sel_Profound = models.BooleanField(default=False)
    if_abnormal = models.CharField(max_length=18, blank=True, null=True, choices=If_abnormal_sel)
    Sleep_Studies = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Specify_findings_if_abnormal = models.CharField(max_length=100, blank=True, null=True)

    #
    # ochemical estimations
    Urine_spot_test = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Urinary_GAGs_analysis = models.CharField(max_length=10, blank=True, null=True, choices=Ultrasonography_sel)
    Patient_urine = models.CharField(max_length=100, blank=True, null=True)
    Normal_Control_urine = models.CharField(max_length=100, blank=True, null=True)
    Normal_range_urine = models.CharField(max_length=100, blank=True, null=True)

    # Enzyme assay: (Upload Report) (drop down)
    enzyme_var_sel=[('Alpha_L_iduronidase','Alpha_L_iduronidase'),('Iduronate_sulfatase','Iduronate_sulfatase'),
                    ('GALNS','GALNS'),('b_galactosidase','b_galactosidase'),
                    ('arylsulfatase_B','arylsulfatase_B'),
                    ('other', 'other')]
    enzyme_var=models.CharField(max_length=100, blank=True, null=True,choices=enzyme_var_sel)

    enzyme_sam_sel = [('DBS', 'DBS'), ('Plasma', 'Plasma'),
                      ('Whole blood', 'Whole blood'), ('Skin Fibroblast', 'Skin Fibroblast'),
                      ('Serum', 'Serum')
                      ]
    enzyme_sam = models.CharField(max_length=100, blank=True, null=True, choices=enzyme_sam_sel)
    # Alpha_L_iduronidase = models.CharField(max_length=100, blank=True, null=True)
    # Iduronate_sulfatase = models.CharField(max_length=100, blank=True, null=True)
    # gALNS = models.CharField(max_length=100, blank=True, null=True)
    # b_galactosidase = models.CharField(max_length=100, blank=True, null=True)
    Other_specify = models.CharField(max_length=100, blank=True, null=True)
    Patient_enzyme = models.CharField(max_length=100, blank=True, null=True)
    Normal_Control = models.CharField(max_length=100, blank=True, null=True)
    Normal_range = models.CharField(max_length=100, blank=True, null=True)
    Enzyme_upload = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

    #	Molecular Diagnostics
    Causative_DNA_sequence_variation_sel = [('done', 'done'), ('not done', 'not done')]
    Causative_DNA_sequence_variation = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    # If_done =
    molecular_upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)
    Patient_molecular = models.CharField(max_length=100, blank=True, null=True)
    Gene_molecula = models.CharField(max_length=100, blank=True, null=True)
    trans_molecul = models.CharField(max_length=100, blank=True, null=True)
    mul_dna1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mul_pro1 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mul_var_sel = [('Novel', 'Novel '),
                  ('Reported', 'Reported')]
    mul_var1 = models.CharField(max_length=100, null=True, blank=True, choices=mul_var_sel)
    mul_zyg_sel = [('Homozygous', 'Homozygous '),
                   ('Heterozygous', 'Heterozygous'),
                    ('Hemizygous', 'Hemizygous')]
    mul_zygo1 = models.CharField(max_length=100, null=True, blank=True, choices=mul_zyg_sel)
    mul_vari_sel = [('Pathogenic ', 'Pathogenic '),
                   ('Likely Pathogenic', 'Likely Pathogenic'),
                   ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    mul_var_cla1 = models.CharField(max_length=100, null=True, blank=True, choices=mul_vari_sel)

    mul_dna2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mul_pro2 = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mul_var_sel = [('Novel', 'Novel '),
                   ('Reported', 'Reported')]
    mul_var2 = models.CharField(max_length=100, null=True, blank=True, choices=mul_var_sel)
    mul_zygo_sel = [('Homozygous', 'Homozygous '),
                    ('Heterozygous', 'Heterozygous'),
                    ('Hemizygous', 'Hemizygous')]
    mul_zygo2 = models.CharField(max_length=100, null=True, blank=True, choices=mul_zygo_sel)
    mul_varin_sel = [('Pathogenic ', 'Pathogenic '),
                    ('Likely Pathogenic', 'Likely Pathogenic'),
                    ('Variant of uncertain significance ', 'Variant of uncertain significance')]
    mul_var_cla2 = models.CharField(max_length=100, null=True, blank=True, choices=mul_varin_sel)
    mul_seg = models.CharField(max_length=100, null=True, blank=True, choices=yes_no_sel)
    father = models.CharField(max_length=100, blank=True, null=True)
    mother = models.CharField(max_length=100, blank=True, null=True)

    # Treatment
    Enzyme_Replacement_Therapy = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Date_of_initiation = models.DateField(blank=True, null=True)
    Age_of_Start = models.IntegerField(blank=True, null=True)
    Dosage = models.CharField(max_length=100, blank=True, null=True)
    Duration = models.IntegerField(blank=True, null=True)
    Adverse_events = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    if_yes_specify = models.CharField(max_length=100, blank=True, null=True)
    # Current_ERT_Status_Ongoing
    Any_interruption = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Reason_for_interruption = models.CharField(max_length=100, blank=True, null=True)
    Duration_of_interruption = models.CharField(max_length=100, blank=True, null=True)
    Response = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    # Bone Marrow Transplantation
    Bone_Marrow_Transplantation = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    # If yes
    date = models.DateField(blank=True, null=True)
    Donor = models.CharField(max_length=100, blank=True, null=True)
    Hospital = models.CharField(max_length=100, blank=True, null=True)

    # Surgery
    Surgery = models.CharField(max_length=20, blank=True, null=True, choices=yes_no_sel)
    # if_yes
    Hernia_sel = [('Inguinal', 'Inguinal'), ('umbilical', 'umbilical')]
    Hernia_surgery = models.CharField(max_length=100, blank=True, null=True, choices=Hernia_sel)
    # CTS =
    Age_at_surgery = models.CharField(max_length=100, blank=True, null=True)

    # Supportive
    Calcium_and_multivitamin_supplements = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Regular_Physiotherapy = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    Any_ocular_medication = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)
    CPAP_BiPAP_for_sleep_apnea = models.CharField(max_length=5, blank=True, null=True, choices=yes_no_sel)


    mg_Finaldiagnosis_sel = [('MPS-I', 'MPS-I'),
                            ('MPS-II', 'MPS-II'),
                             ('MPS-III (a/b/c/d)', 'MPS-III (a/b/c/d)'),
                             ('MPS-IV(a/b)', 'MPS-IV(a/b)'),
                             ('MPS-VI', 'MPS-VI'),
                             ('MPS-VII', 'MPS-VII'),
                             ('Mucolipidosis', 'Mucolipidosis')]
    Finaldiagnosis = models.CharField(max_length=100, null=True, blank=True, choices=mg_Finaldiagnosis_sel)
    mg_Finaloutcomes_sel = [('Death', 'Death'),
                              ('Alive', 'Alive'),
                            ('Followup required', 'Followup required'),
                            ('Unknown', 'Unknown'),]
    Finaloutcomes = models.CharField(max_length=100, null=True, blank=True, choices=mg_Finaloutcomes_sel)

    mg_filed_by_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mg_clinician_name = models.CharField(max_length=100, null=True, blank=True, validators=[MaxLengthValidator(100)])
    mg_filled_date = models.DateTimeField(null=True, blank=True)
    mg_date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

