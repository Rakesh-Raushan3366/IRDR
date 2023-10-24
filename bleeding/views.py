import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


@login_required(login_url='login')
def add_record_bd(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = ProfilebleedingdisorderForm()
    if request.method == 'POST':
        form1 = ProfilebleedingdisorderForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(demographic_bd, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_bd.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_bd.html', context)


@login_required(login_url='login')
def view_profile_bd(request, pk):
    try:
        form1 = profile_bleeding.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_bd.html', context)


@login_required(login_url='login')
def update_patient_record_bd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_bleeding.objects.get(id=pk)

    form1 = ProfilebleedingdisorderForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfilebleedingdisorderForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect("total_record_bd")
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_bd.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_bd.html', context)


@login_required(login_url='login')
def demographic_bd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_bleeding.objects.get(id=pk)
    form1 = SocioDemographicDetailsFormbd()
    if request.method == 'POST':
        form1 = SocioDemographicDetailsFormbd(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.patient = patient
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_bd, args=(pk,)))
        else:
            context = {'form1': form1, }
            return render(request, 'demographic_bd.html', context)

    context = {'form1': form1, }
    return render(request, 'demographic_bd.html', context)


@login_required(login_url='login')
def update_record_bd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_bleeding.objects.get(id=pk)
    try:
        socio = demographic_bleeding.objects.get(patient=patient)
        form1 = SocioDemographicDetailsFormbd(instance=socio)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsFormbd(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect("total_record_bd")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_bd.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsFormbd(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_bd")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_bd.html', context)
        if request.method == 'POST' and 'save' in request.POST:
            form1 = SocioDemographicDetailsFormbd(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                # patient.complete = 'Yes'
                # patient.save()
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_bd.html', context)
    except:
        form1 = SocioDemographicDetailsFormbd()
        if request.method == 'POST':
            form1 = SocioDemographicDetailsFormbd(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                return redirect('total_record_bd')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_bd.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_bd.html', context)


@login_required(login_url='login')
def view_record_bd(request, pk):
    patient = profile_bleeding.objects.get(id=pk)
    try:
        form1 = demographic_bleeding.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_record_bd.html', context)


@login_required(login_url='login')
def total_record_bd(request):
    pat = profile_bleeding.objects.filter(user=request.user).order_by('bd_date_created')
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_bd.html', context)


@login_required(login_url='login')
def total_record_bd_admin(request):
    pat = profile_bleeding.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_bd_admin.html', context)


@login_required(login_url='login')
def delete_record_bd(request, pk):
    order = profile_bleeding.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_bd')

    context = {'order': order}
    return render(request, 'delete_record_bd.html', context)


def export_bleeding_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bleeding.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_record', 'date_of_clinical_exam', 'date_of_birth',
         'patient_name', 'father_name', 'mother_name',
         'paitent_id_yes_no', 'paitent_id', 'patient_id_no', 'mother_father_id', 'mother_father_id_no',
         'permanent_addr', 'state', 'district', 'city_name', 'country_name', 'land_line_no',
         'mother_mobile_no', 'father_mobile_no', 'email', 'religion', 'caste', 'gender',
         'referred_status', 'referred_by', 'referred_by_desc', 'consent_given', 'consent_upload',
         'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no', 'patient_edu_status',
         'patient_occupation', 'father_edu_status', 'father_occupation', 'mother_edu_status',
         'mother_occupation', 'monthly_income_status', 'diagnosis_type_1', 'diagnosis_type_other', 'anthr_weight',
         'anthr_height', 'anthr_head_circum', 'diagnosis_age', 'first_bleed_age',
         'bleeding_site', 'blood_pressure_type', 'blooding_fam_hist', 'fam_name', 'fam_reln',
         'fam_daignosis', 'test_center_name', 'diagnosis_method', 'blood_group', 'hiv_status',
         'hbv_status', 'hcv_status', 'factory_deficiency', 'factory_deficiency_other', 'factory_level_per',
         'factory_severity', 'vwf_antigen_per', 'vwf_method', 'vwf_ris_cofactor',
         'screening_test', 'quant_assay', 'inhibitor_method', 'inhibitor_titer', 'platelet_count',
         'platelet_agregatin_Ristocetin_low_dose', 'platelet_agregatin_Ristocetin_high_dose',
         'platelet_agregatin_ADP', 'platelet_agregatin_Collagen', 'platelet_agregatin_Epinephrine',
         'platelet_agregatin_Arachidonic_acid', 'platelet_agregatin_others', 'platelet_receptors_1',
         'platelet_receptors_2', 'platelet_receptors_3', 'platelet_receptors_4', 'platelet_receptors_5',
         'platelet_receptors_6', 'platelet_receptors_7', 'platelet_receptors_8',
         'platelet_receptors_9', 'platelet_receptors_others', 'mutation_identified', 'mutation_type',
         'final_diagnosis', 'fam_pedigree', 'diag_invest_report', 'carrier_studies',
         'carr_female_1_name', 'carr_female_1_adhaar', 'carr_female_1_dob', 'carr_female_1_age',
         'carr_female_1_rel_index', 'carr_female_1_status', 'carr_female_1_dos', 'carr_female_2_name',
         'carr_female_2_adhaar', 'carr_female_2_dob', 'carr_female_2_age', 'carr_female_2_rel_index',
         'carr_female_2_status', 'carr_female_2_dos', 'carr_any_other_details', 'ante_female_1_name',
         'ante_female_1_adhaar', 'ante_female_1_dob', 'ante_female_1_age', 'ante_female_1_rel_index',
         'ante_female_1_proc', 'ante_female_1_per_by', 'ante_female_1_dos', 'ante_female_1_res',
         'ante_other_info_1', 'ante_female_2_name', 'ante_female_2_adhaar', 'ante_female_2_dob',
         'ante_female_2_age', 'ante_female_2_rel_index', 'ante_female_2_proc', 'ante_female_2_per_by',
         'ante_female_2_dos', 'ante_female_2_res', 'ante_other_info_2', 'bleed_past_12', 'bleed_life_time',
         'spontaneous_past_12', 'spontaneous_life_time', 'traumatic_past_12',
         'traumatic_life_time', 'haemorrhages_past_12', 'haemorrhages_life_time', 'cns_past_12', 'cns_life_time',
         'muscle_past_12', 'muscle_life_time', 'mucosal_past_12', 'mucosal_life_time',
         'chronic_def', 'bleeds_others', 'first_fact_age', 'birth_exposure_days', 'transfusion_product',
         'transfusion_product_others', 'curr_mode_treatment', 'demand_bd_episodes',
         'demand_bd_duration', 'funding_source', 'funding_source_other', 'dose', 'frequency',
         'start_date', 'end_date', 'ongoing_status', 'duration', 'infusion_skill',
         'inhibitor_status',
         'any_other_info', 'surgery_num', 'surgery_1', 'surgery_1_transfusin',
         'surgery_1_transfusin_others', 'surgery_2', 'surgery_2_transfusin',
         'surgery_2_transfusin_others', 'surgery_3', 'surgery_3_transfusin',
         'surgery_3_transfusin_others', 'physical_dis_status', 'cronic_anthr', 'joint', 'target_joint', ])

    users = profile_bleeding.objects.filter(user=request.user).prefetch_related('patient_bleeding').values_list('register_id__institute_name', 'uniqueId', 'bd_icmr_unique_no', 'bd_final_diagnosis',
                                                                                                                'bd_date_of_record', 'bd_date_of_clinical_exam', 'bd_date_of_birth',
                                                                                                                'bd_patient_name', 'bd_father_name', 'bd_mother_name', 'bd_paitent_id_yes_no',
                                                                                                                'bd_paitent_id', 'bd_patient_id_no', 'bd_mother_father_id', 'bd_mother_father_id_no',
                                                                                                                'bd_permanent_addr', 'bd_state', 'bd_district', 'bd_city_name', 'bd_country_name',
                                                                                                                'bd_land_line_no', 'bd_mother_mobile_no', 'bd_father_mobile_no', 'bd_email',
                                                                                                                'bd_religion', 'bd_caste', 'bd_gender', 'bd_referred_status', 'bd_referred_by',
                                                                                                                'bd_referred_by_desc', 'bd_consent_given', 'bd_consent_upload', 'bd_assent_given',
                                                                                                                'bd_assent_upload', 'bd_hospital_name', 'bd_hospital_reg_no', 'patient_bleeding__bd_patient_edu_status',
                                                                                                                'patient_bleeding__bd_patient_occupation', 'patient_bleeding__bd_father_edu_status',
                                                                                                                'patient_bleeding__bd_father_occupation', 'patient_bleeding__bd_mother_edu_status',
                                                                                                                'patient_bleeding__bd_mother_occupation',
                                                                                                                'patient_bleeding__bd_monthly_income_status', 'patient_bleeding__bd_diagnosis_type_1',
                                                                                                                'patient_bleeding__bd_diagnosis_type_other', 'patient_bleeding__bd_anthr_weight',
                                                                                                                'patient_bleeding__bd_anthr_height',
                                                                                                                'patient_bleeding__bd_anthr_head_circum', 'patient_bleeding__bd_diagnosis_age',
                                                                                                                'patient_bleeding__bd_first_bleed_age', 'patient_bleeding__bd_bleeding_site',
                                                                                                                'patient_bleeding__bd_blood_pressure_type', 'patient_bleeding__bd_blooding_fam_hist',
                                                                                                                'patient_bleeding__bd_fam_name', 'patient_bleeding__bd_fam_reln', 'patient_bleeding__bd_fam_daignosis',
                                                                                                                'patient_bleeding__bd_test_center_name', 'patient_bleeding__bd_diagnosis_method',
                                                                                                                'patient_bleeding__bd_blood_group', 'patient_bleeding__bd_hiv_status',
                                                                                                                'patient_bleeding__bd_hbv_status', 'patient_bleeding__bd_hcv_status',
                                                                                                                'patient_bleeding__bd_factory_deficiency', 'patient_bleeding__bd_factory_deficiency_other',
                                                                                                                'patient_bleeding__bd_factory_level_per',
                                                                                                                'patient_bleeding__bd_factory_severity', 'patient_bleeding__bd_vwf_antigen_per',
                                                                                                                'patient_bleeding__bd_vwf_method', 'patient_bleeding__bd_vwf_ris_cofactor',
                                                                                                                'patient_bleeding__bd_screening_test', 'patient_bleeding__bd_quant_assay',
                                                                                                                'patient_bleeding__bd_inhibitor_method', 'patient_bleeding__bd_inhibitor_titer',
                                                                                                                'patient_bleeding__bd_platelet_count', 'patient_bleeding__bd_platelet_agregatin_Ristocetin_low_dose',
                                                                                                                'patient_bleeding__bd_platelet_agregatin_Ristocetin_high_dose',
                                                                                                                'patient_bleeding__bd_platelet_agregatin_ADP', 'patient_bleeding__bd_platelet_agregatin_Collagen',
                                                                                                                'patient_bleeding__bd_platelet_agregatin_Epinephrine',
                                                                                                                'patient_bleeding__bd_platelet_agregatin_Arachidonic_acid',
                                                                                                                'patient_bleeding__bd_platelet_agregatin_others',
                                                                                                                'patient_bleeding__bd_platelet_receptors_1', 'patient_bleeding__bd_platelet_receptors_2',
                                                                                                                'patient_bleeding__bd_platelet_receptors_3', 'patient_bleeding__bd_platelet_receptors_4',
                                                                                                                'patient_bleeding__bd_platelet_receptors_5',
                                                                                                                'patient_bleeding__bd_platelet_receptors_6', 'patient_bleeding__bd_platelet_receptors_7',
                                                                                                                'patient_bleeding__bd_platelet_receptors_8', 'patient_bleeding__bd_platelet_receptors_9',
                                                                                                                'patient_bleeding__bd_platelet_receptors_others', 'patient_bleeding__bd_mutation_identified',
                                                                                                                'patient_bleeding__bd_mutation_type', 'patient_bleeding__bd_final_diagnosis',
                                                                                                                'patient_bleeding__bd_fam_pedigree',
                                                                                                                'patient_bleeding__bd_diag_invest_report', 'patient_bleeding__bd_carrier_studies',
                                                                                                                'patient_bleeding__bd_carr_female_1_name', 'patient_bleeding__bd_carr_female_1_adhaar',
                                                                                                                'patient_bleeding__bd_carr_female_1_dob',
                                                                                                                'patient_bleeding__bd_carr_female_1_age', 'patient_bleeding__bd_carr_female_1_rel_index',
                                                                                                                'patient_bleeding__bd_carr_female_1_status', 'patient_bleeding__bd_carr_female_1_dos',
                                                                                                                'patient_bleeding__bd_carr_female_2_name',
                                                                                                                'patient_bleeding__bd_carr_female_2_adhaar', 'patient_bleeding__bd_carr_female_2_dob',
                                                                                                                'patient_bleeding__bd_carr_female_2_age', 'patient_bleeding__bd_carr_female_2_rel_index',
                                                                                                                'patient_bleeding__bd_carr_female_2_status',
                                                                                                                'patient_bleeding__bd_carr_female_2_dos', 'patient_bleeding__bd_carr_any_other_details',
                                                                                                                'patient_bleeding__bd_ante_female_1_name', 'patient_bleeding__bd_ante_female_1_adhaar',
                                                                                                                'patient_bleeding__bd_ante_female_1_dob',
                                                                                                                'patient_bleeding__bd_ante_female_1_age', 'patient_bleeding__bd_ante_female_1_rel_index',
                                                                                                                'patient_bleeding__bd_ante_female_1_proc', 'patient_bleeding__bd_ante_female_1_per_by',
                                                                                                                'patient_bleeding__bd_ante_female_1_dos',
                                                                                                                'patient_bleeding__bd_ante_female_1_res', 'patient_bleeding__bd_ante_other_info_1',
                                                                                                                'patient_bleeding__bd_ante_female_2_name', 'patient_bleeding__bd_ante_female_2_adhaar',
                                                                                                                'patient_bleeding__bd_ante_female_2_dob',
                                                                                                                'patient_bleeding__bd_ante_female_2_age', 'patient_bleeding__bd_ante_female_2_rel_index',
                                                                                                                'patient_bleeding__bd_ante_female_2_proc', 'patient_bleeding__bd_ante_female_2_per_by',
                                                                                                                'patient_bleeding__bd_ante_female_2_dos',
                                                                                                                'patient_bleeding__bd_ante_female_2_res', 'patient_bleeding__bd_ante_other_info_2',
                                                                                                                'patient_bleeding__bd_bleed_past_12', 'patient_bleeding__bd_bleed_life_time',
                                                                                                                'patient_bleeding__bd_spontaneous_past_12',
                                                                                                                'patient_bleeding__bd_spontaneous_life_time', 'patient_bleeding__bd_traumatic_past_12',
                                                                                                                'patient_bleeding__bd_traumatic_life_time', 'patient_bleeding__bd_haemorrhages_past_12',
                                                                                                                'patient_bleeding__bd_haemorrhages_life_time',
                                                                                                                'patient_bleeding__bd_cns_past_12', 'patient_bleeding__bd_cns_life_time',
                                                                                                                'patient_bleeding__bd_muscle_past_12', 'patient_bleeding__bd_muscle_life_time',
                                                                                                                'patient_bleeding__bd_mucosal_past_12', 'patient_bleeding__bd_mucosal_life_time',
                                                                                                                'patient_bleeding__bd_chronic_def', 'patient_bleeding__bd_bleeds_others',
                                                                                                                'patient_bleeding__bd_first_fact_age', 'patient_bleeding__bd_birth_exposure_days',
                                                                                                                'patient_bleeding__bd_transfusion_product',
                                                                                                                'patient_bleeding__bd_transfusion_product_others', 'patient_bleeding__bd_curr_mode_treatment',
                                                                                                                'patient_bleeding__bd_demand_bd_episodes', 'patient_bleeding__bd_demand_bd_duration',
                                                                                                                'patient_bleeding__bd_funding_source',
                                                                                                                'patient_bleeding__bd_funding_source_other', 'patient_bleeding__bd_dose', 'patient_bleeding__bd_frequency',
                                                                                                                'patient_bleeding__bd_start_date', 'patient_bleeding__bd_end_date', 'patient_bleeding__bd_ongoing_status',
                                                                                                                'patient_bleeding__bd_duration',
                                                                                                                'patient_bleeding__bd_infusion_skill', 'patient_bleeding__bd_inhibitor_status',
                                                                                                                'patient_bleeding__bd_any_other_info', 'patient_bleeding__bd_surgery_num',
                                                                                                                'patient_bleeding__bd_surgery_1',
                                                                                                                'patient_bleeding__bd_surgery_1_transfusin', 'patient_bleeding__bd_surgery_1_transfusin_others',
                                                                                                                'patient_bleeding__bd_surgery_2',
                                                                                                                'patient_bleeding__bd_surgery_2_transfusin',
                                                                                                                'patient_bleeding__bd_surgery_2_transfusin_others',
                                                                                                                'patient_bleeding__bd_surgery_3', 'patient_bleeding__bd_surgery_3_transfusin',
                                                                                                                'patient_bleeding__bd_surgery_3_transfusin_others',
                                                                                                                'patient_bleeding__bd_physical_dis_status', 'patient_bleeding__bd_cronic_anthr',
                                                                                                                'patient_bleeding__bd_joint', 'patient_bleeding__bd_target_joint', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def update_qa_qc_bleeding(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_bleeding.objects.get(id=pk)
    form2 = QAbleedingForm(instance=patient)

    if request.method == 'POST':
        form2 = QAbleedingForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_bd_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_bleeding.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_bleeding.html', context)


@login_required(login_url='login')
def view_qa_qc_bleeding(request, pk):
    user = request.user
    patient = profile_bleeding.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
