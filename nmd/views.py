import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *


@login_required(login_url='login')
def add_record_nmd(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = ProfileNMDForm()
    if request.method == 'POST':
        form1 = ProfileNMDForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(nmd_demographic, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_nmd.html', context)

    context = {'form1': form1, }
    return render(request, 'add_record_nmd.html', context)


@login_required(login_url='login')
def update_patient_record_nmd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_nmd.objects.get(id=pk)

    form1 = ProfileNMDForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfileNMDForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect("total_record_nmd")
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_nmd.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_nmd.html', context)


@login_required(login_url='login')
def nmd_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_nmd.objects.get(id=pk)
    form1 = SocioDemographicDetailsNMDForm()
    form2 = DYSTOPHINOPATHYDetailsNMDForm()
    form3 = SpinalMuscularAtrophyDetailsNMDForm()
    form4 = LimbGirdleMuscularDystrophyDetailsNMDForm()

    # user1 = Registration.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = SocioDemographicDetailsNMDForm(request.POST, request.FILES, )
        form2 = DYSTOPHINOPATHYDetailsNMDForm(request.POST, request.FILES, )
        form3 = SpinalMuscularAtrophyDetailsNMDForm(request.POST, request.FILES, )
        form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(request.POST, request.FILES, )

        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():

            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()

            auth2 = form2.save(commit=False)
            auth2.user = user
            auth2.register = register
            auth2.patient = patient
            auth2.save()

            auth3 = form3.save(commit=False)
            auth3.user = user
            auth3.register = register
            auth3.patient = patient
            auth3.save()

            auth4 = form4.save(commit=False)
            auth4.user = user
            auth4.register = register
            auth4.patient = patient
            auth4.save()

            return HttpResponseRedirect(reverse(update_record_nmd, args=(pk,)))

        else:
            context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, }
            return render(request, 'nmd_demographic.html', context)

    context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, }
    return render(request, 'nmd_demographic.html', context)


@login_required(login_url='login')
def update_record_nmd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_nmd.objects.get(id=pk)
    try:
        socio = demographic_nmd.objects.get(patient=patient)
        develop = dsystophinopathy_nmd.objects.get(patient=patient)
        isaq = spinal_nmd.objects.get(patient=patient)
        isaa = limb_gridle_nmd.objects.get(patient=patient)
        form1 = SocioDemographicDetailsNMDForm(instance=socio)
        form2 = DYSTOPHINOPATHYDetailsNMDForm(instance=develop)
        form3 = SpinalMuscularAtrophyDetailsNMDForm(instance=isaq)
        form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(instance=isaa)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = SocioDemographicDetailsNMDForm(request.POST, request.FILES, instance=socio)
            form2 = DYSTOPHINOPATHYDetailsNMDForm(request.POST, request.FILES, instance=develop)
            form3 = SpinalMuscularAtrophyDetailsNMDForm(request.POST, request.FILES, instance=isaq)
            form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(request.POST, request.FILES, instance=isaa)
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                auth2 = form2.save(commit=False)
                auth2.user = user
                auth2.patient = patient
                auth2.register = register
                auth2.save()
                auth3 = form3.save(commit=False)
                auth3.user = user
                auth3.patient = patient
                auth3.register = register
                auth3.save()
                auth4 = form4.save(commit=False)
                auth4.user = user
                auth4.patient = patient
                auth4.register = register
                auth4.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect("total_record_nmd")
            else:
                context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, }
                return render(request, 'update_record_nmd.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = SocioDemographicDetailsNMDForm(request.POST, request.FILES, instance=socio)
            form2 = DYSTOPHINOPATHYDetailsNMDForm(request.POST, request.FILES, instance=develop)
            form3 = SpinalMuscularAtrophyDetailsNMDForm(request.POST, request.FILES, instance=isaq)
            form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(request.POST, request.FILES, instance=isaa)
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()
                auth2 = form2.save(commit=False)
                auth2.user = user
                auth2.patient = patient
                auth2.register = register
                auth2.save()
                auth3 = form3.save(commit=False)
                auth3.user = user
                auth3.patient = patient
                auth3.register = register
                auth3.save()
                auth4 = form4.save(commit=False)
                auth4.user = user
                auth4.patient = patient
                auth4.register = register
                auth4.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_nmd")
            else:
                context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4,'patient': patient, }
                return render(request, 'update_record_nmd.html', context)
        if request.method == 'POST' and 'save' in request.POST:
            form1 = SocioDemographicDetailsNMDForm(request.POST, request.FILES, instance=socio)
            form2 = DYSTOPHINOPATHYDetailsNMDForm(request.POST, request.FILES, instance=develop)
            form3 = SpinalMuscularAtrophyDetailsNMDForm(request.POST, request.FILES, instance=isaq)
            form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(request.POST, request.FILES, instance=isaa)
            if form1.is_valid():
                    auth1 = form1.save(commit=False)
                    auth1.user = user
                    auth1.patient = patient
                    auth1.register = register
                    auth1.save()
                    auth2 = form2.save(commit=False)
                    auth2.user = user
                    auth2.patient = patient
                    auth2.register = register
                    auth2.save()
                    auth3 = form3.save(commit=False)
                    auth3.user = user
                    auth3.patient = patient
                    auth3.register = register
                    auth3.save()
                    auth4 = form4.save(commit=False)
                    auth4.user = user
                    auth4.patient = patient
                    auth4.register = register
                    auth4.save()
                    # patient.complete = 'Yes'
                    # patient.save()
            else:
                    context = {'form1': form1,  'form2': form2, 'form3': form3, 'form4': form4,'patient': patient,}
                    return render(request, 'update_record_nmd.html', context)
    except:
        form1 = SocioDemographicDetailsNMDForm()
        form2 = DYSTOPHINOPATHYDetailsNMDForm()
        form3 = SpinalMuscularAtrophyDetailsNMDForm()
        form4 = LimbGirdleMuscularDystrophyDetailsNMDForm()
        if request.method == 'POST':
            form1 = SocioDemographicDetailsNMDForm(request.POST, request.FILES, )
            form2 = DYSTOPHINOPATHYDetailsNMDForm(request.POST, request.FILES, )
            form3 = SpinalMuscularAtrophyDetailsNMDForm(request.POST, request.FILES, )
            form4 = LimbGirdleMuscularDystrophyDetailsNMDForm(request.POST, request.FILES, )
            if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.patient = patient
                auth1.register = register
                auth1.save()

                auth2 = form2.save(commit=False)
                auth2.user = user
                auth2.patient = patient
                auth2.register = register
                auth2.save()

                auth3 = form3.save(commit=False)
                auth3.user = user
                auth3.patient = patient
                auth3.register = register
                auth3.save()

                auth4 = form4.save(commit=False)
                auth4.user = user
                auth4.patient = patient
                auth4.register = register
                auth4.save()
                return redirect('total_record_nmd')
            else:
                context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4,'patient': patient,  }
                return render(request, 'nmd_demographic.html', context)

    context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, 'patient': patient, }
    return render(request, 'update_record_nmd.html', context)


