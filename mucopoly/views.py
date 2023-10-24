from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
import csv
from django.http import HttpResponse
from .forms import *


@login_required(login_url='login')
def add_record_mg(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = ProfileMGForm()
    if request.method == 'POST':
        form1 = ProfileMGForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()

            return HttpResponseRedirect(reverse(mg_demographic, args=(auth1,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_mg.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_mg.html', context)


@login_required(login_url='login')
def update_patient_record_mg(request,pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    form1 = ProfileMGForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfileMGForm(request.POST, request.FILES,instance=patient )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()

            return redirect('total_record_mg')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_mg.html', context)
    context = {'form1': form1, }
    return render(request, 'update_patient_record_mg.html', context)


@login_required(login_url='login')
def view_profile_mg(request, pk):

    try:
        form1 = profile_mucopolysaccharidosis.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_record_mg.html', context)


@login_required(login_url='login')
def mg_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    form2 = SocioDemographicDataSheetMGForm()
    # user1 = Registration.objects.get(user=request.user)
    if request.method == 'POST':

        form2 = SocioDemographicDataSheetMGForm(request.POST, request.FILES, )
        if form2.is_valid():
            auth1 = form2.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_mg, args=(pk,)))

        else:
            context = {'form2': form2, }
            return render(request, 'mg_demographic.html', context)

    context = {'form2': form2, }
    return render(request, 'mg_demographic.html', context)


@login_required(login_url='login')
def update_record_mg(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    try:
        form5 = demographic_mucopolysaccharidosis.objects.get(patient=patient)
        form2 = SocioDemographicDataSheetMGForm(instance=form5)
        # user1 = Registration.objects.get(user=request.user)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form2 = SocioDemographicDataSheetMGForm(request.POST, request.FILES, instance=form5)
            if form2.is_valid():
                auth1 = form2.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect('total_record_mg')
            else:
                context = {'form2': form2, 'patient': patient,}
                return render(request, 'update_record_mg.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form2 = SocioDemographicDataSheetMGForm(request.POST, request.FILES, instance=form5)
            if form2.is_valid():
                auth1 = form2.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
            else:
                context = {'form2': form2,'patient': patient, }
                return render(request, 'update_record_mg.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form2 = SocioDemographicDataSheetMGForm(request.POST, request.FILES, instance=form5)
                if form2.is_valid():
                    auth1 = form2.save(commit=False)
                    auth1.user = user
                    auth1.patient = patient
                    auth1.register = register
                    auth1.save()
                    # patient.complete = 'Yes'
                    # patient.save()
                else:
                    context = {'form2': form2, 'patient': patient, }
                    return render(request, 'update_record_mg.html', context)
    except:
        form2 = SocioDemographicDataSheetMGForm()
        # user1 = Registration.objects.get(user=request.user)
        if request.method == 'POST':

            form2 = SocioDemographicDataSheetMGForm(request.POST, request.FILES, )
            if form2.is_valid():
                auth1 = form2.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()

                return redirect('total_record_mg')

            else:
                context = {'form2': form2,'patient': patient, }
                return render(request, 'update_record_mg.html', context)
    context = {'form2': form2,'patient': patient, }
    return render(request, 'update_record_mg.html', context)


@login_required(login_url='login')
def view_record_mg(request, pk):
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    try:
        form2 = demographic_mucopolysaccharidosis.objects.get(patient=patient)
    except:
        form2 = None
    context = {'form2': form2, }
    return render(request, 'view_record_mg.html', context)


@login_required(login_url='login')
def total_record_mg(request):
    pat = profile_mucopolysaccharidosis.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_mg.html', context)



@login_required(login_url='login')
def view_record_mg(request, pk):
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    try:
        form2 = demographic_mucopolysaccharidosis.objects.get(patient=patient)
    except:
        form2 = None
    context = {'form2': form2, }
    return render(request, 'view_record_mg.html', context)


@login_required(login_url='login')
def total_record_mg(request):
    pat = profile_mucopolysaccharidosis.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_mg.html', context)


@login_required(login_url='login')
def total_record_mg_admin(request):
    pat = profile_mucopolysaccharidosis.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_mg_admin.html', context)


@login_required(login_url='login')
def delete_record_mg(request, pk):
    order = profile_mucopolysaccharidosis.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_mg')

    context = {'order': order}
    return render(request, 'delete_record_mg.html', context)

def export_mucopoly_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Mucopoly.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'muco_final_diagnosis', 'muco_date_of_records',
         'muco_date_of_clinical_exam', 'muco_date_of_birth', 'muco_patient_name',
         'muco_father_name',
         'muco_mother_name', 'muco_paitent_id_yes_no', 'muco_paitent_id', 'muco_patient_id_no', 'muco_father_mother_id',
         'muco_mother_father_id_no', 'muco_permanent_addr', 'muco_state', 'muco_district', 'muco_city_name',
         'muco_country_name', 'muco_land_line_no', 'muco_mother_mobile_no', 'muco_father_mobile_no', 'muco_email',
         'muco_religion', 'muco_caste', 'muco_gender', 'muco_referred_status', 'muco_referred_by',
         'muco_referred_by_desc', 'muco_consent_given', 'muco_consent_upload', 'muco_assent_given',
         'muco_assent_upload', 'muco_hospital_name', 'muco_hospital_reg_no', 'education_status_of_patient',
         'occupation_of_patient', 'education_status_of_father', 'occupation_of_father', 'education_status_of_mother',
         'occupation_of_mother', 'family_income', 'gl_anth_wght_pat', 'gl_anth_wght_per',
         'gl_anth_wght_sd', 'gl_anth_height_pat', 'gl_anth_height_per', 'gl_anth_height_sd',
         'gl_anth_head_cir_pat',
         'gl_anth_head_cir_per', 'gl_anth_head_cir_sd',
         'Age_at_Onset_of_symptoms_years', 'Age_at_Onset_of_symptoms_months',
         'Age_at_Onset_of_symptoms_day', 'Age_at_Onset_of_symptoms_intrauterine',

         'Age_at_Presentation_years', 'Age_at_Presentation_months',
         'Age_at_Presentation_day', 'Age_at_Presentation_intrauterine',

         'Age_at_diagnosis_years', 'Age_at_diagnosis_months',
         'Age_at_diagnosis_day', 'Age_at_diagnosis_intrauterine',

         'Pedigree_generation_upload', 'positive_family_history', 'family_history_specify', 'consanguinity',
         'consanguinity_mention_degree', 'antenatal_findings',
         'if_abnormal_specify', 'antenatal_present_absent', 'antenatal_other_specify', 'type_of_delivery',
         'baby_cried_immediately_after_delivery', 'resuscitation_required', 'yes_specify', 'specify', 'birth_weight',
         'developmental_milestones', 'motor', 'globall', 'cognitive', 'mental_retardation_Delay', 'Neuroregression',
         'behavioural_problems', 'Hyperactivity', 'On_some_drugs', 'Seizures', 'On_some_antiepileptics_drugs',
         'Symptoms', 'Recurrent_diarrheoa', 'Recurrent_pneumonia', 'persistent_upper_respiratory_symptoms',
         'Sleep_disturbance', 'Snoring', 'Visual_problem', 'Deafness', 'Chronic_otitis_media', 'Use_of_hearing_aid',
         'PE_ear_tube_placement', 'Any_surgery_for_hernia_or_others', 'Functional_status', 'face_coarse',
         'enlarged_tongue', 'head_shape', 'skin', 'pebbly_MPSII', 'mongolian_spots_at_back', 'ichthyosis',
         'stiff_thick_skin', 'telangiectasia', 'edema', 'hydrops', 'Tone', 'Power', 'Reflexes', 'ataxia',
         'Signs_of_raised_ICT',
         'Symptoms_of_CTS', 'IQ', 'iq_value', 'DQ', 'dq_value', 'corneal_clouding', 'papilledema', 'glaucoma',
         'optic_nerve_atrophy', 'retinal_degeneration_pigmentation', 'corneal_opacity', 'cataract', 'squint',
         'nystagmus', 'any_other_specify', 'Cardiomyopathy', 'Congestive_Heart_failure', 'Cor_pulomonale',
         'Valvular_involvement', 'Enlarged_tonsils', 'Sleep_apnea',
         'Reactive_Airway_Disease', 'Dyspnea', 'Gum_hyperplasia', 'hepatomegaly', 'size_hepatomegaly',
         'span_hepatomegaly', 'Splenomegaly', 'size_splenomegaly', 'hernia', 'specify_if', 'Umbilical_hernia',
         'Inguinal_hernia', 'Joint_Contractures', 'Joint_arthritis', 'Joint_laxity', 'Scoliosis', 'Kyphosis_Gibbus',
         'Genu_valgum', 'Pes_Cavus', 'Toe_Walking', 'Echocardiography', 'abnormal_finding', 'Ultrasonography',
         'Liver_Size_volume', 'Spleen_Size_Volume', 'Skull_J_shaped_sella', 'Spine_Beaked_vertebra',
         'Central_lower_tick', 'Metacarpals_Bullet_shaped', 'Ribs_oar_shaped', 'Pelvis_Hip_dysplasia',
         'Dislocation_of_hip',
         'Flared_iliac_wings', 'Long_bones', 'Dexa_Z_score', 'if_done_specify', 'EPS_for_CTS',
         'If_abnormal_specify_findings', 'Pulmonary_function_test', 'if_yes', 'if_abnormal_finding_specify', 'CT_Scan',
         'Specify_findings_if_abnormall', 'MRI_Brain', 'Specify_findings_if_abnormal_mri', 'EEG',
         'Specify_findings_if_abnormal_eeg', 'Corneal_clouding1', 'Fundus', 'Specify_if_abnormal', 'Glaucoma1',
         'Hearing_Assessment', 'if_abnormal', 'Sleep_Studies', 'Specify_findings_if_abnormal', 'Urine_spot_test',
         'Urinary_GAGs_analysis', 'Patient_urine', 'Normal_Control_urine', 'Normal_range_urine',
         'enzyme_var', 'enzyme_sam', 'Other_specify', 'Patient_enzyme', 'Normal_Control', 'Normal_range',
         'Causative_DNA_sequence_variation', 'molecular_upload',
         'Patient_molecular', 'Gene_molecula', 'trans_molecul', 'mul_dna1', 'mul_pro1', 'mul_var1', 'mul_zygo1',
         'mul_var_cla1',
         'mul_dna2', 'mul_pro2', 'mul_var2', 'mul_zygo2', 'mul_var_cla2',
         'mul_seg', 'father', 'mother', 'Enzyme_Replacement_Therapy', 'Date_of_initiation', 'Age_of_Start',
         'Dosage', 'Duration', 'Adverse_events', 'if_yes_specify', 'Any_interruption',
         'Reason_for_interruption', 'Duration_of_interruption', 'Response', 'Bone_Marrow_Transplantation', 'date',
         'Donor', 'Hospital', 'Response', 'Surgery', 'Hernia_surgery', 'Age_at_surgery',
         'Calcium_and_multivitamin_supplements', 'Regular_Physiotherapy', 'Any_ocular_medication',
         'CPAP_BiPAP_for_sleep_apnea', 'Finaldiagnosis', 'Finaloutcomes', 'mg_filed_by_name',
         'mg_clinician_name', 'mg_filled_date'])

    users = profile_mucopolysaccharidosis.objects.all().prefetch_related('patient_mucopoly').values_list(
        'register_id__institute_name', 'uniqueId', 'muco_icmr_unique_no', 'muco_final_diagnosis',
        'muco_date_of_records', 'muco_date_of_clinical_exam', 'muco_date_of_birth',
        'muco_patient_name', 'muco_father_name', 'muco_mother_name', 'muco_paitent_id_yes_no', 'muco_paitent_id',
        'muco_patient_id_no', 'muco_father_mother_id', 'muco_mother_father_id_no', 'muco_permanent_addr', 'muco_state',
        'muco_district', 'muco_city_name', 'muco_country_name', 'muco_land_line_no', 'muco_mother_mobile_no',
        'muco_father_mobile_no', 'muco_email', 'muco_religion', 'muco_caste', 'muco_gender', 'muco_referred_status',
        'muco_referred_by', 'muco_referred_by_desc', 'muco_consent_given', 'muco_consent_upload', 'muco_assent_given',
        'muco_assent_upload', 'muco_hospital_name', 'muco_hospital_reg_no',
        'patient_mucopoly__education_status_of_patient', 'patient_mucopoly__occupation_of_patient',
        'patient_mucopoly__education_status_of_father', 'patient_mucopoly__occupation_of_father',
        'patient_mucopoly__education_status_of_mother', 'patient_mucopoly__occupation_of_mother',
        'patient_mucopoly__family_income', 'patient_mucopoly__gl_anth_wght_pat',
        'patient_mucopoly__gl_anth_wght_per', 'patient_mucopoly__gl_anth_wght_sd',
        'patient_mucopoly__gl_anth_height_pat',
        'patient_mucopoly__gl_anth_height_per',
        'patient_mucopoly__gl_anth_height_sd',
        'patient_mucopoly__gl_anth_head_cir_pat',
        'patient_mucopoly__gl_anth_head_cir_per', 'patient_mucopoly__gl_anth_head_cir_sd',

        'patient_mucopoly__Age_at_Onset_of_symptoms_years', 'patient_mucopoly__Age_at_Onset_of_symptoms_months',
        'patient_mucopoly__Age_at_Onset_of_symptoms_day', 'patient_mucopoly__Age_at_Onset_of_symptoms_intrauterine',

        'patient_mucopoly__Age_at_Presentation_years', 'patient_mucopoly__Age_at_Presentation_months',
        'patient_mucopoly__Age_at_Presentation_day', 'patient_mucopoly__Age_at_Presentation_intrauterine',

        'patient_mucopoly__Age_at_diagnosis_years', 'patient_mucopoly__Age_at_diagnosis_months',
        'patient_mucopoly__Age_at_diagnosis_day', 'patient_mucopoly__Age_at_diagnosis_intrauterine',

        'patient_mucopoly__Pedigree_generation_upload', 'patient_mucopoly__positive_family_history',
        'patient_mucopoly__family_history_specify', 'patient_mucopoly__consanguinity',
        'patient_mucopoly__consanguinity_mention_degree', 'patient_mucopoly__antenatal_findings',
        'patient_mucopoly__if_abnormal_specify', 'patient_mucopoly__antenatal_present_absent',
        'patient_mucopoly__antenatal_other_specify', 'patient_mucopoly__type_of_delivery',
        'patient_mucopoly__baby_cried_immediately_after_delivery', 'patient_mucopoly__resuscitation_required',
        'patient_mucopoly__yes_specify', 'patient_mucopoly__specify', 'patient_mucopoly__birth_weight',
        'patient_mucopoly__developmental_milestones', 'patient_mucopoly__motor', 'patient_mucopoly__globall',
        'patient_mucopoly__cognitive', 'patient_mucopoly__mental_retardation_Delay',
        'patient_mucopoly__Neuroregression',
        'patient_mucopoly__behavioural_problems', 'patient_mucopoly__Hyperactivity', 'patient_mucopoly__On_some_drugs',
        'patient_mucopoly__Seizures', 'patient_mucopoly__On_some_antiepileptics_drugs', 'patient_mucopoly__Symptoms',
        'patient_mucopoly__Recurrent_diarrheoa', 'patient_mucopoly__Recurrent_pneumonia',
        'patient_mucopoly__persistent_upper_respiratory_symptoms', 'patient_mucopoly__Sleep_disturbance',
        'patient_mucopoly__Snoring', 'patient_mucopoly__Visual_problem', 'patient_mucopoly__Deafness',
        'patient_mucopoly__Chronic_otitis_media', 'patient_mucopoly__Use_of_hearing_aid',
        'patient_mucopoly__PE_ear_tube_placement', 'patient_mucopoly__Any_surgery_for_hernia_or_others',
        'patient_mucopoly__Functional_status', 'patient_mucopoly__face_coarse', 'patient_mucopoly__enlarged_tongue',
        'patient_mucopoly__head_shape', 'patient_mucopoly__skin', 'patient_mucopoly__pebbly_MPSII',
        'patient_mucopoly__mongolian_spots_at_back', 'patient_mucopoly__ichthyosis',
        'patient_mucopoly__stiff_thick_skin',
        'patient_mucopoly__telangiectasia', 'patient_mucopoly__edema', 'patient_mucopoly__hydrops',
        'patient_mucopoly__Tone', 'patient_mucopoly__Power', 'patient_mucopoly__Reflexes', 'patient_mucopoly__ataxia',
        'patient_mucopoly__Signs_of_raised_ICT', 'patient_mucopoly__Symptoms_of_CTS', 'patient_mucopoly__IQ',
        'patient_mucopoly__iq_value', 'patient_mucopoly__DQ', 'patient_mucopoly__dq_value',
        'patient_mucopoly__corneal_clouding', 'patient_mucopoly__papilledema', 'patient_mucopoly__glaucoma',
        'patient_mucopoly__optic_nerve_atrophy', 'patient_mucopoly__retinal_degeneration_pigmentation',
        'patient_mucopoly__corneal_opacity', 'patient_mucopoly__cataract', 'patient_mucopoly__squint',
        'patient_mucopoly__nystagmus', 'patient_mucopoly__any_other_specify', 'patient_mucopoly__Cardiomyopathy',
        'patient_mucopoly__Congestive_Heart_failure', 'patient_mucopoly__Cor_pulomonale',
        'patient_mucopoly__Valvular_involvement',
        'patient_mucopoly__Enlarged_tonsils',
        'patient_mucopoly__Sleep_apnea', 'patient_mucopoly__Reactive_Airway_Disease', 'patient_mucopoly__Dyspnea',
        'patient_mucopoly__Gum_hyperplasia', 'patient_mucopoly__hepatomegaly', 'patient_mucopoly__size_hepatomegaly',
        'patient_mucopoly__span_hepatomegaly', 'patient_mucopoly__Splenomegaly', 'patient_mucopoly__size_splenomegaly',
        'patient_mucopoly__hernia', 'patient_mucopoly__specify_if', 'patient_mucopoly__Umbilical_hernia',
        'patient_mucopoly__Inguinal_hernia', 'patient_mucopoly__Joint_Contractures',
        'patient_mucopoly__Joint_arthritis',
        'patient_mucopoly__Joint_laxity', 'patient_mucopoly__Scoliosis', 'patient_mucopoly__Kyphosis_Gibbus',
        'patient_mucopoly__Genu_valgum', 'patient_mucopoly__Pes_Cavus', 'patient_mucopoly__Toe_Walking',
        'patient_mucopoly__Echocardiography', 'patient_mucopoly__abnormal_finding', 'patient_mucopoly__Ultrasonography',
        'patient_mucopoly__Liver_Size_volume', 'patient_mucopoly__Spleen_Size_Volume',
        'patient_mucopoly__Skull_J_shaped_sella', 'patient_mucopoly__Spine_Beaked_vertebra',
        'patient_mucopoly__Central_lower_tick', 'patient_mucopoly__Metacarpals_Bullet_shaped',
        'patient_mucopoly__Ribs_oar_shaped', 'patient_mucopoly__Pelvis_Hip_dysplasia',
        'patient_mucopoly__Dislocation_of_hip', 'patient_mucopoly__Flared_iliac_wings', 'patient_mucopoly__Long_bones',
        'patient_mucopoly__Dexa_Z_score', 'patient_mucopoly__if_done_specify', 'patient_mucopoly__EPS_for_CTS',
        'patient_mucopoly__If_abnormal_specify_findings', 'patient_mucopoly__Pulmonary_function_test',
        'patient_mucopoly__if_yes', 'patient_mucopoly__if_abnormal_finding_specify', 'patient_mucopoly__CT_Scan',
        'patient_mucopoly__Specify_findings_if_abnormall', 'patient_mucopoly__MRI_Brain',
        'patient_mucopoly__Specify_findings_if_abnormal_mri', 'patient_mucopoly__EEG',
        'patient_mucopoly__Specify_findings_if_abnormal_eeg', 'patient_mucopoly__Corneal_clouding1',
        'patient_mucopoly__Fundus', 'patient_mucopoly__Specify_if_abnormal', 'patient_mucopoly__Glaucoma1',
        'patient_mucopoly__Hearing_Assessment', 'patient_mucopoly__if_abnormal', 'patient_mucopoly__Sleep_Studies',
        'patient_mucopoly__Specify_findings_if_abnormal', 'patient_mucopoly__Urine_spot_test',
        'patient_mucopoly__Urinary_GAGs_analysis', 'patient_mucopoly__Patient_urine',
        'patient_mucopoly__Normal_Control_urine', 'patient_mucopoly__Normal_range_urine',
        'patient_mucopoly__enzyme_var',
        'patient_mucopoly__Other_specify', 'patient_mucopoly__enzyme_sam', 'patient_mucopoly__Patient_enzyme',
        'patient_mucopoly__Normal_Control', 'patient_mucopoly__Normal_range',
        'patient_mucopoly__Causative_DNA_sequence_variation', 'patient_mucopoly__molecular_upload',
        'patient_mucopoly__Patient_molecular',
        'patient_mucopoly__Gene_molecula', 'patient_mucopoly__trans_molecul', 'patient_mucopoly__mul_dna1',
        'patient_mucopoly__mul_pro1', 'patient_mucopoly__mul_var1', 'patient_mucopoly__mul_zygo1',
        'patient_mucopoly__mul_var_cla1',
        'patient_mucopoly__mul_dna2', 'patient_mucopoly__mul_pro2', 'patient_mucopoly__mul_var2',
        'patient_mucopoly__mul_zygo2', 'patient_mucopoly__mul_var_cla2',
        'patient_mucopoly__mul_seg',
        'patient_mucopoly__father', 'patient_mucopoly__mother',
        'patient_mucopoly__Enzyme_Replacement_Therapy', 'patient_mucopoly__Date_of_initiation',
        'patient_mucopoly__Age_of_Start', 'patient_mucopoly__Dosage', 'patient_mucopoly__Duration',
        'patient_mucopoly__Adverse_events', 'patient_mucopoly__if_yes_specify', 'patient_mucopoly__Any_interruption',
        'patient_mucopoly__Reason_for_interruption', 'patient_mucopoly__Duration_of_interruption',
        'patient_mucopoly__Response', 'patient_mucopoly__Bone_Marrow_Transplantation', 'patient_mucopoly__date',
        'patient_mucopoly__Donor', 'patient_mucopoly__Hospital', 'patient_mucopoly__Response',
        'patient_mucopoly__Surgery',
        'patient_mucopoly__Hernia_surgery', 'patient_mucopoly__Age_at_surgery',
        'patient_mucopoly__Calcium_and_multivitamin_supplements', 'patient_mucopoly__Regular_Physiotherapy',
        'patient_mucopoly__Any_ocular_medication', 'patient_mucopoly__CPAP_BiPAP_for_sleep_apnea',
        'patient_mucopoly__Finaldiagnosis',
        'patient_mucopoly__Finaloutcomes',
        'patient_mucopoly__mg_filed_by_name',
        'patient_mucopoly__mg_clinician_name',
        'patient_mucopoly__mg_filled_date'
    )

    for user in users:
        writer.writerow(user)

    return response






@login_required(login_url='login')
def update_qa_qc_muco(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    form2 = QAMGForm(instance=patient)

    if request.method == 'POST':
        form2 = QAMGForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_mg_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_muco.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_muco.html', context)



@login_required(login_url='login')
def view_qa_qc_muco(request, pk):
    user = request.user
    patient = profile_mucopolysaccharidosis.objects.get(id=pk)
    form2 = QAMGForm(instance=patient)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
