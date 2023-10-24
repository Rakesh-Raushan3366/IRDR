import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


# Create your views here.


@login_required(login_url='login')
def add_record_th(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = ProfilethalasemiaForm()
    if request.method == 'POST':
        form1 = ProfilethalasemiaForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()

            return HttpResponseRedirect(reverse(demographic_th, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_th.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_th.html', context)


@login_required(login_url='login')
def update_patient_record_th(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_thalassemia.objects.get(id=pk)
    form1 = ProfilethalasemiaForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfilethalasemiaForm(request.POST, request.FILES, instance=patient)
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()

            return redirect('total_record_th')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_th.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_th.html', context)


@login_required(login_url='login')
def view_profile_th(request, pk):
    try:
        form1 = profile_thalassemia.objects.get(id=pk)

    except:
        form1 = None

    context = {'form1': form1, }
    return render(request, 'view_profile_th.html', context)


@login_required(login_url='login')
def demographic_th(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    profile = profile_thalassemia.objects.get(id=pk)
    form1 = SocioDemographicDetailsthForm()
    if request.method == 'POST':
        form1 = SocioDemographicDetailsthForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.patient = profile
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_th, args=(pk,)))

        else:
            context = {'form1': form1, }
            return render(request, 'demographic_th.html', context)

    context = {'form1': form1, }
    return render(request, 'demographic_th.html', context)


@login_required(login_url='login')
def update_record_th(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_thalassemia.objects.get(id=pk)

    try:

        socio = demographic_thalassemia.objects.get(patient=patient)

        form1 = SocioDemographicDetailsthForm(instance=socio)

        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsthForm(request.POST, request.FILES, instance=socio)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect("total_record_th")
            else:
                context = {'form1': form1,'patient': pat, }
                return render(request, 'update_record_th.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsthForm(request.POST, request.FILES, instance=socio)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_th")
            else:
                context = {'form1': form1,'patient': patient,  }
                return render(request, 'update_record_th.html', context)

        if request.method == 'POST' and 'save' in request.POST:
            form1 = SocioDemographicDetailsthForm(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                # patient.complete = 'Yes'
                # patient.save()
            else:
                context = {'form1': form1, 'patient': pat, }
                return render(request, 'update_record_th.html', context)
    except:

        form1 = SocioDemographicDetailsthForm()

        if request.method == 'POST':
            form1 = SocioDemographicDetailsthForm(request.POST, request.FILES)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()

                return redirect('total_record_th')

            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_th.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_th.html', context)


@login_required(login_url='login')
def view_record_th(request, pk):
    patient = profile_thalassemia.objects.get(id=pk)
    try:
        form1 = demographic_thalassemia.objects.get(patient=patient)
    except:
        form1 = None

    context = {'form1': form1,'patient': patient, }
    return render(request, 'view_record_th.html', context)


@login_required(login_url='login')
def delete_record_th(request, pk):
    order = profile_thalassemia.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_th')

    context = {'order': order}
    return render(request, 'delete_record_th.html', context)


@login_required(login_url='login')
def total_record_th(request):
    pat = profile_thalassemia.objects.filter(user=request.user)
    date1 = None
    date2 = None

    context = {'patient': pat, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_th.html', context)


@login_required(login_url='login')
def total_record_th_admin(request):
    pat = profile_thalassemia.objects.all()
    date1 = None
    date2 = None

    context = {'patient': pat, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_th_admin.html', context)


def export_thalassemia_csv_user(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="thalassemia.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'th_final_diagnosis', 'th_date_record', 'date_clinical_examination', 'th_date_of_birth', 'th_patient_name', 'th_father_name',
         'th_mother_name', 'th_patient_adhaar_no', 'th_paitent_id',
         'th_patient_id_no', 'th_father_adhaar_no', 'th_father_id', 'th_father_id_no', 'th_permanent_addr', 'th_state', 'th_district', 'th_city_name', 'th_country_name', 'th_land_line_no', 'th_mother_mobile_no',
         'th_father_mobile_no', 'th_email', 'th_religion', 'th_religion_other_specify', 'th_caste', 'th_caste_other_specify', 'th_gender', 'th_referred_status', 'th_referred_by', 'th_referred_by_desc',
         'th_consent_given', 'th_consent_upload', 'th_assent_given', 'th_assent_upload', 'th_hospital_name', 'th_hospital_reg_no', 'th_nationality', 'th_patient_edu_status', 'th_patient_occupation',
         'th_father_edu_status', 'th_father_occupation', 'th_mother_edu_status', 'th_mother_occupation', 'th_monthly_income_status', 'th_tribal', 'th_non_tribal_caste', 'th_diagnosis_type', 'th_diagonosis_other_specify',
         'th_presentation_age', 'th_diagnosis_age', 'th_pres_feature', 'th_pres_pallor', 'th_pres_yellowness', 'th_pres_rec_fever', 'th_pres_dist_abd', 'th_pres_lethargy', 'th_pres_fatigue', 'th_curr_child_age',
         'th_consanguinity', 'th_sibling_aff', 'th_other_family_mem', 'th_other_family_mem_details', 'th_pedigree_upload', 'th_f_fatigue', 'th_f_dyspnoea', 'th_f_rec_fever', 'th_f_abdominal_pain', 'th_f_chest_pain',
         'th_f_bone_joint_pain', 'th_f_any_other', 'th_f_any_other_specify', 'th_f_past_hist', 'th_crisis_num', 'th_crisis_num_last_12', 'th_acute_chest_syndrome', 'th_crisis_hyperhemolyitc',
         'th_crisis_pain_pr_yr_before_hydoxyurea', 'th_crisis_pain_pr_yr_before_hydoxyurea', 'th_crisis_pain_pr_yr_after_hydoxyurea', 'th_other_illness', 'th_other_illness_name', 'th_other_illness_age',
         'th_other_illness_dur', 'th_height', 'th_height_z_score', 'th_weight', 'th_weight_z_score', 'th_hemolytic_facies', 'th_pallor', 'th_jaundice', 'th_edema', 'th_leg_ulcers', 'th_hepatomegaly', 'th_splenomegaly',
         'th_any_systematic_anom', 'th_any_sys_ab_specify', 'th_neurological_abnor', 'th_neurological_abnor_option', 'th_neurological_abnor_option_other', 'th_renal_involvement', 'th_renal_involvement_opts',
         'th_renal_involvement_opts_other', 'th_feet_swelling', 'th_clin_leg_ulcers', 'th_clin_gallstones', 'th_iron_overload_yes_no', 'th_iron_overload_cardiac', 'th_iron_overload_Endocrine', 'th_iron_overload_Growth',
         'th_hist_infection', 'th_hist_infection_opt', 'th_hist_infection_opt_other_specify', 'th_haem_wbc', 'th_haem_hb', 'th_haem_mcv', 'th_haem_mch', 'th_haem_mchc', 'th_haem_rbc_count', 'th_haem_rdw_per',
         'th_haem_plts', 'th_haem_plts', 'th_haem_retic_count', 'th_haem_hba', 'th_haem_hbf', 'th_haem_hba2', 'th_haem_hbf', 'th_red_cell_morphology', 'th_red_cell_morphology_other_specify', 'th_haem_unstable_haem',
         'th_haem_var_hb', 'th_haem_var_hb_hbs', 'th_haem_var_hb_hbe', 'th_haem_var_hb_hbd', 'th_haem_var_hb_other_per', 'th_haem_var_hb_retention_time', 'th_mol_alpha_thal', 'th_mol_alpha_thal_opt', 'th_haem_hbh_incl',
         'th_mol_hbh_thal_opt', 'th_mol_alpha_thal_opt_other', 'th_mol_beta_thal', 'th_mol_beta_thal_opt_1', 'th_mol_beta_thal_opt_2', 'th_mol_beta_thal_opt_3', 'th_mol_beta_thal_opt_4', 'th_mol_beta_thal_opt_5',
         'th_mol_beta_thal_opt_6', 'th_mol_beta_thal_opt_7', 'th_mol_beta_thal_opt_8', 'th_mol_beta_thal_other_spec', 'th_mol_interpretaion', 'th_HPFH_test', 'th_HPFH_test_result', 'th_mol_alpha_beta_test',
         'th_mol_alpha_beta_test_result', 'th_curr_invest_date', 'th_curr_pretasnsfusion', 'th_curr_post_transfusion', 'th_curr_hiv', 'th_curr_hbsag', 'th_curr_hcv', 'th_treat_recieved', 'th_bio_serum_ferritin',
         'th_bio_serum_dehyd', 'th_bio_vitamin_b12', 'th_bio_folate_levels', 'th_bio_ser_bilirubin', 'th_bio_alan_amino', 'th_bio_ser_alkline', 'th_bio_ser_calc', 'th_bio_ser_calc_ionized', 'th_bio_ser_phosp',
         'th_bio_s_creatinine', 'th_bio_t4', 'th_bio_tsh', 'th_bio_s_cortisol_early', 'th_bio_s_cortisol_stimulates', 'th_bio_blood_sugar_fast', 'th_bio_blood_sugar_post_meal', 'th_ecg', 'th_ECHOcardiography',
         'th_Any_other', 'th_bone_marrow_treat', 'th_bmt_done_outcome', 'th_hyper_trans_therapy', 'th_inter_transfusion', 'th_splenectomy', 'th_splenectomy_age', 'th_diagnosis_age1', 'th_transfusion',
         'th_transfusion_age', 'th_transfusion_frequency', 'th_hydroxyurea', 'th_hydroxyurea_dose', 'th_hydroxyurea_duration', 'th_pre_hydroxyurea_hb', 'th_post_hydroxyurea_hb', 'th_pre_hydroxyurea_trans',
         'th_post_hydroxyurea_trans', 'th_hydroxyurea_pain', 'th_any_other_disease', 'th_any_other_disease_detail', 'th_chelation_status', 'th_deferasirox_dose', 'th_deferasirox_dose_other_specify',
         'th_deferiprone_dose', 'th_any_other_disease_dur', 'th_other_medication', 'th_final_diagnosis', 'th_f_diag_other_specify', 'th_comp_iron_overload_beta_thalassemia_detail', 'th_comp_iron_overload',
         'th_comp_iron_overload_detail', 'th_impr_mngt', 'th_filled_by_deo_name', 'th_filled_by_name', 'th_filled_date', ])

    users = profile_thalassemia.objects.filter(user=request.user).prefetch_related('patient_thalassemia').values_list('register_id__institute_name', 'uniqueId', 'th_icmr_unique_no', 'th_final_diagnosis',
                                                                                                                      'th_date_record', 'date_clinical_examination',
                                                                                                                      'th_date_of_birth', 'th_patient_name', 'th_father_name', 'th_mother_name',
                                                                                                                      'th_patient_adhaar_no', 'th_paitent_id', 'th_patient_id_no', 'th_father_adhaar_no', 'th_father_id',
                                                                                                                      'th_father_id_no', 'th_permanent_addr', 'th_state__name', 'th_district__name', 'th_city_name',
                                                                                                                      'th_country_name', 'th_land_line_no', 'th_mother_mobile_no', 'th_father_mobile_no', 'th_email',
                                                                                                                      'th_religion', 'th_religion_other_specify', 'th_caste', 'th_caste_other_specify', 'th_gender',
                                                                                                                      'th_referred_status', 'th_referred_by', 'th_referred_by_desc', 'th_consent_given',
                                                                                                                      'th_consent_upload', 'th_assent_given', 'th_assent_upload', 'th_hospital_name', 'th_hospital_reg_no',
                                                                                                                      'th_nationality', 'patient_thalassemia__th_patient_edu_status',
                                                                                                                      'patient_thalassemia__th_patient_occupation', 'patient_thalassemia__th_father_edu_status',
                                                                                                                      'patient_thalassemia__th_father_occupation', 'patient_thalassemia__th_mother_edu_status',
                                                                                                                      'patient_thalassemia__th_mother_occupation', 'patient_thalassemia__th_monthly_income_status',
                                                                                                                      'patient_thalassemia__th_tribal', 'patient_thalassemia__th_non_tribal_caste',
                                                                                                                      'patient_thalassemia__th_diagnosis_type', 'patient_thalassemia__th_diagonosis_other_specify',
                                                                                                                      'patient_thalassemia__th_presentation_age', 'patient_thalassemia__th_diagnosis_age',
                                                                                                                      'patient_thalassemia__th_pres_feature', 'patient_thalassemia__th_pres_pallor',
                                                                                                                      'patient_thalassemia__th_pres_yellowness', 'patient_thalassemia__th_pres_rec_fever',
                                                                                                                      'patient_thalassemia__th_pres_dist_abd', 'patient_thalassemia__th_pres_lethargy',
                                                                                                                      'patient_thalassemia__th_pres_fatigue', 'patient_thalassemia__th_curr_child_age',
                                                                                                                      'patient_thalassemia__th_consanguinity', 'patient_thalassemia__th_sibling_aff',
                                                                                                                      'patient_thalassemia__th_other_family_mem', 'patient_thalassemia__th_other_family_mem_details',
                                                                                                                      'patient_thalassemia__th_pedigree_upload', 'patient_thalassemia__th_f_fatigue',
                                                                                                                      'patient_thalassemia__th_f_dyspnoea', 'patient_thalassemia__th_f_rec_fever',
                                                                                                                      'patient_thalassemia__th_f_abdominal_pain', 'patient_thalassemia__th_f_chest_pain',
                                                                                                                      'patient_thalassemia__th_f_bone_joint_pain', 'patient_thalassemia__th_f_any_other',
                                                                                                                      'patient_thalassemia__th_f_any_other_specify', 'patient_thalassemia__th_f_past_hist',
                                                                                                                      'patient_thalassemia__th_crisis_num', 'patient_thalassemia__th_crisis_num_last_12',
                                                                                                                      'patient_thalassemia__th_acute_chest_syndrome', 'patient_thalassemia__th_crisis_hyperhemolyitc',
                                                                                                                      'patient_thalassemia__th_crisis_pain_pr_yr_before_hydoxyurea',
                                                                                                                      'patient_thalassemia__th_crisis_pain_pr_yr_before_hydoxyurea',
                                                                                                                      'patient_thalassemia__th_crisis_pain_pr_yr_after_hydoxyurea', 'patient_thalassemia__th_other_illness',
                                                                                                                      'patient_thalassemia__th_other_illness_name', 'patient_thalassemia__th_other_illness_age',
                                                                                                                      'patient_thalassemia__th_other_illness_dur', 'patient_thalassemia__th_height',
                                                                                                                      'patient_thalassemia__th_height_z_score', 'patient_thalassemia__th_weight',
                                                                                                                      'patient_thalassemia__th_weight_z_score', 'patient_thalassemia__th_hemolytic_facies',
                                                                                                                      'patient_thalassemia__th_pallor', 'patient_thalassemia__th_jaundice', 'patient_thalassemia__th_edema',
                                                                                                                      'patient_thalassemia__th_leg_ulcers', 'patient_thalassemia__th_hepatomegaly',
                                                                                                                      'patient_thalassemia__th_splenomegaly', 'patient_thalassemia__th_any_systematic_anom',
                                                                                                                      'patient_thalassemia__th_any_sys_ab_specify', 'patient_thalassemia__th_neurological_abnor',
                                                                                                                      'patient_thalassemia__th_neurological_abnor_option',
                                                                                                                      'patient_thalassemia__th_neurological_abnor_option_other',
                                                                                                                      'patient_thalassemia__th_renal_involvement', 'patient_thalassemia__th_renal_involvement_opts',
                                                                                                                      'patient_thalassemia__th_renal_involvement_opts_other', 'patient_thalassemia__th_feet_swelling',
                                                                                                                      'patient_thalassemia__th_clin_leg_ulcers', 'patient_thalassemia__th_clin_gallstones',
                                                                                                                      'patient_thalassemia__th_iron_overload_yes_no', 'patient_thalassemia__th_iron_overload_cardiac',
                                                                                                                      'patient_thalassemia__th_iron_overload_Endocrine', 'patient_thalassemia__th_iron_overload_Growth',
                                                                                                                      'patient_thalassemia__th_hist_infection', 'patient_thalassemia__th_hist_infection_opt',
                                                                                                                      'patient_thalassemia__th_hist_infection_opt_other_specify', 'patient_thalassemia__th_haem_wbc',
                                                                                                                      'patient_thalassemia__th_haem_hb', 'patient_thalassemia__th_haem_mcv',
                                                                                                                      'patient_thalassemia__th_haem_mch', 'patient_thalassemia__th_haem_mchc',
                                                                                                                      'patient_thalassemia__th_haem_rbc_count', 'patient_thalassemia__th_haem_rdw_per',
                                                                                                                      'patient_thalassemia__th_haem_plts', 'patient_thalassemia__th_haem_plts',
                                                                                                                      'patient_thalassemia__th_haem_retic_count', 'patient_thalassemia__th_haem_hba',
                                                                                                                      'patient_thalassemia__th_haem_hbf', 'patient_thalassemia__th_haem_hba2',
                                                                                                                      'patient_thalassemia__th_haem_hbf', 'patient_thalassemia__th_red_cell_morphology',
                                                                                                                      'patient_thalassemia__th_red_cell_morphology_other_specify',
                                                                                                                      'patient_thalassemia__th_haem_unstable_haem', 'patient_thalassemia__th_haem_var_hb',
                                                                                                                      'patient_thalassemia__th_haem_var_hb_hbs', 'patient_thalassemia__th_haem_var_hb_hbe',
                                                                                                                      'patient_thalassemia__th_haem_var_hb_hbd', 'patient_thalassemia__th_haem_var_hb_other_per',
                                                                                                                      'patient_thalassemia__th_haem_var_hb_retention_time', 'patient_thalassemia__th_mol_alpha_thal',
                                                                                                                      'patient_thalassemia__th_mol_alpha_thal_opt', 'patient_thalassemia__th_haem_hbh_incl',
                                                                                                                      'patient_thalassemia__th_mol_hbh_thal_opt', 'patient_thalassemia__th_mol_alpha_thal_opt_other',
                                                                                                                      'patient_thalassemia__th_mol_beta_thal', 'patient_thalassemia__th_mol_beta_thal_opt_1',
                                                                                                                      'patient_thalassemia__th_mol_beta_thal_opt_2', 'patient_thalassemia__th_mol_beta_thal_opt_3',
                                                                                                                      'patient_thalassemia__th_mol_beta_thal_opt_4', 'patient_thalassemia__th_mol_beta_thal_opt_5',
                                                                                                                      'patient_thalassemia__th_mol_beta_thal_opt_6', 'patient_thalassemia__th_mol_beta_thal_opt_7',
                                                                                                                      'patient_thalassemia__th_mol_beta_thal_opt_8', 'patient_thalassemia__th_mol_beta_thal_other_spec',
                                                                                                                      'patient_thalassemia__th_mol_interpretaion', 'patient_thalassemia__th_HPFH_test',
                                                                                                                      'patient_thalassemia__th_HPFH_test_result', 'patient_thalassemia__th_mol_alpha_beta_test',
                                                                                                                      'patient_thalassemia__th_mol_alpha_beta_test_result', 'patient_thalassemia__th_curr_invest_date',
                                                                                                                      'patient_thalassemia__th_curr_pretasnsfusion', 'patient_thalassemia__th_curr_post_transfusion',
                                                                                                                      'patient_thalassemia__th_curr_hiv', 'patient_thalassemia__th_curr_hbsag',
                                                                                                                      'patient_thalassemia__th_curr_hcv', 'patient_thalassemia__th_treat_recieved',
                                                                                                                      'patient_thalassemia__th_bio_serum_ferritin', 'patient_thalassemia__th_bio_serum_dehyd',
                                                                                                                      'patient_thalassemia__th_bio_vitamin_b12', 'patient_thalassemia__th_bio_folate_levels',
                                                                                                                      'patient_thalassemia__th_bio_ser_bilirubin', 'patient_thalassemia__th_bio_alan_amino',
                                                                                                                      'patient_thalassemia__th_bio_ser_alkline', 'patient_thalassemia__th_bio_ser_calc',
                                                                                                                      'patient_thalassemia__th_bio_ser_calc_ionized', 'patient_thalassemia__th_bio_ser_phosp',
                                                                                                                      'patient_thalassemia__th_bio_s_creatinine', 'patient_thalassemia__th_bio_t4',
                                                                                                                      'patient_thalassemia__th_bio_tsh', 'patient_thalassemia__th_bio_s_cortisol_early',
                                                                                                                      'patient_thalassemia__th_bio_s_cortisol_stimulates', 'patient_thalassemia__th_bio_blood_sugar_fast',
                                                                                                                      'patient_thalassemia__th_bio_blood_sugar_post_meal', 'patient_thalassemia__th_ecg',
                                                                                                                      'patient_thalassemia__th_ECHOcardiography', 'patient_thalassemia__th_Any_other',
                                                                                                                      'patient_thalassemia__th_bone_marrow_treat', 'patient_thalassemia__th_bmt_done_outcome',
                                                                                                                      'patient_thalassemia__th_hyper_trans_therapy', 'patient_thalassemia__th_inter_transfusion',
                                                                                                                      'patient_thalassemia__th_splenectomy', 'patient_thalassemia__th_splenectomy_age',
                                                                                                                      'patient_thalassemia__th_diagnosis_age1', 'patient_thalassemia__th_transfusion',
                                                                                                                      'patient_thalassemia__th_transfusion_age', 'patient_thalassemia__th_transfusion_frequency',
                                                                                                                      'patient_thalassemia__th_hydroxyurea', 'patient_thalassemia__th_hydroxyurea_dose',
                                                                                                                      'patient_thalassemia__th_hydroxyurea_duration', 'patient_thalassemia__th_pre_hydroxyurea_hb',
                                                                                                                      'patient_thalassemia__th_post_hydroxyurea_hb', 'patient_thalassemia__th_pre_hydroxyurea_trans',
                                                                                                                      'patient_thalassemia__th_post_hydroxyurea_trans', 'patient_thalassemia__th_hydroxyurea_pain',
                                                                                                                      'patient_thalassemia__th_any_other_disease', 'patient_thalassemia__th_any_other_disease_detail',
                                                                                                                      'patient_thalassemia__th_chelation_status', 'patient_thalassemia__th_deferasirox_dose',
                                                                                                                      'patient_thalassemia__th_deferasirox_dose_other_specify', 'patient_thalassemia__th_deferiprone_dose',
                                                                                                                      'patient_thalassemia__th_any_other_disease_dur', 'patient_thalassemia__th_other_medication',
                                                                                                                      'patient_thalassemia__th_final_diagnosis', 'patient_thalassemia__th_f_diag_other_specify',
                                                                                                                      'patient_thalassemia__th_comp_iron_overload_beta_thalassemia_detail',
                                                                                                                      'patient_thalassemia__th_comp_iron_overload', 'patient_thalassemia__th_comp_iron_overload_detail',
                                                                                                                      'patient_thalassemia__th_impr_mngt', 'patient_thalassemia__th_filled_by_deo_name',
                                                                                                                      'patient_thalassemia__th_filled_by_name', 'patient_thalassemia__th_filled_date', )
    for user in users:
        writer.writerow(user)

    return response





@login_required(login_url='login')
def update_qa_qc_thalasemia(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_thalassemia.objects.get(id=pk)
    form2 = QATHForm(instance=patient)

    if request.method == 'POST':
        form2 = QATHForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_th_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_thalasemia.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_thalasemia.html', context)



@login_required(login_url='login')
def view_qa_qc_thalasemia(request, pk):
    user = request.user
    patient = profile_thalassemia.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")

