from django.contrib import messages
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear, ExtractWeekDay, \
    ExtractWeek, TruncMonth, \
    TruncWeek, \
    TruncDay
from collections import OrderedDict

from account.decorators import unauthenticated_user
from .forms import *


@login_required(login_url='login')
def add_record_meta(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = ProfilemetabolismForm()
    if request.method == 'POST':
        form1 = ProfilemetabolismForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(demographic_meta, args=(auth1.id,)))

    context = {'form1': form1, }
    return render(request, 'add_record_meta.html', context)


@login_required(login_url='login')
def update_patient_record_meta(request,pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_metabolism.objects.get(id=pk)

    form1 = ProfilemetabolismForm(instance=patient )
    if request.method == 'POST':
        form1 = ProfilemetabolismForm(request.POST, request.FILES,instance=patient )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_mt')

        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_meta.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_meta.html', context)


@login_required(login_url='login')
def view_profile_mt(request, pk):

    try:
        form1 = profile_metabolism.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_mt.html', context)


@login_required(login_url='login')
def demographic_meta(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_metabolism.objects.get(id=pk)
    form1 = SocioDemographicDetailsmetaForm()
    if request.method == 'POST':
        form1 = SocioDemographicDetailsmetaForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.patient = patient
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_mt, args=(pk,)))
        else:
            context = {'form1': form1, }
            return render(request, 'demographic_meta.html', context)

    context = {'form1': form1, }
    return render(request, 'demographic_meta.html', context)