@login_required(login_url='login')
def view_profile_record_nmd(request, pk):
    try:
        form1 = profile_nmd.objects.get(id=pk)
    except:
        form1 = None

    context = {'form1': form1, }
    return render(request, 'view_profile_record_nmd.html', context)


@login_required(login_url='login')
def total_record_nmd(request):
    pat = profile_nmd.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_nmd.html', context)


@login_required(login_url='login')
def total_record_nmd_admin(request):
    pat = profile_nmd.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_nmd_admin.html', context)


@login_required(login_url='login')
def delete_record_nmd(request, pk):
    order = profile_nmd.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_nmd')

    context = {'order': order}
    return render(request, 'delete_record_nmd.html', context)


@login_required(login_url='login')
def view_record_nmd(request, pk):
    patient = profile_nmd.objects.get(id=pk)
    try:
        form1 = demographic_nmd.objects.get(patient=patient)
        form2 = dsystophinopathy_nmd.objects.get(patient=patient)
        form3 = spinal_nmd.objects.get(patient=patient)
        form4 = limb_gridle_nmd.objects.get(patient=patient)
    except:
        form1 = None
        form2 = None
        form3 = None
        form4 = None

    context = {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, }
    return render(request, 'view_record_nmd.html', context)


def export_dystonmd_csv_user(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_records', 'date_of_clinical_exam', 'date_of_birth', 'patient_name', 'father_name',
         'mother_name', 'paitent_id_yes_no', 'paitent_id', 'patient_id_no', 'father_mother_id', 'mother_father_no', 'permanent_addr', 'state', 'district', 'city_name',
         'country_name', 'land_line_no', 'mother_mobile_no', 'father_mobile_no', 'email', 'religion', 'caste', 'gender', 'referred_status', 'referred_by', 'referred_by_desc',
         'consent_given', 'consent_upload', 'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no', 'diagnosis_type', 'enrollment_status', 'diagnosis_age', 'aproximate_age',
         'symptoms_age_onset',
         'onset_age', 'pedigree', 'positive_family_hist', 'positive_family_siblings', 'positive_family_sibling_nubmer_affected', 'positive_family_cousins', 'positive_family_sCousins_nubmer_affected',
         'positive_family_Maternal_uncles', 'positive_family_Maternal_uncles_nubmer_affected', 'positive_family_Grand_materna', 'positive_family_Grand_materna_affected', 'positive_family_mothers',
         'difficulty_running_walking_fast', 'unable_rise_low_chair_floor', 'repeated_false', 'muscle_hypertrophy', 'mental_sub_normality', 'learning_disability', 'delayed_motor_milestrones',
         'symtoms_signs_other_specify', 'CEF_anthropometric_wieght', 'CEF_anthropometric_height', 'CEF_anthropometric_head_circumference', 'MP_MRC_grade_upperlimb_proximal_muscles',
         'MP_MRC_grade_upperlimb_distal_muscles', 'MP_MRC_grade_lowerlimb_proximal_muscles', 'MP_MRC_grade_lowerlimb_distal_muscles', 'functional_status_Independently_ambulant',
         'functional_status_NeedsPhysicalAssistance', 'functional_status_AmbulantHome', 'functional_status_WheelchairBound', 'functional_status_WheelchairBound_age', 'functional_status_BedBound',
         'functional_status_BedBound_age', 'functional_status_FunctionalScoreAvailable', 'functional_status_BrookeScale', 'functional_status_VignosScale', 'intelligent_quotient_tested',
         'intelligent_quotient_tested_if_yes', 'autism', 'Contractures_dmd', 'Contractures_ankle', 'Contractures_knee', 'Contractures_hips', 'Contractures_elbows', 'Scoliosis', 'Kyphosis', 'Respiratory_difficulty',
         'LaboratoryInvestigation_serum_ck_lvel', 'LaboratoryInvestigation_Cardiac_Evaluation', 'LaboratoryInvestigation_ecg_status', 'LaboratoryInvestigation_ecg_normal_abnormal', 'diagnosis_type',
         'LaboratoryInvestigation_2DECHO_status', 'LaboratoryInvestigation_2DECHO_normal_abnormal', 'diagnosis_type', 'pulmonary_function_tests', 'pulmonary_function_tests_normal_abnormal',
         'pulmonary_function_forced_vital_capacity', 'genetic_diagnosis_confirmed_mPCR', 'genetic_diagnosis_confirmed_MLPA', 'genetic_diagnosis_confirmed_MicroArray', 'genetic_diagnosis_confirmed_SangerSequencing',
         'genetic_diagnosis_confirmed_next_generation', 'genetic_diagnosis_next_generation', 'enetic_diagnosis_next_generation_TargetedPanel', 'enetic_diagnosis_next_generation_WholeExomeSequencing',
         'enetic_diagnosis_next_generation_WholeGenomeSequencing', 'upload_genetic_report', 'diagnosis_type', 'inframe_outframe', 'list_of_deleted_exons', 'list_of_duplicate_exons', 'mutation_identified_Missense',
         'mutation_identified_Missense_mutation', 'mutation_identified_Nonsense', 'mutation_identified_Nonsense_mutation', 'mutation_identified_Mutation', 'mutation_identified_Mutation_mutation',
         'mutation_identified_Frameshift', 'mutation_identified_Frameshift_mutation', 'mutation_identified_Splicesite', 'mutation_identified_Splicesite_mutation', 'mutation_identified_InframeInsertion',
         'mutation_identified_InframeInsertion_mutation', 'mutation_identified_InframeDeletion', 'mutation_identified_InframeDeletion_mutation', 'mutation_identified_INDEL', 'mutation_identified_INDEL_mutation',
         'mutation_identified_Others', 'mutation_identified_Others_mutation', 'gene_location', 'gene_variant', 'gene_Zygosity', 'gene_Disease', 'gene_Inheritance', 'gene_classification', 'Muscle_Biopsy',
         'Muscle_Biopsy_MuscleImmunohistochemistry', 'Muscle_Biopsy_MuscleImmunohistochemistry_if_yes', 'final_diagnosis', 'current_past_treatment_Steroids', 'current_past_treatment_Steroids_starting_age',
         'current_past_treatment_Prednisone', 'current_past_treatment_1', 'current_past_treatment_2', 'current_past_treatment_Deflazacort', 'current_past_treatment_Deflazacort_1',
         'current_past_treatment_Deflazacort_anyother_specify', 'current_past_treatment_Supplements', 'current_past_treatment_Supplements_calcium', 'current_past_treatment_Supplements_vit_D',
         'Respiratoryassistance_BiPAP', 'Respiratoryassistance_BiPAP_age', 'Respiratoryassistance_Ventilator', 'Respiratoryassistance_Ventilator_age', 'Tendon_lengthening_surgery',
         'Tendon_lengthening_surgery_if_yes_age', 'Surgicalcorrectionscoliosis', 'Surgicalcorrectionscoliosis_if_yes_age', 'last_follow_up', 'last_follow_up_if_yes', 'last_follow_up_if_yes_age', 'Functionalstatus',
         'functional_status_options', 'functional_score', 'functional_score_brooks_grade', 'functional_score_vignos_grade', 'outcome', 'outcome_age', 'oucome_cause_of_death', 'outcome_death_cause', 'death_place',
         'mother_carrier_status', 'mother_carrier_status_outcome', 'sister_carrier_status', 'sister_carrier_status_outcome',
         ])

    users = profile_nmd.objects.filter(user=request.user).prefetch_related('dystonmd', ).values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                                     'nmd_date_of_clinical_exam',
                                                                                                     'nmd_date_of_birth', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name',
                                                                                                     'nmd_paitent_id_yes_no',
                                                                                                     'nmd_paitent_id',
                                                                                                     'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                                     'nmd_city_name',
                                                                                                     'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                                     'nmd_caste',
                                                                                                     'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given',
                                                                                                     'nmd_consent_upload',
                                                                                                     'nmd_assent_given',
                                                                                                     'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                                     'dystonmd__NMD_diagnosis_type', 'dystonmd__NMD_enrollment_status', 'dystonmd__diagnosis_age',
                                                                                                     'dystonmd__aproximate_age',
                                                                                                     'dystonmd__symptoms_age_onset', 'dystonmd__onset_age', 'dystonmd__pedigree', 'dystonmd__positive_family_hist',
                                                                                                     'dystonmd__positive_family_siblings', 'dystonmd__positive_family_sibling_nubmer_affected',
                                                                                                     'dystonmd__positive_family_cousins',
                                                                                                     'dystonmd__positive_family_sCousins_nubmer_affected', 'dystonmd__positive_family_Maternal_uncles',
                                                                                                     'dystonmd__positive_family_Maternal_uncles_nubmer_affected', 'dystonmd__positive_family_Grand_materna',
                                                                                                     'dystonmd__positive_family_Grand_materna_affected', 'dystonmd__positive_family_mothers',
                                                                                                     'dystonmd__difficulty_running_walking_fast',
                                                                                                     'dystonmd__unable_rise_low_chair_floor', 'dystonmd__repeated_false', 'dystonmd__muscle_hypertrophy',
                                                                                                     'dystonmd__mental_sub_normality',
                                                                                                     'dystonmd__learning_disability', 'dystonmd__delayed_motor_milestrones', 'dystonmd__symtoms_signs_other_specify',
                                                                                                     'dystonmd__CEF_anthropometric_wieght', 'dystonmd__CEF_anthropometric_height',
                                                                                                     'dystonmd__CEF_anthropometric_head_circumference',
                                                                                                     'dystonmd__MP_MRC_grade_upperlimb_proximal_muscles', 'dystonmd__MP_MRC_grade_upperlimb_distal_muscles',
                                                                                                     'dystonmd__MP_MRC_grade_lowerlimb_proximal_muscles', 'dystonmd__MP_MRC_grade_lowerlimb_distal_muscles',
                                                                                                     'dystonmd__functional_status_Independently_ambulant', 'dystonmd__functional_status_NeedsPhysicalAssistance',
                                                                                                     'dystonmd__functional_status_AmbulantHome', 'dystonmd__functional_status_WheelchairBound',
                                                                                                     'dystonmd__functional_status_WheelchairBound_age',
                                                                                                     'dystonmd__functional_status_BedBound', 'dystonmd__functional_status_BedBound_age',
                                                                                                     'dystonmd__functional_status_FunctionalScoreAvailable',
                                                                                                     'dystonmd__functional_status_BrookeScale', 'dystonmd__functional_status_VignosScale',
                                                                                                     'dystonmd__intelligent_quotient_tested',
                                                                                                     'dystonmd__intelligent_quotient_tested_if_yes', 'dystonmd__autism', 'dystonmd__Contractures_dmd',
                                                                                                     'dystonmd__Contractures_ankle',
                                                                                                     'dystonmd__Contractures_knee', 'dystonmd__Contractures_hips', 'dystonmd__Contractures_elbows',
                                                                                                     'dystonmd__Scoliosis_dmd',
                                                                                                     'dystonmd__Kyphosis_dmd',
                                                                                                     'dystonmd__Respiratory_difficulty', 'dystonmd__LaboratoryInvestigation_serum_ck_lvel',
                                                                                                     'dystonmd__LaboratoryInvestigation_Cardiac_Evaluation',
                                                                                                     'dystonmd__LaboratoryInvestigation_ecg_status', 'dystonmd__LaboratoryInvestigation_ecg_normal_abnormal',
                                                                                                     'dystonmd__NMD_diagnosis_type',
                                                                                                     'dystonmd__LaboratoryInvestigation_2DECHO_status', 'dystonmd__LaboratoryInvestigation_2DECHO_normal_abnormal',
                                                                                                     'dystonmd__NMD_diagnosis_type',
                                                                                                     'dystonmd__pulmonary_function_tests', 'dystonmd__pulmonary_function_tests_normal_abnormal',
                                                                                                     'dystonmd__pulmonary_function_forced_vital_capacity', 'dystonmd__genetic_diagnosis_confirmed_mPCR',
                                                                                                     'dystonmd__genetic_diagnosis_confirmed_MLPA', 'dystonmd__genetic_diagnosis_confirmed_MicroArray',
                                                                                                     'dystonmd__genetic_diagnosis_confirmed_SangerSequencing', 'dystonmd__genetic_diagnosis_confirmed_next_generation',
                                                                                                     'dystonmd__genetic_diagnosis_next_generation', 'dystonmd__enetic_diagnosis_next_generation_TargetedPanel',
                                                                                                     'dystonmd__enetic_diagnosis_next_generation_WholeExomeSequencing',
                                                                                                     'dystonmd__enetic_diagnosis_next_generation_WholeGenomeSequencing',
                                                                                                     'dystonmd__upload_genetic_report', 'dystonmd__NMD_diagnosis_type', 'dystonmd__inframe_outframe',
                                                                                                     'dystonmd__list_of_deleted_exons',
                                                                                                     'dystonmd__list_of_duplicate_exons', 'dystonmd__mutation_identified_Missense',
                                                                                                     'dystonmd__mutation_identified_Missense_mutation',
                                                                                                     'dystonmd__mutation_identified_Nonsense', 'dystonmd__mutation_identified_Nonsense_mutation',
                                                                                                     'dystonmd__mutation_identified_Mutation',
                                                                                                     'dystonmd__mutation_identified_Mutation_mutation', 'dystonmd__mutation_identified_Frameshift',
                                                                                                     'dystonmd__mutation_identified_Frameshift_mutation', 'dystonmd__mutation_identified_Splicesite',
                                                                                                     'dystonmd__mutation_identified_Splicesite_mutation', 'dystonmd__mutation_identified_InframeInsertion',
                                                                                                     'dystonmd__mutation_identified_InframeInsertion_mutation', 'dystonmd__mutation_identified_InframeDeletion',
                                                                                                     'dystonmd__mutation_identified_InframeDeletion_mutation', 'dystonmd__mutation_identified_INDEL',
                                                                                                     'dystonmd__mutation_identified_INDEL_mutation', 'dystonmd__mutation_identified_Others',
                                                                                                     'dystonmd__mutation_identified_Others_mutation',
                                                                                                     'dystonmd__gene_location', 'dystonmd__gene_variant', 'dystonmd__gene_Zygosity', 'dystonmd__gene_Disease',
                                                                                                     'dystonmd__gene_Inheritance',
                                                                                                     'dystonmd__gene_classification', 'dystonmd__Muscle_Biopsy', 'dystonmd__Muscle_Biopsy_MuscleImmunohistochemistry',
                                                                                                     'dystonmd__Muscle_Biopsy_MuscleImmunohistochemistry_if_yes', 'dystonmd__final_diagnosis',
                                                                                                     'dystonmd__current_past_treatment_Steroids',
                                                                                                     'dystonmd__current_past_treatment_Steroids_starting_age', 'dystonmd__current_past_treatment_Prednisone',
                                                                                                     'dystonmd__current_past_treatment_1',
                                                                                                     'dystonmd__current_past_treatment_2', 'dystonmd__current_past_treatment_Deflazacort',
                                                                                                     'dystonmd__current_past_treatment_Deflazacort_1',
                                                                                                     'dystonmd__current_past_treatment_Deflazacort_anyother_specify', 'dystonmd__current_past_treatment_Supplements',
                                                                                                     'dystonmd__current_past_treatment_Supplements_calcium', 'dystonmd__current_past_treatment_Supplements_vit_D',
                                                                                                     'dystonmd__Respiratoryassistance_BiPAP', 'dystonmd__Respiratoryassistance_BiPAP_age',
                                                                                                     'dystonmd__Respiratoryassistance_Ventilator',
                                                                                                     'dystonmd__Respiratoryassistance_Ventilator_age', 'dystonmd__Tendon_lengthening_surgery',
                                                                                                     'dystonmd__Tendon_lengthening_surgery_if_yes_age',
                                                                                                     'dystonmd__Surgicalcorrectionscoliosis', 'dystonmd__Surgicalcorrectionscoliosis_if_yes_age',
                                                                                                     'dystonmd__last_follow_up',
                                                                                                     'dystonmd__last_follow_up_if_yes', 'dystonmd__last_follow_up_if_yes_age', 'dystonmd__Functionalstatus',
                                                                                                     'dystonmd__functional_status_options',
                                                                                                     'dystonmd__functional_score', 'dystonmd__functional_score_brooks_grade', 'dystonmd__functional_score_vignos_grade',
                                                                                                     'dystonmd__outcome',
                                                                                                     'dystonmd__outcome_age', 'dystonmd__oucome_cause_of_death', 'dystonmd__outcome_death_cause', 'dystonmd__death_place',
                                                                                                     'dystonmd__mother_carrier_status', 'dystonmd__mother_carrier_status_outcome', 'dystonmd__sister_carrier_status',
                                                                                                     'dystonmd__sister_carrier_status_outcome', )
    for user in users:
        writer.writerow(user)

    return response


