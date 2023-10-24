import csv
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import messages
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
def add_record_sm(request):
    user = request.user
    register = Register.objects.get(user=request.user)

    form1 = ProfileSMForm()
    if request.method == 'POST':
        form1 = ProfileSMForm(request.POST, request.FILES, )

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(sm_demographic, args=(auth1.id,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_sm.html', context)
    context = {'form1': form1, }
    return render(request, 'add_record_sm.html', context)

@login_required(login_url='login')
def update_patient_record_sm(request,pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_smallmolecule.objects.get(id=pk)

    form1 = ProfileSMForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfileSMForm(request.POST, request.FILES, instance=patient)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_sm')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_sm.html', context)

    context = {'form1': form1, }
    return render(request, 'update_patient_record_sm.html', context)


@login_required(login_url='login')
def sm_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_smallmolecule.objects.get(id=pk)
    form1 = FirstSymptomDataSheetSMForm()
    if request.method == 'POST':
        form1 = FirstSymptomDataSheetSMForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_sm, args=(pk,)))
        else:
            context = {'form1': form1, }
            return render(request, 'sm_demographic.html', context)

    context = {'form1': form1, }
    return render(request, 'sm_demographic.html', context)


@login_required(login_url='login')
def view_profile_sm(request, pk):

    try:
        form1 = profile_smallmolecule.objects.get(id=pk)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_profile_record_sm.html', context)