@login_required(login_url='login')
def update_record_mt(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_metabolism.objects.get(id=pk)
    try:
        socio = demographic_matabolism.objects.get(patient=patient)
        form1 = SocioDemographicDetailsmetaForm(instance=socio)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsmetaForm(request.POST, request.FILES, instance=socio)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect("total_record_mt")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_mt.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsmetaForm(request.POST, request.FILES, instance=socio)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_mt")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_mt.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = SocioDemographicDetailsmetaForm(request.POST, request.FILES, instance=socio)
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
                    return render(request, 'update_record_mt.html', context)
    except:

        form1 = SocioDemographicDetailsmetaForm()
        # user1 = Registration.objects.get(user=request.user)
        if request.method == 'POST':
            form1 = SocioDemographicDetailsmetaForm(request.POST, request.FILES, )

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()

                return redirect('total_record_mt')

            else:
                context = {'form1': form1,'patient': patient,  }
                return render(request, 'demographic_meta.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_mt.html', context)


@login_required(login_url='login')
def total_record_mt(request):
    pat = profile_metabolism.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_mt.html', context)


@login_required(login_url='login')
def total_record_mt_admin(request):
    pat = profile_metabolism.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_mt_admin.html', context)


@login_required(login_url='login')
def delete_record_mt(request, pk):
    order = profile_metabolism.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_mt')

    context = {'order': order}
    return render(request, 'delete_record_mt.html', context)


@login_required(login_url='login')
def view_record_mt(request, pk):
    patient = profile_metabolism.objects.get(id=pk)
    try:
        form1 = demographic_matabolism.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_record_mt.html', context)


def export_iem_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iem.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_records', 'date_of_clinical_exam', 'date_of_birth', 'patient_name', 'father_name', 'mother_name',
         'paitent_id_yes_no', 'paitent_id', 'patient_id_no', 'father_mother_id', 'mother_father_id_no', 'permanent_addr', 'state', 'district', 'city_name', 'country_name', 'land_line_no',
         'mother_mobile_no', 'father_mobile_no', 'email', 'religion', 'religion_other_specify', 'caste', 'caste_other_specify', 'gender', 'referred_status', 'referred_by',
         'referred_by_desc', 'consent_given', 'consent_upload', 'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no', 'patient_edu_status','mt_patient_occupation',
'mt_father_edu_status',
'mt_father_occupation',
'mt_mother_edu_status',
'mt_mother_occupation',
'mt_monthly_income_status',
'mt_anthropometry_date',
'mt_anth_wght_pat',
'mt_anth_wght_per',
'mt_anth_wght_sd',
'mt_anth_height_pat',
'mt_anth_height_per',
'mt_anth_height_sd',
'mt_lower_segment_patient',
'mt_lower_segment_percemtile',
'mt_lower_segment_sd',
'mt_lower_us_ls_patient',
'mt_lower_us_ls_percemtile',
'mt_lower_us_ls_sd',
'mt_anth_head_cir_pat',
'mt_anth_head_cir_perc',
'mt_anth_head_cir_sd',
'mt_lower_arm_spam_patient',
'mt_lower_arm_spam_percemtile',
'mt_lower_arm_spam_sd',
'mt_presenting_complaints_years',
'mt_presenting_complaints_months',
'mt_presenting_complaints_day',
'mt_presenting_complaints_intrauterine',
'mt_presenting_complaints_age_presentation_years',
'mt_presenting_complaints_age_presentation_months',
'mt_presenting_complaints_age_presentation_day',
'mt_presenting_complaints_age_presentation_intrauterine',
'mt_presenting_complaints_age_diagnosis_years',
'mt_presenting_complaints_age_diagnosis_months',
'mt_presenting_complaints_age_diagnosis_day',
'mt_presenting_complaints_age_diagnosis_intrauterine',
'mt_pedigree_upload',
'mt_fam_hist_status',
'mt_fam_hist_descr',
'mt_cons_status',
'mt_cons_degree_specify',
'mt_Inbreeding',
'mt_Inbreeding_specify_degree',
'mt_Inbreeding_coefficient_degree',
'mt_encephalopathic_presentation',
'mt_encephalopathic_presentation_age_presentaion',
'mt_encephalopathic_presentation_age_diagnosis',
'mt_encephalopathic_presentation_duration',
'mt_Presentation_neonatal_jaundice',
'mt_Presentation_neonatal_jaundice_age_presentation',
'mt_Presentation_neonatal_jaundice_ae_diagnosis',
'mt_Presentation_neonatal_jaundice_duraions',
'mt_Presentation_cardiac_symptoms',
'mt_Presentation_cardiac_symptoms_age_presentation',
'mt_Presentation_cardiac_symptoms_age_diagnosis',
'mt_Presentation_cardiac_symptoms_duration',
'mt_symptoms_after_long_normalcy',
'mt_symptoms_after_long_normalcy_sugar',
'mt_symptoms_after_long_normalcy_fruit_juice',
'mt_symptoms_after_long_normalcy_fasting',
'mt_symptoms_after_long_normalcy_protein_foods',
'mt_symptoms_after_long_normalcy_febrile_illness',
'mt_Presentation_refractory_epilepsy',
'mt_Presentation_refractory_epilepsy_age_presentation',
'mt_Presentation_refractory_epilepsy_age_diagnosis',
'mt_Presentation_refractory_epilepsy_duration',
'mt_mental_retardation_or_dev_delay',
'mt_mental_retardation_Motor',
'mt_mental_retardation_Cognitive',
'mt_mental_retardation_Global',
'mt_Neuroregression',
'mt_Neuroregression_Motor',
'mt_Neuroregression_Cognitive',
'mt_Neuroregression_Global',
'mt_Age_onset_regression',
'mt_Vomiting',
'mt_Aversion_sweet_protein',
'mt_Loose_stools',
'mt_Loose_stools_dropdown',
'mt_Pneumonia',
'mt_Pneumonia_dropdown',
'mt_Fever',
'mt_Fever_dropdown',
'mt_Fever_type',
'mt_Lethargy',
'mt_Behavioral_problems',
'mt_Excessive_crying',
'mt_Decreased_attention_span',
'mt_Speech_disturbances',
'mt_Decline_school_performance',
'mt_Clumsiness',
'mt_Seizures',
'mt_Seizures_Partial',
'mt_Seizures_generalized',
'mt_Seizures_myoclonic',
'mt_Seizures_other',
'mt_Seizures_other_specify',
'mt_Seizures_frequency',
'mt_AntiConvulsant_therapy',
'mt_AntiConvulsant_Monotherapy',
'mt_AntiConvulsant_Monotherapy_drug_name',
'mt_AntiConvulsant_Monotherapy_dose',
'mt_AntiConvulsant_Polytherapy',
'mt_AntiConvulsant_Polytherapy_drug_name',
'mt_AntiConvulsant_Polytherapy_dose',
'mt_HistoryPreviousAdmission',
'mt_history_nuroregression',
'mt_history_nuroregression_text',
'mt_history_diagnosis',
'mt_history_diagnosis_text',
'mt_history_mech_ventilation',
'mt_history_mech_ventilation_text',
'mt_history_mech_distention',
'mt_history_mech_distention_text',
'mt_any_surgery',
'mt_any_surgery_specify',
'mt_History_liver_dysfunction',
'mt_History_liver_dysfunction_trimester_pregnancy',
'mt_Ultrasound',
'mt_Ultrasound_Polyhydramnios',
'mt_Ultrasound_Oligoamnios',
'mt_Ultrasound_Skeletal_anomalies',
'mt_Ultrasound_Hydrops',
'mt_Ultrasound_abnormal_specify',
'mt_Delivery_type',
'mt_Baby_cried_immediately_after_delivery',
'mt_Resuscitation_required',
'mt_NICU_Stay',
'mt_Symptomatic_asymptomatic',
'mt_Shock',
'mt_Shock_catecholamine_sensitive',
'mt_Shock_refractory',
'mt_Ventilation',
'mt_Ventilation_CPAP',
'mt_Ventilation_NIV',
'mt_Ventilation_MV',
'mt_feeding_issues',
'mt_feeding_issues_Regurgitation_oral_feed',
'mt_feeding_issues_NG_feeding',
'mt_feeding_issues_Parenteral',
'mt_Neonatal_hyperbilurubinemia',
'mt_Neonatal_hyperbilurubinemia_direct',
'mt_Neonatal_hyperbilurubinemia_indirect',
'mt_Neonatal_hyperbilurubinemia_total_bill_value',
'mt_Sepsis',
'mt_Sepsis_Organism',
'mt_CRRT_PD_required',
'mt_EEG_natel',
'mt_EEG_BurstSuppressionPattern_natel',
'mt_EEG_Hypsarrythmia_natel',
'mt_EEG_GeneralizedSlowing_natel',
'mt_EEG_Comb_like_pattern_natel',
'mt_facial_dysmorphism',
'mt_Facial_dysmorphism_upload_file',
'mt_Skin_Pigmentation',
'mt_Skin_Pigmentation_Hypopigmentation_diffuse',
'mt_Skin_Pigmentation_Hypopigmentation_patchy',
'mt_Skin_Pigmentation_Hypopigmentation',
'mt_Hirsutism',
'mt_Hirsutism_Facial',
'mt_Hirsutism_generalised',
'mt_Excessive_mongolion_spots',
'mt_Ichthyosis',
'mt_Telengiectasia',
'mt_Edema',
'mt_Hydrops',
'mt_Inverted_nipples',
'mt_fat_distribution_Lipodystrophy',
'mt_Hemoglobinura',
'mt_Encephalopathy',
'mt_Hypotonia',
'mt_Hypertonia',
'mt_Brisk_reflexes',
'mt_Hyporeflexia',
'mt_Opisthotonus',
'mt_Other_Abnormal_Movement',
'mt_Tremor_chorea_athetosis',
'mt_AnyOther_TremorJitteriness',
'mt_AnyOther_chorea',
'mt_AnyOther_athetosis',
'mt_Gait_abnormalities',
'mt_Optic_Nerve_atrophy',
'mt_Retinal_degeneration',
'mt_Cataract',
'mt_Squint',
'mt_Nystagmus_oculogyria',
'mt_Fundus_Abnormal',
'mt_Fundus_Abnormal_specify',
'mt_cheery_red_spot',
'mt_cheery_red_spot_specify',
'mt_Murmur',
'mt_Congestive_Heart_Failure',
'mt_Cardio_myopathy',
'mt_Hepatomegaly',
'mt_Consistency',
'mt_surface',
'mt_margin',
'mt_BCM_size',
'mt_Span_cm',
'mt_Splenomegaly',
'mt_Splenomegaly_size_cm',
'mt_IQ',
'mt_IQ_value',
'mt_DQ',
'mt_DQ_value',
'mt_Any_other_findings',
'mt_Hb_gm_dl',
'mt_wbc_tc_ul',
'mt_wbc_dc_perc',
'mt_Absolut_Neutrophil_count_mm_3',
'mt_Platelet_count_ul',
'mt_Acanthocytes',
'mt_S_calcium_mg_dl',
'mt_S_phosphorous_mg_dl',
'mt_S_alkaline_phosphate_UI',
'mt_S_acid_phosphatase_U_L',
'mt_CPK_U_L_total',
'mt_MM_MB',
'mt_Blood_Urea',
'mt_Blood_creatinine_mg_dl',
'mt_Serum_sodium_meq_l',
'mt_Serum_potassium_meq_l',
'mt_Total_protein_g_dl',
'mt_Serum_albumin_g_dl',
'mt_SGPT_IU_L',
'mt_SGOT_IU_L',
'mt_PT_sec',
'mt_APTT_sec',
'mt_TSB_mg_dl',
'mt_DSB_mg_dl',
'mt_IRON_IU_L',
'mt_TIBC_IU_L',
'mt_Lactate_mmol_l',
'mt_Uric_acid_mg_dl',
'mt_Blood_sugar_mg_dl',
'mt_HbA1C_per',
'mt_Total_Cholesterol_mg_dl',
'mt_TGs_mg_dl',
'mt_HDL_mg_dl',
'mt_LDL_mg_dl',
'mt_VLDL_mg_dl',
'mt_Homocysteine_uml_l',
'mt_Prolactin_ng_ml',
'mt_Ultrasonography',
'mt_Ultrasonography_abnormal_Liver',
'mt_Ultrasonography_abnormal_Kidney',
'mt_Ultrasonography_abnormal_Spleen',
'mt_Ultrasonography_abnormal_AnyAdenoma',
'mt_Ultrasonography_abnormal_RenalCysts',
'mt_Skeletal_survey',
'mt_Skeletal_survey_Rickets',
'mt_Skeletal_survey_DysostosisMultiplex',
'mt_Skeletal_survey_ShortLimbs',
'mt_Skeletal_survey_SpineAbnormalities',
'mt_Skeletal_survey_ChondrodyplasiaPuncta',
'mt_ctc_scan',
'mt_ctc_scan_ThalamusHypointesity',
'mt_ctc_scan_calcification',
'mt_ctc_scan_ventriculomegaly',
'mt_ctc_scan_cerebralAtrophy',
'mt_ctc_scan_infarct',
'mt_ctc_scan_hemorrhage',
'mt_ctc_scan_cerebraledema',
'mt_ctc_scan_cysts',
'mt_mri_brain_status',
'mt_mri_brain_corticalAtrophy',
'mt_mri_brain_cerebellarAtrophy',
'mt_mri_brain_ventriculomegaly',
'mt_mri_brain_basalGangliaHypo',
'mt_mri_brain_hyperintensity',
'mt_mri_brain_deepGrayMatterHyperintensity',
'mt_mri_brain_thalamicHypo',
'mt_mri_brain_demyelinationDysmyelination',
'mt_mri_brain_cerebralEdema',
'mt_mri_brain_cysts',
'mt_mri_brain_infarct',
'mt_mri_brain_hemorrhage',
'mt_mri_brain_other',
'mt_mrs_done',
'mt_mrs_LactatePeak',
'mt_mrs_NAAPeak',
'mt_mrs_LowCreatininePeak',
'mt_mrs_CholinePeak',
'mt_echocardiography',
'mt_echocardiography_DialtedCardiomyopathy',
'mt_echocardiography_hypertrophicCardiomyopathy',
'mt_echocardiography_valvularAbnormality',
'mt_echocardiography_structuralDefects',
'mt_echocardiography_SpecifyStructuralDefect',
'mt_echocardiography_EjectionFraction',
'mt_eeg',
'mt_eeg_BurstSuppressionPattern',
'mt_eeg_Hypsarrythmia',
'mt_eeg_GeneralizedSlowing',
'mt_eeg_CombLikePattern',
'mt_ocular_examination_slit',
'mt_veps',
'mt_veps_abnormal_latency',
'mt_erg',
'mt_erg_abnormal_specify',
'mt_OAE_BERA',
'mt_OAE_BERA_Unilateral',
'mt_OAE_BERA_bilateral',
'mt_OAE_BERA_mild',
'mt_OAE_BERA_moderate',
'mt_OAE_BERA_severe',
'mt_OAE_BERA_profoundHearingLoss',
'mt_nerve_conduction_study',
'mt_nerve_conduction_study_motor',
'mt_nerve_conduction_study_sensory',
'mt_nerve_conduction_study_mixed',
'mt_nerve_conduction_study_upperLimb',
'mt_nerve_conduction_study_lowerLimb',
'mt_nerve_conduction_study_reducedMUAPAmplitude',
'mt_nerve_conduction_study_shortMUAPDuration',
'mt_nerve_conduction_study_decreasedConductionVelocity',
'mt_nerve_conduction_study_increasedDistalLatency',
'mt_nerve_conduction_study_decreasedSNAP',
'mt_nerve_conduction_study_increasedFwaveLatency',
'mt_muscle_biopsy',
'mt_Any_other_investigations',
'mt_blood_gas_metabolism_acidosis',
'mt_blood_gas_metabolism_acidosis_PH',
'mt_blood_gas_metabolism_acidosis_HCO_3',
'mt_blood_gas_metabolism_acidosis_Anion_gap',
'mt_metabolic_alkalosis',
'mt_Hyper_ammonemia',
'mt_Hyper_ammonemia_value',
'mt_Hyper_ammonemia_duration',
'mt_high_lactate',
'mt_high_lactate_value',
'mt_high_lactate_csf',
'mt_high_lactate_csf_value',
'mt_ief_transferring_pattern_type',
'mt_ief_transferring_pattern_type_tpye1',
'mt_ief_transferring_pattern_type_tpye2',
'mt_urine_ketones',
'mt_urine_ketones_value',
'mt_plasma_ketones',
'mt_plasma_ketones_value',
'mt_plasma_ketones_ffa_ratio',
'mt_plasma_ketones_ffa_ratio_value',
'mt_hplc',
'mt_hplc_specify',
'mt_hplc_value',
'mt_tms_primary_analyte',
'mt_tms_primary_analyte_specify_anlyte',
'mt_tms_primary_analyte_value',
'mt_gcms',
'mt_gcms_abnormal_specify',
'mt_gcms_abnormal_value',
'mt_orotic_acid',
'mt_vlcfa',
'mt_vlcfa_abnormal_specify',
'mt_succinyl_acetone_status',
'mt_succinyl_acetone_abnormal_specify',
'mt_csf',
'mt_csf_amino_acid',
'mt_csf_glucose',
'mt_csf_lactose',
'mt_csf_protien',
'mt_csf_nurotransonitres',
'mt_csf_porphyrins',
'mt_csf_purine',
'mt_csf_pyrinidies',
'mt_csf_glycine',
'mt_csf_others',
'mt_enzyme_analusis',
'mt_enzyme_analusis_ref_range',
'mt_enzyme_analusis_lab_name',
'mt_enzyme_analusis_normal_control',
'mt_enzyme_analusis_normal_range',
'mt_enzyme_analusis_sample_dbs_blood',
'mt_enzyme_analusis_upload_report',
'mt_enzyme_analusis_sample_dbs_blood_date',
'mt_Causative_DNA_sequence_variat',
'mt_molecular_upload',
'mt_Gene_molecula',
'mt_trans_molecul',
'mt_mul_dna1',
'mt_mul_pro1',
'mt_mul_var1',
'mt_mul_var_cla1',
'mt_mul_zygo1',
'mt_mul_dna2',
'mt_mul_pro2',
'mt_mul_var2',
'mt_mul_var_cla2',
'mt_mul_zygo2',
'mt_mul_seg',
'mt_father',
'mt_mother',
'mt_special_diet',
'mt_dietary_managment_1',
'mt_dietary_managment_2',
'mt_dietary_managment_3',
'mt_dietary_managment_4',
'mt_dietary_managment_type_of_diet_1',
'mt_dietary_managment_type_of_diet_2',
'mt_dietary_managment_type_of_diet_3',
'mt_dietary_managment_type_of_diet_4',
'mt_dietary_managment_type_of_diet_5',
'mt_dietary_managment_type_of_diet_6',
'mt_liver_transplantation',
'mt_kidney_transplantation',
'mt_heart_transplantation',
'mt_lung_transplantation',
'mt_calcium_multivitamin_supplements',
'mt_regular_physiotherapy',
'mt_any_ocular_medication',
'mt_CPAP_BiPAP_sleep_apnea',
'mt_any_other_specify',
'mt_any_other_special_drug',
'mt_any_other_special_drug_1',
'mt_any_other_special_drug_2',
'mt_any_other_special_drug_3',
'mt_any_other_special_drug_4',
'mt_any_other_special_drug_5',
'mt_any_other_special_drug_6',
'mt_any_other_special_drug_7',
'mt_any_other_special_drug_8',
'mt_any_other_special_drug_9',
'mt_any_other_special_drug_10',
'mt_any_other_special_drug_11',
'mt_any_other_special_drug_12',
'mt_any_other_special_drug_13',
'mt_any_other_special_drug_14',
'mt_any_other_special_drug_specify',
'mt_Final_Diagnosis',
'organic_cat',
'organic_cat_other',
'aminoacidpathies_cat',
'aminoacidpathies_cat_BCAA',
'aminoacidpathies_cat_other',
'urea_cat',
'urea_cat_NAGS',
'vitamin_cat',
'vitamin_cobalamin',
'vitamin_folate',
'vitamin_biotin',
'vitamin_pyridoxine',
'vitamin_other',
'fatty_cat',
'fatty_cat_other',
'metal_cat',
'metal_cat_other',
'carbohydrate_cat',
'Carbohydrate_sub3',
'Congenital_disorder',
'Peroxisomal_disorder_specify',
'mitochondrial_cat',
'mitochondrial_nuclear',
'mitochondrial_mitochondrial',
'mitochondrial_other',
'Neurotransmitter_cat',
'Neurotransmitter_pterin',
'Neurotransmitter_tyrosine',
'Neurotransmitter_other',
'mt_diag_other',
'mt_Final_Outcome',
'mt_death_cause',
'mt_age_timedeath',
'mt_filled_by_deo_name',
'mt_clinician_name',
'mt_date_filled',])

    users = profile_metabolism.objects.filter(user=request.user).prefetch_related('patient_metabolism').values_list('register_id__institute_name', 'uniqueId', 'mt_icmr_unique_no',
                                                                                                    'mt_final_diagnosis',
                                                                                       'mt_date_of_records', 'mt_date_of_clinical_exam', 'mt_date_of_birth',
                                                                                       'mt_patient_name', 'mt_father_name', 'mt_mother_name', 'mt_paitent_id_yes_no',
                                                                                       'mt_paitent_id', 'mt_patient_id_no', 'mt_father_mother_id', 'mt_mother_father_id_no',
                                                                                       'mt_permanent_addr', 'mt_state', 'mt_district', 'mt_city_name', 'mt_country_name',
                                                                                       'mt_land_line_no', 'mt_mother_mobile_no', 'mt_father_mobile_no', 'mt_email',
                                                                                       'mt_religion', 'mt_religion_other_specify', 'mt_caste', 'mt_caste_other_specify',
                                                                                       'mt_gender', 'mt_referred_status', 'mt_referred_by', 'mt_referred_by_desc',
                                                                                       'mt_consent_given', 'mt_consent_upload', 'mt_assent_given', 'mt_assent_upload',
                                                                                       'mt_hospital_name', 'mt_hospital_reg_no', 'patient_metabolism__mt_patient_edu_status',
'patient_metabolism__mt_patient_occupation',
'patient_metabolism__mt_father_edu_status',
'patient_metabolism__mt_father_occupation',
'patient_metabolism__mt_mother_edu_status',
'patient_metabolism__mt_mother_occupation',
'patient_metabolism__mt_monthly_income_status',
'patient_metabolism__mt_anthropometry_date',
'patient_metabolism__mt_anth_wght_pat',
'patient_metabolism__mt_anth_wght_per',
'patient_metabolism__mt_anth_wght_sd',
'patient_metabolism__mt_anth_height_pat',
'patient_metabolism__mt_anth_height_per',
'patient_metabolism__mt_anth_height_sd',
'patient_metabolism__mt_lower_segment_patient',
'patient_metabolism__mt_lower_segment_percemtile',
'patient_metabolism__mt_lower_segment_sd',
'patient_metabolism__mt_lower_us_ls_patient',
'patient_metabolism__mt_lower_us_ls_percemtile',
'patient_metabolism__mt_lower_us_ls_sd',
'patient_metabolism__mt_anth_head_cir_pat',
'patient_metabolism__mt_anth_head_cir_perc',
'patient_metabolism__mt_anth_head_cir_sd',
'patient_metabolism__mt_lower_arm_spam_patient',
'patient_metabolism__mt_lower_arm_spam_percemtile',
'patient_metabolism__mt_lower_arm_spam_sd',
'patient_metabolism__mt_presenting_complaints_years',
'patient_metabolism__mt_presenting_complaints_months',
'patient_metabolism__mt_presenting_complaints_day',
'patient_metabolism__mt_presenting_complaints_intrauterine',
'patient_metabolism__mt_presenting_complaints_age_presentation_years',
'patient_metabolism__mt_presenting_complaints_age_presentation_months',
'patient_metabolism__mt_presenting_complaints_age_presentation_day',
'patient_metabolism__mt_presenting_complaints_age_presentation_intrauterine',
'patient_metabolism__mt_presenting_complaints_age_diagnosis_years',
'patient_metabolism__mt_presenting_complaints_age_diagnosis_months',
'patient_metabolism__mt_presenting_complaints_age_diagnosis_day',
'patient_metabolism__mt_presenting_complaints_age_diagnosis_intrauterine',
'patient_metabolism__mt_pedigree_upload',
'patient_metabolism__mt_fam_hist_status',
'patient_metabolism__mt_fam_hist_descr',
'patient_metabolism__mt_cons_status',
'patient_metabolism__mt_cons_degree_specify',
'patient_metabolism__mt_Inbreeding',
'patient_metabolism__mt_Inbreeding_specify_degree',
'patient_metabolism__mt_Inbreeding_coefficient_degree',
'patient_metabolism__mt_encephalopathic_presentation',
'patient_metabolism__mt_encephalopathic_presentation_age_presentaion',
'patient_metabolism__mt_encephalopathic_presentation_age_diagnosis',
'patient_metabolism__mt_encephalopathic_presentation_duration',
'patient_metabolism__mt_Presentation_neonatal_jaundice',
'patient_metabolism__mt_Presentation_neonatal_jaundice_age_presentation',
'patient_metabolism__mt_Presentation_neonatal_jaundice_ae_diagnosis',
'patient_metabolism__mt_Presentation_neonatal_jaundice_duraions',
'patient_metabolism__mt_Presentation_cardiac_symptoms',
'patient_metabolism__mt_Presentation_cardiac_symptoms_age_presentation',
'patient_metabolism__mt_Presentation_cardiac_symptoms_age_diagnosis',
'patient_metabolism__mt_Presentation_cardiac_symptoms_duration',
'patient_metabolism__mt_symptoms_after_long_normalcy',
'patient_metabolism__mt_symptoms_after_long_normalcy_sugar',
'patient_metabolism__mt_symptoms_after_long_normalcy_fruit_juice',
'patient_metabolism__mt_symptoms_after_long_normalcy_fasting',
'patient_metabolism__mt_symptoms_after_long_normalcy_protein_foods',
'patient_metabolism__mt_symptoms_after_long_normalcy_febrile_illness',
'patient_metabolism__mt_Presentation_refractory_epilepsy',
'patient_metabolism__mt_Presentation_refractory_epilepsy_age_presentation',
'patient_metabolism__mt_Presentation_refractory_epilepsy_age_diagnosis',
'patient_metabolism__mt_Presentation_refractory_epilepsy_duration',
'patient_metabolism__mt_mental_retardation_or_dev_delay',
'patient_metabolism__mt_mental_retardation_Motor',
'patient_metabolism__mt_mental_retardation_Cognitive',
'patient_metabolism__mt_mental_retardation_Global',
'patient_metabolism__mt_Neuroregression',
'patient_metabolism__mt_Neuroregression_Motor',
'patient_metabolism__mt_Neuroregression_Cognitive',
'patient_metabolism__mt_Neuroregression_Global',
'patient_metabolism__mt_Age_onset_regression',
'patient_metabolism__mt_Vomiting',
'patient_metabolism__mt_Aversion_sweet_protein',
'patient_metabolism__mt_Loose_stools',
'patient_metabolism__mt_Loose_stools_dropdown',
'patient_metabolism__mt_Pneumonia',
'patient_metabolism__mt_Pneumonia_dropdown',
'patient_metabolism__mt_Fever',
'patient_metabolism__mt_Fever_dropdown',
'patient_metabolism__mt_Fever_type',
'patient_metabolism__mt_Lethargy',
'patient_metabolism__mt_Behavioral_problems',
'patient_metabolism__mt_Excessive_crying',
'patient_metabolism__mt_Decreased_attention_span',
'patient_metabolism__mt_Speech_disturbances',
'patient_metabolism__mt_Decline_school_performance',
'patient_metabolism__mt_Clumsiness',
'patient_metabolism__mt_Seizures',
'patient_metabolism__mt_Seizures_Partial',
'patient_metabolism__mt_Seizures_generalized',
'patient_metabolism__mt_Seizures_myoclonic',
'patient_metabolism__mt_Seizures_other',
'patient_metabolism__mt_Seizures_other_specify',
'patient_metabolism__mt_Seizures_frequency',
'patient_metabolism__mt_AntiConvulsant_therapy',
'patient_metabolism__mt_AntiConvulsant_Monotherapy',
'patient_metabolism__mt_AntiConvulsant_Monotherapy_drug_name',
'patient_metabolism__mt_AntiConvulsant_Monotherapy_dose',
'patient_metabolism__mt_AntiConvulsant_Polytherapy',
'patient_metabolism__mt_AntiConvulsant_Polytherapy_drug_name',
'patient_metabolism__mt_AntiConvulsant_Polytherapy_dose',
'patient_metabolism__mt_HistoryPreviousAdmission',
'patient_metabolism__mt_history_nuroregression',
'patient_metabolism__mt_history_nuroregression_text',
'patient_metabolism__mt_history_diagnosis',
'patient_metabolism__mt_history_diagnosis_text',
'patient_metabolism__mt_history_mech_ventilation',
'patient_metabolism__mt_history_mech_ventilation_text',
'patient_metabolism__mt_history_mech_distention',
'patient_metabolism__mt_history_mech_distention_text',
'patient_metabolism__mt_any_surgery',
'patient_metabolism__mt_any_surgery_specify',
'patient_metabolism__mt_History_liver_dysfunction',
'patient_metabolism__mt_History_liver_dysfunction_trimester_pregnancy',
'patient_metabolism__mt_Ultrasound',
'patient_metabolism__mt_Ultrasound_Polyhydramnios',
'patient_metabolism__mt_Ultrasound_Oligoamnios',
'patient_metabolism__mt_Ultrasound_Skeletal_anomalies',
'patient_metabolism__mt_Ultrasound_Hydrops',
'patient_metabolism__mt_Ultrasound_abnormal_specify',
'patient_metabolism__mt_Delivery_type',
'patient_metabolism__mt_Baby_cried_immediately_after_delivery',
'patient_metabolism__mt_Resuscitation_required',
'patient_metabolism__mt_NICU_Stay',
'patient_metabolism__mt_Symptomatic_asymptomatic',
'patient_metabolism__mt_Shock',
'patient_metabolism__mt_Shock_catecholamine_sensitive',
'patient_metabolism__mt_Shock_refractory',
'patient_metabolism__mt_Ventilation',
'patient_metabolism__mt_Ventilation_CPAP',
'patient_metabolism__mt_Ventilation_NIV',
'patient_metabolism__mt_Ventilation_MV',
'patient_metabolism__mt_feeding_issues',
'patient_metabolism__mt_feeding_issues_Regurgitation_oral_feed',
'patient_metabolism__mt_feeding_issues_NG_feeding',
'patient_metabolism__mt_feeding_issues_Parenteral',
'patient_metabolism__mt_Neonatal_hyperbilurubinemia',
'patient_metabolism__mt_Neonatal_hyperbilurubinemia_direct',
'patient_metabolism__mt_Neonatal_hyperbilurubinemia_indirect',
'patient_metabolism__mt_Neonatal_hyperbilurubinemia_total_bill_value',
'patient_metabolism__mt_Sepsis',
'patient_metabolism__mt_Sepsis_Organism',
'patient_metabolism__mt_CRRT_PD_required',
'patient_metabolism__mt_EEG_natel',
'patient_metabolism__mt_EEG_BurstSuppressionPattern_natel',
'patient_metabolism__mt_EEG_Hypsarrythmia_natel',
'patient_metabolism__mt_EEG_GeneralizedSlowing_natel',
'patient_metabolism__mt_EEG_Comb_like_pattern_natel',
'patient_metabolism__mt_facial_dysmorphism',
'patient_metabolism__mt_Facial_dysmorphism_upload_file',
'patient_metabolism__mt_Skin_Pigmentation',
'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_diffuse',
'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_patchy',
'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation',
'patient_metabolism__mt_Hirsutism',
'patient_metabolism__mt_Hirsutism_Facial',
'patient_metabolism__mt_Hirsutism_generalised',
'patient_metabolism__mt_Excessive_mongolion_spots',
'patient_metabolism__mt_Ichthyosis',
'patient_metabolism__mt_Telengiectasia',
'patient_metabolism__mt_Edema',
'patient_metabolism__mt_Hydrops',
'patient_metabolism__mt_Inverted_nipples',
'patient_metabolism__mt_fat_distribution_Lipodystrophy',
'patient_metabolism__mt_Hemoglobinura',
'patient_metabolism__mt_Encephalopathy',
'patient_metabolism__mt_Hypotonia',
'patient_metabolism__mt_Hypertonia',
'patient_metabolism__mt_Brisk_reflexes',
'patient_metabolism__mt_Hyporeflexia',
'patient_metabolism__mt_Opisthotonus',
'patient_metabolism__mt_Other_Abnormal_Movement',
'patient_metabolism__mt_Tremor_chorea_athetosis',
'patient_metabolism__mt_AnyOther_TremorJitteriness',
'patient_metabolism__mt_AnyOther_chorea',
'patient_metabolism__mt_AnyOther_athetosis',
'patient_metabolism__mt_Gait_abnormalities',
'patient_metabolism__mt_Optic_Nerve_atrophy',
'patient_metabolism__mt_Retinal_degeneration',
'patient_metabolism__mt_Cataract',
'patient_metabolism__mt_Squint',
'patient_metabolism__mt_Nystagmus_oculogyria',
'patient_metabolism__mt_Fundus_Abnormal',
'patient_metabolism__mt_Fundus_Abnormal_specify',
'patient_metabolism__mt_cheery_red_spot',
'patient_metabolism__mt_cheery_red_spot_specify',
'patient_metabolism__mt_Murmur',
'patient_metabolism__mt_Congestive_Heart_Failure',
'patient_metabolism__mt_Cardio_myopathy',
'patient_metabolism__mt_Hepatomegaly',
'patient_metabolism__mt_Consistency',
'patient_metabolism__mt_surface',
'patient_metabolism__mt_margin',
'patient_metabolism__mt_BCM_size',
'patient_metabolism__mt_Span_cm',
'patient_metabolism__mt_Splenomegaly',
'patient_metabolism__mt_Splenomegaly_size_cm',
'patient_metabolism__mt_IQ',
'patient_metabolism__mt_IQ_value',
'patient_metabolism__mt_DQ',
'patient_metabolism__mt_DQ_value',
'patient_metabolism__mt_Any_other_findings',
'patient_metabolism__mt_Hb_gm_dl',
'patient_metabolism__mt_wbc_tc_ul',
'patient_metabolism__mt_wbc_dc_perc',
'patient_metabolism__mt_Absolut_Neutrophil_count_mm_3',
'patient_metabolism__mt_Platelet_count_ul',
'patient_metabolism__mt_Acanthocytes',
'patient_metabolism__mt_S_calcium_mg_dl',
'patient_metabolism__mt_S_phosphorous_mg_dl',
'patient_metabolism__mt_S_alkaline_phosphate_UI',
'patient_metabolism__mt_S_acid_phosphatase_U_L',
'patient_metabolism__mt_CPK_U_L_total',
'patient_metabolism__mt_MM_MB',
'patient_metabolism__mt_Blood_Urea',
'patient_metabolism__mt_Blood_creatinine_mg_dl',
'patient_metabolism__mt_Serum_sodium_meq_l',
'patient_metabolism__mt_Serum_potassium_meq_l',
'patient_metabolism__mt_Total_protein_g_dl',
'patient_metabolism__mt_Serum_albumin_g_dl',
'patient_metabolism__mt_SGPT_IU_L',
'patient_metabolism__mt_SGOT_IU_L',
'patient_metabolism__mt_PT_sec',
'patient_metabolism__mt_APTT_sec',
'patient_metabolism__mt_TSB_mg_dl',
'patient_metabolism__mt_DSB_mg_dl',
'patient_metabolism__mt_IRON_IU_L',
'patient_metabolism__mt_TIBC_IU_L',
'patient_metabolism__mt_Lactate_mmol_l',
'patient_metabolism__mt_Uric_acid_mg_dl',
'patient_metabolism__mt_Blood_sugar_mg_dl',
'patient_metabolism__mt_HbA1C_per',
'patient_metabolism__mt_Total_Cholesterol_mg_dl',
'patient_metabolism__mt_TGs_mg_dl',
'patient_metabolism__mt_HDL_mg_dl',
'patient_metabolism__mt_LDL_mg_dl',
'patient_metabolism__mt_VLDL_mg_dl',
'patient_metabolism__mt_Homocysteine_uml_l',
'patient_metabolism__mt_Prolactin_ng_ml',
'patient_metabolism__mt_Ultrasonography',
'patient_metabolism__mt_Ultrasonography_abnormal_Liver',
'patient_metabolism__mt_Ultrasonography_abnormal_Kidney',
'patient_metabolism__mt_Ultrasonography_abnormal_Spleen',
'patient_metabolism__mt_Ultrasonography_abnormal_AnyAdenoma',
'patient_metabolism__mt_Ultrasonography_abnormal_RenalCysts',
'patient_metabolism__mt_Skeletal_survey',
'patient_metabolism__mt_Skeletal_survey_Rickets',
'patient_metabolism__mt_Skeletal_survey_DysostosisMultiplex',
'patient_metabolism__mt_Skeletal_survey_ShortLimbs',
'patient_metabolism__mt_Skeletal_survey_SpineAbnormalities',
'patient_metabolism__mt_Skeletal_survey_ChondrodyplasiaPuncta',
'patient_metabolism__mt_ctc_scan',
'patient_metabolism__mt_ctc_scan_ThalamusHypointesity',
'patient_metabolism__mt_ctc_scan_calcification',
'patient_metabolism__mt_ctc_scan_ventriculomegaly',
'patient_metabolism__mt_ctc_scan_cerebralAtrophy',
'patient_metabolism__mt_ctc_scan_infarct',
'patient_metabolism__mt_ctc_scan_hemorrhage',
'patient_metabolism__mt_ctc_scan_cerebraledema',
'patient_metabolism__mt_ctc_scan_cysts',
'patient_metabolism__mt_mri_brain_status',
'patient_metabolism__mt_mri_brain_corticalAtrophy',
'patient_metabolism__mt_mri_brain_cerebellarAtrophy',
'patient_metabolism__mt_mri_brain_ventriculomegaly',
'patient_metabolism__mt_mri_brain_basalGangliaHypo',
'patient_metabolism__mt_mri_brain_hyperintensity',
'patient_metabolism__mt_mri_brain_deepGrayMatterHyperintensity',
'patient_metabolism__mt_mri_brain_thalamicHypo',
'patient_metabolism__mt_mri_brain_demyelinationDysmyelination',
'patient_metabolism__mt_mri_brain_cerebralEdema',
'patient_metabolism__mt_mri_brain_cysts',
'patient_metabolism__mt_mri_brain_infarct',
'patient_metabolism__mt_mri_brain_hemorrhage',
'patient_metabolism__mt_mri_brain_other',
'patient_metabolism__mt_mrs_done',
'patient_metabolism__mt_mrs_LactatePeak',
'patient_metabolism__mt_mrs_NAAPeak',
'patient_metabolism__mt_mrs_LowCreatininePeak',
'patient_metabolism__mt_mrs_CholinePeak',
'patient_metabolism__mt_echocardiography',
'patient_metabolism__mt_echocardiography_DialtedCardiomyopathy',
'patient_metabolism__mt_echocardiography_hypertrophicCardiomyopathy',
'patient_metabolism__mt_echocardiography_valvularAbnormality',
'patient_metabolism__mt_echocardiography_structuralDefects',
'patient_metabolism__mt_echocardiography_SpecifyStructuralDefect',
'patient_metabolism__mt_echocardiography_EjectionFraction',
'patient_metabolism__mt_eeg',
'patient_metabolism__mt_eeg_BurstSuppressionPattern',
'patient_metabolism__mt_eeg_Hypsarrythmia',
'patient_metabolism__mt_eeg_GeneralizedSlowing',
'patient_metabolism__mt_eeg_CombLikePattern',
'patient_metabolism__mt_ocular_examination_slit',
'patient_metabolism__mt_veps',
'patient_metabolism__mt_veps_abnormal_latency',
'patient_metabolism__mt_erg',
'patient_metabolism__mt_erg_abnormal_specify',
'patient_metabolism__mt_OAE_BERA',
'patient_metabolism__mt_OAE_BERA_Unilateral',
'patient_metabolism__mt_OAE_BERA_bilateral',
'patient_metabolism__mt_OAE_BERA_mild',
'patient_metabolism__mt_OAE_BERA_moderate',
'patient_metabolism__mt_OAE_BERA_severe',
'patient_metabolism__mt_OAE_BERA_profoundHearingLoss',
'patient_metabolism__mt_nerve_conduction_study',
'patient_metabolism__mt_nerve_conduction_study_motor',
'patient_metabolism__mt_nerve_conduction_study_sensory',
'patient_metabolism__mt_nerve_conduction_study_mixed',
'patient_metabolism__mt_nerve_conduction_study_upperLimb',
'patient_metabolism__mt_nerve_conduction_study_lowerLimb',
'patient_metabolism__mt_nerve_conduction_study_reducedMUAPAmplitude',
'patient_metabolism__mt_nerve_conduction_study_shortMUAPDuration',
'patient_metabolism__mt_nerve_conduction_study_decreasedConductionVelocity',
'patient_metabolism__mt_nerve_conduction_study_increasedDistalLatency',
'patient_metabolism__mt_nerve_conduction_study_decreasedSNAP',
'patient_metabolism__mt_nerve_conduction_study_increasedFwaveLatency',
'patient_metabolism__mt_muscle_biopsy',
'patient_metabolism__mt_Any_other_investigations',
'patient_metabolism__mt_blood_gas_metabolism_acidosis',
'patient_metabolism__mt_blood_gas_metabolism_acidosis_PH',
'patient_metabolism__mt_blood_gas_metabolism_acidosis_HCO_3',
'patient_metabolism__mt_blood_gas_metabolism_acidosis_Anion_gap',
'patient_metabolism__mt_metabolic_alkalosis',
'patient_metabolism__mt_Hyper_ammonemia',
'patient_metabolism__mt_Hyper_ammonemia_value',
'patient_metabolism__mt_Hyper_ammonemia_duration',
'patient_metabolism__mt_high_lactate',
'patient_metabolism__mt_high_lactate_value',
'patient_metabolism__mt_high_lactate_csf',
'patient_metabolism__mt_high_lactate_csf_value',
'patient_metabolism__mt_ief_transferring_pattern_type',
'patient_metabolism__mt_ief_transferring_pattern_type_tpye1',
'patient_metabolism__mt_ief_transferring_pattern_type_tpye2',
'patient_metabolism__mt_urine_ketones',
'patient_metabolism__mt_urine_ketones_value',
'patient_metabolism__mt_plasma_ketones',
'patient_metabolism__mt_plasma_ketones_value',
'patient_metabolism__mt_plasma_ketones_ffa_ratio',
'patient_metabolism__mt_plasma_ketones_ffa_ratio_value',
'patient_metabolism__mt_hplc',
'patient_metabolism__mt_hplc_specify',
'patient_metabolism__mt_hplc_value',
'patient_metabolism__mt_tms_primary_analyte',
'patient_metabolism__mt_tms_primary_analyte_specify_anlyte',
'patient_metabolism__mt_tms_primary_analyte_value',
'patient_metabolism__mt_gcms',
'patient_metabolism__mt_gcms_abnormal_specify',
'patient_metabolism__mt_gcms_abnormal_value',
'patient_metabolism__mt_orotic_acid',
'patient_metabolism__mt_vlcfa',
'patient_metabolism__mt_vlcfa_abnormal_specify',
'patient_metabolism__mt_succinyl_acetone_status',
'patient_metabolism__mt_succinyl_acetone_abnormal_specify',
'patient_metabolism__mt_csf',
'patient_metabolism__mt_csf_amino_acid',
'patient_metabolism__mt_csf_glucose',
'patient_metabolism__mt_csf_lactose',
'patient_metabolism__mt_csf_protien',
'patient_metabolism__mt_csf_nurotransonitres',
'patient_metabolism__mt_csf_porphyrins',
'patient_metabolism__mt_csf_purine',
'patient_metabolism__mt_csf_pyrinidies',
'patient_metabolism__mt_csf_glycine',
'patient_metabolism__mt_csf_others',
'patient_metabolism__mt_enzyme_analusis',
'patient_metabolism__mt_enzyme_analusis_ref_range',
'patient_metabolism__mt_enzyme_analusis_lab_name',
'patient_metabolism__mt_enzyme_analusis_normal_control',
'patient_metabolism__mt_enzyme_analusis_normal_range',
'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood',
'patient_metabolism__mt_enzyme_analusis_upload_report',
'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood_date',
'patient_metabolism__mt_Causative_DNA_sequence_variat',
'patient_metabolism__mt_molecular_upload',
'patient_metabolism__mt_Gene_molecula',
'patient_metabolism__mt_trans_molecul',
'patient_metabolism__mt_mul_dna1',
'patient_metabolism__mt_mul_pro1',
'patient_metabolism__mt_mul_var1',
'patient_metabolism__mt_mul_var_cla1',
'patient_metabolism__mt_mul_zygo1',
'patient_metabolism__mt_mul_dna2',
'patient_metabolism__mt_mul_pro2',
'patient_metabolism__mt_mul_var2',
'patient_metabolism__mt_mul_var_cla2',
'patient_metabolism__mt_mul_zygo2',
'patient_metabolism__mt_mul_seg',
'patient_metabolism__mt_father',
'patient_metabolism__mt_mother',
'patient_metabolism__mt_special_diet',
'patient_metabolism__mt_dietary_managment_1',
'patient_metabolism__mt_dietary_managment_2',
'patient_metabolism__mt_dietary_managment_3',
'patient_metabolism__mt_dietary_managment_4',
'patient_metabolism__mt_dietary_managment_type_of_diet_1',
'patient_metabolism__mt_dietary_managment_type_of_diet_2',
'patient_metabolism__mt_dietary_managment_type_of_diet_3',
'patient_metabolism__mt_dietary_managment_type_of_diet_4',
'patient_metabolism__mt_dietary_managment_type_of_diet_5',
'patient_metabolism__mt_dietary_managment_type_of_diet_6',
'patient_metabolism__mt_liver_transplantation',
'patient_metabolism__mt_kidney_transplantation',
'patient_metabolism__mt_heart_transplantation',
'patient_metabolism__mt_lung_transplantation',
'patient_metabolism__mt_calcium_multivitamin_supplements',
'patient_metabolism__mt_regular_physiotherapy',
'patient_metabolism__mt_any_ocular_medication',
'patient_metabolism__mt_CPAP_BiPAP_sleep_apnea',
'patient_metabolism__mt_any_other_specify',
'patient_metabolism__mt_any_other_special_drug',
'patient_metabolism__mt_any_other_special_drug_1',
'patient_metabolism__mt_any_other_special_drug_2',
'patient_metabolism__mt_any_other_special_drug_3',
'patient_metabolism__mt_any_other_special_drug_4',
'patient_metabolism__mt_any_other_special_drug_5',
'patient_metabolism__mt_any_other_special_drug_6',
'patient_metabolism__mt_any_other_special_drug_7',
'patient_metabolism__mt_any_other_special_drug_8',
'patient_metabolism__mt_any_other_special_drug_9',
'patient_metabolism__mt_any_other_special_drug_10',
'patient_metabolism__mt_any_other_special_drug_11',
'patient_metabolism__mt_any_other_special_drug_12',
'patient_metabolism__mt_any_other_special_drug_13',
'patient_metabolism__mt_any_other_special_drug_14',
'patient_metabolism__mt_any_other_special_drug_specify',
'patient_metabolism__mt_Final_Diagnosis',
'patient_metabolism__organic_cat',
'patient_metabolism__organic_cat_other',
'patient_metabolism__aminoacidpathies_cat',
'patient_metabolism__aminoacidpathies_cat_BCAA',
'patient_metabolism__aminoacidpathies_cat_other',
'patient_metabolism__urea_cat',
'patient_metabolism__urea_cat_NAGS',
'patient_metabolism__vitamin_cat',
'patient_metabolism__vitamin_cobalamin',
'patient_metabolism__vitamin_folate',
'patient_metabolism__vitamin_biotin',
'patient_metabolism__vitamin_pyridoxine',
'patient_metabolism__vitamin_other',
'patient_metabolism__fatty_cat',
'patient_metabolism__fatty_cat_other',
'patient_metabolism__metal_cat',
'patient_metabolism__metal_cat_other',
'patient_metabolism__carbohydrate_cat',
'patient_metabolism__Carbohydrate_sub3',
'patient_metabolism__Congenital_disorder',
'patient_metabolism__Peroxisomal_disorder_specify',
'patient_metabolism__mitochondrial_cat',
'patient_metabolism__mitochondrial_nuclear',
'patient_metabolism__mitochondrial_mitochondrial',
'patient_metabolism__mitochondrial_other',
'patient_metabolism__Neurotransmitter_cat',
'patient_metabolism__Neurotransmitter_pterin',
'patient_metabolism__Neurotransmitter_tyrosine',
'patient_metabolism__Neurotransmitter_other',
'patient_metabolism__mt_diag_other',
'patient_metabolism__mt_Final_Outcome',
'patient_metabolism__mt_death_cause',
'patient_metabolism__mt_age_timedeath',
'patient_metabolism__mt_filled_by_deo_name',
'patient_metabolism__mt_clinician_name',
'patient_metabolism__mt_date_filled',
)
    for user in users:
        writer.writerow(user)

    return response




@login_required(login_url='login')
def update_qa_qc_iem(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_metabolism.objects.get(id=pk)
    form2 = QAmetabolismForm(instance=patient)

    if request.method == 'POST':
        form2 = QAmetabolismForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_mt_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_iem.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_iem.html', context)


@login_required(login_url='login')
def view_qa_qc_iem(request, pk):
    user = request.user
    patient = profile_metabolism.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