def export_spinalnmd_csv_user(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam', 'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name',
         'nmd_mother_name', 'nmd_paitent_id_yes_no', 'nmd_paitent_id', 'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district', 'nmd_city_name',
         'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion', 'nmd_caste', 'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc',
         'nmd_consent_given', 'nmd_consent_upload', 'nmd_assent_given', 'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
         'gender', 'born_consanguineous_parents', 'consanguineous_parents_if_yes', 'familyHistory_sibling_affected', 'familyHistory_sibling_affected_number', 'upload_pedegree}}', 'age_first_evaluation', 'age_at_onset',
         'age_onset_options', 'age_onset_options_yes_no', 'ConditionBirth_cry', 'conditionBirth_feedingDifficulty', 'conditionBirth_RespiratoryDistress', 'conditionBirth_ReceivedOxygen', 'conditionBirth_KeptIncubator',
         'arthrogryposisBirth', 'RecurrentLowerRespiratory', 'Scoliosis', 'Kyphosis', 'Contractures', 'HipDislocation', 'Fractures', 'MotorSystemExam_Minipolymyoclonus', 'MotorSystemExam_TongueFasciculations',
         'MotorSystemExam_MotorPower_ModifiedMRCgrade', 'MotorSystemExam_UpperLimb_ProximalMuscles', 'MotorSystemExam_UpperLimb_DistalMuscles', 'MotorSystemExam_lowerLimb_ProximalMuscles',
         'MotorSystemExam_lowerLimb_DistalMuscles', 'LimbWeakness', 'LimbWeakness_if_yes_UpperLimb_ProximalGrade', 'LimbWeakness_if_yes_UpperLimb_DistalGrade', 'LimbWeakness_if_yes_LowerLimb_ProximalGrade',
         'LimbWeakness_if_yes_LowerLimb_DistalGrade', 'currentMotor_ability', 'currentMotor_WheelchairBound', 'currentMotor_WheelchairBound_if_yes_age', 'currentMotor_BedBound', 'currentMotor_BedBound_age', 'HMAS',
         'HMAS_score', 'clinicalDiagnosis_SMA0', 'clinicalDiagnosis_SMA1', 'clinicalDiagnosis_SMA2', 'clinicalDiagnosis_SMA3', 'clinicalDiagnosis_SMA4', 'LaboratoryInvestigation_CK_Level', 'geneticDiagnosis',
         'NAIP_deletion', 'geneticFindings_gene', 'geneticFindings_Location', 'geneticFindings_Variant', 'geneticFindings_Zygosity', 'geneticFindings_Disease', 'geneticFindings_Inheritance',
         'geneticFindings_classification', 'geneticDiagnosis2', 'final_diagnosis_1', 'genetic_report_upload}}', 'Treatment_RespiratorySupport', 'Treatment_RespiratorySupport_ifyes_BIPAP',
         'Treatment_RespiratorySupport_ifyes_IPPR', 'Treatment_RespiratorySupport_ifyes_Ventilation', 'Feeding_Oral', 'Feeding_Nasogastric', 'Feeding_PEG', 'OperatedScoliosis', 'OperatedScoliosis_ifyes_age',
         'CurrentPastTreatment_ReceivedNusinersin', 'CurrentPastTreatment_ReceivedNusinersin_if_yes', 'CurrentPastTreatment_ReceivedRisdiplam', 'CurrentPastTreatment_ReceivedRisdiplam_if_yes_age',
         'CurrentPastTreatment_ReceivedZolgensma', 'CurrentPastTreatment_ReceivedZolgensma_if_yes_age', 'finalOutcome', 'finalOutcome_if_dead_age', 'finalOutcome_death_place1', 'finalOutcome_deathCause',
         'finalOutcome_deathCause_known', 'finalOutcome_death_place2', 'carrier_testing_parents', 'prenatal_testing', 'prenatal_testing_if_yes', ])

    users = profile_nmd.objects.filter(user=request.user).prefetch_related('spinalnmd').values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                                    'nmd_date_of_clinical_exam',
                                                                                                    'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name',
                                                                                                    'nmd_paitent_id_yes_no',
                                                                                                    'nmd_paitent_id',
                                                                                                    'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                                    'nmd_city_name',
                                                                                                    'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                                    'nmd_caste',
                                                                                                    'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given',
                                                                                                    'nmd_consent_upload',
                                                                                                    'nmd_assent_given',
                                                                                                    'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                                    'spinalnmd__gender', 'spinalnmd__born_consanguineous_parents', 'spinalnmd__consanguineous_parents_if_yes',
                                                                                                    'spinalnmd__familyHistory_sibling_affected', 'spinalnmd__familyHistory_sibling_affected_number',
                                                                                                    'spinalnmd__upload_pedegree',
                                                                                                    'spinalnmd__age_first_evaluation', 'spinalnmd__age_at_onset', 'spinalnmd__age_onset_options',
                                                                                                    'spinalnmd__age_onset_options_yes_no',
                                                                                                    'spinalnmd__ConditionBirth_cry', 'spinalnmd__conditionBirth_feedingDifficulty',
                                                                                                    'spinalnmd__conditionBirth_RespiratoryDistress',
                                                                                                    'spinalnmd__conditionBirth_ReceivedOxygen', 'spinalnmd__conditionBirth_KeptIncubator', 'spinalnmd__arthrogryposisBirth',
                                                                                                    'spinalnmd__RecurrentLowerRespiratory', 'spinalnmd__Scoliosis_sma', 'spinalnmd__Kyphosis_sma',
                                                                                                    'spinalnmd__Contractures',
                                                                                                    'spinalnmd__HipDislocation',
                                                                                                    'spinalnmd__Fractures', 'spinalnmd__MotorSystemExam_Minipolymyoclonus',
                                                                                                    'spinalnmd__MotorSystemExam_TongueFasciculations',
                                                                                                    'spinalnmd__MotorSystemExam_MotorPower_ModifiedMRCgrade', 'spinalnmd__MotorSystemExam_UpperLimb_ProximalMuscles',
                                                                                                    'spinalnmd__MotorSystemExam_UpperLimb_DistalMuscles', 'spinalnmd__MotorSystemExam_lowerLimb_ProximalMuscles',
                                                                                                    'spinalnmd__MotorSystemExam_lowerLimb_DistalMuscles', 'spinalnmd__LimbWeakness',
                                                                                                    'spinalnmd__LimbWeakness_if_yes_UpperLimb_ProximalGrade',
                                                                                                    'spinalnmd__LimbWeakness_if_yes_UpperLimb_DistalGrade', 'spinalnmd__LimbWeakness_if_yes_LowerLimb_ProximalGrade',
                                                                                                    'spinalnmd__LimbWeakness_if_yes_LowerLimb_DistalGrade', 'spinalnmd__currentMotor_ability',
                                                                                                    'spinalnmd__currentMotor_WheelchairBound',
                                                                                                    'spinalnmd__currentMotor_WheelchairBound_if_yes_age', 'spinalnmd__currentMotor_BedBound',
                                                                                                    'spinalnmd__currentMotor_BedBound_age',
                                                                                                    'spinalnmd__HMAS', 'spinalnmd__HMAS_score', 'spinalnmd__clinicalDiagnosis_SMA0', 'spinalnmd__clinicalDiagnosis_SMA1',
                                                                                                    'spinalnmd__clinicalDiagnosis_SMA2', 'spinalnmd__clinicalDiagnosis_SMA3', 'spinalnmd__clinicalDiagnosis_SMA4',
                                                                                                    'spinalnmd__LaboratoryInvestigation_CK_Level', 'spinalnmd__geneticDiagnosis', 'spinalnmd__NAIP_deletion',
                                                                                                    'spinalnmd__geneticFindings_gene',
                                                                                                    'spinalnmd__geneticFindings_Location', 'spinalnmd__geneticFindings_Variant', 'spinalnmd__geneticFindings_Zygosity',
                                                                                                    'spinalnmd__geneticFindings_Disease', 'spinalnmd__geneticFindings_Inheritance',
                                                                                                    'spinalnmd__geneticFindings_classification',
                                                                                                    'spinalnmd__geneticDiagnosis2', 'spinalnmd__final_diagnosis_1', 'spinalnmd__genetic_report_upload',
                                                                                                    'spinalnmd__Treatment_RespiratorySupport',
                                                                                                    'spinalnmd__Treatment_RespiratorySupport_ifyes_BIPAP', 'spinalnmd__Treatment_RespiratorySupport_ifyes_IPPR',
                                                                                                    'spinalnmd__Treatment_RespiratorySupport_ifyes_Ventilation', 'spinalnmd__Feeding_Oral',
                                                                                                    'spinalnmd__Feeding_Nasogastric',
                                                                                                    'spinalnmd__Feeding_PEG', 'spinalnmd__OperatedScoliosis', 'spinalnmd__OperatedScoliosis_ifyes_age',
                                                                                                    'spinalnmd__CurrentPastTreatment_ReceivedNusinersin', 'spinalnmd__CurrentPastTreatment_ReceivedNusinersin_if_yes',
                                                                                                    'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam', 'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam_if_yes_age',
                                                                                                    'spinalnmd__CurrentPastTreatment_ReceivedZolgensma', 'spinalnmd__CurrentPastTreatment_ReceivedZolgensma_if_yes_age',
                                                                                                    'spinalnmd__finalOutcome', 'spinalnmd__finalOutcome_if_dead_age', 'spinalnmd__finalOutcome_death_place1',
                                                                                                    'spinalnmd__finalOutcome_deathCause', 'spinalnmd__finalOutcome_deathCause_known',
                                                                                                    'spinalnmd__finalOutcome_death_place2',
                                                                                                    'spinalnmd__carrier_testing_parents', 'spinalnmd__prenatal_testing', 'spinalnmd__prenatal_testing_if_yes', )
    for user in users:
        writer.writerow(user)

    return response


