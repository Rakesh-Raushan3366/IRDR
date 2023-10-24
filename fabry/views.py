import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


@login_required(login_url='login')
def add_record_fb(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = ProfilefabridiseaseForm()
    if request.method == 'POST':
        form1 = ProfilefabridiseaseForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(demographic_fb, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_fb.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_fb.html', context)


@login_required(login_url='login')
def update_patient_record_fb(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_fabry.objects.get(id=pk)
    form1 = ProfilefabridiseaseForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfilefabridiseaseForm(request.POST, request.FILES, instance=patient)
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()

            return redirect('total_record_fb')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_fb.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_fb.html', context)


@login_required(login_url='login')
def view_profile_fb(request, pk):
    try:
        form1 = profile_fabry.objects.get(id=pk)

    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_fb.html', context)


@login_required(login_url='login')
def demographic_fb(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_fabry.objects.get(id=pk)
    form1 = SocioDemographicDetailsFormfb()
    if request.method == 'POST':
        form1 = SocioDemographicDetailsFormfb(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.patient = patient
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_fb, args=(pk,)))
        else:
            context = {'form1': form1, }
            return render(request, 'demographic_fb.html', context)

    context = {'form1': form1, }
    return render(request, 'demographic_fb.html', context)


@login_required(login_url='login')
def delete_record_fb(request, pk):
    order = profile_fabry.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_fb')

    context = {'order': order}
    return render(request, 'delete_record_fb.html', context)


@login_required(login_url='login')
def view_record_fb(request, pk):
    patient = profile_fabry.objects.get(id=pk)
    try:
        form1 = demographic_fabry.objects.get(patient=patient)

    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_record_fb.html', context)


@login_required(login_url='login')
def update_record_fb(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_fabry.objects.get(id=pk)
    try:
        socio = demographic_fabry.objects.get(patient=patient)
        form1 = SocioDemographicDetailsFormfb(instance=socio)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsFormfb(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'

                patient.save()
                return redirect("total_record_fb")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_fb.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsFormfb(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_fb")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_fb.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = SocioDemographicDetailsFormfb(request.POST, request.FILES, instance=socio)
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
                    return render(request, 'update_record_fb.html', context)
    except:
        form1 = SocioDemographicDetailsFormfb()
        if request.method == 'POST':
            form1 = SocioDemographicDetailsFormfb(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                return redirect('total_record_fb')
            else:
                context = {'form1': form1,'patient': patient }
                return render(request, 'update_record_fb.html', context)

    context = {'form1': form1, 'patient': patient}
    return render(request, 'update_record_fb.html', context)


@login_required(login_url='login')
def total_record_fb(request):
    pat = profile_fabry.objects.filter(user=request.user).order_by('fb_date_created')
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_fb.html', context)


@login_required(login_url='login')
def total_record_fb_admin(request):
    pat = profile_fabry.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_fb_admin.html', context)


def export_fabry_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fabry.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_fabry__fb_final_diagnosis',
         'patient_fabry__fb_date_of_record', 'patient_fabry__fb_clinical_exam_date', 'patient_fabry__fb_date_of_birth',
         'patient_fabry__fb_patient_name', 'patient_fabry__fb_father_name',
         'patient_fabry__fb_mother_name',
         'patient_fabry__fb_paitent_id', 'patient_fabry__fb_paitent_id_list',
         'patient_fabry__fb_patient_id_no', 'patient_fabry__fb_father_mother_id',
         'patient_fabry__fb_father_mother_id_no', 'patient_fabry__fb_permanent_addr', 'patient_fabry__fb_state',
         'patient_fabry__fb_district',
         'patient_fabry__fb_city_name', 'patient_fabry__fb_country_name', 'patient_fabry__fb_land_line_no',
         'patient_fabry__fb_mother_mobile_no',
         'patient_fabry__fb_father_mobile_no', 'patient_fabry__fb_email', 'patient_fabry__fb_religion',
         'patient_fabry__fb_caste', 'patient_fabry__fb_gender', 'patient_fabry__fb_referred_status',
         'patient_fabry__fb_referred_by', 'patient_fabry__fb_referred_by_desc', 'patient_fabry__fb_consent_given',
         'patient_fabry__fb_consent_upload', 'patient_fabry__fb_assent_given',
         'patient_fabry__fb_assent_upload', 'patient_fabry__fb_hospital_name', 'patient_fabry__fb_hospital_reg_no',
         'patient_fabry__fb_patient_edu_status', 'patient_fabry__fb_patient_occupation',
         'patient_fabry__fb_father_edu_status', 'patient_fabry__fb_father_occupation',
         'patient_fabry__fb_mother_edu_status',
         'patient_fabry__fb_mother_occupation', 'patient_fabry__fb_monthly_income_status',
         'patient_fabry__fb_anth_wght_pat', 'patient_fabry__fb_anth_wght_per', 'patient_fabry__fb_anth_wght_sd',
         'patient_fabry__fb_anth_height_pat', 'patient_fabry__fb_anth_height_per', 'patient_fabry__fb_anth_height_sd',

         'patient_fabry__fb_anth_head_cir_pat',
         'patient_fabry__fb_anth_head_cir_perc', 'patient_fabry__fb_anth_head_cir_sd',
         'patient_fabry__fb_presenting_complaints_years',
         'patient_fabry__fb_presenting_complaints_months',
         'patient_fabry__fb_presenting_complaints_day',
         'patient_fabry__fb_presenting_complaints_intrauterine',

         'patient_fabry__fb_presenting_complaints_age_presentation_years',
         'patient_fabry__fb_presenting_complaints_age_presentation_months',
         'patient_fabry__fb_presenting_complaints_age_presentation_day',
         'patient_fabry__fb_presenting_complaints_age_presentation_intrauterine',

         'patient_fabry__fb_presenting_complaints_age_diagnosis_years',
         'patient_fabry__fb_presenting_complaints_age_diagnosis_months',
         'patient_fabry__fb_presenting_complaints_age_diagnosis_day',
         'patient_fabry__fb_presenting_complaints_age_diagnosis_intrauterine',
         'patient_fabry__fb_onset_age',
         'patient_fabry__fb_pedigree_upload',
         'patient_fabry__fb_fam_hist_status', 'patient_fabry__fb_fam_hist_descr', 'patient_fabry__fb_cons_status',
         'patient_fabry__fb_cons_degree_specify', 'patient_fabry__fb_gi_symtoms', 'patient_fabry__fb_fever',
         'patient_fabry__fb_abdominal_pain', 'patient_fabry__fb_diarrhea', 'patient_fabry__fb_constipation',
         'patient_fabry__fb_nausea', 'patient_fabry__fb_vomiting', 'patient_fabry__fb_irritable_bowel',
         'patient_fabry__fb_acroparesthesia',
         'patient_fabry__fb_neuronopathic_pain', 'patient_fabry__fb_onset_age', 'patient_fabry__fb_hand',
         'patient_fabry__fb_feet', 'patient_fabry__fb_both',
         'patient_fabry__fb_improvement_after_ert', 'patient_fabry__fb_improvement_after_medication',
         'patient_fabry__fb_improvement_after_medication_specify', 'patient_fabry__fb_medication_effect',
         'patient_fabry__fb_angiokeratoma', 'patient_fabry__fb_angiok_onset_age', 'patient_fabry__fb_hypohidrosis',
         'patient_fabry__fb_inter_physical_act', 'patient_fabry__fb_hydro_impro_after_ert',
         'patient_fabry__fb_cardiac_symtoms', 'patient_fabry__fb_myocardial_infarction',
         'patient_fabry__fb_unstable_angina', 'patient_fabry__fb_hypertension', 'patient_fabry__fb_echo',
         'patient_fabry__fb_echo_date',
         'patient_fabry__fb_left_vent_diastolic_dia', 'patient_fabry__fb_left_vent_diastolic_dia_date',
         'patient_fabry__fb_pwt_septum_lvm', 'patient_fabry__fb_left_vent_diastolic_dia_date', 'patient_fabry__fb_co',
         'patient_fabry__fb_co_date', 'patient_fabry__fb_ef_per', 'patient_fabry__fb_ef_per_date',
         'patient_fabry__fb_lvh', 'patient_fabry__fb_lvh_date', 'patient_fabry__fb_mr_tr',
         'patient_fabry__fb_mr_tr_date', 'patient_fabry__fb_lvmi', 'patient_fabry__fb_mr_tr_date',
         'patient_fabry__fb_cardiomyopathy', 'patient_fabry__fb_cardiomyopathy_date',
         'patient_fabry__fb_cardiomyopathy_specify', 'patient_fabry__fb_ecg', 'patient_fabry__fb_ecg_date',
         'patient_fabry__fb_ecg_abnormal_pr_select', 'patient_fabry__fb_any_rhythm_abnormality',
         'patient_fabry__fb_any_rhythm_abnormality_specify',
         'patient_fabry__fb_neropsychiatric_symp', 'patient_fabry__fb_neuropsychiatric_types',
         'patient_fabry__fb_depression_status', 'patient_fabry__fb_stroke', 'patient_fabry__fb_stroke_age',
         'patient_fabry__fb_rec_stroke', 'patient_fabry__fb_trans_isch_attack', 'patient_fabry__fb_visual_prob',
         'patient_fabry__fb_cornea_vertic',
         'patient_fabry__fb_corneal_opacity', 'patient_fabry__fb_hearing_loss', 'patient_fabry__fb_sensory_type',
         'patient_fabry__fb_proteinuria', 'patient_fabry__fb_proteinuria_age_onset',
         'patient_fabry__fb_microalbuminuri', 'patient_fabry__fb_microalbuminuri_date',
         'patient_fabry__fb_microalbuminuri_value',
         'patient_fabry__fb_albumin_creatinine', 'patient_fabry__fb_albumin_creatinine_date',
         'patient_fabry__fb_albumin_creatinine_val', 'patient_fabry__fb_urea_base_line_value',
         'patient_fabry__fb_urea_date',
         'patient_fabry__fb_creatinine_base_value', 'patient_fabry__fb_creatinine_date',
         'patient_fabry__fb_renal_biops',
         'patient_fabry__fb_renal_biops_status', 'patient_fabry__fb_renal_biops_abnorm_specify',
         'patient_fabry__fb_renal_transplant', 'patient_fabry__fb_renal_transplant_specify',
         'patient_fabry__fb_dialysis',
         'patient_fabry__fb_plasma_gl_3_lab_name', 'patient_fabry__fb_plasma_gl_3_date',
         'patient_fabry__fb_plasma_gl_3_value', 'patient_fabry__fb_urine_gl_3_lab_name',
         'patient_fabry__fb_urine_gl_3_date', 'patient_fabry__fb_urine_gl_3_lab_value', 'patient_fabry__fb_mri_brain',
         'patient_fabry__fb_mri_brain_abnormal_spcify', 'patient_fabry__fb_enzyme_assy_lab_name',
         'patient_fabry__fb_enzyme_assy_ref_range', 'patient_fabry__fb_enzyme_assy_report_details',
         'patient_fabry__fb_enzyme_assy_upload_report', 'patient_fabry__fb_mutaion_rep_lab_name',
         'patient_fabry__fb_gene_name', 'patient_fabry__fb_transcript_id',
         'patient_fabry__fb_enzyme_assy1', 'patient_fabry__fb_cDNA_change1',
         'patient_fabry__fb_protein_change1', 'patient_fabry__fb_variant1', 'fb_variant_class1',
         'patient_fabry__fb_enzyme_assy2', 'patient_fabry__fb_cDNA_change2',
         'patient_fabry__fb_protein_change2', 'patient_fabry__fb_variant2', 'fb_variant_class2',
         'patient_fabry__fb_segregation_parents', 'patient_fabry__fb_father', 'patient_fabry__fb_mother',
         'patient_fabry__fb_enzyme_assy_report_details', 'patient_fabry__fb_enzyme_assy_cont',
         'patient_fabry__fb_mutaion_rep_lab_name', 'patient_fabry__fb_mutaion_rep_datails',
         'patient_fabry__fb_mutaion_rep_upload_report', 'patient_fabry__fb_ert_status',
         'patient_fabry__fb_ert_initial_date', 'patient_fabry__fb_ert_start_age', 'patient_fabry__fb_ert_dosage',
         'patient_fabry__fb_ert_duration',
         'patient_fabry__fb_adverse_events', 'patient_fabry__fb_adverse_events_specify',
         'patient_fabry__fb_curr_ert_status', 'patient_fabry__fb_any_interuption',
         'patient_fabry__fb_reseason_interrupt',
         'patient_fabry__fb_dur_interrupt', 'patient_fabry__fb_fabri_disease_pain_score',
         'patient_fabry__fb_drugs_recieved',
         'patient_fabry__fb_pain_killers', 'patient_fabry__fb_pain_medication_name',
         'patient_fabry__fb_pain_killers_spcify', 'patient_fabry__fb_ace_inhibitors',
         'patient_fabry__fb_ace_inhibitors_name',
         'patient_fabry__fb_any_other','patient_fabry__fb_treatment', 'patient_fabry__fb_Finaloutcomes', 'patient_fabry__fb_filled_by_deo_name',
         'patient_fabry__fb_clinicial_name',
         'patient_fabry__fb_date'])

    users = profile_fabry.objects.all().prefetch_related('patient_fabry').values_list('register_id__institute_name',
                                                                                      'uniqueId', 'fb_icmr_unique_no',
                                                                                      'fb_final_diagnosis',
                                                                                      'fb_date_of_record',
                                                                                      'fb_clinical_exam_date',
                                                                                      'fb_date_of_birth',
                                                                                      'fb_patient_name',
                                                                                      'fb_father_name',
                                                                                      'fb_mother_name', 'fb_paitent_id',
                                                                                      'fb_paitent_id_list',
                                                                                      'fb_patient_id_no',
                                                                                      'fb_father_mother_id',
                                                                                      'fb_father_mother_id_no',
                                                                                      'fb_permanent_addr',
                                                                                      'fb_state', 'fb_district',
                                                                                      'fb_city_name', 'fb_country_name',
                                                                                      'fb_land_line_no',
                                                                                      'fb_mother_mobile_no',
                                                                                      'fb_father_mobile_no', 'fb_email',
                                                                                      'fb_religion', 'fb_caste',
                                                                                      'fb_gender',
                                                                                      'fb_referred_status',
                                                                                      'fb_referred_by',
                                                                                      'fb_referred_by_desc',
                                                                                      'fb_consent_given',
                                                                                      'fb_consent_upload',
                                                                                      'fb_assent_given',
                                                                                      'fb_assent_upload',
                                                                                      'fb_hospital_name',
                                                                                      'fb_hospital_reg_no',
                                                                                      'patient_fabry__fb_patient_edu_status',
                                                                                      'patient_fabry__fb_patient_occupation',
                                                                                      'patient_fabry__fb_father_edu_status',
                                                                                      'patient_fabry__fb_father_occupation',
                                                                                      'patient_fabry__fb_mother_edu_status',
                                                                                      'patient_fabry__fb_mother_occupation',
                                                                                      'patient_fabry__fb_monthly_income_status',
                                                                                      'patient_fabry__fb_anth_wght_pat',
                                                                                      'patient_fabry__fb_anth_wght_per',
                                                                                      'patient_fabry__fb_anth_wght_sd',
                                                                                      'patient_fabry__fb_anth_height_pat',
                                                                                      'patient_fabry__fb_anth_height_per',
                                                                                      'patient_fabry__fb_anth_height_sd',
                                                                                      'patient_fabry__fb_anth_head_cir_pat',
                                                                                      'patient_fabry__fb_anth_head_cir_perc',
                                                                                      'patient_fabry__fb_anth_head_cir_sd',

                                                                                      'patient_fabry__fb_presenting_complaints_years',
                                                                                      'patient_fabry__fb_presenting_complaints_months',
                                                                                      'patient_fabry__fb_presenting_complaints_day',
                                                                                      'patient_fabry__fb_presenting_complaints_intrauterine',

                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_years',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_months',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_day',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_intrauterine',

                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_years',
                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_months',
                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_day',
                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_intrauterine',

                                                                                      'patient_fabry__fb_onset_age',
                                                                                      'patient_fabry__fb_pedigree_upload',
                                                                                      'patient_fabry__fb_fam_hist_status',
                                                                                      'patient_fabry__fb_fam_hist_descr',
                                                                                      'patient_fabry__fb_cons_status',
                                                                                      'patient_fabry__fb_cons_degree_specify',
                                                                                      'patient_fabry__fb_gi_symtoms',
                                                                                      'patient_fabry__fb_fever',
                                                                                      'patient_fabry__fb_abdominal_pain',
                                                                                      'patient_fabry__fb_diarrhea',
                                                                                      'patient_fabry__fb_constipation',
                                                                                      'patient_fabry__fb_nausea',
                                                                                      'patient_fabry__fb_vomiting',
                                                                                      'patient_fabry__fb_irritable_bowel',
                                                                                      'patient_fabry__fb_acroparesthesia',
                                                                                      'patient_fabry__fb_neuronopathic_pain',
                                                                                      'patient_fabry__fb_onset_age',
                                                                                      'patient_fabry__fb_hand',
                                                                                      'patient_fabry__fb_feet',
                                                                                      'patient_fabry__fb_both',
                                                                                      'patient_fabry__fb_improvement_after_ert',
                                                                                      'patient_fabry__fb_improvement_after_medication',
                                                                                      'patient_fabry__fb_improvement_after_medication_specify',
                                                                                      'patient_fabry__fb_medication_effect',
                                                                                      'patient_fabry__fb_angiokeratoma',
                                                                                      'patient_fabry__fb_angiok_onset_age',
                                                                                      'patient_fabry__fb_hypohidrosis',
                                                                                      'patient_fabry__fb_inter_physical_act',
                                                                                      'patient_fabry__fb_hydro_impro_after_ert',
                                                                                      'patient_fabry__fb_cardiac_symtoms',
                                                                                      'patient_fabry__fb_myocardial_infarction',
                                                                                      'patient_fabry__fb_unstable_angina',
                                                                                      'patient_fabry__fb_hypertension',
                                                                                      'patient_fabry__fb_echo',
                                                                                      'patient_fabry__fb_echo_date',
                                                                                      'patient_fabry__fb_left_vent_diastolic_dia',
                                                                                      'patient_fabry__fb_left_vent_diastolic_dia_date',
                                                                                      'patient_fabry__fb_pwt_septum_lvm',
                                                                                      'patient_fabry__fb_left_vent_diastolic_dia_date',
                                                                                      'patient_fabry__fb_co',
                                                                                      'patient_fabry__fb_co_date',
                                                                                      'patient_fabry__fb_ef_per',
                                                                                      'patient_fabry__fb_ef_per_date',
                                                                                      'patient_fabry__fb_lvh',
                                                                                      'patient_fabry__fb_lvh_date',
                                                                                      'patient_fabry__fb_mr_tr',
                                                                                      'patient_fabry__fb_mr_tr_date',
                                                                                      'patient_fabry__fb_lvmi',
                                                                                      'patient_fabry__fb_mr_tr_date',
                                                                                      'patient_fabry__fb_cardiomyopathy',
                                                                                      'patient_fabry__fb_cardiomyopathy_date',
                                                                                      'patient_fabry__fb_cardiomyopathy_specify',
                                                                                      'patient_fabry__fb_ecg',
                                                                                      'patient_fabry__fb_ecg_date',
                                                                                      'patient_fabry__fb_ecg_abnormal_pr_select',
                                                                                      'patient_fabry__fb_any_rhythm_abnormality',
                                                                                      'patient_fabry__fb_any_rhythm_abnormality_specify',
                                                                                      'patient_fabry__fb_neropsychiatric_symp',
                                                                                      'patient_fabry__fb_neuropsychiatric_types',
                                                                                      'patient_fabry__fb_depression_status',
                                                                                      'patient_fabry__fb_stroke',
                                                                                      'patient_fabry__fb_stroke_age',
                                                                                      'patient_fabry__fb_rec_stroke',
                                                                                      'patient_fabry__fb_trans_isch_attack',
                                                                                      'patient_fabry__fb_visual_prob',
                                                                                      'patient_fabry__fb_cornea_vertic',
                                                                                      'patient_fabry__fb_corneal_opacity',
                                                                                      'patient_fabry__fb_hearing_loss',
                                                                                      'patient_fabry__fb_sensory_type',
                                                                                      'patient_fabry__fb_proteinuria',
                                                                                      'patient_fabry__fb_proteinuria_age_onset',
                                                                                      'patient_fabry__fb_microalbuminuri',
                                                                                      'patient_fabry__fb_microalbuminuri_date',
                                                                                      'patient_fabry__fb_microalbuminuri_value',
                                                                                      'patient_fabry__fb_albumin_creatinine',
                                                                                      'patient_fabry__fb_albumin_creatinine_date',
                                                                                      'patient_fabry__fb_albumin_creatinine_val',
                                                                                      'patient_fabry__fb_urea_base_line_value',
                                                                                      'patient_fabry__fb_urea_date',
                                                                                      'patient_fabry__fb_creatinine_base_value',
                                                                                      'patient_fabry__fb_creatinine_date',
                                                                                      'patient_fabry__fb_renal_biops',
                                                                                      'patient_fabry__fb_renal_biops_status',
                                                                                      'patient_fabry__fb_renal_biops_abnorm_specify',
                                                                                      'patient_fabry__fb_renal_transplant',
                                                                                      'patient_fabry__fb_renal_transplant_specify',
                                                                                      'patient_fabry__fb_dialysis',
                                                                                      'patient_fabry__fb_plasma_gl_3_lab_name',
                                                                                      'patient_fabry__fb_plasma_gl_3_date',
                                                                                      'patient_fabry__fb_plasma_gl_3_value',
                                                                                      'patient_fabry__fb_urine_gl_3_lab_name',
                                                                                      'patient_fabry__fb_urine_gl_3_date',
                                                                                      'patient_fabry__fb_urine_gl_3_lab_value',
                                                                                      'patient_fabry__fb_mri_brain',
                                                                                      'patient_fabry__fb_mri_brain_abnormal_spcify',
                                                                                      'patient_fabry__fb_enzyme_assy_lab_name',
                                                                                      'patient_fabry__fb_enzyme_assy_ref_range',
                                                                                      'patient_fabry__fb_enzyme_assy_report_details',
                                                                                      'patient_fabry__fb_enzyme_assy_upload_report',
                                                                                      'patient_fabry__fb_mutaion_rep_lab_name',

                                                                                      'patient_fabry__fb_gene_name',
                                                                                      'patient_fabry__fb_transcript_id',
                                                                                      'patient_fabry__fb_enzyme_assy1',
                                                                                      'patient_fabry__fb_cDNA_change1',
                                                                                      'patient_fabry__fb_protein_change1',
                                                                                      'patient_fabry__fb_variant1',
                                                                                      'patient_fabry__fb_variant_class1',
                                                                                      'patient_fabry__fb_enzyme_assy2',
                                                                                      'patient_fabry__fb_cDNA_change2',
                                                                                      'patient_fabry__fb_protein_change2',
                                                                                      'patient_fabry__fb_variant2',
                                                                                      'patient_fabry__fb_variant_class2',
                                                                                      'patient_fabry__fb_segregation_parents',
                                                                                      'patient_fabry__fb_father',
                                                                                      'patient_fabry__fb_mother',
                                                                                      'patient_fabry__fb_enzyme_assy_report_details',
                                                                                      'patient_fabry__fb_enzyme_assy_cont',
                                                                                      'patient_fabry__fb_mutaion_rep_lab_name',
                                                                                      'patient_fabry__fb_mutaion_rep_datails',
                                                                                      'patient_fabry__fb_mutaion_rep_upload_report',
                                                                                      'patient_fabry__fb_ert_status',
                                                                                      'patient_fabry__fb_ert_initial_date',
                                                                                      'patient_fabry__fb_ert_start_age',
                                                                                      'patient_fabry__fb_ert_dosage',
                                                                                      'patient_fabry__fb_ert_duration',
                                                                                      'patient_fabry__fb_adverse_events',
                                                                                      'patient_fabry__fb_adverse_events_specify',
                                                                                      'patient_fabry__fb_curr_ert_status',
                                                                                      'patient_fabry__fb_any_interuption',
                                                                                      'patient_fabry__fb_reseason_interrupt',
                                                                                      'patient_fabry__fb_dur_interrupt',
                                                                                      'patient_fabry__fb_fabri_disease_pain_score',
                                                                                      'patient_fabry__fb_drugs_recieved',
                                                                                      'patient_fabry__fb_pain_killers',
                                                                                      'patient_fabry__fb_pain_medication_name',
                                                                                      'patient_fabry__fb_pain_killers_spcify',
                                                                                      'patient_fabry__fb_ace_inhibitors',
                                                                                      'patient_fabry__fb_ace_inhibitors_name',
                                                                                      'patient_fabry__fb_any_other',
                                                                                      'patient_fabry__fb_treatment',
                                                                                      'patient_fabry__fb_Finaloutcomes',
                                                                                      'patient_fabry__fb_filled_by_deo_name',
                                                                                      'patient_fabry__fb_clinicial_name',

                                                                                      'patient_fabry__fb_date',
                                                                                       )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def update_qa_qc_fabry(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_fabry.objects.get(id=pk)
    form2 = QAfabryForm(instance=patient)

    if request.method == 'POST':
        form2 = QAfabryForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_fb_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_fabry.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_fabry.html', context)


@login_required(login_url='login')
def view_qa_qc_fabry(request, pk):
    user = request.user
    patient = profile_fabry.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
