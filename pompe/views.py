from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
import csv
from django.http import HttpResponse
from .forms import *


@login_required(login_url='login')
def add_record_pompe(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = PompeRegistrationForm()
    if request.method == 'POST':
        form1 = PompeRegistrationForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(pompe_demographic, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_pompe.html', context)
    context = {'form1': form1, }
    return render(request, 'add_record_pompe.html', context)


@login_required(login_url='login')
def update_patient_record_pompe(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pompe.objects.get(id=pk)

    form1 = PompeRegistrationForm(instance=patient)
    if request.method == 'POST':
        form1 = PompeRegistrationForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('pompe_total_record')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_pompe.html', context)
    context = {'form1': form1, }
    return render(request, 'update_patient_record_pompe.html', context)


@login_required(login_url='login')
def view_profile_pm(request, pk):
   
    try:
        form1 = profile_pompe.objects.get(id=pk)
    except:

        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_pm.html', context)



@login_required(login_url='login')
def pompe_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pompe.objects.get(id=pk)
    form1 = PompeSocioDemographicDetailsForm()
    if request.method == 'POST':
        form1 = PompeSocioDemographicDetailsForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()
            return HttpResponseRedirect(reverse(update_pompe_demographic, args=(pk,)))
    else:
        context = {'form1': form1, }
        return render(request, 'pompe_demographic.html', context)

    context = {'form1': form1, }
    return render(request, 'pompe_demographic.html', context)


@login_required(login_url='login')
def update_pompe_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pompe.objects.get(id=pk)
    try:
        form4 = demographic_pompe.objects.get(patient=patient)
        form1 = PompeSocioDemographicDetailsForm(instance=form4)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = PompeSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect('pompe_total_record')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_pompe_demographic.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = PompeSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("pompe_total_record")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_pompe_demographic.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = PompeSocioDemographicDetailsForm(request.POST, request.FILES, instance=form4)
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
                    return render(request, 'update_pompe_demographic.html', context)
    except:
        form1 = PompeSocioDemographicDetailsForm()
        if request.method == 'POST':
            form1 = PompeSocioDemographicDetailsForm(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                return redirect('pompe_total_record')
        else:
            context = {'form1': form1,'patient': patient, }
            return render(request, 'update_pompe_demographic.html', context)

    context = {'form1': form1,'patient': patient }
    return render(request, 'update_pompe_demographic.html', context)


@login_required(login_url='login')
def pompe_total_record(request):
    register = profile_pompe.objects.filter(user=request.user)
    context = {'register': register, }
    return render(request, 'pompe_total_record.html', context)


@login_required(login_url='login')
def pompe_total_record_admin(request):
    register = profile_pompe.objects.all()
    context = {'register': register, }
    return render(request, 'pompe_total_record_admin.html', context)


@login_required(login_url='login')
def view_pompe_record(request, pk):
    register = profile_pompe.objects.get(id=pk)
    try:
        form1 = demographic_pompe.objects.get(patient=register)
    except:

        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_pompe_record.html', context)


@login_required(login_url='login')
def delete_record_pm(request, pk):
    order = profile_pompe.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('pompe_total_record')

    context = {'order': order}
    return render(request, 'delete_record_pm.html', context)


@login_required(login_url='login')
def total_record_pm(request):
    pat = demographic_pompe.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_pm.html', context)

def export_pompe_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pompe.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'pmp_final_diagnosis', 'pmp_date_of_records',
         'pmp_date_of_clinical_exam', 'pmp_date_of_birth', 'pmp_patient_name', 'pmp_father_name',
         'pmp_mother_name', 'pmp_paitent_id_yes_no', 'pmp_paitent_id', 'pmp_patient_id_no', 'pmp_father_mother_id',
         'pmp_father_mother_id_no', 'pmp_permanent_addr', 'pmp_state', 'pmp_district', 'pmp_city_name',
         'pmp_country_name', 'pmp_land_line_no', 'pmp_mother_mobile_no', 'pmp_father_mobile_no', 'pmp_email',
         'pmp_religion', 'pmp_caste', 'pmp_gender', 'pmp_referred_status', 'pmp_referred_by', 'pmp_referred_by_desc',
         'pmp_consent_given', 'pmp_consent_upload', 'pmp_assent_given', 'pmp_assent_upload', 'pmp_hospital_name',
         'pmp_hospital_reg_no', 'patient_pompe__pd_Patient_education', 'patient_pompe__pd_Patient_occupation',
         'patient_pompe__pd_Father_education',
         'patient_pompe__pd_Father_occupation', 'patient_pompe__pd_Mother_education',
         'patient_pompe__pd_Mother_occupation', 'patient_pompe__pd_Monthly_family_income',
         'patient_pompe__pd_weight_patient',
         'patient_pompe__pd_weight_percentile', 'patient_pompe__pd_weight_SD', 'patient_pompe__pd_height_patient',
         'patient_pompe__pd_height_percentile',
         'patient_pompe__pd_height_SD', 'patient_pompe__pd_Head_circumference_patient',
         'patient_pompe__pd_Head_circumference_percentile', 'patient_pompe__pd_Head_circumference_sd',
         'patient_pompe__pd_Age_at_onset_of_symptoms_year', 'patient_pompe__pd_Age_at_onset_of_symptoms_month',
         'patient_pompe__pd_Age_at_onset_of_symptoms_day', 'patient_pompe__pd_Age_at_onset_of_symptoms_Intrauterine',
         'patient_pompe__pd_Age_at_presentation_year', 'patient_pompe__pd_Age_at_presentation_month',
         'patient_pompe__pd_Age_at_presentation_day', 'patient_pompe__pd_Age_at_presentation_Intrauterine',
         'patient_pompe__pd_Age_at_diagnosis_year', 'patient_pompe__pd_Age_at_diagnosis_month',
         'patient_pompe__pd_Age_at_diagnosis_day', 'patient_pompe__pd_Age_at_diagnosis_Intrauterine',
         'patient_pompe__pd_Pedigree_to_be_uploaded', 'patient_pompe__pd_positive_family_history',
         'patient_pompe__pd_family_history_specify',
         'patient_pompe__pd_Consanguinity', 'patient_pompe__pd_Consanguinity_specify',
         'patient_pompe__pd_Ultrasound_findings', 'patient_pompe__pd_Polyhydramnios',
         'patient_pompe__pd_Fetal_echocardiography',
         'patient_pompe__pd_Natal_History_Type_of_delivery',
         'patient_pompe__pd_Natal_History_Baby_cried_immediately_after_delivery',
         'patient_pompe__pd_Natal_History_Resuscitation_required', 'patient_pompe__pd_Natal_History_ventilater',
         'patient_pompe__pd_Natal_History_o_2_Cpap', 'patient_pompe__pd_Natal_History_Nursery_stay',
         'patient_pompe__pd_Birth_weight', 'patient_pompe__pd_Development_milestones',
         'patient_pompe__pd_if_delayed_Motor', 'patient_pompe__pd_if_delayed_Global',
         'patient_pompe__pd_if_delayed_Cognitive',
         'patient_pompe__pd_head', 'patient_pompe__pd_face', 'patient_pompe__pd_Eyes_Ptosis',
         'patient_pompe__pd_Large_tongue', 'patient_pompe__pd_Others_specify',
         'patient_pompe__pd_Ever_had_respiratory_distress', 'patient_pompe__pd_No_of_episode',
         'patient_pompe__pd_Ventilator_or_other_respiratory_support', 'patient_pompe__pd_Mode_of_ventilation',
         'patient_pompe__pd_Age_at_ventilator', 'patient_pompe__pd_Tracheostomy',
         'patient_pompe__pd_Was_weaning_off_from_ventilator_possible', 'patient_pompe__pd_Feeding_difficulties',
         'patient_pompe__pd_Feeding',
         'patient_pompe__pd_Protuberantabdomen', 'patient_pompe__pd_Hepatomegaly', 'patient_pompe__pd_Size_BCM',
         'patient_pompe__pd_Span', 'patient_pompe__pd_Hernia', 'patient_pompe__pd_Others',
         'patient_pompe__pd_Edema', 'patient_pompe__pd_Cyanosis', 'patient_pompe__pd_Cardiac_medications_date_started',
         'patient_pompe__pd_Cardiac_medications_dose', 'patient_pompe__pd_Heart_rate',
         'patient_pompe__pd_Gallop', 'patient_pompe__pd_arrythmia', 'patient_pompe__pd_Muscle_weakness',
         'patient_pompe__pd_Age_at_Onset_of_weakness',
         'patient_pompe__pd_Onset_of_weakness', 'patient_pompe__pd_Difficulty_in_sitting_from_lying_position',
         'patient_pompe__pd_Difficulty_in_standing_from_standing_position', 'patient_pompe__pd_Wheelchair_bound',
         'patient_pompe__pd_Age_at_Wheelchair_bound', 'patient_pompe__pd_Sleep_disturbances_apnea',
         'patient_pompe__pd_Hypotonia', 'patient_pompe__pd_Proximal_muscle_weakness_in_upper_extremities',
         'patient_pompe__pd_Distal_muscle_weakness_in_upper_extremities',
         'patient_pompe__pd_Proximal_muscle_weakness_in_lower_extremities',
         'patient_pompe__pd_Distal_muscle_weakness_in_lower_extremities', 'patient_pompe__pd_Neck_muscle_weakness',
         'patient_pompe__pd_Muscle_weakness_in_trunk', 'patient_pompe__pd_Reflexes',
         'patient_pompe__pd_Gower_positive', 'patient_pompe__pd_Contractures', 'patient_pompe__pd_Abnormal_Gait',
         'patient_pompe__pd_Muscles_of_respiration_involved', 'patient_pompe__pd_bulbar_and_lingual_weakness',
         'patient_pompe__pd_if_yes', 'patient_pompe__pd_Rigid_spine', 'patient_pompe__pd_Higher_mental_functions',
         'patient_pompe__pd_Cranial_nerve_involvement', 'patient_pompe__pd_Altered_or_reduced_visual_acuity',
         'patient_pompe__pd_Hearing_loss', 'patient_pompe__pd_Foot_drop',
         'patient_pompe__pd_Radiography_of_chest_to_assess_for_cardiomegaly', 'patient_pompe__pd_ECG',
         'patient_pompe__pd_Short_PR',
         'patient_pompe__pd_Tall_broad_QRS', 'patient_pompe__pd_ECHO_date', 'patient_pompe__pd_ECHO',
         'patient_pompe__pd_PFT_date', 'patient_pompe__pd_PFT', 'patient_pompe__pd_ECHO_specify',
         'patient_pompe__pd_PFT_Supine_FVC', 'patient_pompe__pd_PFT_Sitting_FVC', 'patient_pompe__pd_PFT_Supine_FEV1',
         'patient_pompe__pd_PFT_Sitting_FEV1', 'patient_pompe__pd_PFT_Mean_Inspiratory_Pressure',
         'patient_pompe__pd_PFT_Mean_Expiratory_Pressure', 'patient_pompe__pd_Swallow_study',
         'patient_pompe__pd_Swallow_study_specify',
         'patient_pompe__pd_CK', 'patient_pompe__pd_CK_MB', 'patient_pompe__pd_AST', 'patient_pompe__pd_ALT',
         'patient_pompe__pd_LDH',
         'patient_pompe__pd_Enzyme_analysis_done', 'patient_pompe__pd_Sample_date_done',
         'patient_pompe__pd_patien',
         'patient_pompe__pd_contro',
         'patient_pompe__pd_nor_ran',
         'patient_pompe__pd_CRIM_Status',
         'patient_pompe__pd_Enzyme_analysis_uploaded',
         'patient_pompe__pd_Causative_DNA_sequence_variat',
         'patient_pompe__pd_molecular_upload', 'patient_pompe__pd_Patient_molecular', 'patient_pompe__pd_Gene_molecula',
         'patient_pompe__pd_trans_molecul', 'patient_pompe__pd_mul_dna1', 'patient_pompe__pd_mul_pro1',
         'patient_pompe__pd_mul_var1', 'patient_pompe__pd_mul_zygo1',
         'patient_pompe__pd_mul_var_cla1',
         'patient_pompe__pd_mul_dna2', 'patient_pompe__pd_mul_pro2',
         'patient_pompe__pd_mul_var2', 'patient_pompe__pd_mul_zygo2',
         'patient_pompe__pd_mul_var_cla2',
         'patient_pompe__pd_mul_seg', 'patient_pompe__pd_father', 'patient_pompe__pd_mother',
         'patient_pompe__pd_ERT', 'patient_pompe__pd_name_of_com','patient_pompe__pd_ERT_enz', 'patient_pompe__pd_Date_Initiation',
         'patient_pompe__pd_Age_of_Start', 'patient_pompe__pd_Dosage',
         'patient_pompe__pd_Duration', 'patient_pompe__pd_Adverse_events', 'patient_pompe__pd_Adverse_events_specify',
         'patient_pompe__pd_Response', 'patient_pompe__pd_Immunomodulation',
         'patient_pompe__pd_Immunomodulation_methotrexate', 'patient_pompe__pd_Immunomodulation_rituximab',
         'patient_pompe__pd_Immunomodulation_ivig',
         'patient_pompe__pd_Current_ERT_Status', 'patient_pompe__pd_Ongoing', 'patient_pompe__pd_moto_sca',
         'patient_pompe__pd_Any_interruption', 'patient_pompe__pd_Reason_for_interruption',
         'patient_pompe__pd_Duration_of_interruption', 'patient_pompe__pd_Physiotherapy_date',
         'patient_pompe__pd_moto_qmft', 'patient_pompe__pd_moto_gsgc',
         'patient_pompe__pd_moto_wlk_ts',
         'patient_pompe_pd_Finaldiagnosis', 'patient_pompe_pd_Finaloutcomes', 'patient_pompe__pd_filed_by_DEO_name',
         'patient_pompe__pd_clinician_name', 'patient_pompe__pd_filled_date', ])

    users = profile_pompe.objects.all().prefetch_related('patient_pompe').values_list('register_id__institute_name',
                                                                                      'uniqueId', 'pmp_icmr_unique_no',
                                                                                      'pmp_final_diagnosis',
                                                                                      'pmp_date_of_records',
                                                                                      'pmp_date_of_clinical_exam',
                                                                                      'pmp_date_of_birth',

                                                                                      'pmp_patient_name',
                                                                                      'pmp_father_name',
                                                                                      'pmp_mother_name',
                                                                                      'pmp_paitent_id_yes_no',
                                                                                      'pmp_paitent_id',
                                                                                      'pmp_patient_id_no',
                                                                                      'pmp_father_mother_id',
                                                                                      'pmp_father_mother_id_no',
                                                                                      'pmp_permanent_addr', 'pmp_state',
                                                                                      'pmp_district', 'pmp_city_name',
                                                                                      'pmp_country_name',
                                                                                      'pmp_land_line_no',
                                                                                      'pmp_mother_mobile_no',
                                                                                      'pmp_father_mobile_no',
                                                                                      'pmp_email',
                                                                                      'pmp_religion', 'pmp_caste',
                                                                                      'pmp_gender',
                                                                                      'pmp_referred_status',
                                                                                      'pmp_referred_by',
                                                                                      'pmp_referred_by_desc',
                                                                                      'pmp_consent_given',
                                                                                      'pmp_consent_upload',
                                                                                      'pmp_assent_given',
                                                                                      'pmp_assent_upload',
                                                                                      'pmp_hospital_name',
                                                                                      'pmp_hospital_reg_no',
                                                                                      'patient_pompe__pd_Patient_education',
                                                                                      'patient_pompe__pd_Patient_occupation',
                                                                                      'patient_pompe__pd_Father_education',
                                                                                      'patient_pompe__pd_Father_occupation',
                                                                                      'patient_pompe__pd_Mother_education',
                                                                                      'patient_pompe__pd_Mother_occupation',
                                                                                      'patient_pompe__pd_Monthly_family_income',
                                                                                      'patient_pompe__pd_weight_patient',
                                                                                      'patient_pompe__pd_weight_percentile',
                                                                                      'patient_pompe__pd_weight_SD',
                                                                                      'patient_pompe__pd_height_patient',
                                                                                      'patient_pompe__pd_height_percentile',
                                                                                      'patient_pompe__pd_height_SD',
                                                                                      'patient_pompe__pd_Head_circumference_patient',
                                                                                      'patient_pompe__pd_Head_circumference_percentile',
                                                                                      'patient_pompe__pd_Head_circumference_sd',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_year',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_month',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_day',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_Intrauterine',
                                                                                      'patient_pompe__pd_Age_at_presentation_year',
                                                                                      'patient_pompe__pd_Age_at_presentation_month',
                                                                                      'patient_pompe__pd_Age_at_presentation_day',
                                                                                      'patient_pompe__pd_Age_at_presentation_Intrauterine',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_year',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_month',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_day',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_Intrauterine',
                                                                                      'patient_pompe__pd_Pedigree_to_be_uploaded',
                                                                                      'patient_pompe__pd_positive_family_history',
                                                                                      'patient_pompe__pd_family_history_specify',
                                                                                      'patient_pompe__pd_Consanguinity',
                                                                                      'patient_pompe__pd_Consanguinity_specify',
                                                                                      'patient_pompe__pd_Ultrasound_findings',
                                                                                      'patient_pompe__pd_Polyhydramnios',
                                                                                      'patient_pompe__pd_Fetal_echocardiography',
                                                                                      'patient_pompe__pd_Natal_History_Type_of_delivery',
                                                                                      'patient_pompe__pd_Natal_History_Baby_cried_immediately_after_delivery',
                                                                                      'patient_pompe__pd_Natal_History_Resuscitation_required',
                                                                                      'patient_pompe__pd_Natal_History_ventilater',
                                                                                      'patient_pompe__pd_Natal_History_o_2_Cpap',
                                                                                      'patient_pompe__pd_Natal_History_Nursery_stay',
                                                                                      'patient_pompe__pd_Birth_weight',
                                                                                      'patient_pompe__pd_Development_milestones',
                                                                                      'patient_pompe__pd_if_delayed_Motor',
                                                                                      'patient_pompe__pd_if_delayed_Global',
                                                                                      'patient_pompe__pd_if_delayed_Cognitive',
                                                                                      'patient_pompe__pd_head',
                                                                                      'patient_pompe__pd_face',
                                                                                      'patient_pompe__pd_Eyes_Ptosis',
                                                                                      'patient_pompe__pd_Large_tongue',
                                                                                      'patient_pompe__pd_Others_specify',
                                                                                      'patient_pompe__pd_Ever_had_respiratory_distress',
                                                                                      'patient_pompe__pd_No_of_episode',
                                                                                      'patient_pompe__pd_Ventilator_or_other_respiratory_support',
                                                                                      'patient_pompe__pd_Mode_of_ventilation',
                                                                                      'patient_pompe__pd_Age_at_ventilator',
                                                                                      'patient_pompe__pd_Tracheostomy',
                                                                                      'patient_pompe__pd_Was_weaning_off_from_ventilator_possible',
                                                                                      'patient_pompe__pd_Feeding_difficulties',
                                                                                      'patient_pompe__pd_Feeding',
                                                                                      'patient_pompe__pd_Protuberantabdomen',
                                                                                      'patient_pompe__pd_Hepatomegaly',
                                                                                      'patient_pompe__pd_Size_BCM',
                                                                                      'patient_pompe__pd_Span',
                                                                                      'patient_pompe__pd_Hernia',
                                                                                      'patient_pompe__pd_Others',
                                                                                      'patient_pompe__pd_Edema',
                                                                                      'patient_pompe__pd_Cyanosis',
                                                                                      'patient_pompe__pd_Cardiac_medications_date_started',
                                                                                      'patient_pompe__pd_Cardiac_medications_dose',
                                                                                      'patient_pompe__pd_Heart_rate',
                                                                                      'patient_pompe__pd_Gallop',
                                                                                      'patient_pompe__pd_arrythmia',
                                                                                      'patient_pompe__pd_Muscle_weakness',
                                                                                      'patient_pompe__pd_Age_at_Onset_of_weakness',
                                                                                      'patient_pompe__pd_Onset_of_weakness',
                                                                                      'patient_pompe__pd_Difficulty_in_sitting_from_lying_position',
                                                                                      'patient_pompe__pd_Difficulty_in_standing_from_standing_position',
                                                                                      'patient_pompe__pd_Wheelchair_bound',
                                                                                      'patient_pompe__pd_Age_at_Wheelchair_bound',
                                                                                      'patient_pompe__pd_Sleep_disturbances_apnea',
                                                                                      'patient_pompe__pd_Hypotonia',
                                                                                      'patient_pompe__pd_Proximal_muscle_weakness_in_upper_extremities',
                                                                                      'patient_pompe__pd_Distal_muscle_weakness_in_upper_extremities',
                                                                                      'patient_pompe__pd_Proximal_muscle_weakness_in_lower_extremities',
                                                                                      'patient_pompe__pd_Distal_muscle_weakness_in_lower_extremities',
                                                                                      'patient_pompe__pd_Neck_muscle_weakness',
                                                                                      'patient_pompe__pd_Muscle_weakness_in_trunk',
                                                                                      'patient_pompe__pd_Reflexes',
                                                                                      'patient_pompe__pd_Gower_positive',
                                                                                      'patient_pompe__pd_Contractures',
                                                                                      'patient_pompe__pd_Abnormal_Gait',
                                                                                      'patient_pompe__pd_Muscles_of_respiration_involved',
                                                                                      'patient_pompe__pd_bulbar_and_lingual_weakness',
                                                                                      'patient_pompe__pd_if_yes',
                                                                                      'patient_pompe__pd_Rigid_spine',
                                                                                      'patient_pompe__pd_Higher_mental_functions',
                                                                                      'patient_pompe__pd_Cranial_nerve_involvement',
                                                                                      'patient_pompe__pd_Altered_or_reduced_visual_acuity',
                                                                                      'patient_pompe__pd_Hearing_loss',
                                                                                      'patient_pompe__pd_Foot_drop',
                                                                                      'patient_pompe__pd_Radiography_of_chest_to_assess_for_cardiomegaly',
                                                                                      'patient_pompe__pd_ECG',
                                                                                      'patient_pompe__pd_Short_PR',
                                                                                      'patient_pompe__pd_Tall_broad_QRS',
                                                                                      'patient_pompe__pd_ECHO_date',
                                                                                      'patient_pompe__pd_ECHO',
                                                                                      'patient_pompe__pd_PFT_date',
                                                                                      'patient_pompe__pd_PFT',
                                                                                      'patient_pompe__pd_ECHO_specify',
                                                                                      'patient_pompe__pd_PFT_Supine_FVC',
                                                                                      'patient_pompe__pd_PFT_Sitting_FVC',
                                                                                      'patient_pompe__pd_PFT_Supine_FEV1',
                                                                                      'patient_pompe__pd_PFT_Sitting_FEV1',
                                                                                      'patient_pompe__pd_PFT_Mean_Inspiratory_Pressure',
                                                                                      'patient_pompe__pd_PFT_Mean_Expiratory_Pressure',
                                                                                      'patient_pompe__pd_Swallow_study',
                                                                                      'patient_pompe__pd_Swallow_study_specify',
                                                                                      'patient_pompe__pd_CK',
                                                                                      'patient_pompe__pd_CK_MB',
                                                                                      'patient_pompe__pd_AST',
                                                                                      'patient_pompe__pd_ALT',
                                                                                      'patient_pompe__pd_LDH',

                                                                                      'patient_pompe__pd_Enzyme_analysis_done',
                                                                                      'patient_pompe__pd_Sample_date_done',
                                                                                      'patient_pompe__pd_patien',
                                                                                      'patient_pompe__pd_contro',
                                                                                      'patient_pompe__pd_nor_ran',
                                                                                      'patient_pompe__pd_CRIM_Status',
                                                                                      'patient_pompe__pd_Enzyme_analysis_uploaded',
                                                                                      'patient_pompe__pd_Causative_DNA_sequence_variat',
                                                                                      'patient_pompe__pd_molecular_upload',
                                                                                      'patient_pompe__pd_Patient_molecular',
                                                                                      'patient_pompe__pd_Gene_molecula',
                                                                                      'patient_pompe__pd_trans_molecul',
                                                                                      'patient_pompe__pd_mul_dna1',
                                                                                      'patient_pompe__pd_mul_pro1',
                                                                                      'patient_pompe__pd_mul_var1',
                                                                                      'patient_pompe__pd_mul_zygo1',

                                                                                      'patient_pompe__pd_mul_var_cla1',
                                                                                      'patient_pompe__pd_mul_dna2',
                                                                                      'patient_pompe__pd_mul_pro2',
                                                                                      'patient_pompe__pd_mul_var2',
                                                                                      'patient_pompe__pd_mul_zygo2',

                                                                                      'patient_pompe__pd_mul_var_cla2',
                                                                                      'patient_pompe__pd_mul_seg',
                                                                                      'patient_pompe__pd_father',
                                                                                      'patient_pompe__pd_mother',
                                                                                      'patient_pompe__pd_ERT',
                                                                                      'patient_pompe__pd_name_of_com',
                                                                                      'patient_pompe__pd_ERT_enz',
                                                                                      'patient_pompe__pd_Date_Initiation',
                                                                                      'patient_pompe__pd_Age_of_Start',
                                                                                      'patient_pompe__pd_Dosage',
                                                                                      'patient_pompe__pd_Duration',
                                                                                      'patient_pompe__pd_Adverse_events',
                                                                                      'patient_pompe__pd_Adverse_events_specify',
                                                                                      'patient_pompe__pd_Response',
                                                                                      'patient_pompe__pd_Immunomodulation',
                                                                                      'patient_pompe__pd_Immunomodulation_methotrexate',
                                                                                      'patient_pompe__pd_Immunomodulation_rituximab',
                                                                                      'patient_pompe__pd_Immunomodulation_ivig',
                                                                                      'patient_pompe__pd_Current_ERT_Status',
                                                                                      'patient_pompe__pd_Ongoing',
                                                                                      'patient_pompe__pd_moto_sca',
                                                                                      'patient_pompe__pd_Any_interruption',
                                                                                      'patient_pompe__pd_Reason_for_interruption',
                                                                                      'patient_pompe__pd_Duration_of_interruption',
                                                                                      'patient_pompe__pd_Physiotherapy_date',
                                                                                      'patient_pompe__pd_moto_qmft',
                                                                                      'patient_pompe__pd_moto_gsgc',
                                                                                      'patient_pompe__pd_moto_wlk_ts',
                                                                                      'patient_pompe__pd_Finaldiagnosis',
                                                                                      'patient_pompe__pd_Finaloutcomes',
                                                                                      'patient_pompe__pd_filed_by_DEO_name',
                                                                                      'patient_pompe__pd_clinician_name',
                                                                                      'patient_pompe__pd_filled_date', )
    for user in users:
        writer.writerow(user)

    return response




@login_required(login_url='login')
def update_qa_qc_pompe(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pompe.objects.get(id=pk)
    form2 = QApompeForm(instance=patient)

    if request.method == 'POST':
        form2 = QApompeForm(request.POST, request.FILES, instance=patient)
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
            return redirect('pompe_total_record_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_pompe.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_pompe.html', context)


@login_required(login_url='login')
def view_qa_qc_pompe(request, pk):
    user = request.user
    patient = profile_pompe.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