def export_limbnmd_csv_user(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam', 'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name',
         'nmd_mother_name', 'nmd_paitent_id_yes_no', 'nmd_paitent_id', 'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district', 'nmd_city_name',
         'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion', 'nmd_caste', 'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc',
         'nmd_consent_given', 'nmd_consent_upload', 'nmd_assent_given', 'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
         'limb_gender', 'evaluation_age', 'limb_symptoms_onset_age', 'limb_born_consanguineous_parents', 'limb_consanguineous_parents_if_yes', 'MuscleHypertrophy', 'MuscleWasting', 'Contractures_3',
         'Contractures_3_ankle', 'Contractures_3_knee', 'Contractures_3_hip', 'Contractures_3_elbow', 'Contractures_3_neck', 'limb_weakness', 'limb_weakness_UpperlimbProximal', 'limb_weakness_UpperlimbDistal',
         'limb_weakness_LowerlimbProximal', 'limb_weakness_lowerlimbDistal', 'BulbarWeakness', 'BulbarWeakness_if_yes', 'CardiacSymptoms', 'cardiac_symptoms_options', 'RespiratorySymptoms', 'RespiratorySymptoms_options',
         'InheritancePattern', 'PositiveFamilyHistory', 'PositiveFamilyHistory_SiblingsAffected', 'PositiveFamilyHistory_SiblingsAffected_number', 'PositiveFamilyHistory_MotherAffected',
         'PositiveFamilyHistory_FatherAffected', 'PositiveFamilyHistory_GrandmotherAffected', 'PositiveFamilyHistory_GrandFatherAffected', 'PositiveFamilyHistory_CousinsAffected',
         'PositiveFamilyHistory_CousinsAffected_number', 'PositiveFamilyHistory_AnyOther', 'PositiveFamilyHistory_AnyOther_specify', 'PositiveFamilyHistory_AnyOther_Specify_names',
         'PositiveFamilyHistory_upload_pedidegree', 'current_motor', 'CurrentMotor_yes_no', 'CurrentMotor_if_yes_age', 'LaboratoryInvestigations_CK_level', 'NerveConductionStudies', 'NerveConductionStudies_options',
         'CardiacEvaluation', 'CardiacEvaluation_ECG', 'CardiacEvaluation_ECG_status', 'CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia', 'CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia_if_yes', 'limb_2DECHO',
         'limb_2DECHO_status', 'limb_2DECHO_if_abnormal', 'limb_2DECHO_yes_no', 'limb_2DECHO_AnyOther', 'MuscleBiopsy', 'MuscleBiopsy_Immunohistochemistry', 'MuscleBiopsy_if_yes', 'DiagnosisConfirmed_sanger',
         'DiagnosisConfirmed_nextGenerationSeq_options', 'DiagnosisConfirmed_nextGenerationSeq_options', 'upload_genetic_report', 'limb_mutation', 'mutationDetails_Missense', 'mutationDetails_Missense_mutation',
         'mutationDetails_Nonsense', 'mutationDetails_Nonsense_mutation', 'mutationDetails_SpliceSite', 'mutationDetails_SpliceSite_mutation', 'mutationDetails_Insertion', 'mutationDetails_Insertion_mutation',
         'mutationDetails_Deletions', 'mutationDetails_Deletions_mutation', 'mutationDetails_AnyOther_specify', 'mutationDetails_AnyOther_mutation', 'MutationDetected_Homozygous', 'MutationDetected_CompoundHeterozygous',
         'MutationDetected_Heterozygous', 'MutationDetected_VariantUnknownSignificance', 'gene_Location', 'gene_Variant', 'gene_Zygosity', 'gene_Disease', 'gene_Inheritance', 'gene_classification', 'AR_LGMD_type',
         'ADLGMD_type', 'SegregationPattern_Father', 'SegregationPattern_Mother', 'TreatmentReceived_TendonLengthening', 'TreatmentReceived_TendonLengthening_age', 'Scoliosis', 'Scoliosis_SurgicalCorrection',
         'Scoliosis_SurgicalCorrection_age', 'CardiacAbnormalities_pacemaker', 'CardiacAbnormalities_Prophylactic', 'CardiacAbnormalities_CardiacTransplant', 'RespiratoryAssistance', 'RespiratoryAssistance_BiPAP',
         'RespiratoryAssistance_BiPAP_age', 'RespiratoryAssistance_Ventilator', 'RespiratoryAssistance_Ventilator_age', 'Final_Outcome_last_followup_Date', 'Final_Outcome_status', 'Final_Outcome_if_death_age',
         'Final_Outcome_death_cause', 'Final_Outcome_Cardiac', 'Final_Outcome_death_place', 'Final_Outcome_Respiratory', 'Final_Outcome_Respiratory_place', ])

    users = profile_nmd.objects.filter(user=request.user).prefetch_related('limbnmd', ).values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis',
                                                                                                    'nmd_date_of_records',
                                                                                                    'nmd_date_of_clinical_exam',
                                                                                                    'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name',
                                                                                                    'nmd_paitent_id_yes_no',
                                                                                                    'nmd_paitent_id',
                                                                                                    'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                                    'nmd_city_name',
                                                                                                    'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                                    'nmd_caste',
                                                                                                    'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given',
                                                                                                    'nmd_consent_upload',
                                                                                                    'nmd_assent_given',
                                                                                                    'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                                    'limbnmd__limb_gender', 'limbnmd__evaluation_age', 'limbnmd__limb_symptoms_onset_age',
                                                                                                    'limbnmd__limb_born_consanguineous_parents', 'limbnmd__limb_consanguineous_parents_if_yes',
                                                                                                    'limbnmd__MuscleHypertrophy',
                                                                                                    'limbnmd__MuscleWasting', 'limbnmd__Contractures_3', 'limbnmd__Contractures_3_ankle', 'limbnmd__Contractures_3_knee',
                                                                                                    'limbnmd__Contractures_3_hip', 'limbnmd__Contractures_3_elbow', 'limbnmd__Contractures_3_neck',
                                                                                                    'limbnmd__limb_weakness',
                                                                                                    'limbnmd__limb_weakness_UpperlimbProximal', 'limbnmd__limb_weakness_UpperlimbDistal',
                                                                                                    'limbnmd__limb_weakness_LowerlimbProximal', 'limbnmd__limb_weakness_lowerlimbDistal', 'limbnmd__BulbarWeakness',
                                                                                                    'limbnmd__BulbarWeakness_if_yes', 'limbnmd__CardiacSymptoms', 'limbnmd__cardiac_symptoms_options',
                                                                                                    'limbnmd__RespiratorySymptoms', 'limbnmd__RespiratorySymptoms_options', 'limbnmd__InheritancePattern',
                                                                                                    'limbnmd__PositiveFamilyHistory', 'limbnmd__PositiveFamilyHistory_SiblingsAffected',
                                                                                                    'limbnmd__PositiveFamilyHistory_SiblingsAffected_number', 'limbnmd__PositiveFamilyHistory_MotherAffected',
                                                                                                    'limbnmd__PositiveFamilyHistory_FatherAffected', 'limbnmd__PositiveFamilyHistory_GrandmotherAffected',
                                                                                                    'limbnmd__PositiveFamilyHistory_GrandFatherAffected', 'limbnmd__PositiveFamilyHistory_CousinsAffected',
                                                                                                    'limbnmd__PositiveFamilyHistory_CousinsAffected_number', 'limbnmd__PositiveFamilyHistory_AnyOther',
                                                                                                    'limbnmd__PositiveFamilyHistory_AnyOther_specify', 'limbnmd__PositiveFamilyHistory_AnyOther_Specify_names',
                                                                                                    'limbnmd__PositiveFamilyHistory_upload_pedidegree', 'limbnmd__current_motor', 'limbnmd__CurrentMotor_yes_no',
                                                                                                    'limbnmd__CurrentMotor_if_yes_age', 'limbnmd__LaboratoryInvestigations_CK_level', 'limbnmd__NerveConductionStudies',
                                                                                                    'limbnmd__NerveConductionStudies_options', 'limbnmd__CardiacEvaluation', 'limbnmd__CardiacEvaluation_ECG',
                                                                                                    'limbnmd__CardiacEvaluation_ECG_status', 'limbnmd__CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia',
                                                                                                    'limbnmd__CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia_if_yes', 'limbnmd__limb_2DECHO',
                                                                                                    'limbnmd__limb_2DECHO_status', 'limbnmd__limb_2DECHO_if_abnormal', 'limbnmd__limb_2DECHO_yes_no',
                                                                                                    'limbnmd__limb_2DECHO_AnyOther', 'limbnmd__MuscleBiopsy', 'limbnmd__MuscleBiopsy_Immunohistochemistry',
                                                                                                    'limbnmd__MuscleBiopsy_if_yes', 'limbnmd__DiagnosisConfirmed_sanger',
                                                                                                    'limbnmd__DiagnosisConfirmed_nextGenerationSeq_options', 'limbnmd__DiagnosisConfirmed_nextGenerationSeq_options',
                                                                                                    'limbnmd__upload_genetic_report', 'limbnmd__limb_mutation', 'limbnmd__mutationDetails_Missense',
                                                                                                    'limbnmd__mutationDetails_Missense_mutation', 'limbnmd__mutationDetails_Nonsense',
                                                                                                    'limbnmd__mutationDetails_Nonsense_mutation', 'limbnmd__mutationDetails_SpliceSite',
                                                                                                    'limbnmd__mutationDetails_SpliceSite_mutation', 'limbnmd__mutationDetails_Insertion',
                                                                                                    'limbnmd__mutationDetails_Insertion_mutation', 'limbnmd__mutationDetails_Deletions',
                                                                                                    'limbnmd__mutationDetails_Deletions_mutation', 'limbnmd__mutationDetails_AnyOther_specify',
                                                                                                    'limbnmd__mutationDetails_AnyOther_mutation', 'limbnmd__MutationDetected_Homozygous',
                                                                                                    'limbnmd__MutationDetected_CompoundHeterozygous', 'limbnmd__MutationDetected_Heterozygous',
                                                                                                    'limbnmd__MutationDetected_VariantUnknownSignificance', 'limbnmd__gene_Location1', 'limbnmd__gene_Variant1',
                                                                                                    'limbnmd__gene_Zygosity1', 'limbnmd__gene_Disease1', 'limbnmd__gene_Inheritance1', 'limbnmd__gene_classification1',
                                                                                                    'limbnmd__AR_LGMD_type', 'limbnmd__ADLGMD_type', 'limbnmd__SegregationPattern_Father',
                                                                                                    'limbnmd__SegregationPattern_Mother',
                                                                                                    'limbnmd__TreatmentReceived_TendonLengthening', 'limbnmd__TreatmentReceived_TendonLengthening_age',
                                                                                                    'limbnmd__Scoliosis_limb',
                                                                                                    'limbnmd__Scoliosis_SurgicalCorrection', 'limbnmd__Scoliosis_SurgicalCorrection_age',
                                                                                                    'limbnmd__CardiacAbnormalities_pacemaker', 'limbnmd__CardiacAbnormalities_Prophylactic',
                                                                                                    'limbnmd__CardiacAbnormalities_CardiacTransplant', 'limbnmd__RespiratoryAssistance',
                                                                                                    'limbnmd__RespiratoryAssistance_BiPAP',
                                                                                                    'limbnmd__RespiratoryAssistance_BiPAP_age', 'limbnmd__RespiratoryAssistance_Ventilator',
                                                                                                    'limbnmd__RespiratoryAssistance_Ventilator_age', 'limbnmd__Final_Outcome_last_followup_Date',
                                                                                                    'limbnmd__Final_Outcome_status', 'limbnmd__Final_Outcome_if_death_age', 'limbnmd__Final_Outcome_death_cause',
                                                                                                    'limbnmd__Final_Outcome_Cardiac', 'limbnmd__Final_Outcome_death_place', 'limbnmd__Final_Outcome_Respiratory',
                                                                                                    'limbnmd__Final_Outcome_Respiratory_place', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def update_qa_qc_nmd(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_nmd.objects.get(id=pk)
    form2 = QAnmdForm(instance=patient)

    if request.method == 'POST':
        form2 = QAnmdForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_nmd_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_nmd.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_nmd.html', context)


@login_required(login_url='login')
def view_qa_qc_nmd(request, pk):
    user = request.user
    patient = profile_nmd.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
