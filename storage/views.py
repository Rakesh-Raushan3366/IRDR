import csv

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


@login_required(login_url='login')
def add_record_storage(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = StorageRegistrationForm()
    if request.method == 'POST':
        form1 = StorageRegistrationForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(storage_demographic, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_storage.html', context)
    context = {'form1': form1, }
    return render(request, 'add_record_storage.html', context)


@login_required(login_url='login')
def update_patient_record_storage(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_storage.objects.get(id=pk)
    form1 = StorageRegistrationForm(instance=patient)
    if request.method == 'POST':
        form1 = StorageRegistrationForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_sd')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_storage.html', context)
    context = {'form1': form1, }
    return render(request, 'update_patient_record_storage.html', context)


@login_required(login_url='login')
def storage_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_storage.objects.get(id=pk)
    form1 = StorageSocioDemographicDetailsForm()
    if request.method == 'POST':
        form1 = StorageSocioDemographicDetailsForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()
            return HttpResponseRedirect(reverse(update_storage_demographic, args=(pk,)))
    else:
        context = {'form1': form1, }
        return render(request, 'storage_demographic.html', context)

    context = {'form1': form1, }
    return render(request, 'storage_demographic.html', context)


@login_required(login_url='login')
def delete_record_sd(request, pk):
    order = profile_storage.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_sd')

    context = {'order': order}
    return render(request, 'delete_record_sd.html', context)


@login_required(login_url='login')
def total_record_sd(request):
    pat = profile_storage.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_sd.html', context)


@login_required(login_url='login')
def total_record_sd_admin(request):
    pat = profile_storage.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_sd_admin.html', context)


@login_required(login_url='login')
def view_profile_record_storage(request, pk):
    try:
        form1 = profile_storage.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_storage_profile_record.html', context)


@login_required(login_url='login')
def view_storage_record(request, pk):
    patient = profile_storage.objects.get(id=pk)
    try:
        form1 = demographic_storage.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_storage_record.html', context)


@login_required(login_url='login')
def update_storage_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_storage.objects.get(id=pk)
    try:
        form4 = demographic_storage.objects.get(patient=patient)
        form1 = StorageSocioDemographicDetailsForm(instance=form4)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = StorageSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect('total_record_sd')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_storage_demographic.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = StorageSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_sd")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_storage_demographic.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = StorageSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
                if form1.is_valid():
                    auth1 = form1.save(commit=False)
                    auth1.user = user
                    auth1.patient = patient
                    auth1.register = register
                    auth1.save()

                    # patient.complete = 'Yes'
                    # patient.save()
                else:
                    context = {'form1': form1, 'patient': patient, }
                    return render(request, 'update_storage_demographic.html', context)
    except:
        form1 = StorageSocioDemographicDetailsForm()
        if request.method == 'POST':
            form1 = StorageSocioDemographicDetailsForm(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                return redirect('total_record_sd')
        else:
            context = {'form1': form1,'patient': patient,  }
            return render(request, 'update_storage_demographic.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_storage_demographic.html', context)


@login_required(login_url='login')
def storage_total_record(request):
    register = profile_storage.objects.all()
    context = {'register': register, }
    return render(request, 'storage_total_record.html', context)


def export_storage_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="storage.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_records', 'date_of_clinical_exam', 'date_of_birth',
         'Patient_name', 'Father_name', 'Mother_name',
         'paitent_id_yes_no', 'paitent_id', 'patient_id_no', 'Father_mother_id', 'Father_mother_id_no',
         'permanent_addr', 'state', 'district', 'city_name', 'country_name',
         'land_line_number', 'Mother_mobile_no', 'Father_mobile_no', 'email', 'religion', 'cast',
         'gender', 'referred_status', 'referred_by', 'referred_by_desc', 'consent_given',
         'consent_upload', 'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no',
         'sd_Patient_education',
'sd_Patient_occupation',
'sd_Father_education',
'sd_Father_occupation',
'sd_Mother_education',
'sd_Mother_occupation',
'sd_Monthly_family_income',
'sd_weight_patient',
'sd_weight_percentile',
'sd_weight_SD',
'sd_height_patient',
'sd_height_percentile',
'sd_height_SD',
'sd_Head_circumference_patient',
'sd_Head_circumference_percentile',
'sd_Head_circumference_sd',
'sd_Age_at_onset_of_symptoms_year',
'sd_Age_at_onset_of_symptoms_month',
'sd_Age_at_onset_of_symptoms_day',
'sd_Age_at_onset_of_symptoms_Intrauterine',
'sd_Age_at_presentation_year',
'sd_Age_at_presentation_month',
'sd_Age_at_presentation_day',
'sd_Age_at_presentation_Intrauterine',
'sd_Age_at_diagnosis_year',
'sd_Age_at_diagnosis_month',
'sd_Age_at_diagnosis_day',
'sd_Age_at_diagnosis_Intrauterine',
'sd_Pedigree_to_be_uploaded',
'sd_positive_family_history',
'sd_family_history_specify',
'sd_Consanguinity',
'sd_Consanguinity_specify',
'sd_Antenatal_Ultrasound',
'sd_Polyhydramnios',
'sd_Hydrops',
'sd_Hydrops_specify',
'sd_Type_of_delivery',
'sd_Baby_cried_immediately_after_delivery',
'sd_Resuscitation_required',
'sk_Resuscitation_specify',
'sd_Resuscitation_ventilation',
'sd_NICU_stay',
'sd_NICU_specify',
'sd_NICU_stay_other',
'sd_Birth_weight',
'sd_Development_milestones',
'sd_delayed_Motor',
'sd_delayed_Global',
'sd_delayed_Cognitive',
'sd_Abdominal_distentesion',
'sd_Increasing_pallor',
'sd_Bleeding',
'sd_Developmental_Delay',
'sd_Neuroregression',
'sd_Behavioral_problems',
'sd_Hyperactivity',
'sd_Psychomotor_arrest',
'sd_Seizures',
'sd_Seizures_specify',
'sd_On_some_antiepileptics_drugs',
'sd_antiepileptics_specify',
'sd_Decreased_attention_span',
'sd_Stiffness',
'sd_Poor_feeding',
'sd_Choking',
'sd_Loss_of_Vision',
'sd_Hearing_loss',
'sd_Recurrent_persistent_upper_respiratory_symptoms',
'sd_Fractures',
'sd_Gait_disturbances',
'sd_Speech_disturbances',
'sd_Any_surgery',
'sd_Surgery',
'sd_Surgery_age_history',
'sd_Surgery_other_specify',
'sd_Functional_status',
'sd_Head_shape_Abnormal',
'sd_Mongolian_spots_at_back',
'sd_Ichthyosis',
'sd_Stiff_Thick_skin',
'sd_Telangiectasia',
'sd_Edema',
'sd_Hydrops1',
'sd_Angiokeratomas',
'sd_Exaggerated_startle_reflex',
'sd_Hypotonia',
'sd_Hypertonia',
'sd_Brisk_reflexes',
'sd_Hyporeflexia',
'sd_Gait_abnormalities',
'sd_Opisthotonus',
'sd_Dystonia',
'sd_IQ_done',
'sd_IQ_done_value',
'sd_DQ_done',
'sd_DQ_done_value',
'sd_gaze_palsy',
'sd_Ophthalmology',
'sd_Epilepsy',
'sd_Age_seizure',
'sd_Development_Cognitive_ability',
'sd_Ataxia_of_gait',
'sd_Cerebellar_tremor',
'sd_Pyramidal',
'sd_Extrapyramidal',
'sd_Swallowing_difficulties_Oral_bulbar_function',
'sd_Speech',
'sd_Spinal_alignement',
'sd_final_diagnosis_other',
'sd_Oculomotor_apraxia',
'sd_Saccades',
'sd_Corneal_clouding_opacity',
'sd_Glaucoma',
'sd_Optic_Nerve_atrophy',
'sd_Retinal_degeneration_pigmentation',
'sd_Cataract',
'sd_Squint',
'sd_Nystagmus',
'sd_Supranuclear_gaze_palsy',
'sd_Fundus_abnormal',
'sd_Cherry_Red_Spot',
'sd_Pigmentary_changes',
'sd_Cardiovascular_Congestive_Heart_Failure',
'sd_Cardiovascular_Cor_Pulomonale',
'sd_Respiratory_Enlarged_tonsils',
'sd_Respiratory_Sleep_apnea',
'sd_Respiratory_Reactive_Airway_Disease',
'sd_Respiratory_Dyspnea',
'sd_Hepatomegaly',
'sd_if_yes_size_bcm',
'sd_if_yes_span',
'sd_if_yes_Consistency',
'sd_if_yes_surface',
'sd_if_yes_margin',
'sd_Splenomegaly',
'sd_if_Splenomegaly',
'sd_Joint_stiffness',
'sd_Scoliosis',
'sd_Kyphosis_Gibbus',
'sd_Genu_valgum',
'sd_Pes_Cavus',
'sd_Toe_Walking',
'sd_Hb',
'sd_WBC_Total_Count',
'sd_Platelet_Count',
'sd_WBC_Differnetial',
'sd_Absolute_neutrophil_counts',
'sd_PT_sec',
'sd_APTT_sec',
'sd_S_calcium_mg_dl',
'sd_S_Phosphorus_mg_dl',
'sd_S_alkaline_phosphatise_IU',
'sd_S_Acid_phosphatise_IU',
'sd_S_Total_protein_g_dl',
'sd_S_Serum_albumin_g_dl',
'sd_SGPT_IU',
'sd_GGT',
'sd_GGT',
'sd_IRON_mg_dl',
'sd_TIBC_mg_dl',
'sd_Vit_B12_pg_ml',
'sd_Vit_D_ng_ml',
'sd_PTH_ng_ml',
'sd_Skeletal_survey',
'sd_Erlenmeyer_flask_deformity',
'sd_Osteopenia',
'sd_Skeletal_Scoliosis',
'sd_Dysostosis_multiplex',
'sd_Dexa_Z_Score',
'sd_xray_bone_age',
'sd_Pulmonary_function_test',
'sd_sitting_FEV1',
'sd_sittingFVC',
'sd_Supine_FEV1',
'sd_SupineFVC',
'sd_rad_ultrasono_type',
'sd_rad_liversize',
'sd_rad_liverEchotexture',
'sd_rad_hepatic',
'sd_rad_Kidney',
'sd_rad_kidney_size',
'sd_rad_kidney_size',
'sd_rad_lymphnodes_size',
'sd_rad_portal_vien_dia',
'sd_rad_adenoma',
'sd_renal_par_pathalogy',
'sd_renal_par_pathalogy_specify',
'sd_nephrocalcinosis',
'sd_pancreatitis',
'sd_cholethiasis',
'sd_CT_scan',
'sd_CT_scan_specify',
'sd_MRI_Brain',
'cerebral_atrophy',
'hydrocephalus',
'basal_ganglia_hypo',
'hyperintensity',
'thalamic',
'dysmyelination',
'Any_other_MRI',
'sd_MRI_Spine_limbs_pelvis',
'sd_Osteonecrosis',
'sd_Compression_spine_deformity_fractures',
'sd_Marrow_infiltration',
'sd_marrow_Any_other',
'sd_MRI_abdomen',
'sd_Liver_volume',
'sd_Spleen_volume',
'sd_Gaucher_related_nodules',
'sd_Echocardiography_test',
'sd_Specify_findings_Cardiomyopathy',
'Cardiomyopathy',
'sd_Cardiomyopathy',
'sd_Mention_LVMI',
'sd_Valvular_involvement',
'Valvular_Stenosis_mitral',
'Valvular_Stenosis_tricuspid',
'Valvular_Stenosis_aortic',
'Valvular_Stenosis_pulmonary',
'sd_Valvular_Regurgitation',
'Valvular_Regurgitation_mitral',
'Valvular_Regurgitation_tricuspid',
'Valvular_Regurgitation_aortic',
'Valvular_Regurgitation_pulmonary',
'sd_Ejection_fraction',
'sd_EEG',
'sd_EEG_specify_Findings',
'sd_Sleep_Studies',
'sd_Sleep_Studies_Findings',
'sd_SLIT_lamp_examination',
'sd_VEP',
'sd_ved_specify',
'sd_Opthalmological_Examination',
'sd_Describe_if_abnormal',
'sd_SLIT_Lamp',
'sd_BERA_Audiogram',
'sd_BERA_Describe_if_abnormal',
'sd_Servirity',
'sd_Unilat_bilat',
'sd_Nerve_Conduction_Study',
'sd_Nerve_Describe_if_abnormal',
'sd_Chitrotriosidase_Study',
'sd_Chitrotriosidase_if_abnormal',
'Any_Other_Biomarker2',
'sd_Biomarker_if_abnormal',
'sd_Enzyme_assay',
'sd_Sample_used',
'sd_Enzyme',
'sd_Enzyme_other',
'mt_enzyme_patient_control',
'mt_enzyme_control_range',
'mt_enzyme_normal_range',
'sd_Enzyme_upload',
'sd_Causative_DNA_sequence_variat',
'sd_molecular_upload',
'sd_Gene_molecula',
'sd_trans_molecul',
'sd_mul_dna1',
'sd_mul_pro1',
'sd_mul_var1',
'sd_mul_var_cla1',
'sd_mul_zygo1',
'sd_mul_dna2',
'sd_mul_pro2',
'sd_mul_var2',
'sd_mul_var_cla2',
'sd_mul_zygo2',
'sd_mul_seg',
'sd_father',
'sd_mother',
'sd_ERT',
'sd_Date_of_initiation',
'sd_age_of_start',
'sd_Dosage',
'sd_Duration',
'sd_Adverse_events',
'sd_Adverse_events_specify',
'sd_ERT_Status',
'sd_Response_to_therapy ',
'sd_Any_interruption',
'sd_Reason_interruption',
'sd_Duration_interruption',
'sd_Bone_Marrow_Transplantation',
'sd_Bone_Marrow_Date',
'sd_Donor',
'sd_Hospital',
'sd_Response',
'sd_Surgery1',
'Surgery_Splenectomy',
'Surgery_Hernia',
'Surgery_others',
'Surgery_others_text',
'sd_Surgery_age',
'sd_Calcium_and_multivitamin_supplements',
'sd_Regular_Physiotherapy',
'sd_Antiepileptics',
'sd_Blood_Transfusion',
'sd_BL_freq',
'sd_BL_Trans',
'sd_Platlet_Transfusion',
'sd_PL_freq',
'sd_PL_Trans',
'PL_Any_other',
'sd_final_diagnosis',
'sd_final_diagnosis_other',
'sd_Final_Outcome',
'sd_death_cause ',
'sd_age_timedeath ',
'sd_filed_by_DEO_name',
'sd_clinician_name',
'sd_filled_date',
])

    users = profile_storage.objects.filter(user=request.user).prefetch_related('patient_storage').values_list('register_id__institute_name', 'uniqueId', 'sd_icmr_unique_no', 'sd_final_diagnosis',
                                                                                                              'sd_date_of_records', 'sd_date_of_clinical_exam', 'sd_date_of_birth',
                                                                                                              'sd_Patient_name', 'sd_Father_name', 'sd_Mother_name', 'sd_paitent_id_yes_no',
                                                                                                              'sd_paitent_id', 'sd_patient_id_no', 'sd_Father_mother_id', 'sd_Father_mother_id_no',
                                                                                                              'sd_permanent_addr', 'sd_state', 'sd_district', 'sd_city_name', 'sd_country_name',
                                                                                                              'sd_land_line_number', 'sd_Mother_mobile_no', 'sd_Father_mobile_no', 'sd_email',
                                                                                                              'sd_religion', 'sd_cast', 'sd_gender', 'sd_referred_status', 'sd_referred_by',
                                                                                                              'sd_referred_by_desc', 'sd_consent_given', 'sd_consent_upload', 'sd_assent_given',
                                                                                                              'sd_assent_upload', 'sd_hospital_name', 'sd_hospital_reg_no', 'patient_storage__sd_Patient_education','patient_storage__sd_Patient_occupation','patient_storage__sd_Father_education','patient_storage__sd_Father_occupation','patient_storage__sd_Mother_education','patient_storage__sd_Mother_occupation',
         'patient_storage__sd_Monthly_family_income','patient_storage__sd_weight_patient','patient_storage__sd_weight_percentile','patient_storage__sd_weight_SD','patient_storage__sd_height_patient',
         'patient_storage__sd_height_percentile','patient_storage__sd_height_SD','patient_storage__sd_Head_circumference_patient','patient_storage__sd_Head_circumference_percentile',
'patient_storage__sd_Head_circumference_sd',
'patient_storage__sd_Age_at_onset_of_symptoms_year',
'patient_storage__sd_Age_at_onset_of_symptoms_month',
'patient_storage__sd_Age_at_onset_of_symptoms_day',
'patient_storage__sd_Age_at_onset_of_symptoms_Intrauterine',
'patient_storage__sd_Age_at_presentation_year',
'patient_storage__sd_Age_at_presentation_month',
'patient_storage__sd_Age_at_presentation_day',
'patient_storage__sd_Age_at_presentation_Intrauterine',
'patient_storage__sd_Age_at_diagnosis_year',
'patient_storage__sd_Age_at_diagnosis_month',
'patient_storage__sd_Age_at_diagnosis_day',
'patient_storage__sd_Age_at_diagnosis_Intrauterine',
'patient_storage__sd_Pedigree_to_be_uploaded',
'patient_storage__sd_positive_family_history',
'patient_storage__sd_family_history_specify',
'patient_storage__sd_Consanguinity',
'patient_storage__sd_Consanguinity_specify',
'patient_storage__sd_Antenatal_Ultrasound',
'patient_storage__sd_Polyhydramnios',
'patient_storage__sd_Hydrops',
'patient_storage__sd_Hydrops_specify',
'patient_storage__sd_Type_of_delivery',
'patient_storage__sd_Baby_cried_immediately_after_delivery',
'patient_storage__sd_Resuscitation_required',
'patient_storage__sk_Resuscitation_specify',
'patient_storage__sd_Resuscitation_ventilation',
'patient_storage__sd_NICU_stay',
'patient_storage__sd_NICU_specify',
'patient_storage__sd_NICU_stay_other',
'patient_storage__sd_Birth_weight',
'patient_storage__sd_Development_milestones',
'patient_storage__sd_delayed_Motor',
'patient_storage__sd_delayed_Global',
'patient_storage__sd_delayed_Cognitive',
'patient_storage__sd_Abdominal_distentesion',
'patient_storage__sd_Increasing_pallor',
'patient_storage__sd_Bleeding',
'patient_storage__sd_Developmental_Delay',
'patient_storage__sd_Neuroregression',
'patient_storage__sd_Behavioral_problems',
'patient_storage__sd_Hyperactivity',
'patient_storage__sd_Psychomotor_arrest',
'patient_storage__sd_Seizures',
'patient_storage__sd_Seizures_specify',
'patient_storage__sd_On_some_antiepileptics_drugs',
'patient_storage__sd_antiepileptics_specify',
'patient_storage__sd_Decreased_attention_span',
'patient_storage__sd_Stiffness',
'patient_storage__sd_Poor_feeding',
'patient_storage__sd_Choking',
'patient_storage__sd_Loss_of_Vision',
'patient_storage__sd_Hearing_loss',
'patient_storage__sd_Recurrent_persistent_upper_respiratory_symptoms',
'patient_storage__sd_Fractures',
'patient_storage__sd_Gait_disturbances',
'patient_storage__sd_Speech_disturbances',
'patient_storage__sd_Any_surgery',
'patient_storage__sd_Surgery',
'patient_storage__sd_Surgery_age_history',
'patient_storage__sd_Surgery_other_specify',
'patient_storage__sd_Functional_status',
'patient_storage__sd_Head_shape_Abnormal',
'patient_storage__sd_Mongolian_spots_at_back',
'patient_storage__sd_Ichthyosis',
'patient_storage__sd_Stiff_Thick_skin',
'patient_storage__sd_Telangiectasia',
'patient_storage__sd_Edema',
'patient_storage__sd_Hydrops1',
'patient_storage__sd_Angiokeratomas',
'patient_storage__sd_Exaggerated_startle_reflex',
'patient_storage__sd_Hypotonia',
'patient_storage__sd_Hypertonia',
'patient_storage__sd_Brisk_reflexes',
'patient_storage__sd_Hyporeflexia',
'patient_storage__sd_Gait_abnormalities',
'patient_storage__sd_Opisthotonus',
'patient_storage__sd_Dystonia',
'patient_storage__sd_IQ_done',
'patient_storage__sd_IQ_done_value',
'patient_storage__sd_DQ_done',
'patient_storage__sd_DQ_done_value',
'patient_storage__sd_gaze_palsy',
'patient_storage__sd_Ophthalmology',
'patient_storage__sd_Epilepsy',
'patient_storage__sd_Age_seizure',
'patient_storage__sd_Development_Cognitive_ability',
'patient_storage__sd_Ataxia_of_gait',
'patient_storage__sd_Cerebellar_tremor',
'patient_storage__sd_Pyramidal',
'patient_storage__sd_Extrapyramidal',
'patient_storage__sd_Swallowing_difficulties_Oral_bulbar_function',
'patient_storage__sd_Speech',
'patient_storage__sd_Spinal_alignement',
'patient_storage__sd_final_diagnosis_other',
'patient_storage__sd_Oculomotor_apraxia',
'patient_storage__sd_Saccades',
'patient_storage__sd_Corneal_clouding_opacity',
'patient_storage__sd_Glaucoma',
'patient_storage__sd_Optic_Nerve_atrophy',
'patient_storage__sd_Retinal_degeneration_pigmentation',
'patient_storage__sd_Cataract',
'patient_storage__sd_Squint',
'patient_storage__sd_Nystagmus',
'patient_storage__sd_Supranuclear_gaze_palsy',
'patient_storage__sd_Fundus_abnormal',
'patient_storage__sd_Cherry_Red_Spot',
'patient_storage__sd_Pigmentary_changes',
'patient_storage__sd_Cardiovascular_Congestive_Heart_Failure',
'patient_storage__sd_Cardiovascular_Cor_Pulomonale',
'patient_storage__sd_Respiratory_Enlarged_tonsils',
'patient_storage__sd_Respiratory_Sleep_apnea',
'patient_storage__sd_Respiratory_Reactive_Airway_Disease',
'patient_storage__sd_Respiratory_Dyspnea',
'patient_storage__sd_Hepatomegaly',
'patient_storage__sd_if_yes_size_bcm',
'patient_storage__sd_if_yes_span',
'patient_storage__sd_if_yes_Consistency',
'patient_storage__sd_if_yes_surface',
'patient_storage__sd_if_yes_margin',
'patient_storage__sd_Splenomegaly',
'patient_storage__sd_if_Splenomegaly',
'patient_storage__sd_Joint_stiffness',
'patient_storage__sd_Scoliosis',
'patient_storage__sd_Kyphosis_Gibbus',
'patient_storage__sd_Genu_valgum',
'patient_storage__sd_Pes_Cavus',
'patient_storage__sd_Toe_Walking',
'patient_storage__sd_Hb',
'patient_storage__sd_WBC_Total_Count',
'patient_storage__sd_Platelet_Count',
'patient_storage__sd_WBC_Differnetial',
'patient_storage__sd_Absolute_neutrophil_counts',
'patient_storage__sd_PT_sec',
'patient_storage__sd_APTT_sec',
'patient_storage__sd_S_calcium_mg_dl',
'patient_storage__sd_S_Phosphorus_mg_dl',
'patient_storage__sd_S_alkaline_phosphatise_IU',
'patient_storage__sd_S_Acid_phosphatise_IU',
'patient_storage__sd_S_Total_protein_g_dl',
'patient_storage__sd_S_Serum_albumin_g_dl',
'patient_storage__sd_SGPT_IU',
'patient_storage__sd_GGT',
'patient_storage__sd_GGT',
'patient_storage__sd_IRON_mg_dl',
'patient_storage__sd_TIBC_mg_dl',
'patient_storage__sd_Vit_B12_pg_ml',
'patient_storage__sd_Vit_D_ng_ml',
'patient_storage__sd_PTH_ng_ml',
'patient_storage__sd_Skeletal_survey',
'patient_storage__sd_Erlenmeyer_flask_deformity',
'patient_storage__sd_Osteopenia',
'patient_storage__sd_Skeletal_Scoliosis',
'patient_storage__sd_Dysostosis_multiplex',
'patient_storage__sd_Dexa_Z_Score',
'patient_storage__sd_xray_bone_age',
'patient_storage__sd_Pulmonary_function_test',
'patient_storage__sd_sitting_FEV1',
'patient_storage__sd_sittingFVC',
'patient_storage__sd_Supine_FEV1',
'patient_storage__sd_SupineFVC',
'patient_storage__sd_rad_ultrasono_type',
'patient_storage__sd_rad_liversize',
'patient_storage__sd_rad_liverEchotexture',
'patient_storage__sd_rad_hepatic',
'patient_storage__sd_rad_Kidney',
'patient_storage__sd_rad_kidney_size',
'patient_storage__sd_rad_kidney_size',
'patient_storage__sd_rad_lymphnodes_size',
'patient_storage__sd_rad_portal_vien_dia',
'patient_storage__sd_rad_adenoma',
'patient_storage__sd_renal_par_pathalogy',
'patient_storage__sd_renal_par_pathalogy_specify',
'patient_storage__sd_nephrocalcinosis',
'patient_storage__sd_pancreatitis',
'patient_storage__sd_cholethiasis',
'patient_storage__sd_CT_scan',
'patient_storage__sd_CT_scan_specify',
'patient_storage__sd_MRI_Brain',
'patient_storage__cerebral_atrophy',
'patient_storage__hydrocephalus',
'patient_storage__basal_ganglia_hypo',
'patient_storage__hyperintensity',
'patient_storage__thalamic',
'patient_storage__dysmyelination',
'patient_storage__Any_other_MRI',
'patient_storage__sd_MRI_Spine_limbs_pelvis',
'patient_storage__sd_Osteonecrosis',
'patient_storage__sd_Compression_spine_deformity_fractures',
'patient_storage__sd_Marrow_infiltration',
'patient_storage__sd_marrow_Any_other',
'patient_storage__sd_MRI_abdomen',
'patient_storage__sd_Liver_volume',
'patient_storage__sd_Spleen_volume',
'patient_storage__sd_Gaucher_related_nodules',
'patient_storage__sd_Echocardiography_test',
'patient_storage__sd_Specify_findings_Cardiomyopathy',
'patient_storage__Cardiomyopathy',
'patient_storage__sd_Cardiomyopathy',
'patient_storage__sd_Mention_LVMI',
'patient_storage__sd_Valvular_involvement',
'patient_storage__Valvular_Stenosis_mitral',
'patient_storage__Valvular_Stenosis_tricuspid',
'patient_storage__Valvular_Stenosis_aortic',
'patient_storage__Valvular_Stenosis_pulmonary',
'patient_storage__sd_Valvular_Regurgitation',
'patient_storage__Valvular_Regurgitation_mitral',
'patient_storage__Valvular_Regurgitation_tricuspid',
'patient_storage__Valvular_Regurgitation_aortic',
'patient_storage__Valvular_Regurgitation_pulmonary',
'patient_storage__sd_Ejection_fraction',
'patient_storage__sd_EEG',
'patient_storage__sd_EEG_specify_Findings',
'patient_storage__sd_Sleep_Studies',
'patient_storage__sd_Sleep_Studies_Findings',
'patient_storage__sd_SLIT_lamp_examination',
'patient_storage__sd_VEP',
'patient_storage__sd_ved_specify',
'patient_storage__sd_Opthalmological_Examination',
'patient_storage__sd_Describe_if_abnormal',
'patient_storage__sd_SLIT_Lamp',
'patient_storage__sd_BERA_Audiogram',
'patient_storage__sd_BERA_Describe_if_abnormal',
'patient_storage__sd_Servirity',
'patient_storage__sd_Unilat_bilat',
'patient_storage__sd_Nerve_Conduction_Study',
'patient_storage__sd_Nerve_Describe_if_abnormal',
'patient_storage__sd_Chitrotriosidase_Study',
'patient_storage__sd_Chitrotriosidase_if_abnormal',
'patient_storage__Any_Other_Biomarker2',
'patient_storage__sd_Biomarker_if_abnormal',
'patient_storage__sd_Enzyme_assay',
'patient_storage__sd_Sample_used',
'patient_storage__sd_Enzyme',
'patient_storage__sd_Enzyme_other',
'patient_storage__mt_enzyme_patient_control',
'patient_storage__mt_enzyme_control_range',
'patient_storage__mt_enzyme_normal_range',
'patient_storage__sd_Enzyme_upload',
'patient_storage__sd_Causative_DNA_sequence_variat',
'patient_storage__sd_molecular_upload',
'patient_storage__sd_Gene_molecula',
'patient_storage__sd_trans_molecul',
'patient_storage__sd_mul_dna1',
'patient_storage__sd_mul_pro1',
'patient_storage__sd_mul_var1',
'patient_storage__sd_mul_var_cla1',
'patient_storage__sd_mul_zygo1',
'patient_storage__sd_mul_dna2',
'patient_storage__sd_mul_pro2',
'patient_storage__sd_mul_var2',
'patient_storage__sd_mul_var_cla2',
'patient_storage__sd_mul_zygo2',
'patient_storage__sd_mul_seg',
'patient_storage__sd_father',
'patient_storage__sd_mother',
'patient_storage__sd_ERT',
'patient_storage__sd_Date_of_initiation',
'patient_storage__sd_age_of_start',
'patient_storage__sd_Dosage',
'patient_storage__sd_Duration',
'patient_storage__sd_Adverse_events',
'patient_storage__sd_Adverse_events_specify',
'patient_storage__sd_ERT_Status',
'patient_storage__sd_Response_to_therapy',
'patient_storage__sd_Any_interruption',
'patient_storage__sd_Reason_interruption',
'patient_storage__sd_Duration_interruption',
'patient_storage__sd_Bone_Marrow_Transplantation',
'patient_storage__sd_Bone_Marrow_Date',
'patient_storage__sd_Donor',
'patient_storage__sd_Hospital',
'patient_storage__sd_Response',
'patient_storage__sd_Surgery1',
'patient_storage__Surgery_Splenectomy',
'patient_storage__Surgery_Hernia',
'patient_storage__Surgery_others',
'patient_storage__Surgery_others_text',
'patient_storage__sd_Surgery_age',
'patient_storage__sd_Calcium_and_multivitamin_supplements',
'patient_storage__sd_Regular_Physiotherapy',
'patient_storage__sd_Antiepileptics',
'patient_storage__sd_Blood_Transfusion',
'patient_storage__sd_BL_freq',
'patient_storage__sd_BL_Trans',
'patient_storage__sd_Platlet_Transfusion',
'patient_storage__sd_PL_freq',
'patient_storage__sd_PL_Trans',
'patient_storage__PL_Any_other',
'patient_storage__sd_final_diagnosis',
'patient_storage__sd_final_diagnosis_other',
'patient_storage__sd_Final_Outcome',
'patient_storage__sd_death_cause',
'patient_storage__sd_age_timedeath',
'patient_storage__sd_filed_by_DEO_name',
'patient_storage__sd_clinician_name',
'patient_storage__sd_filled_date', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def update_qa_qc_storage(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_storage.objects.get(id=pk)
    form2 = QAstorageForm(instance=patient)

    if request.method == 'POST':
        form2 = QAstorageForm(request.POST, request.FILES, instance=patient)
        if form2.is_valid():
            auth1 = form2.save(commit=False)
            auth1.qa_user = user
            auth1.qa_register = register
            if auth1.quality_result == 'Pass':
                auth1.quality_status = 'Completed'
            else:
                auth1.quality_status = 'Pending'
            # auth1.patient = patient
            auth1.save()
            return redirect('total_record_sd_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_storage.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_storage.html', context)


@login_required(login_url='login')
def view_qa_qc_storage(request, pk):
    user = request.user
    patient = profile_storage.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