@login_required(login_url='login')
def update_record_sm(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_smallmolecule.objects.get(id=pk)
    try:
        form5 = demographic_smallmolecule.objects.get(patient=patient)
        form1 = FirstSymptomDataSheetSMForm(instance=form5)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = FirstSymptomDataSheetSMForm(request.POST, request.FILES, instance=form5)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect('total_record_sm')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_sm.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = FirstSymptomDataSheetSMForm(request.POST, request.FILES, instance=form5)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_sm")

            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_sm.html', context)
        if request.method == 'POST' and 'save' in request.POST:
                form1 = FirstSymptomDataSheetSMForm(request.POST, request.FILES, instance=socio)
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
                    return render(request, 'update_record_sm.html', context)
    except:
        form1 = FirstSymptomDataSheetSMForm()
        if request.method == 'POST':
            form1 = FirstSymptomDataSheetSMForm(request.POST, request.FILES, )
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()

                return redirect('total_record_sm')
            else:
                context = {'form1': form1,'patient': patient,  }
                return render(request, 'update_record_sm.html', context)
    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_sm.html', context)


@login_required(login_url='login')
def view_record_sm(request, pk):
    patient = profile_smallmolecule.objects.get(id=pk)
    try:
        form1 = demographic_smallmolecule.objects.get(patient=patient)
    except:
        form1 = None
    context = {'form1': form1, }
    return render(request, 'view_record_sm.html', context)


@login_required(login_url='login')
def total_record_sm(request):
    pat = profile_smallmolecule.objects.filter(user=request.user)
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_sm.html', context)


@login_required(login_url='login')
def total_record_sm_admin(request):
    pat = profile_smallmolecule.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None
    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_sm_admin.html', context)


@login_required(login_url='login')
def delete_record_sm(request, pk):
    order = profile_smallmolecule.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_sm')

    context = {'order': order}
    return render(request, 'delete_record_sm.html', context)


def export_smallmolecule_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="smallmolecule.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_records', 'date_of_clinical_exam', 'date_of_birth', 'patient_name', 'father_name',
         'mother_name', 'paitent_id_yes_no', 'paitent_id', 'patient_id_no', 'father_mother_id', 'father_mother_no', 'permanent_addr', 'state', 'district',
         'city_name', 'country_name', 'land_line_no', 'mother_mobile_no', 'father_mobile_no', 'email', 'religion', 'caste', 'gender', 'referred_status',
         'referred_by', 'referred_by_desc', 'consent_given', 'consent_upload', 'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no', 'head_circumference',
         'age_at_first_symptom', 'visual_problem', 'any_malformation', 'developmental_delay', 'developmental_findings', 'vomiting', 'vomiting_finding', 'loose_stools', 'stools_findings', 'pneumonia',
         'pneumonia_findings', 'fever', 'fever_findings', 'lethargy', 'lethargy_findings', 'seizures', 'seizures_findings', 'abdominal_distention', 'abdominal_distention_findings', 'history_admission',
         'history_findings', 'any_surgery', 'surgery_findings', 'aversion_sweet_protein', 'sweet_protein_findings', 'encephalopathy', 'encephalopathy_findings', 'deafness', 'deafness_findings', 'extra_pyramidal_symp',
         'extra_pyramidal_symp_findings', 'hypotonia', 'hypotonia_findings', 'hypertonia', 'hypertonia_findings', 'facial_dysmorphism', 'facial_dysmorphism_findings', 'congential_heart_disease',
         'congential_heart_disease_findings', 'cardiomyopathy', 'cardiomyopathy_findings', 'hepatomegaly', 'hepatomegaly_findings', 'splenomegaly', 'splenomegaly_findings', 'pigmentary', 'pigmentary_findings',
         'deranged_LFT', 'deranged_LFT_findings', 'deranged_RFT', 'deranged_RFT_findings', 'hypoglycemia', 'hypoglycemia_findings', 'metabolic_acidosis', 'metabolic_acidosis_findings', 'metabolic_alkalosis',
         'metabolic_alkalosis_findings', 'hyper_ammonia', 'hyper_ammonia_findings', 'high_lactate', 'high_lactate_findings', 'urine_ketones', 'urine_ketones_findings', 'cherry_red_spot', 'cherry_red_spot_findings',
         'retinitis_pigmentosa', 'retinitis_pigmentosa_findings', 'optic_atrophy', 'optic_atrophy_findings', 'mechanical_ventilation', 'mechanical_ventilation_findings', 'dialysis', 'dialysis_findings', 'regression',
         'regression_findings', 'distonia_abnormal_movement', 'distonia_abnormal_findings', 'high_cpk', 'high_cpk_findings', 'generic_analysis', 'generic_analysis_findings', 'final_dagnosis', 'final_dagnosis_findings',
         'dna_storage', 'dna_storage_findings', 'CT_brain', 'CT_brain_date', 'CT_brain_age', 'mri_brain', 'mri_brain_date', 'mri_brain_age', 'mrs_brain', 'mrs_brain_date', 'mrs_brain_age', 'ms_ms', 'ms_date', 'ms_age',
         'gcms', 'gcms_date', 'gcms_age', 'enzyme_assay', 'enzyme_assay_date', 'enzyme_assay_age', 'quantitative_plasma', 'quantitative_plasma_date', 'quantitative_plasma_age', 'quantitative_csf',
         'quantitative_csf_date', 'quantitative_csf_age', 'muscle_biopsy', 'muscle_biopsy_date', 'muscle_biopsy_age', 'ncv', 'ncv_date', 'ncv_age', 'ief_cdg', 'ief_cdg_date', 'ief_cdg_age', 'glycine', 'glycine_date',
         'glycine_age', 'other_info', 'other_info_date', 'other_info_age', 'tms', 'tms_date', 'tms_age', 'photos', 'photos_specify', 'molecular_studies', 'molecular_studies_date', 'molecular_studies_place',
         'upload_studies', 'Final_Outcome', 'death_cause', 'age_timedeath', ])

    users = profile_smallmolecule.objects.filter(user=request.user).prefetch_related('patient_small').values_list('register_id__institute_name', 'uniqueId', 'small_icmr_unique_no', 'small_final_diagnosis',
                                                                                                        'small_date_of_records', 'small_date_of_clinical_exam', 'small_date_of_birth', 'small_patient_name', 'small_father_name', 'small_mother_name', 'small_paitent_id_yes_no', 'small_paitent_id', 'small_patient_id_no', 'small_father_mother_id', 'small_father_mother_no', 'small_permanent_addr', 'small_state', 'small_district', 'small_city_name', 'small_country_name', 'small_land_line_no', 'small_mother_mobile_no', 'small_father_mobile_no', 'small_email', 'small_religion', 'small_caste', 'small_gender', 'small_referred_status', 'small_referred_by', 'small_referred_by_desc', 'small_consent_given', 'small_consent_upload', 'small_assent_given', 'small_assent_upload', 'small_hospital_name', 'small_hospital_reg_no', 'patient_small__head_circumference', 'patient_small__age_at_first_symptom', 'patient_small__visual_problem', 'patient_small__any_malformation', 'patient_small__developmental_delay', 'patient_small__developmental_findings', 'patient_small__vomiting', 'patient_small__vomiting_finding', 'patient_small__loose_stools', 'patient_small__stools_findings', 'patient_small__pneumonia', 'patient_small__pneumonia_findings', 'patient_small__fever', 'patient_small__fever_findings', 'patient_small__lethargy', 'patient_small__lethargy_findings', 'patient_small__seizures', 'patient_small__seizures_findings', 'patient_small__abdominal_distention', 'patient_small__abdominal_distention_findings', 'patient_small__history_admission', 'patient_small__history_findings', 'patient_small__any_surgery', 'patient_small__surgery_findings', 'patient_small__aversion_sweet_protein', 'patient_small__sweet_protein_findings', 'patient_small__encephalopathy', 'patient_small__encephalopathy_findings', 'patient_small__deafness', 'patient_small__deafness_findings', 'patient_small__extra_pyramidal_symp', 'patient_small__extra_pyramidal_symp_findings', 'patient_small__hypotonia', 'patient_small__hypotonia_findings', 'patient_small__hypertonia', 'patient_small__hypertonia_findings', 'patient_small__facial_dysmorphism', 'patient_small__facial_dysmorphism_findings', 'patient_small__congential_heart_disease', 'patient_small__congential_heart_disease_findings', 'patient_small__cardiomyopathy', 'patient_small__cardiomyopathy_findings', 'patient_small__hepatomegaly', 'patient_small__hepatomegaly_findings', 'patient_small__splenomegaly', 'patient_small__splenomegaly_findings', 'patient_small__pigmentary', 'patient_small__pigmentary_findings', 'patient_small__deranged_LFT', 'patient_small__deranged_LFT_findings', 'patient_small__deranged_RFT', 'patient_small__deranged_RFT_findings', 'patient_small__hypoglycemia', 'patient_small__hypoglycemia_findings', 'patient_small__metabolic_acidosis', 'patient_small__metabolic_acidosis_findings', 'patient_small__metabolic_alkalosis', 'patient_small__metabolic_alkalosis_findings', 'patient_small__hyper_ammonia', 'patient_small__hyper_ammonia_findings', 'patient_small__high_lactate', 'patient_small__high_lactate_findings', 'patient_small__urine_ketones', 'patient_small__urine_ketones_findings', 'patient_small__cherry_red_spot', 'patient_small__cherry_red_spot_findings', 'patient_small__retinitis_pigmentosa', 'patient_small__retinitis_pigmentosa_findings', 'patient_small__optic_atrophy', 'patient_small__optic_atrophy_findings', 'patient_small__mechanical_ventilation', 'patient_small__mechanical_ventilation_findings', 'patient_small__dialysis', 'patient_small__dialysis_findings', 'patient_small__regression', 'patient_small__regression_findings', 'patient_small__distonia_abnormal_movement', 'patient_small__distonia_abnormal_findings', 'patient_small__high_cpk', 'patient_small__high_cpk_findings', 'patient_small__generic_analysis', 'patient_small__generic_analysis_findings', 'patient_small__final_dagnosis', 'patient_small__final_dagnosis_findings', 'patient_small__dna_storage', 'patient_small__dna_storage_findings', 'patient_small__CT_brain', 'patient_small__CT_brain_date', 'patient_small__CT_brain_age', 'patient_small__mri_brain', 'patient_small__mri_brain_date', 'patient_small__mri_brain_age', 'patient_small__mrs_brain', 'patient_small__mrs_brain_date', 'patient_small__mrs_brain_age', 'patient_small__ms_ms', 'patient_small__ms_date', 'patient_small__ms_age', 'patient_small__gcms', 'patient_small__gcms_date', 'patient_small__gcms_age', 'patient_small__enzyme_assay', 'patient_small__enzyme_assay_date', 'patient_small__enzyme_assay_age', 'patient_small__quantitative_plasma', 'patient_small__quantitative_plasma_date', 'patient_small__quantitative_plasma_age', 'patient_small__quantitative_csf', 'patient_small__quantitative_csf_date', 'patient_small__quantitative_csf_age', 'patient_small__muscle_biopsy', 'patient_small__muscle_biopsy_date', 'patient_small__muscle_biopsy_age', 'patient_small__ncv', 'patient_small__ncv_date', 'patient_small__ncv_age', 'patient_small__ief_cdg', 'patient_small__ief_cdg_date', 'patient_small__ief_cdg_age', 'patient_small__glycine', 'patient_small__glycine_date', 'patient_small__glycine_age', 'patient_small__other_info', 'patient_small__other_info_date', 'patient_small__other_info_age', 'patient_small__tms', 'patient_small__tms_date', 'patient_small__tms_age', 'patient_small__photos', 'patient_small__photos_specify', 'patient_small__molecular_studies', 'patient_small__molecular_studies_date', 'patient_small__molecular_studies_place', 'patient_small__upload_studies', 'patient_small__Final_Outcome', 'patient_small__death_cause', 'patient_small__age_timedeath',)
    for user in users:
        writer.writerow(user)

    return response



@login_required(login_url='login')
def update_qa_qc_small(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_smallmolecule.objects.get(id=pk)
    form2 = QAsmallForm(instance=patient)

    if request.method == 'POST':
        form2 = QAsmallForm(request.POST, request.FILES, instance=patient)
        if form2.is_valid():
            auth1 = form2.save(commit=False)
            auth1.qa_user = user
            auth1.qa_register = register
            # auth1.patient = patient
            auth1.save()
            return redirect('total_record_sm_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_small.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_small.html', context)


@login_required(login_url='login')
def view_qa_qc_small(request, pk):
    user = request.user
    patient = profile_smallmolecule.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")