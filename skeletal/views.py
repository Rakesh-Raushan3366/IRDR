import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


@login_required(login_url='login')
def add_record_skeletal(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = skeletal_RegistrationForm()
    if request.method == 'POST':
        form1 = skeletal_RegistrationForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(skeletal_demographic, args=(auth1.id,)))

    context = {'form1': form1, }
    return render(request, 'add_record_skeletal.html', context)


@login_required(login_url='login')
def update_patient_record_skeletal(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_skeletal.objects.get(id=pk)
    form1 = skeletal_RegistrationForm(instance=patient)
    if request.method == 'POST':
        form1 = skeletal_RegistrationForm(request.POST, request.FILES, instance=patient)
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_skd')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_skeletal.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_skeletal.html', context)


@login_required(login_url='login')
def view_profile_record(request, pk):
    try:
        form1 = profile_skeletal.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_skeletal_profile_record.html', context)


@login_required(login_url='login')
def skeletal_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_skeletal.objects.get(id=pk)
    form1 = skeletal_SocioDemographicDetailsForm()
    if request.method == 'POST':
        form1 = skeletal_SocioDemographicDetailsForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()

            return HttpResponseRedirect(reverse(update_skeletal_demographic, args=(pk,)))

        else:
            context = {'form1': form1, }
            return render(request, 'skeletal_demographic.html', context)

    context = {'form1': form1, }
    return render(request, 'skeletal_demographic.html', context)


