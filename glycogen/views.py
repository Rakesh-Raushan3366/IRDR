from django.shortcuts import render
import csv

# Create your views here.
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse

from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear, ExtractWeekDay, \
    ExtractWeek, TruncMonth, \
    TruncWeek, \
    TruncDay
from collections import OrderedDict

from account.decorators import unauthenticated_user
from .forms import *


@login_required(login_url='login')
def add_record_gl(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = ProfileglycogenForm()
    if request.method == 'POST':
        form1 = ProfileglycogenForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(demographic_gl, args=(auth1,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_gl.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_gl.html', context)


@login_required(login_url='login')
def update_patient_record_gl(request,pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_glycogen.objects.get(id=pk)
    form1 = ProfileglycogenForm( instance=patient)
    if request.method == 'POST':
        form1 = ProfileglycogenForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_gl')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_gl.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_gl.html', context)


def view_profile_gl(request, pk):

    try:
        form1 = profile_glycogen.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_gl.html', context)


@login_required(login_url='login')
def demographic_gl(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_glycogen.objects.get(id=pk)

    form1 = SocioDemographicDetailsFormgl()
    if request.method == 'POST':
        form1 = SocioDemographicDetailsFormgl(request.POST, request.FILES, )

        if form1.is_valid():

            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.patient = patient
            auth1.register = register
            auth1.save()

            return HttpResponseRedirect(reverse(update_record_gl, args=(pk,)))

        else:
            context = {'form1': form1, }
            return render(request, 'demographic_gl.html', context)

    context = {'form1': form1, }
    return render(request, 'demographic_gl.html', context)


@login_required(login_url='login')
def update_record_gl(request, pk):
    user = request.user
    patient = profile_glycogen.objects.get(id=pk)
    register = Register.objects.get(user=request.user)
    try:
        socio = demographic_glycogen.objects.get(patient=patient)
        form1 = SocioDemographicDetailsFormgl(instance=socio)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsFormgl(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect("total_record_gl")
            else:
                context = {'form1': form1, }
                return render(request, 'update_record_gl.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsFormgl(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_gl")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_gl.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = SocioDemographicDetailsFormgl(request.POST, request.FILES, instance=socio)
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
                    return render(request, 'update_record_gl.html', context)
    except:
        form1 = SocioDemographicDetailsFormgl()
        if request.method == 'POST':
            form1 = SocioDemographicDetailsFormgl(request.POST, request.FILES)

            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                return redirect('total_record_gl')
            else:
                context = {'form1': form1,'patient': patient,  }
                return render(request, 'update_record_gl.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_gl.html', context)


@login_required(login_url='login')
def view_record_gl(request, pk):
    patient = profile_glycogen.objects.get(id=pk)
    try:
        form1 = demographic_glycogen.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_record_gl.html', context)


@login_required(login_url='login')
def delete_record_gl(request, pk):
    order = profile_glycogen.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_gl')

    context = {'order': order}
    return render(request, 'delete_record_gl.html', context)


@login_required(login_url='login')
def total_record_gl(request):
    pat = profile_glycogen.objects.filter(user=request.user).order_by('gl_date_created')
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_gl.html', context)


@login_required(login_url='login')
def total_record_gl_admin(request):
    pat = profile_glycogen.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_gl_admin.html', context)


def export_gylcogen_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="glycogen.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'gl_final_dignosis', 'gl_date_of_record', 'gl_clinical_exam_date',
         'gl_date_of_birth',
         'gl_patient_name', 'gl_father_name', 'gl_mother_name', 'gl_paitent_id', 'gl_paitent_id_list',
         'gl_patient_id_no', 'gl_mother_father_id',
         'gl_mother_father_id_no', 'gl_permanent_addr', 'gl_state', 'gl_district', 'gl_city_name', 'gl_country_name',
         'gl_land_line_no',
         'gl_mother_mobile_no', 'gl_father_mobile_no', 'gl_email', 'gl_religion', 'gl_caste', 'gl_gender',
         'gl_referred_status', 'gl_referred_by',
         'gl_referred_by_desc', 'gl_consent_given', 'gl_consent_upload', 'gl_assent_given', 'gl_assent_upload',
         'gl_hospital_name', 'gl_hospital_reg_no',
         'patient_glycogen__gl_patient_edu_status', 'patient_glycogen__gl_patient_occupation',
         'patient_glycogen__gl_father_edu_status', 'patient_glycogen__gl_father_occupation',
         'patient_glycogen__gl_mother_edu_status', 'patient_glycogen__gl_mother_occupation',
         'patient_glycogen__gl_monthly_income_status', 'patient_glycogen__gl_anth_wght_pat',
         'patient_glycogen__gl_anth_wght_per', 'patient_glycogen__gl_anth_wght_sd',

         'patient_glycogen__gl_anth_height_pat',
         'patient_glycogen__gl_anth_height_per', 'patient_glycogen__gl_anth_height_sd',

         'patient_glycogen__gl_anth_head_cir_pat',
         'patient_glycogen__gl_anth_head_cir_perc', 'patient_glycogen__gl_anth_head_cir_sd',

         'patient_glycogen__gl_presenting_complaints_years',
         'patient_glycogen__gl_presenting_complaints_months',
         'patient_glycogen__gl_presenting_complaints_day',
         'patient_glycogen__gl_presenting_complaints_intrauterine',

         'patient_glycogen__gl_presenting_complaints_age_presentation_years',
         'patient_glycogen__gl_presenting_complaints_age_presentation_months',
         'patient_glycogen__gl_presenting_complaints_age_presentation_day',
         'patient_glycogen__gl_presenting_complaints_age_presentation_intrauterine',

         'patient_glycogen__gl_presenting_complaints_age_diagnosis_years',
         'patient_glycogen__gl_presenting_complaints_age_diagnosis_months',
         'patient_glycogen__gl_presenting_complaints_age_diagnosis_day',
         'patient_glycogen__gl_presenting_complaints_age_diagnosis_intrauterine',

         'patient_glycogen__gl_fam_hist_status',
         'patient_glycogen__gl_fam_hist_descr',
         'patient_glycogen__gl_cons_status',
         'patient_glycogen__gl_cons_degree_specify',
         'patient_glycogen__gl_anti_natal_altra',
         'patient_glycogen__antenatal_ultrasound_if_abnormal',
         'patient_glycogen__gl_other_specify',
         'patient_glycogen__gl_delivery_type',
         'patient_glycogen__gl_baby_cried_after_del',
         'patient_glycogen__gl_resusciation_yes_no',
         'patient_glycogen__gl_resusciation_req',
         'patient_glycogen__gl_resusciation_req_other',
         'patient_glycogen__gl_nicu_stay',
         'patient_glycogen__gl_birth_weight',
         'patient_glycogen__gl_dev_milestone',
         'patient_glycogen__gl_dev_motor_status',
         'patient_glycogen__gl_dev_global_status',
         'patient_glycogen__gl_dev_cognitive_status',
         'patient_glycogen__gl_morn_leth_seiz',
         'patient_glycogen__gl_dev_delay',
         'patient_glycogen__gl_irritability',
         'patient_glycogen__gl_tremors',
         'patient_glycogen__gl_muscle_weak_floppy',
         'patient_glycogen__gl_exerc_cramping',
         'patient_glycogen__gl_abdominal_dist',
         'patient_glycogen__gl_jaundice',
         'patient_glycogen__gl_over_hunger',
         'patient_glycogen__gl_vomiting',
         'patient_glycogen__gl_diarrhia',
         'patient_glycogen__gl_weight_gain_fail',
         'patient_glycogen__gl_oral_ulcers',
         'patient_glycogen__gl_perianal_ulcar',
         'patient_glycogen__gl_rec_infections',
         'patient_glycogen__gl_rec_infections_type',
         'patient_glycogen__gl_rec_infections_type_other',
         'patient_glycogen__gl_bony_deforminty',
         'patient_glycogen__gl_site_bleeding',
         'patient_glycogen__gl_site_bleeding_type',
         'patient_glycogen__gl_polyurea',
         'patient_glycogen__gl_puberty_delay',
         'patient_glycogen__gl_joint_pain',
         'patient_glycogen__gl_exertion_dyspnoea',
         'patient_glycogen__gl_doll_like_face',
         'patient_glycogen__gl_hepatomegaly',
         'patient_glycogen__hepatomegalySize',
         'patient_glycogen__hepatomegalySpan',
         'patient_glycogen__gl_hepatomegaly_left_lobe_enlargement',
         'patient_glycogen__hepatomegalyConsistencyChoice',
         'patient_glycogen__hepatomegalysurfaceChoice',
         'patient_glycogen__hepatomegalyMarginChoice',
         'patient_glycogen__gl_splenomegaly_size',
         'patient_glycogen__gl_renal_enlargement',
         'patient_glycogen__gl_rachitic_changes',
         'patient_glycogen__gl_hypotonia',
         'patient_glycogen__IIQChoice',
         'patient_glycogen__IQValue',
         'patient_glycogen__DQChoice',

         'patient_glycogen__DQValue',
         'patient_glycogen__gl_cong_heart_fail',
         'patient_glycogen__gl_core_pulomonable',
         'patient_glycogen__gl_hypertension',
         'patient_glycogen__gl_any_other_findings',
         'patient_glycogen__gl_inv_hb',
         'patient_glycogen__gl_inv_wbc',
         'patient_glycogen__gl_inv_platelet_count',
         'patient_glycogen__gl_inv_wbc',
         'patient_glycogen__gl_inv_abs_neutrophil_count',
         'patient_glycogen__gl_inv_pt_sec',
         'patient_glycogen__gl_inv_aptt_sec',
         'patient_glycogen__gl_inv_ph',
         'patient_glycogen__gl_inv_hco_3',
         'patient_glycogen__gl_inv_lactate',
         'patient_glycogen__gl_inv_anion_gap',
         'patient_glycogen__gl_inv_fasting_sugar',
         'patient_glycogen__gl_inv_s_cal',
         'patient_glycogen__gl_inv_s_phosphorous',
         'patient_glycogen__gl_inv_s_alkaline',
         'patient_glycogen__gl_inv_total_bilirubin',
         'patient_glycogen__gl_inv_direct_bilirubin',
         'patient_glycogen__gl_inv_total_protien',
         'patient_glycogen__gl_inv_serum_albumin',
         'patient_glycogen__gl_inv_sgpt',
         'patient_glycogen__gl_inv_sgot',
         'patient_glycogen__gl_inv_ggt',
         'patient_glycogen__gl_inv_serum_urea',
         'patient_glycogen__gl_inv_serum_creatinine',
         'patient_glycogen__gl_inv_micro_alb',
         'patient_glycogen__gl_inv_proteinuria',
         'patient_glycogen__gl_inv_hypercal',
         'patient_glycogen__gl_inv_hypercitrauria',
         'patient_glycogen__gl_inv_bld',
         'patient_glycogen__gl_inv_tg',
         'patient_glycogen__gl_inv_tc',
         'patient_glycogen__gl_inv_vldl',
         'patient_glycogen__gl_inv_hdl',
         'patient_glycogen__gl_inv_ldl',
         'patient_glycogen__gl_inv_iron',
         'patient_glycogen__gl_inv_tibc',
         'patient_glycogen__gl_inv_vit_d',
         'patient_glycogen__gl_inv_pth',
         'patient_glycogen__gl_inv_s_uric_acid',
         'patient_glycogen__gl_inv_s_cpk',
         'patient_glycogen__gl_inv_s_afp',
         'patient_glycogen__gl_inv_biotinidase',
         'patient_glycogen__gl_inv_biotinidase_if_abnormal',
         'patient_glycogen__gl_inv_tms',
         'patient_glycogen__gl_inv_tms_if_abnormal_value',
         'patient_glycogen__urine_ketosis',
         'patient_glycogen__gl_ketosis',
         'patient_glycogen__gl_theroid_function_test',
         'patient_glycogen__gl_inv_t_3',
         'patient_glycogen__gl_inv_t_4',
         'patient_glycogen__gl_inv_tsh',
         'patient_glycogen__gl_rad_ultrasono_type',
         'patient_glycogen__gl_rad_liversize',
         'patient_glycogen__gl_rad_liverEchotexture',
         'patient_glycogen__gl_rad_hepatic',
         'patient_glycogen__gl_rad_Kidney',
         'patient_glycogen__gl_rad_kidney_size',
         'patient_glycogen__gl_rad_kidney_size',
         'patient_glycogen__gl_rad_lymphnodes_size',
         'patient_glycogen__gl_rad_portal_vien_dia',
         'patient_glycogen__gl_rad_adenoma',
         'patient_glycogen__gl_renal_par_pathalogy',
         'patient_glycogen__gl_renal_par_pathalogy_specify',
         'patient_glycogen__gl_nephrocalcinosis',
         'patient_glycogen__gl_pancreatitis',
         'patient_glycogen__gl_cholethiasis',
         'patient_glycogen__gl_xray_bone_age',
         'patient_glycogen__gl_echocardiography_status',
         'patient_glycogen__gl_echo_abnormal_cardio',
         'patient_glycogen__gl_volvular_stenosis',
         'patient_glycogen__gl_volvular_mitral1',
         'patient_glycogen__gl_volvular_tricuspid1',
         'patient_glycogen__gl_volvular_aortic1',
         'patient_glycogen__gl_volvular_pulmonary1',
         'patient_glycogen__gl_volvular_regurgitation',
         'patient_glycogen__gl_volvular_mitral2',
         'patient_glycogen__gl_volvular_tricuspid2',
         'patient_glycogen__gl_volvular_aortic2',
         'patient_glycogen__gl_volvular_pulmonary2',
         'patient_glycogen__gl_echo_abnormal_mention_lvmi',
         'patient_glycogen__gl_ejection_fraction',
         'patient_glycogen__gl_live_histopathology',
         'patient_glycogen__gl_live_histopathology_val',
         'patient_glycogen__gl_Muscule_histopathology',
         'patient_glycogen__gl_Muscule_histopathology_val',
         'patient_glycogen__gl_enzyme_assay',
         'patient_glycogen__gl_enzyme_assay_type',
         'patient_glycogen__gl_patient_value',
         'patient_glycogen__gl_normal_control',
         'patient_glycogen__gl_normal_range',
         'patient_glycogen__gl_enzyme_assay_report',
         'patient_glycogen__Causative_DNA_sequence_variation',
         'patient_glycogen__molecular_upload',
         'patient_glycogen__Gene_molecula',
         'patient_glycogen__trans_molecul',
         'patient_glycogen__Gene_molecula',
         'patient_glycogen__trans_molecul',
         'patient_glycogen__gl_dna1',
         'patient_glycogen__gl_pro1',
         'patient_glycogen__gl_var1',
         'patient_glycogen__gl_var_cla1',
         'patient_glycogen__gl_zygo1',
         'patient_glycogen__gl_dna2',
         'patient_glycogen__gl_pro2',
         'patient_glycogen__gl_var2',
         'patient_glycogen__gl_var_cla2',
         'patient_glycogen__gl_zygo2',
         'patient_glycogen__gl_seg',
         'patient_glycogen__Patient_molecular',
         'patient_glycogen__father',
         'patient_glycogen__mother',
         'patient_glycogen__gl_treat_diet_alone',
         'patient_glycogen__gl_treat_diet_anti_lipic',
         'patient_glycogen__gl_treat_diet_anti_lipic_hypouricemia',
         'patient_glycogen__gl_treat_diet_anti_hypouricemia',
         'patient_glycogen__gl_supportive_therapy',
         'patient_glycogen__gl_any_surgery',
         'patient_glycogen__gl_any_surgery_specify',
         'patient_glycogen__gl_any_organ_transplantation',
         'patient_glycogen__gl_any_organ_transplantation_specify',
         'patient_glycogen__gl_any_other_info',
         'patient_glycogen__gl_filled_by_name',
         'patient_glycogen__gl_clinical_name',
         'patient_glycogen__gl_date',
         'patient_glycogen__gl_Finaldiagnosis',
         'patient_glycogen__gl_Finaldiagnosis_other',
         'patient_glycogen__gl_Finaloutcomes',
         'patient_glycogen__gl_filled_by_name',
         'patient_glycogen__gl_clinical_name',
         'patient_glycogen__gl_date', ])
    users = profile_glycogen.objects.all().prefetch_related('patient_glycogen').values_list(
        'register_id__institute_name', 'uniqueId', 'gl_icmr_unique_no', 'gl_final_dignosis', 'gl_date_of_record',
        'gl_clinical_exam_date',
        'gl_date_of_birth', 'gl_patient_name', 'gl_father_name', 'gl_mother_name', 'gl_paitent_id',
        'gl_paitent_id_list', 'gl_patient_id_no', 'gl_mother_father_id', 'gl_mother_father_id_no', 'gl_permanent_addr',
        'gl_state',
        'gl_district', 'gl_city_name', 'gl_country_name', 'gl_land_line_no', 'gl_mother_mobile_no',
        'gl_father_mobile_no', 'gl_email',
        'gl_religion', 'gl_caste', 'gl_gender', 'gl_referred_status', 'gl_referred_by', 'gl_referred_by_desc',
        'gl_consent_given',
        'gl_consent_upload', 'gl_assent_given', 'gl_assent_upload', 'gl_hospital_name', 'gl_hospital_reg_no',
        'patient_glycogen__gl_patient_edu_status', 'patient_glycogen__gl_patient_occupation',
        'patient_glycogen__gl_father_edu_status', 'patient_glycogen__gl_father_occupation',
        'patient_glycogen__gl_mother_edu_status', 'patient_glycogen__gl_mother_occupation',
        'patient_glycogen__gl_monthly_income_status', 'patient_glycogen__gl_anth_wght_pat',
        'patient_glycogen__gl_anth_wght_per', 'patient_glycogen__gl_anth_wght_sd',

        'patient_glycogen__gl_anth_height_pat',
        'patient_glycogen__gl_anth_height_per', 'patient_glycogen__gl_anth_height_sd',

        'patient_glycogen__gl_anth_head_cir_pat',
        'patient_glycogen__gl_anth_head_cir_perc', 'patient_glycogen__gl_anth_head_cir_sd',

        'patient_glycogen__gl_presenting_complaints_years',
        'patient_glycogen__gl_presenting_complaints_months',
        'patient_glycogen__gl_presenting_complaints_day',
        'patient_glycogen__gl_presenting_complaints_intrauterine',

        'patient_glycogen__gl_presenting_complaints_age_presentation_years',
        'patient_glycogen__gl_presenting_complaints_age_presentation_months',
        'patient_glycogen__gl_presenting_complaints_age_presentation_day',
        'patient_glycogen__gl_presenting_complaints_age_presentation_intrauterine',

        'patient_glycogen__gl_presenting_complaints_age_diagnosis_years',
        'patient_glycogen__gl_presenting_complaints_age_diagnosis_months',
        'patient_glycogen__gl_presenting_complaints_age_diagnosis_day',
        'patient_glycogen__gl_presenting_complaints_age_diagnosis_intrauterine',

        'patient_glycogen__gl_fam_hist_status',
        'patient_glycogen__gl_fam_hist_descr',
        'patient_glycogen__gl_cons_status',
        'patient_glycogen__gl_cons_degree_specify',
        'patient_glycogen__gl_anti_natal_altra',
        'patient_glycogen__antenatal_ultrasound_if_abnormal',
        'patient_glycogen__gl_other_specify',
        'patient_glycogen__gl_delivery_type',
        'patient_glycogen__gl_baby_cried_after_del',
        'patient_glycogen__gl_resusciation_yes_no',
        'patient_glycogen__gl_resusciation_req',
        'patient_glycogen__gl_resusciation_req_other',
        'patient_glycogen__gl_nicu_stay',
        'patient_glycogen__gl_birth_weight',
        'patient_glycogen__gl_dev_milestone',
        'patient_glycogen__gl_dev_motor_status',
        'patient_glycogen__gl_dev_global_status',
        'patient_glycogen__gl_dev_cognitive_status',
        'patient_glycogen__gl_morn_leth_seiz',
        'patient_glycogen__gl_dev_delay',
        'patient_glycogen__gl_irritability',
        'patient_glycogen__gl_tremors',
        'patient_glycogen__gl_muscle_weak_floppy',
        'patient_glycogen__gl_exerc_cramping',
        'patient_glycogen__gl_abdominal_dist',
        'patient_glycogen__gl_jaundice',
        'patient_glycogen__gl_over_hunger',
        'patient_glycogen__gl_vomiting',
        'patient_glycogen__gl_diarrhia',
        'patient_glycogen__gl_weight_gain_fail',
        'patient_glycogen__gl_oral_ulcers',
        'patient_glycogen__gl_perianal_ulcar',
        'patient_glycogen__gl_rec_infections',
        'patient_glycogen__gl_rec_infections_type',
        'patient_glycogen__gl_rec_infections_type_other',
        'patient_glycogen__gl_bony_deforminty',
        'patient_glycogen__gl_site_bleeding',
        'patient_glycogen__gl_site_bleeding_type',
        'patient_glycogen__gl_polyurea',
        'patient_glycogen__gl_puberty_delay',
        'patient_glycogen__gl_joint_pain',
        'patient_glycogen__gl_exertion_dyspnoea',
        'patient_glycogen__gl_doll_like_face',
        'patient_glycogen__gl_hepatomegaly',
        'patient_glycogen__hepatomegalySize',
        'patient_glycogen__hepatomegalySpan',
        'patient_glycogen__gl_hepatomegaly_left_lobe_enlargement',
        'patient_glycogen__hepatomegalyConsistencyChoice',
        'patient_glycogen__hepatomegalysurfaceChoice',
        'patient_glycogen__hepatomegalyMarginChoice',
        'patient_glycogen__gl_splenomegaly_size',
        'patient_glycogen__gl_renal_enlargement',
        'patient_glycogen__gl_rachitic_changes',
        'patient_glycogen__gl_hypotonia',
        'patient_glycogen__IIQChoice',
        'patient_glycogen__IQValue',
        'patient_glycogen__DQChoice',

        'patient_glycogen__DQValue',
        'patient_glycogen__gl_cong_heart_fail',
        'patient_glycogen__gl_core_pulomonable',
        'patient_glycogen__gl_hypertension',
        'patient_glycogen__gl_any_other_findings',
        'patient_glycogen__gl_inv_hb',
        'patient_glycogen__gl_inv_wbc',
        'patient_glycogen__gl_inv_platelet_count',
        'patient_glycogen__gl_inv_wbc',
        'patient_glycogen__gl_inv_abs_neutrophil_count',
        'patient_glycogen__gl_inv_pt_sec',
        'patient_glycogen__gl_inv_aptt_sec',
        'patient_glycogen__gl_inv_ph',
        'patient_glycogen__gl_inv_hco_3',
        'patient_glycogen__gl_inv_lactate',
        'patient_glycogen__gl_inv_anion_gap',
        'patient_glycogen__gl_inv_fasting_sugar',
        'patient_glycogen__gl_inv_s_cal',
        'patient_glycogen__gl_inv_s_phosphorous',
        'patient_glycogen__gl_inv_s_alkaline',
        'patient_glycogen__gl_inv_total_bilirubin',
        'patient_glycogen__gl_inv_direct_bilirubin',
        'patient_glycogen__gl_inv_total_protien',
        'patient_glycogen__gl_inv_serum_albumin',
        'patient_glycogen__gl_inv_sgpt',
        'patient_glycogen__gl_inv_sgot',
        'patient_glycogen__gl_inv_ggt',
        'patient_glycogen__gl_inv_serum_urea',
        'patient_glycogen__gl_inv_serum_creatinine',
        'patient_glycogen__gl_inv_micro_alb',
        'patient_glycogen__gl_inv_proteinuria',
        'patient_glycogen__gl_inv_hypercal',
        'patient_glycogen__gl_inv_hypercitrauria',
        'patient_glycogen__gl_inv_bld',
        'patient_glycogen__gl_inv_tg',
        'patient_glycogen__gl_inv_tc',
        'patient_glycogen__gl_inv_vldl',
        'patient_glycogen__gl_inv_hdl',
        'patient_glycogen__gl_inv_ldl',
        'patient_glycogen__gl_inv_iron',
        'patient_glycogen__gl_inv_tibc',
        'patient_glycogen__gl_inv_vit_d',
        'patient_glycogen__gl_inv_pth',
        'patient_glycogen__gl_inv_s_uric_acid',
        'patient_glycogen__gl_inv_s_cpk',
        'patient_glycogen__gl_inv_s_afp',
        'patient_glycogen__gl_inv_biotinidase',
        'patient_glycogen__gl_inv_biotinidase_if_abnormal',
        'patient_glycogen__gl_inv_tms',
        'patient_glycogen__gl_inv_tms_if_abnormal_value',
        'patient_glycogen__urine_ketosis',
        'patient_glycogen__gl_ketosis',
        'patient_glycogen__gl_theroid_function_test',
        'patient_glycogen__gl_inv_t_3',
        'patient_glycogen__gl_inv_t_4',
        'patient_glycogen__gl_inv_tsh',
        'patient_glycogen__gl_rad_ultrasono_type',
        'patient_glycogen__gl_rad_liversize',
        'patient_glycogen__gl_rad_liverEchotexture',
        'patient_glycogen__gl_rad_hepatic',
        'patient_glycogen__gl_rad_Kidney',
        'patient_glycogen__gl_rad_kidney_size',
        'patient_glycogen__gl_rad_kidney_size',
        'patient_glycogen__gl_rad_lymphnodes_size',
        'patient_glycogen__gl_rad_portal_vien_dia',
        'patient_glycogen__gl_rad_adenoma',
        'patient_glycogen__gl_renal_par_pathalogy',
        'patient_glycogen__gl_renal_par_pathalogy_specify',
        'patient_glycogen__gl_nephrocalcinosis',
        'patient_glycogen__gl_pancreatitis',
        'patient_glycogen__gl_cholethiasis',
        'patient_glycogen__gl_xray_bone_age',
        'patient_glycogen__gl_echocardiography_status',
        'patient_glycogen__gl_echo_abnormal_cardio',
        'patient_glycogen__gl_volvular_stenosis',
        'patient_glycogen__gl_volvular_mitral1',
        'patient_glycogen__gl_volvular_tricuspid1',
        'patient_glycogen__gl_volvular_aortic1',
        'patient_glycogen__gl_volvular_pulmonary1',
        'patient_glycogen__gl_volvular_regurgitation',
        'patient_glycogen__gl_volvular_mitral2',
        'patient_glycogen__gl_volvular_tricuspid2',
        'patient_glycogen__gl_volvular_aortic2',
        'patient_glycogen__gl_volvular_pulmonary2',
        'patient_glycogen__gl_echo_abnormal_mention_lvmi',
        'patient_glycogen__gl_ejection_fraction',
        'patient_glycogen__gl_live_histopathology',
        'patient_glycogen__gl_live_histopathology_val',
        'patient_glycogen__gl_Muscule_histopathology',
        'patient_glycogen__gl_Muscule_histopathology_val',
        'patient_glycogen__gl_enzyme_assay',
        'patient_glycogen__gl_enzyme_assay_type',
        'patient_glycogen__gl_patient_value',
        'patient_glycogen__gl_normal_control',
        'patient_glycogen__gl_normal_range',
        'patient_glycogen__gl_enzyme_assay_report',
        'patient_glycogen__Causative_DNA_sequence_variation',
        'patient_glycogen__molecular_upload',
        'patient_glycogen__Gene_molecula',
        'patient_glycogen__trans_molecul',
        'patient_glycogen__Gene_molecula',
        'patient_glycogen__trans_molecul',
        'patient_glycogen__gl_dna1',
        'patient_glycogen__gl_pro1',
        'patient_glycogen__gl_var1',
        'patient_glycogen__gl_var_cla1',
        'patient_glycogen__gl_zygo1',
        'patient_glycogen__gl_dna2',
        'patient_glycogen__gl_pro2',
        'patient_glycogen__gl_var2',
        'patient_glycogen__gl_var_cla2',
        'patient_glycogen__gl_zygo2',
        'patient_glycogen__gl_seg',
        'patient_glycogen__Patient_molecular',
        'patient_glycogen__father',
        'patient_glycogen__mother',
        'patient_glycogen__gl_treat_diet_alone',
        'patient_glycogen__gl_treat_diet_anti_lipic',
        'patient_glycogen__gl_treat_diet_anti_lipic_hypouricemia',
        'patient_glycogen__gl_treat_diet_anti_hypouricemia',
        'patient_glycogen__gl_supportive_therapy',
        'patient_glycogen__gl_any_surgery',
        'patient_glycogen__gl_any_surgery_specify',
        'patient_glycogen__gl_any_organ_transplantation',
        'patient_glycogen__gl_any_organ_transplantation_specify',
        'patient_glycogen__gl_any_other_info',
        'patient_glycogen__gl_filled_by_name',
        'patient_glycogen__gl_clinical_name',
        'patient_glycogen__gl_date',
        'patient_glycogen__gl_Finaldiagnosis',
        'patient_glycogen__gl_Finaldiagnosis_other',
        'patient_glycogen__gl_Finaloutcomes',
        'patient_glycogen__gl_filled_by_name',
        'patient_glycogen__gl_clinical_name',
        'patient_glycogen__gl_date', )
    for user in users:
        writer.writerow(user)

    return response





@login_required(login_url='login')
def update_qa_qc_gsd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_glycogen.objects.get(id=pk)
    form2 = QAglycogenForm(instance=patient)

    if request.method == 'POST':
        form2 = QAglycogenForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_gl_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_gsd.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_gsd.html', context)


@login_required(login_url='login')
def view_qa_qc_gsd(request, pk):
    user = request.user
    patient = profile_glycogen.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")