@login_required(login_url='login')
def update_skeletal_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_skeletal.objects.get(id=pk)
    try:
        form5 = demographic_skeletal.objects.get(patient=patient)
        form1 = skeletal_SocioDemographicDetailsForm(instance=form5)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = skeletal_SocioDemographicDetailsForm(request.POST, request.FILES, instance=form5)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                # patient.complete = 'Yes'
                # patient.save()
                return redirect('total_record_skd')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_skeletal_demographic.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = skeletal_SocioDemographicDetailsForm(request.POST, request.FILES, instance=form5)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_skd")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_skeletal_demographic.html', context)

        if request.method == 'POST' and 'save' in request.POST:
            form1 = skeletal_SocioDemographicDetailsForm(request.POST, request.FILES, instance=form5)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_skeletal_demographic.html', context)
    except:
        form1 = skeletal_SocioDemographicDetailsForm()
        if request.method == 'POST':
            form1 = skeletal_SocioDemographicDetailsForm(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()

                return redirect('total_record_skd')

            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_skeletal_demographic.html', context)

    context = {'form1': form1,'patient': patient }
    return render(request, 'update_skeletal_demographic.html', context)


@login_required(login_url='login')
def skeletal_total_record(request):
    register = profile_skeletal.objects.all()
    context = {'register': register, }
    return render(request, 'skeletal_total_record.html', context)


@login_required(login_url='login')
def view_skeletal_record(request, pk):
    patient = profile_skeletal.objects.get(id=pk)
    try:
        form1 = demographic_skeletal.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_skeletal_record.html', context)


@login_required(login_url='login')
def total_record_skd(request):
    pat = profile_skeletal.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_skd.html', context)


@login_required(login_url='login')
def total_record_skd_admin(request):
    pat = profile_skeletal.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_skd_admin.html', context)


@login_required(login_url='login')
def delete_record_skd(request, pk):
    order = profile_skeletal.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_skd')

    context = {'order': order}
    return render(request, 'delete_record_skd.html', context)


def export_skeletal_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skeletal.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_skeletal_sk_final_diagnosis',
         'patient_skeletal_sk_date_of_records', 'patient_skeletal_sk_date_of_clinical_exam',
         'patient_skeletal_sk_date_of_birth',
         'patient_skeletal_sk_patient_name', 'patient_skeletal_sk_father_name',
         'patient_skeletal_sk_mother_name',
         'patient_skeletal_sk_paitent_id_yes_no', 'patient_skeletal_sk_paitent_id', 'patient_skeletal_sk_patient_id_no',
         'patient_skeletal_sk_father_mother_id', 'patient_skeletal_sk_father_mother_id_no',
         'patient_skeletal_sk_permanent_addr', 'patient_skeletal_sk_state', 'patient_skeletal_sk_district',
         'patient_skeletal_sk_city_name', 'patient_skeletal_sk_country_name', 'patient_skeletal_sk_land_line_no',
         'patient_skeletal_sk_mother_mobile_no', 'patient_skeletal_sk_father_mobile_no', 'patient_skeletal_sk_email',
         'patient_skeletal_sk_religion', 'patient_skeletal_sk_caste', 'patient_skeletal_sk_gender',
         'patient_skeletal_sk_referred_status', 'patient_skeletal_sk_referred_by',
         'patient_skeletal_sk_referred_by_desc', 'patient_skeletal_sk_consent_given',
         'patient_skeletal_sk_consent_upload',
         'patient_skeletal_sk_assent_given', 'patient_skeletal_sk_assent_upload', 'patient_skeletal_sk_hospital_name',
         'patient_skeletal_sk_hospital_reg_no', 'patient_skeletal_sk_Patient_education',
         'patient_skeletal_sk_Patient_occupation', 'patient_skeletal_sk_Father_education',
         'patient_skeletal_sk_Father_occupation', 'patient_skeletal_sk_Mother_education',
         'patient_skeletal_sk_Mother_occupation', 'patient_skeletal_sk_Monthly_family_income',
         'patient_skeletal_sk_weight_patient',
         'patient_skeletal_sk_weight_percentile',
         'patient_skeletal_sk_weight_sd',
         'patient_skeletal_sk_height_patient',
         'patient_skeletal_sk_height_percentile',
         'patient_skeletal_sk_height_sd',
         'patient_skeletal_sk_Lower_segment_patient',
         'patient_skeletal_sk_Lower_segment_percentile',
         'patient_skeletal_sk_Lower_segment_sd',
         'patient_skeletal_sk_US_LS_Ratio_patient',
         'patient_skeletal_sk_US_LS_Ratio_percentile',
         'patient_skeletal_sk_US_LS_Ratio_sd',
         'patient_skeletal_sk_Head_circumference_patient',
         'patient_skeletal_sk_Head_circumference_percentile',
         'patient_skeletal_sk_Head_circumference_sd',
         'patient_skeletal_sk_Arm_span_patient',
         'patient_skeletal_sk_Arm_span_percentile',
         'patient_skeletal_sk_Arm_span_sd',
         'patient_skeletal_sk_Age_at_onset_of_symptoms_year',
         'patient_skeletal_sk_Age_at_onset_of_symptoms_month',
         'patient_skeletal_sk_Age_at_onset_of_symptoms_day',
         'patient_skeletal_sk_Age_at_onset_of_symptoms_Intrauterine',
         'patient_skeletal_sk_Age_at_presentation_year',
         'patient_skeletal_sk_Age_at_presentation_month',
         'patient_skeletal_sk_Age_at_presentation_day',
         'patient_skeletal_sk_Age_at_presentation_Intrauterine',
         'patient_skeletal_sk_Age_at_diagnosis_year',
         'patient_skeletal_sk_Age_at_diagnosis_month',
         'patient_skeletal_sk_Age_at_diagnosis_day',
         'patient_skeletal_sk_Age_at_diagnosis_Intrauterine',
         'patient_skeletal_sk_Pedigree_to_be_uploaded',
         'patient_skeletal_sk_positive_family_history',

         'patient_skeletal_sk_Family_history_specify',

         'patient_skeletal_sk_Consanguinity',
         'patient_skeletal_sk_Consanguinity_specify',

         'patient_skeletal_sk_Ultrasound_Polyhydramnios',

         'patient_skeletal_sk_Ultrasound_Any_other_antenatal_investigations',

         'patient_skeletal_sk_Ultrasound_Short_long_Bones_Bending',

         'patient_skeletal_sk_Ultrasound_Short_long_Bones_Bending_gestation_period',

         'patient_skeletal_sk_Ultrasound_Hydrops',

         'patient_skeletal_sk_Natal_History_Type_of_delivery',

         'patient_skeletal_sk_Natal_History_Baby_cried_immediately_after_delivery',

         'patient_skeletal_sk_Natal_History_Resuscitation_required',

         'patient_skeletal_sk_Natal_History_Resuscitation_specify',

         'patient_skeletal_sk_Natal_History_o_2',

         'patient_skeletal_sk_Natal_History_ventilation',

         'patient_skeletal_sk_Natal_History_NICU_stay',

         'patient_skeletal_sk_Natal_History_NICU_stay_specify',

         'patient_skeletal_sk_Natal_History_NICU_stay_other',

         'patient_skeletal_sk_Other_Birth_weight',
         'patient_skeletal_sk_Other_Birth_length',
         'patient_skeletal_sk_Other_Birth_head_circumference',
         'patient_skeletal_sk_Other_Short_Bones',
         'patient_skeletal_sk_Other_Any_other_malformation',
         'patient_skeletal_sk_Other_joint_contractures',
         'patient_skeletal_sk_Other_Fractures',

         'patient_skeletal_sk_Development_milestones',
         'patient_skeletal_sk_if_delayed_Motor',
         'patient_skeletal_sk_if_delayed_Global',
         'patient_skeletal_sk_if_delayed_Cognitive',
         'patient_skeletal_sk_history',
         'patient_skeletal_sk_Any_Fractures',
         'patient_skeletal_sk_Any_Fractures_number',

         'patient_skeletal_sk_Natal_History_NICU_stay_Gestation_at_delivery',

         'patient_skeletal_sk_Any_hearing_impairment',
         'patient_skeletal_sk_Any_visual_problems',
         'patient_skeletal_sk_Any_surgical_intervation',
         'patient_skeletal_sk_Any_surgical_intervation_specify',

         'patient_skeletal_sk_Development_delay',

         'patient_skeletal_sk_IQ_done',
         'patient_skeletal_sk_IQ_done_value',

         'patient_skeletal_sk_DQ_done',
         'patient_skeletal_sk_DQ_done_value',

         'patient_skeletal_sk_Upper_limb_Rhizomelic_shortening',
         'patient_skeletal_sk_Upper_limb_Rhizomelic_shortening_right',

         'patient_skeletal_sk_Upper_limb_Rhizomelic_shortening_left',

         'patient_skeletal_sk_Upper_limb_Mesomelic_shortening',
         'patient_skeletal_sk_Upper_limb_Mesomelic_shortening_right',

         'patient_skeletal_sk_Upper_limb_Mesomelic_shortening_left',

         'patient_skeletal_sk_Upper_limb_Acromelic_shortening',
         'patient_skeletal_sk_Upper_limb_Acromelic_shortening_right',

         'patient_skeletal_sk_Upper_limb_Acromelic_shortening_left',

         'patient_skeletal_sk_Upper_limb_hypoplastic_radius',
         'patient_skeletal_sk_Upper_limb_hypoplastic_radius_right',

         'patient_skeletal_sk_Upper_limb_hypoplastic_radius_left',

         'patient_skeletal_sk_Upper_limb_hypoplastic_ulna',
         'patient_skeletal_sk_Upper_limb_hypoplastic_ulna_right',

         'patient_skeletal_sk_Upper_limb_hypoplastic_ulna_left',

         'patient_skeletal_sk_Upper_limb_Polydactyly_hand_Preaxial',
         'patient_skeletal_sk_Upper_limb_Polydactyly_hand_Preaxial_right',

         'patient_skeletal_sk_Upper_limb_Polydactyly_hand_Preaxial_left',

         'patient_skeletal_sk_Upper_limb_Ectrodactyly',
         'patient_skeletal_sk_Upper_limb_Ectrodactyly_right_right',

         'patient_skeletal_sk_Upper_limb_Ectrodactyly_left',

         'patient_skeletal_sk_Upper_limb_Brachydactyly_hand',
         'patient_skeletal_sk_Upper_limb_Brachydactyly_hand_right',

         'patient_skeletal_sk_Upper_limb_Brachydactyly_hand_left',

         'patient_skeletal_sk_Upper_limb_Trident_hand',
         'patient_skeletal_sk_Upper_limb_Trident_hand_right',

         'patient_skeletal_sk_Upper_limb_Trident_hand_left',

         'patient_skeletal_sk_Upper_limb_Oligodactyly_hand',
         'patient_skeletal_sk_Upper_limb_Oligodactyly_hand_right',

         'patient_skeletal_sk_Upper_limb_Oligodactyly_hand_left',

         'patient_skeletal_sk_Upper_limb_Hypoplastic_thumb',
         'patient_skeletal_sk_Upper_limb_Hypoplastic_thumb_right',

         'patient_skeletal_sk_Upper_limb_Hypoplastic_thumb_left',

         'patient_skeletal_sk_Upper_limb_Syndactyly_Skin',
         'patient_skeletal_sk_Upper_limb_Syndactyly_Skin_right',

         'patient_skeletal_sk_Upper_limb_Syndactyly_Skin_left',

         'patient_skeletal_sk_Upper_limb_Joint_laxity',
         'patient_skeletal_sk_Upper_limb_Joint_laxity_right',

         'patient_skeletal_sk_Upper_limb_Joint_laxity_left',

         'patient_skeletal_sk_Upper_limb_Joint_contractures',
         'patient_skeletal_sk_Upper_limb_Joint_contractures_right',

         'patient_skeletal_sk_Upper_limb_Joint_contractures_left',

         'patient_skeletal_sk_Upper_limb_Deformities',
         'patient_skeletal_sk_Upper_limb_Deformities_right',

         'patient_skeletal_sk_Upper_limb_Deformities_left',

         'patient_skeletal_sk_Upper_limb_Any_other',

         'patient_skeletal_sk_Lower_limb_Rhizomelic_shortening',
         'patient_skeletal_sk_Lower_limb_Rhizomelic_shortening_right',

         'patient_skeletal_sk_Lower_limb_Rhizomelic_shortening_left',

         'patient_skeletal_sk_Lower_limb_Mesomelic_shortening',
         'patient_skeletal_sk_Lower_limb_Mesomelic_shortening_right',

         'patient_skeletal_sk_Lower_limb_Mesomelic_shortening_left',

         'patient_skeletal_sk_Lower_limb_Acromelic_shortening',
         'patient_skeletal_sk_Lower_limb_Acromelic_shortening_right',



         'patient_skeletal_sk_Lower_limb_hypoplastic_fibula',
         'patient_skeletal_sk_Lower_limb_hypoplastic_fibula_right',

         'patient_skeletal_sk_Lower_limb_hypoplastic_fibula_left',

         'patient_skeletal_sk_Lower_limb_hypoplastic_tibula',
         'patient_skeletal_sk_Lower_limb_hypoplastic_tibula_right',

         'patient_skeletal_sk_Lower_limb_hypoplastic_tibula_left',

         'patient_skeletal_sk_Lower_limb_hypoplastic_femur',
         'patient_skeletal_sk_Lower_limb_hypoplastic_femur_right',

         'patient_skeletal_sk_Lower_limb_hypoplastic_femur_left',

         'patient_skeletal_sk_Lower_limb_Polydactyly_foot',
         'patient_skeletal_sk_Lower_limb_Polydactyly_foot_right',

         'patient_skeletal_sk_Lower_limb_Polydactyly_foot_left',

         'patient_skeletal_sk_Lower_limb_Oligodactyly_foot',
         'patient_skeletal_sk_Lower_limb_Oligodactyly_foot_right',

         'patient_skeletal_sk_Lower_limb_Oligodactyly_foot_left',

         'patient_skeletal_sk_Lower_limb_Brachydactyly_foot',
         'patient_skeletal_sk_Lower_limb_Brachydactyly_foot_right',

         'patient_skeletal_sk_Lower_limb_Brachydactyly_foot_left',

         'patient_skeletal_sk_Lower_limb_Ectrodactyly_foot',
         'patient_skeletal_sk_Lower_limb_Ectrodactyly_foot_right',

         'patient_skeletal_sk_Lower_limb_Ectrodactyly_foot_left',

         'patient_skeletal_sk_Lower_limb_Hypoplastic_great_toe',
         'patient_skeletal_sk_Lower_limb_Hypoplastic_great_toe_right',

         'patient_skeletal_sk_Lower_limb_Hypoplastic_great_toe_left',

         'patient_skeletal_sk_Lower_limb_Hallux_vagus',
         'patient_skeletal_sk_Lower_limb_Hallux_vagus_right',

         'patient_skeletal_sk_Lower_limb_Hallux_vagus_left',

         'patient_skeletal_sk_Lower_limb_Broad_great_toe',
         'patient_skeletal_sk_Lower_limb_Broad_great_toe_right',

         'patient_skeletal_sk_Lower_limb_Broad_great_toe_left',

         'patient_skeletal_sk_Lower_limb_Deviated_great_toe',
         'patient_skeletal_sk_Lower_limb_Deviated_great_toe_right',

         'patient_skeletal_sk_Lower_limb_Deviated_great_toe_left',

         'patient_skeletal_sk_Lower_limb_Syndactyly_Skin',
         'patient_skeletal_sk_Lower_limb_Syndactyly_Skin_right',

         'patient_skeletal_sk_Lower_limb_Syndactyly_Skin_left',

         'patient_skeletal_sk_Lower_limb_Joint_laxity',
         'patient_skeletal_sk_Lower_limb_Joint_laxity_right',

         'patient_skeletal_sk_Lower_limb_Joint_laxity_left',

         'patient_skeletal_sk_Lower_limb_Joint_contractures',
         'patient_skeletal_sk_Lower_limb_Joint_contractures_right',

         'patient_skeletal_sk_Lower_limb_Joint_contractures_left',

         'patient_skeletal_sk_Lower_limb_Deformities',
         'patient_skeletal_sk_Lower_limb_Deformities_right',



         'patient_skeletal_sk_Lower_limb_Any_other',

         'patient_skeletal_sk_Face_upload_photograph',
         'patient_skeletal_sk_Frenula',
         'patient_skeletal_sk_Cleft_lip_palate',
         'patient_skeletal_sk_Cleft_lip_palate_right',

         'patient_skeletal_sk_Cleft_lip_palate_left',

         'patient_skeletal_sk_Dysmorphism',
         'patient_skeletal_sk_Dysmorphism_specify',

         'patient_skeletal_sk_high_prominent_forehead_Midface_hypoplasia',

         'patient_skeletal_sk_Abnormal_Hair',
         'patient_skeletal_sk_Abnormal_Hair_specify',

         'patient_skeletal_sk_Ear_abnormality',
         'patient_skeletal_sk_Blue_sclera',
         'patient_skeletal_sk_Dentition',
         'patient_skeletal_sk_Thorax_Narrow',
         'patient_skeletal_sk_Thorax_Carinatum',
         'patient_skeletal_sk_Thorax_Excavatum',

         'patient_skeletal_sk_Spine',
         'patient_skeletal_sk_Spine_abnormal',
         'patient_skeletal_sk_Genitalia',
         'patient_skeletal_sk_Skin_pigmentary_abnormalities',
         'patient_skeletal_sk_Skin_pigmentary_specify',
         'patient_skeletal_sk_Nail_hypoplasia',
         'patient_skeletal_sk_Eye_pigmentary_or_any_other_ocular_abnormality',

         'patient_skeletal_sk_Eye_pigmentary_specify',

         'patient_skeletal_sk_Invetigation_Date',
         'patient_skeletal_sk_Bone_health_assessment',

         'patient_skeletal_sk_S_Cal',
         'patient_skeletal_sk_Po4',
         'patient_skeletal_sk_SAP',
         'patient_skeletal_sk_Vit_D',
         'patient_skeletal_sk_PTH',
         'patient_skeletal_sk_DEXA_Scan_Z_score',
         'patient_skeletal_sk_x_ray_findings_Date',
         'patient_skeletal_sk_skull_ap',
         'patient_skeletal_sk_Dorso_lumbar_Spine_AP',
         'patient_skeletal_sk_Hands_with_wrist_AP',
         'patient_skeletal_sk_Chest_PA',
         'patient_skeletal_sk_Pelvis_with_both_hip_joints',
         'patient_skeletal_sk_Long_bones_AP',
         'patient_skeletal_sk_X_ray_cervical_spine_in_extension_and_flexion_AP',
         'patient_skeletal_sk_Any_other',
         'patient_skeletal_sk_CT_Scan_MRI_Brain',
         'patient_skeletal_sk_CT_Scan2',
         'patient_skeletal_sk_any_other_investigation_date',
         'patient_skeletal_sk_BERA_Audiogram',
         'patient_skeletal_sk_VEP',
         'patient_skeletal_sk_Ocular',
         'patient_skeletal_sk_Thyroid',
         'patient_skeletal_sk_ECHO',
         'patient_skeletal_sk_USG_abdomen',
         'patient_skeletal_sk_genetic_analysis_performed',
         'patient_skeletal_sk_genetic_analysis_performed_report',

         'patient_skeletal_sk_gene',
         'patient_skeletal_sk_tran',
         'patient_skeletal_sk_dna',
         'patient_skeletal_sk_pro',

         'patient_skeletal_sk_var',

         'patient_skeletal_sk_var_cla',
         'patient_skeletal_sk_seg',
         'patient_skeletal_sk_Patient_molecular',
         'patient_skeletal_sk_Gene_molecula',
         'patient_skeletal_sk_trans_molecul',
         'patient_skeletal_sk_mul_dna1',
         'patient_skeletal_sk_mul_pro1',

         'patient_skeletal_sk_mul_var1',

         'patient_skeletal_sk_mul_zygo1',

         'patient_skeletal_sk_mul_var_cla1',

         'patient_skeletal_sk_mul_dna2',
         'patient_skeletal_sk_mul_pro2',

         'patient_skeletal_sk_mul_var2',

         'patient_skeletal_sk_mul_zygo2',

         'patient_skeletal_sk_mul_var_cla2',
         'patient_skeletal_sk_mul_seg',
         'patient_skeletal_sk_father',
         'patient_skeletal_sk_mother',
         'patient_skeletal_sk_diagnosis',
         'patient_skeletal_sk_mention_novel_findings',
         'patient_skeletal_sk_Treatment_Bisphosphonates',

         'patient_skeletal_sk_Bisphosphonates_Pamidronate',
         'patient_skeletal_sk_Bisphosphona_Zolendronate',
         'patient_skeletal_sk_Bisphosphonate_Alendronate',
         'patient_skeletal_sk_Bisphosphon_Other',
         'patient_skeletal_sk_date_of_inititation',
         'patient_skeletal_sk_bisphosphonates_dose',

         'patient_skeletal_sk_bisphosphonates_duration',

         'patient_skeletal_sk_Treatment_Response',

         'patient_skeletal_sk_Any_Surgical_Procedure_Limb',
         'patient_skeletal_sk_Any_Surgical_Procedure_Hydrocephalus',
         'patient_skeletal_sk_Any_Surgical_Procedure_Craniosynostosis',
         'patient_skeletal_sk_Any_Surgical_Procedure_surgery',
         'patient_skeletal_sk_Any_Surgical_Procedure_joint',
         'patient_skeletal_sk_Any_Surgical_Procedure_other',

         'patient_skeletal_sk_other_surgical_information',
         'patient_skeletal_sk_Any_other_therapy',
         'patient_skeletal_sk_other_information',
         'patient_skeletal_sk_filed_by_name',
         'patient_skeletal_sk_clinician_name',
         'patient_skeletal_sk_filled_date',
         'patient_skeletal_sk_date_created',

         'patient_skeletal_sk_Final_outcome',

         'patient_skeletal_sk_Final_diagnosis',
         'patient_skeletal_sk_diagno_other',
         ])

    users = profile_skeletal.objects.all().prefetch_related('patient_skeletal').values_list(
        'register_id__institute_name', 'uniqueId', 'sk_icmr_unique_no', 'sk_final_diagnosis',
        'sk_date_of_records', 'sk_date_of_clinical_exam', 'sk_date_of_birth',
        'sk_patient_name', 'sk_father_name', 'sk_mother_name', 'sk_paitent_id_yes_no',
        'sk_paitent_id', 'sk_patient_id_no', 'sk_father_mother_id', 'sk_father_mother_id_no',
        'sk_permanent_addr', 'sk_state', 'sk_district', 'sk_city_name', 'sk_country_name',
        'sk_land_line_no', 'sk_mother_mobile_no', 'sk_father_mobile_no', 'sk_email',
        'sk_religion', 'sk_caste', 'sk_gender', 'sk_referred_status', 'sk_referred_by',
        'sk_referred_by_desc', 'sk_consent_given', 'sk_consent_upload', 'sk_assent_given',
        'sk_assent_upload', 'sk_hospital_name', 'sk_hospital_reg_no', 'patient_skeletal__sk_Patient_education',
        'patient_skeletal__sk_Patient_occupation', 'patient_skeletal__sk_Father_education',
        'patient_skeletal__sk_Father_occupation',
        'patient_skeletal__sk_Mother_education', 'patient_skeletal__sk_Mother_occupation',
        'patient_skeletal__sk_Monthly_family_income',

        'patient_skeletal__sk_weight_patient',
        'patient_skeletal__sk_weight_percentile',
        'patient_skeletal__sk_weight_sd',
        'patient_skeletal__sk_height_patient',
        'patient_skeletal__sk_height_percentile',
        'patient_skeletal__sk_height_sd',
        'patient_skeletal__sk_Lower_segment_patient',
        'patient_skeletal__sk_Lower_segment_percentile',
        'patient_skeletal__sk_Lower_segment_sd',
        'patient_skeletal__sk_US_LS_Ratio_patient',
        'patient_skeletal__sk_US_LS_Ratio_percentile',
        'patient_skeletal__sk_US_LS_Ratio_sd',
        'patient_skeletal__sk_Head_circumference_patient',
        'patient_skeletal__sk_Head_circumference_percentile',
        'patient_skeletal__sk_Head_circumference_sd',
        'patient_skeletal__sk_Arm_span_patient',
        'patient_skeletal__sk_Arm_span_percentile',
        'patient_skeletal__sk_Arm_span_sd',
        'patient_skeletal__sk_Age_at_onset_of_symptoms_year',
        'patient_skeletal__sk_Age_at_onset_of_symptoms_month',
        'patient_skeletal__sk_Age_at_onset_of_symptoms_day',
        'patient_skeletal__sk_Age_at_onset_of_symptoms_Intrauterine',
        'patient_skeletal__sk_Age_at_presentation_year',
        'patient_skeletal__sk_Age_at_presentation_month',
        'patient_skeletal__sk_Age_at_presentation_day',
        'patient_skeletal__sk_Age_at_presentation_Intrauterine',
        'patient_skeletal__sk_Age_at_diagnosis_year',
        'patient_skeletal__sk_Age_at_diagnosis_month',
        'patient_skeletal__sk_Age_at_diagnosis_day',
        'patient_skeletal__sk_Age_at_diagnosis_Intrauterine',
        'patient_skeletal__sk_Pedigree_to_be_uploaded',
        'patient_skeletal__sk_positive_family_history',

        'patient_skeletal__sk_Family_history_specify',

        'patient_skeletal__sk_Consanguinity',
        'patient_skeletal__sk_Consanguinity_specify',

        'patient_skeletal__sk_Ultrasound_Polyhydramnios',

        'patient_skeletal__sk_Ultrasound_Any_other_antenatal_investigations',

        'patient_skeletal__sk_Ultrasound_Short_long_Bones_Bending',

        'patient_skeletal__sk_Ultrasound_Short_long_Bones_Bending_gestation_period',

        'patient_skeletal__sk_Ultrasound_Hydrops',

        'patient_skeletal__sk_Natal_History_Type_of_delivery',

        'patient_skeletal__sk_Natal_History_Baby_cried_immediately_after_delivery',

        'patient_skeletal__sk_Natal_History_Resuscitation_required',

        'patient_skeletal__sk_Natal_History_Resuscitation_specify',

        'patient_skeletal__sk_Natal_History_o_2',

        'patient_skeletal__sk_Natal_History_ventilation',

        'patient_skeletal__sk_Natal_History_NICU_stay',

        'patient_skeletal__sk_Natal_History_NICU_stay_specify',

        'patient_skeletal__sk_Natal_History_NICU_stay_other',

        'patient_skeletal__sk_Other_Birth_weight',
        'patient_skeletal__sk_Other_Birth_length',
        'patient_skeletal__sk_Other_Birth_head_circumference',
        'patient_skeletal__sk_Other_Short_Bones',
        'patient_skeletal__sk_Other_Any_other_malformation',
        'patient_skeletal__sk_Other_joint_contractures',
        'patient_skeletal__sk_Other_Fractures',

        'patient_skeletal__sk_Development_milestones',
        'patient_skeletal__sk_if_delayed_Motor',
        'patient_skeletal__sk_if_delayed_Global',
        'patient_skeletal__sk_if_delayed_Cognitive',
        'patient_skeletal__sk_history',
        'patient_skeletal__sk_Any_Fractures',
        'patient_skeletal__sk_Any_Fractures_number',

        'patient_skeletal__sk_Natal_History_NICU_stay_Gestation_at_delivery',

        'patient_skeletal__sk_Any_hearing_impairment',
        'patient_skeletal__sk_Any_visual_problems',
        'patient_skeletal__sk_Any_surgical_intervation',
        'patient_skeletal__sk_Any_surgical_intervation_specify',

        'patient_skeletal__sk_Development_delay',

        'patient_skeletal__sk_IQ_done',
        'patient_skeletal__sk_IQ_done_value',

        'patient_skeletal__sk_DQ_done',
        'patient_skeletal__sk_DQ_done_value',

        'patient_skeletal__sk_Upper_limb_Rhizomelic_shortening',
        'patient_skeletal__sk_Upper_limb_Rhizomelic_shortening_right',

        'patient_skeletal__sk_Upper_limb_Rhizomelic_shortening_left',

        'patient_skeletal__sk_Upper_limb_Mesomelic_shortening',
        'patient_skeletal__sk_Upper_limb_Mesomelic_shortening_right',

        'patient_skeletal__sk_Upper_limb_Mesomelic_shortening_left',

        'patient_skeletal__sk_Upper_limb_Acromelic_shortening',
        'patient_skeletal__sk_Upper_limb_Acromelic_shortening_right',

        'patient_skeletal__sk_Upper_limb_Acromelic_shortening_left',

        'patient_skeletal__sk_Upper_limb_hypoplastic_radius',
        'patient_skeletal__sk_Upper_limb_hypoplastic_radius_right',

        'patient_skeletal__sk_Upper_limb_hypoplastic_radius_left',

        'patient_skeletal__sk_Upper_limb_hypoplastic_ulna',
        'patient_skeletal__sk_Upper_limb_hypoplastic_ulna_right',

        'patient_skeletal__sk_Upper_limb_hypoplastic_ulna_left',

        'patient_skeletal__sk_Upper_limb_Polydactyly_hand_Preaxial',
        'patient_skeletal__sk_Upper_limb_Polydactyly_hand_Preaxial_right',

        'patient_skeletal__sk_Upper_limb_Polydactyly_hand_Preaxial_left',

        'patient_skeletal__sk_Upper_limb_Ectrodactyly',
        'patient_skeletal__sk_Upper_limb_Ectrodactyly_right_right',

        'patient_skeletal__sk_Upper_limb_Ectrodactyly_left',

        'patient_skeletal__sk_Upper_limb_Brachydactyly_hand',
        'patient_skeletal__sk_Upper_limb_Brachydactyly_hand_right',

        'patient_skeletal__sk_Upper_limb_Brachydactyly_hand_left',

        'patient_skeletal__sk_Upper_limb_Trident_hand',
        'patient_skeletal__sk_Upper_limb_Trident_hand_right',

        'patient_skeletal__sk_Upper_limb_Trident_hand_left',

        'patient_skeletal__sk_Upper_limb_Oligodactyly_hand',
        'patient_skeletal__sk_Upper_limb_Oligodactyly_hand_right',

        'patient_skeletal__sk_Upper_limb_Oligodactyly_hand_left',

        'patient_skeletal__sk_Upper_limb_Hypoplastic_thumb',
        'patient_skeletal__sk_Upper_limb_Hypoplastic_thumb_right',

        'patient_skeletal__sk_Upper_limb_Hypoplastic_thumb_left',

        'patient_skeletal__sk_Upper_limb_Syndactyly_Skin',
        'patient_skeletal__sk_Upper_limb_Syndactyly_Skin_right',

        'patient_skeletal__sk_Upper_limb_Syndactyly_Skin_left',

        'patient_skeletal__sk_Upper_limb_Joint_laxity',
        'patient_skeletal__sk_Upper_limb_Joint_laxity_right',

        'patient_skeletal__sk_Upper_limb_Joint_laxity_left',

        'patient_skeletal__sk_Upper_limb_Joint_contractures',
        'patient_skeletal__sk_Upper_limb_Joint_contractures_right',

        'patient_skeletal__sk_Upper_limb_Joint_contractures_left',

        'patient_skeletal__sk_Upper_limb_Deformities',
        'patient_skeletal__sk_Upper_limb_Deformities_right',

        'patient_skeletal__sk_Upper_limb_Deformities_left',

        'patient_skeletal__sk_Upper_limb_Any_other',

        'patient_skeletal__sk_Lower_limb_Rhizomelic_shortening',
        'patient_skeletal__sk_Lower_limb_Rhizomelic_shortening_right',

        'patient_skeletal__sk_Lower_limb_Rhizomelic_shortening_left',

        'patient_skeletal__sk_Lower_limb_Mesomelic_shortening',
        'patient_skeletal__sk_Lower_limb_Mesomelic_shortening_right',

        'patient_skeletal__sk_Lower_limb_Mesomelic_shortening_left',

        'patient_skeletal__sk_Lower_limb_Acromelic_shortening',
        'patient_skeletal__sk_Lower_limb_Acromelic_shortening_right',


        'patient_skeletal__sk_Lower_limb_hypoplastic_fibula',
        'patient_skeletal__sk_Lower_limb_hypoplastic_fibula_right',

        'patient_skeletal__sk_Lower_limb_hypoplastic_fibula_left',

        'patient_skeletal__sk_Lower_limb_hypoplastic_tibula',
        'patient_skeletal__sk_Lower_limb_hypoplastic_tibula_right',

        'patient_skeletal__sk_Lower_limb_hypoplastic_tibula_left',

        'patient_skeletal__sk_Lower_limb_hypoplastic_femur',
        'patient_skeletal__sk_Lower_limb_hypoplastic_femur_right',

        'patient_skeletal__sk_Lower_limb_hypoplastic_femur_left',

        'patient_skeletal__sk_Lower_limb_Polydactyly_foot',
        'patient_skeletal__sk_Lower_limb_Polydactyly_foot_right',

        'patient_skeletal__sk_Lower_limb_Polydactyly_foot_left',

        'patient_skeletal__sk_Lower_limb_Oligodactyly_foot',
        'patient_skeletal__sk_Lower_limb_Oligodactyly_foot_right',

        'patient_skeletal__sk_Lower_limb_Oligodactyly_foot_left',

        'patient_skeletal__sk_Lower_limb_Brachydactyly_foot',
        'patient_skeletal__sk_Lower_limb_Brachydactyly_foot_right',

        'patient_skeletal__sk_Lower_limb_Brachydactyly_foot_left',

        'patient_skeletal__sk_Lower_limb_Ectrodactyly_foot',
        'patient_skeletal__sk_Lower_limb_Ectrodactyly_foot_right',

        'patient_skeletal__sk_Lower_limb_Ectrodactyly_foot_left',

        'patient_skeletal__sk_Lower_limb_Hypoplastic_great_toe',
        'patient_skeletal__sk_Lower_limb_Hypoplastic_great_toe_right',

        'patient_skeletal__sk_Lower_limb_Hypoplastic_great_toe_left',

        'patient_skeletal__sk_Lower_limb_Hallux_vagus',
        'patient_skeletal__sk_Lower_limb_Hallux_vagus_right',

        'patient_skeletal__sk_Lower_limb_Hallux_vagus_left',

        'patient_skeletal__sk_Lower_limb_Broad_great_toe',
        'patient_skeletal__sk_Lower_limb_Broad_great_toe_right',

        'patient_skeletal__sk_Lower_limb_Broad_great_toe_left',

        'patient_skeletal__sk_Lower_limb_Deviated_great_toe',
        'patient_skeletal__sk_Lower_limb_Deviated_great_toe_right',

        'patient_skeletal__sk_Lower_limb_Deviated_great_toe_left',

        'patient_skeletal__sk_Lower_limb_Syndactyly_Skin',
        'patient_skeletal__sk_Lower_limb_Syndactyly_Skin_right',

        'patient_skeletal__sk_Lower_limb_Syndactyly_Skin_left',

        'patient_skeletal__sk_Lower_limb_Joint_laxity',
        'patient_skeletal__sk_Lower_limb_Joint_laxity_right',

        'patient_skeletal__sk_Lower_limb_Joint_laxity_left',

        'patient_skeletal__sk_Lower_limb_Joint_contractures',
        'patient_skeletal__sk_Lower_limb_Joint_contractures_right',

        'patient_skeletal__sk_Lower_limb_Joint_contractures_left',

        'patient_skeletal__sk_Lower_limb_Deformities',
        'patient_skeletal__sk_Lower_limb_Deformities_right',



        'patient_skeletal__sk_Lower_limb_Any_other',

        'patient_skeletal__sk_Face_upload_photograph',
        'patient_skeletal__sk_Frenula',
        'patient_skeletal__sk_Cleft_lip_palate',
        'patient_skeletal__sk_Cleft_lip_palate_right',

        'patient_skeletal__sk_Cleft_lip_palate_left',

        'patient_skeletal__sk_Dysmorphism',
        'patient_skeletal__sk_Dysmorphism_specify',

        'patient_skeletal__sk_high_prominent_forehead_Midface_hypoplasia',

        'patient_skeletal__sk_Abnormal_Hair',
        'patient_skeletal__sk_Abnormal_Hair_specify',

        'patient_skeletal__sk_Ear_abnormality',
        'patient_skeletal__sk_Blue_sclera',
        'patient_skeletal__sk_Dentition',
        'patient_skeletal__sk_Thorax_Narrow',
        'patient_skeletal__sk_Thorax_Carinatum',
        'patient_skeletal__sk_Thorax_Excavatum',

        'patient_skeletal__sk_Spine',
        'patient_skeletal__sk_Spine_abnormal',
        'patient_skeletal__sk_Genitalia',
        'patient_skeletal__sk_Skin_pigmentary_abnormalities',
        'patient_skeletal__sk_Skin_pigmentary_specify',
        'patient_skeletal__sk_Nail_hypoplasia',
        'patient_skeletal__sk_Eye_pigmentary_or_any_other_ocular_abnormality',

        'patient_skeletal__sk_Eye_pigmentary_specify',

        'patient_skeletal__sk_Invetigation_Date',
        'patient_skeletal__sk_Bone_health_assessment',

        'patient_skeletal__sk_S_Cal',
        'patient_skeletal__sk_Po4',
        'patient_skeletal__sk_SAP',
        'patient_skeletal__sk_Vit_D',
        'patient_skeletal__sk_PTH',
        'patient_skeletal__sk_DEXA_Scan_Z_score',
        'patient_skeletal__sk_x_ray_findings_Date',
        'patient_skeletal__sk_skull_ap',
        'patient_skeletal__sk_Dorso_lumbar_Spine_AP',
        'patient_skeletal__sk_Hands_with_wrist_AP',
        'patient_skeletal__sk_Chest_PA',
        'patient_skeletal__sk_Pelvis_with_both_hip_joints',
        'patient_skeletal__sk_Long_bones_AP',
        'patient_skeletal__sk_X_ray_cervical_spine_in_extension_and_flexion_AP',
        'patient_skeletal__sk_Any_other',
        'patient_skeletal__sk_CT_Scan_MRI_Brain',
        'patient_skeletal__sk_CT_Scan2',
        'patient_skeletal__sk_any_other_investigation_date',
        'patient_skeletal__sk_BERA_Audiogram',
        'patient_skeletal__sk_VEP',
        'patient_skeletal__sk_Ocular',
        'patient_skeletal__sk_Thyroid',
        'patient_skeletal__sk_ECHO',
        'patient_skeletal__sk_USG_abdomen',
        'patient_skeletal__sk_genetic_analysis_performed',
        'patient_skeletal__sk_genetic_analysis_performed_report',

        'patient_skeletal__sk_gene',
        'patient_skeletal__sk_tran',
        'patient_skeletal__sk_dna',
        'patient_skeletal__sk_pro',

        'patient_skeletal__sk_var',

        'patient_skeletal__sk_var_cla',
        'patient_skeletal__sk_seg',
        'patient_skeletal__sk_Patient_molecular',
        'patient_skeletal__sk_Gene_molecula',
        'patient_skeletal__sk_trans_molecul',
        'patient_skeletal__sk_mul_dna1',
        'patient_skeletal__sk_mul_pro1',

        'patient_skeletal__sk_mul_var1',

        'patient_skeletal__sk_mul_zygo1',

        'patient_skeletal__sk_mul_var_cla1',

        'patient_skeletal__sk_mul_dna2',
        'patient_skeletal__sk_mul_pro2',

        'patient_skeletal__sk_mul_var2',

        'patient_skeletal__sk_mul_zygo2',

        'patient_skeletal__sk_mul_var_cla2',
        'patient_skeletal__sk_mul_seg',
        'patient_skeletal__sk_father',
        'patient_skeletal__sk_mother',
        'patient_skeletal__sk_diagnosis',
        'patient_skeletal__sk_mention_novel_findings',
        'patient_skeletal__sk_Treatment_Bisphosphonates',

        'patient_skeletal__sk_Bisphosphonates_Pamidronate',
        'patient_skeletal__sk_Bisphosphona_Zolendronate',
        'patient_skeletal__sk_Bisphosphonate_Alendronate',
        'patient_skeletal__sk_Bisphosphon_Other',
        'patient_skeletal__sk_date_of_inititation',
        'patient_skeletal__sk_bisphosphonates_dose',

        'patient_skeletal__sk_bisphosphonates_duration',

        'patient_skeletal__sk_Treatment_Response',

        'patient_skeletal__sk_Any_Surgical_Procedure_Limb',
        'patient_skeletal__sk_Any_Surgical_Procedure_Hydrocephalus',
        'patient_skeletal__sk_Any_Surgical_Procedure_Craniosynostosis',
        'patient_skeletal__sk_Any_Surgical_Procedure_surgery',
        'patient_skeletal__sk_Any_Surgical_Procedure_joint',
        'patient_skeletal__sk_Any_Surgical_Procedure_other',

        'patient_skeletal__sk_other_surgical_information',
        'patient_skeletal__sk_Any_other_therapy',
        'patient_skeletal__sk_other_information',
        'patient_skeletal__sk_filed_by_name',
        'patient_skeletal__sk_clinician_name',
        'patient_skeletal__sk_filled_date',
        'patient_skeletal__sk_date_created',

        'patient_skeletal__sk_Final_outcome',

        'patient_skeletal__sk_Final_diagnosis',
        'patient_skeletal__sk_diagno_other',
          )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def update_qa_qc_skeletal(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_skeletal.objects.get(id=pk)
    form2 = QAskeletalForm(instance=patient)

    if request.method == 'POST':
        form2 = QAskeletalForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_skd_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_skeletal.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_skeletal.html', context)



@login_required(login_url='login')
def view_qa_qc_skeletal(request, pk):
    user = request.user
    patient = profile_skeletal.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
