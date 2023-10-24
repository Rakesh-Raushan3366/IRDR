from django.http import HttpResponse
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import csv
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
def add_record_pid(request):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = ProfilePIDForm()
    if request.method == 'POST':
        form1 = ProfilePIDForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return HttpResponseRedirect(reverse(pid_demographic, args=(auth1,)))
        else:
            context = {'form1': form1, }
            return render(request, 'add_record_pid.html', context)
    context = {'form1': form1, }
    return render(request, 'add_record_pid.html', context)


@login_required(login_url='login')
def update_patient_record_pid(request,pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pid.objects.get(id=pk)
    form1 = ProfilePIDForm(instance=patient)
    if request.method == 'POST':
        form1 = ProfilePIDForm(request.POST, request.FILES,instance=patient )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect('total_record_pid')
        else:
            context = {'form1': form1, }
            return render(request, 'update_patient_record_pid.html', context)
    context = {'form1': form1, }
    return render(request, 'update_patient_record_pid.html', context)


@login_required(login_url='login')
def view_profile_pid(request, pk):

    try:
        form1 = profile_pid.objects.get(id=pk)
    except:
        form1 = None

    context = {'form1': form1, }
    return render(request, 'view_profile_record_pid.html', context)


@login_required(login_url='login')
def pid_demographic(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pid.objects.get(id=pk)
    form1 = ClinicalPresentationPIDForm()
    if request.method == 'POST':
        form1 = ClinicalPresentationPIDForm(request.POST, request.FILES, )
        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.patient = patient
            auth1.save()
            return HttpResponseRedirect(reverse(update_record_pid, args=(pk,)))
        else:
            context = {'form1': form1, }
            return render(request, 'pid_demographic.html', context)

    context = {'form1': form1, }
    return render(request, 'pid_demographic.html', context)


@login_required(login_url='login')
def total_record_pid(request):
    pat = profile_pid.objects.filter(user=request.user).order_by('pid_date_created')
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_pid.html', context)


@login_required(login_url='login')
def total_record_pid_admin(request):
    pat = profile_pid.objects.all()
    patient = pat.reverse()
    date1 = None
    date2 = None

    context = {'patient': patient, 'date1': date1, 'date2': date2}
    return render(request, 'total_record_pid_admin.html', context)


@login_required(login_url='login')
def delete_record_pid(request, pk):
    order = profile_pid.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('total_record_pid')

    context = {'order': order}
    return render(request, 'delete_record_pid.html', context)


@login_required(login_url='login')
def view_record_pid(request, pk):
    patient = profile_pid.objects.get(id=pk)
    try:
        form1 = demopraphic_pid.objects.get(patient=patient)
    except:
        form1 = None

    context = {'form1': form1, }
    return render(request, 'view_record_pid.html', context)


@login_required(login_url='login')
def update_record_pid(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pid.objects.get(id=pk)
    try:
        socio = demopraphic_pid.objects.get(patient=patient)

        form1 = ClinicalPresentationPIDForm(instance=socio)
        if request.method == 'POST' and 'submitandexit' in request.POST:
            form1 = ClinicalPresentationPIDForm(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.save()
                return redirect('total_record_pid')
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_pid.html', context)
        if request.method == 'POST' and 'submitandqc' in request.POST:
            form1 = ClinicalPresentationPIDForm(request.POST, request.FILES, instance=socio)
            if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()
                patient.complete = 'Yes'
                patient.quality_status = 'Resubmitted'
                patient.save()
                return redirect("total_record_pid")
            else:
                context = {'form1': form1,'patient': patient, }
                return render(request, 'update_record_pid.html', context)

        if request.method == 'POST' and 'save' in request.POST:
                form1 = ClinicalPresentationPIDForm(request.POST, request.FILES, instance=socio)
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
                    return render(request, 'update_record_pid.html', context)

    except:
         form1 = ClinicalPresentationPIDForm()
         if request.method == 'POST':
              form1 = ClinicalPresentationPIDForm(request.POST, request.FILES)
              if form1.is_valid():
                auth1 = form1.save(commit=False)
                auth1.user = user
                auth1.register = register
                auth1.patient = patient
                auth1.save()


                return redirect('total_record_pid')

              else:
                context = {'form1': form1,'patient': patient,  }
                return render(request, 'pid_demographic.html', context)

    context = {'form1': form1,'patient': patient, }
    return render(request, 'update_record_pid.html', context)

def export_pid_user_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pid.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'final_diagnosis', 'date_of_record', 'clinical_exam_date', 'date_of_birth', 'patient_name', 'father_name', 'mother_name',
         'paitent_id', 'paitent_id_list', 'patient_id_no', 'father_mother_id', 'father_mother_id_no', 'permanent_addr', 'state', 'district', 'city_name', 'country_name',
         'land_line_no', 'mother_mobile_no', 'father_mobile_no', 'email', 'religion', 'caste', 'gender', 'referred_status', 'referred_by', 'referred_by_desc', 'consent_given',
         'consent_upload', 'assent_given', 'assent_upload', 'hospital_name', 'hospital_reg_no', 'has_hiv_been_excluded', 'date_onset_symptoms', 'onset_date', 'age_onset_symptoms_years',
         'age_onset_symptoms_months', 'infections', 'Meningitis_number_of_infection', 'Meningitis_number_of_infection_last_year', 'Otitis_media', 'Otitis_media_last', 'Tonsillitis', 'Tonsillitis_last',
         'Sinusitis', 'Sinusitis_last', 'Pneumonia_Bronchiectasis', 'Pneumonia_Bronchiectasis_last', 'Gastroenteritis_number_of_infection', 'Gastroenteritis_number_of_infection_last_year',
         'Urinary_tract_number_of_infection', 'Urinary_tract_number_of_infection_last_year', 'tissue_infections', 'tissue_infections_last', 'Liver_abscess', 'Liver_abscess_last',
         'Septicemias_number_of_infection', 'Septicemias_number_of_infection_last_year', 'Splenic_abscess', 'Splenic_abscess_last', 'Thrush_or_fungal_number_of_infection',
         'Thrush_or_fungal_number_of_infection_last_year', 'Vaccine_associated_complications', 'bcg', 'Vaccine_associated_complications_BCG_adenitis_age_onset',
         'Vaccine_associated_complications_BCG_adenitis_Axillary', 'Vaccine_associated_complications_BCG_adenitis_Cervical', 'Vaccine_associated_adenitis_Multiple_sites_yes_no',
         'Vaccine_associated_Multiple_sites', 'bcg_options', 'Vaccine_associated_complications_BCG_osis', 'opv', 'OPV_Date_Dose', 'OPV_Flaccid_paralysis', 'OPV_Poliovirus_isolation',
         'Rubella', 'Rubella_Date_Vaccination', 'Rubella_Symptoms_Fever', 'Rubella_Symptoms_Enlarged_lymph_nodes', 'Rubella_Symptoms_Measles_like_rash', 'Measles', 'Measles_Date_Vaccination',
         'Measles_fever', 'Measles_EnlargedLymphNodes', 'Measles_MeaslesLikeRash', 'Failure_to_gain_weight', 'autoimmunity_autoinflammation', 'autoimmunity_autoinflammation_type_symptoms_fever',
         'autoimmunity_autoinflammation_type_symptoms_fever_temp', 'autoimmunity_autoinflammation_type_symptoms_fever_duration', 'autoimmunity_Precipitated_cold',
         'autoimmunity_Precipitated_cold_frequency', 'autoimmunity_AssociatedLymphadenopathy', 'autoimmunity_AbdominalSymptoms', 'autoimmunity_AbdominalSymptoms_1', 'autoimmunity_AbdominalSymptoms_2',
         'autoimmunity_AbdominalSymptoms_3', 'autoimmunity_AbdominalSymptoms_4', 'autoimmunity_AbdominalSymptoms_5', 'autoimmunity_MusculoskeletalSymptoms', 'autoimmunity_MusculoskeletalSymptoms_1',
         'autoimmunity_MusculoskeletalSymptoms_2', 'autoimmunity_MusculoskeletalSymptoms_3', 'autoimmunity_MusculoskeletalSymptoms_3_numberJoints',
         'autoimmunity_MusculoskeletalSymptoms_3_jointDeformity', 'autoimmunity_MusculoskeletalSymptoms_3_Contractures', 'autoimmunity_Osteomyelitis', 'autoimmunity_CNS_Ear_Eye',
         'autoimmunity_CNS_Ear_Eye_1', 'autoimmunity_CNS_Ear_Eye_2', 'autoimmunity_CNS_Ear_Eye_3', 'autoimmunity_CNS_Ear_Eye_4', 'autoimmunity_CNS_Ear_Eye_5', 'autoimmunity_CNS_Ear_Eye_6',
         'autoimmunity_CNS_Ear_Eye_7', 'Skin_Mucosal', 'Skin_Mucosal_1', 'Skin_Mucosal_2', 'Skin_Mucosal_3', 'Skin_Mucosal_4', 'Skin_Mucosal_5', 'Skin_Mucosal_6', 'Skin_Mucosal_7',
         'Skin_Mucosal_8', 'autoimmunity_autoinflammation_type_symptoms_fever_other', 'ALLERGY_ATOPY', 'ALLERGY_ATOPY_opn', 'MALIGNANCY', 'MALIGNANCY_diagnosis',
         'MALIGNANCY_diagnosis_present_before_diagnosis', 'MALIGNANCY_diagnosis_options', 'MALIGNANCY_diagnosis_Biologic', 'ORGANISM_ISOLATED_viral', 'ORGANISM_ISOLATED_viral_1',
         'ORGANISM_ISOLATED_viral_2', 'ORGANISM_ISOLATED_viral_3', 'ORGANISM_ISOLATED_viral_4', 'ORGANISM_ISOLATED_viral_5', 'ORGANISM_ISOLATED_viral_6', 'ORGANISM_ISOLATED_viral_7',
         'ORGANISM_ISOLATED_viral_8', 'ORGANISM_ISOLATED_viral_9', 'ORGANISM_ISOLATED_viral_10', 'ORGANISM_ISOLATED_viral_11', 'ORGANISM_ISOLATED_viral_12', 'ORGANISM_ISOLATED_viral_13',
         'ORGANISM_ISOLATED_viral_14', 'ORGANISM_ISOLATED_viral_14_specify', 'ORGANISM_ISOLATED_Bacterial', 'ORGANISM_ISOLATED_Bacterial_1', 'ORGANISM_ISOLATED_Bacterial_2',
         'ORGANISM_ISOLATED_Bacterial_3', 'ORGANISM_ISOLATED_Bacterial_4', 'ORGANISM_ISOLATED_Bacterial_5', 'ORGANISM_ISOLATED_Bacterial_6', 'ORGANISM_ISOLATED_Bacterial_7',
         'ORGANISM_ISOLATED_Bacterial_8', 'ORGANISM_ISOLATED_Bacterial_9', 'ORGANISM_ISOLATED_Bacterial_10', 'ORGANISM_ISOLATED_Bacterial_11', 'ORGANISM_ISOLATED_Bacterial_12',
         'ORGANISM_ISOLATED_Bacterial_13', 'ORGANISM_ISOLATED_Bacterial_14', 'ORGANISM_ISOLATED_bacterial_14_specify', 'Fungal', 'Fungal_1', 'Fungal_2', 'Fungal_3', 'Fungal_4',
         'Fungal_5', 'Fungal_6', 'Fungal_6_specify', 'Mycobacterial', 'Mycobacterial_1', 'Mycobacterial_2', 'Mycobacterial_3', 'FamilyHistory_Consanguinity',
         'FamilyHistory_Consanguinity_degree', 'FamilyHistory_HistoryYoung_Children', 'FamilyHistory_HistoryYoung_Children_numberSiblingDeaths', 'FamilyHistory_death_cause',
         'FamilyHistory_deaths_male_member', 'FamilyHistory_deaths_male_member_relations', 'FamilyHistory_deaths_male_member_diagnosed_PID', 'FamilyHistory_deaths_male_member_diagnosed_diagnosis',
         'FamilyHistory_deaths_male_member_diagnosed_relation', 'FamilyHistory_diagnosed_listed_registry', 'FamilyHistory_reason_evaluation', 'clinical_exam_Anthropometry_wieght',
         'clinical_exam_Anthropometry_Height', 'clinical_exam_Anthropometry_HeadCircumference', 'DistinctivePhenotypeaDysmorphicFacies', 'DistinctivePhenotypeaaHypoPigmentedHair',
         'DistinctivePhenotypeabTeethAbnormalities', 'DistinctivePhenotypeacAbsentTonsil', 'DistinctivePhenotypeadOralUlcers', 'DistinctivePhenotypeadeSkinHypopigmentation',
         'DistinctivePhenotypeadefLymphAdenopathy', 'DistinctivePhenotypeadefLymphAdenopathy_options', 'DistinctivePhenotypegHepatosplenomegaly', 'DistinctivePhenotypeSkeletalSystemAbnormalities',
         'DistinctivePhenotypeBCG_Scar', 'DistinctivePhenotyFindingaRespiratory', 'DistinctivePhenotyFindingCardiovascular', 'DistinctivePhenotyFindingcAbdominal', 'DistinctivePhenotyFindingdCNS',
         'BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no', 'BroadDiagnosisCategoryImmunodeficiencyAffecting', 'ImmunodeficiencyAffecting_other_specify',
         'BroadDiagnosisCategoryCIDAssociated_yes_no', 'BroadDiagnosisCategoryCIDAssociated', 'BroadDiagnosisCategoryCIDAssociated_Other_Specify', 'BroadDiagnosisCategoryPredominantAntibody_yes_no',
         'BroadDiagnosisCategoryPredominantAntibody', 'BroadDiagnosisCategoryPredominantAntibody_other_specify', 'BroadDiagnosisCategoryDiseasesImmune_yes_no', 'BroadDiagnosisCategoryDiseasesImmune',
         'BroadDiagnosisCategoryDiseasesImmune_other_specify', 'BroadDiagnosisCategoryCongenitalDefects_yes_no', 'BroadDiagnosisCategoryCongenitalDefects',
         'BroadDiagnosisCategoryCongenitalDefects_other_specify', 'BroadDiagnosisCategoryDefectsIntrinsic_yes_no', 'BroadDiagnosisCategoryDefectsIntrinsic',
         'BroadDiagnosisCategoryDefectsIntrinsic_other_specify', 'BroadDiagnosisCategoryAutoinflammatory_yes_no', 'BroadDiagnosisCategoryAutoinflammatory',
         'BroadDiagnosisCategoryAutoinflammatory_other_specify', 'BroadDiagnosisCategoryComplementDeficiency_yes_no', 'BroadDiagnosisCategoryComplementDeficiency',
         'BroadDiagnosisCategoryMarrowFailure_yes_no', 'BroadDiagnosisCategoryMarrowFailure', 'BroadDiagnosisCategoryMarrowFailure_other_specify', 'BroadDiagnosisCategoryPhenocopies_yes_no',
         'BroadDiagnosisCategoryPhenocopies', 'BroadDiagnosisCategoryPhenocopies_other_specify', 'CBC_Date', 'CBC_Date1', 'CBC_Date2', 'CBC_Date3', 'CBC_Hb', 'CBC_Hb1', 'CBC_Hb2',
         'CBC_Hb3', 'CBC_wbc', 'CBC_wbc1', 'CBC_wbc2', 'CBC_wbc3', 'CBC_wbc_level', 'CBC_wbc1_level', 'CBC_wbc2_level', 'CBC_wbc3_level', 'CBC_Lymphcytes', 'CBC_Lymphcytes1',
         'CBC_Lymphcytes2', 'CBC_Lymphcytes3', 'CBC_PMN', 'CBC_PMN1', 'CBC_PMN2', 'CBC_PMN3', 'CBC_Eosinophils', 'CBC_Eosinophils1', 'CBC_Eosinophils2', 'CBC_Eosinophils3',
         'CBC_Basophils', 'CBC_Basophils1', 'CBC_Basophils2', 'CBC_Basophils3', 'CBC_Monocytes', 'CBC_Monocytes1', 'CBC_Monocytes2', 'CBC_Monocytes3', 'CBC_Platelets',
         'CBC_Platelets1', 'CBC_Platelets2', 'CBC_Platelets3', 'M_Platelets', 'M_Platelets1', 'M_Platelets2', 'M_Platelets3', 'phenotype_Absolute_Lymphocyte_count',
         'phenotype_Absolute_Lymphocyte_count_level', 'phenotype_CD3_T_cells', 'phenotype_CD3_T_cells_level', 'CD4_Helper_T', 'CD4_Helper_T_level', 'phenotype_CD8_Cytotoxic_T_cells',
         'phenotype_CD8_Cytotoxic_T_cells_level', 'phenotype_CD19_B_cells', 'phenotype_CD19_B_cells_level', 'phenotype_CD20_B_cells', 'phenotype_CD20_B_cells_level', 'phenotype_CD56CD16_NK_cells',
         'phenotype_CD56CD16_NK_cells_level', 'phenotype_CD25', 'phenotype_CD25_level', 'phenotype_Double_negative_T_cells', 'phenotype_Double_negative_T_cells_level', 'Gamma_delta_T_cells',
         'Gamma_delta_T_cells_level', 'CD4_subset_panel_naive_cd4', 'CD4_subset_panel_naive_cd4_level', 'CD4_subset_panel_Total_Memory_CD4', 'CD4_subset_panel_Total_Memory_CD4_level', 'CD4_CD45RA',
         'CD4_CD45RA_level', 'CD4_CD45RO', 'CD4_CD45RO_level', 'CD8_subset_panel_naive_cd8', 'CD8_subset_panel_naive_cd8_level', 'CD8_subset_panel_Total_Memory_CD8',
         'CD8_subset_panel_Total_Memory_CD8_level', 'CD8_CD45RA', 'CD8_CD45RA_level', 'CD8_CD45RO', 'CD8_CD45RO_level', 'T_regulatory_cells', 'T_regulatory_cells_level', 'Naive_B_cells',
         'Naive_B_cells_level', 'Naive_B_cells_Transitional_B_cells', 'Naive_B_cells_Transitional_B_cells_level', 'cd27_B_cells', 'cd27_B_cells_level', 'cd27_igm_Bcells', 'cd27_igm_Bcells_level',
         'cd27_igD_Bcells', 'cd27_igD_Bcells_level', 'Immunoglobulin_IgG', 'Immunoglobulin_IgG_level', 'Immunoglobulin_IgG1', 'Immunoglobulin_IgG1_level', 'Immunoglobulin_IgG2',
         'Immunoglobulin_IgG2_level', 'Immunoglobulin_IgG3', 'Immunoglobulin_IgG3_level', 'Immunoglobulin_IgG4', 'Immunoglobulin_IgG4_level', 'Immunoglobulin_IgA', 'Immunoglobulin_IgA_level',
         'Immunoglobulin_IgM', 'Immunoglobulin_IgM_level', 'Immunoglobulin_IgE', 'Immunoglobulin_IgE_level', 'Immunoglobulin_IgD', 'Immunoglobulin_IgD_level', 'Vaccine_responses_tested',
         'Vaccine_responses_tested_Protein', 'diphtheria', 'tetanus', 'protien_conjugated_hib', 'Polysaccharide_hib', 'salmonella_typhi', 'PHI_174antigen', 'Vaccine_responses_tested_Iso_hemagglutinin',
         'Iso_hemagglutinin_antiA', 'Iso_hemagglutinin_antiB', 'Vaccine_responses_tested_TREC_tested', 'if_yes', 'Vaccine_responses_tested_Lymphocyte_functional_tests', 'pha', 'anti_cd', 'others',
         'eexpression_studies', 'scid', 'Expression_CD123', 'hlh', 'Expression_Perforin_expression', 'Expression_CD107a_on_NK_cells', 'Expression_CD107a_on_CD8_cells', 'mxc2',
         'Expression_hda_hr_cells', 'foxp3', 'Expression_th1_cells', 'xla', 'btk', 'lad', 'cd18', 'cd11', 'msmd', 'cd212_lymphocytes', 'cd119_monocytes', 'ifn_gama_monocyte',
         'stati_monocyte', 'stat4_monocyte', 'higm', 'cd154', 'cd40', 'was', 'wasp', 'hige', 'DOCK8', 'STAT3', 'TH17', 'Vaccine_responses_Complement_function', 'C2', 'C3', 'C4', 'Cq', 'CH50',
         'AH50', 'factorD', 'factorH', 'factorI', 'Properdin', 'Vaccine_responses_Beta_Repertoire_analysis', 'Vaccine_responses_Beta_yesRepertoire_analysis', 'Vaccine_responses_Auto_antibodies', 'ANA',
         'Anti_neutrophil_antibody', 'Anti_platelet_antibody', 'Anti_C1q_antibody', 'Anti_C1_esterase_antibody', 'ada_enzyme', 'pnp_enzyme', 'NBT', 'Vaccine_responses_DHR', 'yes',
         'Vaccine_responses_Flow_cytometric_expression_b558', 'Vaccine_responses_Flow_cytometric_expression1', 'Vaccine_responses_Flow_cytometric_expression_p67phox',
         'Vaccine_responses_Flow_cytometric_expression_p40phox', 'Vaccine_responses_Flow_cytometric_expression_p22', 'Maternal_engraftment', 'Alfa_feto_protein', 'Alfa_feto_protein_yes', 'Karyotype',
         'Karyotype_finding', 'Chromosomal', 'Chromosomal_finding', 'Radiological_investigation', 'Radiological_investigation_finding', 'FISH', 'FISH_finding', 'any_other', 'any_other_finding',
         'Vaccine_responses_Molecular_diagnosis', 'tb_Nscid', 'tb_Pscid', 'malignancy_RFXANK', 'malignancy_RFXANK', 'malignancy_RFX5', 'malignancy_RFXAP', 'malignancy_DOCK8',
         'malignancy_CD40', 'malignancy_CD40L', 'malignancy_STAT3', 'malignancy_PGM3', 'malignancy_SPJNKS', 'malignancy_WAS', 'malignancy_ATM', 'malignancy_LDC22', 'malignancy_BtK',
         'malignancy_CVID', 'malignancy_PRF1', 'malignancy_STX11', 'malignancy_UNC13D', 'malignancy_STXBP2', 'malignancy_FAAP24', 'malignancy_SLC7A7', 'hlh_others', 'hlh_other',
         'malignancy_TNFRSF6', 'malignancy_TNFSF6', 'malignancy_CASP8', 'malignancy_CASP10', 'malignancy_FADD', 'malignancy_LYST', 'malignancy_RAB27A', 'malignancy_CYBB',
         'malignancy_NCF1', 'malignancy_CYBA', 'malignancy_NCF2', 'malignancy_NCF4', 'malignancy_CYBC1', 'malignancy_G6PD', 'malignancy_ITGB2', 'malignancy_SLC35C1',
         'malignancy_FERMT3', 'malignancy_ELANE', 'malignancy_HAX1', 'malignancy_G6PC3', 'malignancy_GFI1', 'malignancy_VPS45', 'malignancy_CFTR', 'malignancy_IFNGR1',
         'malignancy_IFNGR2', 'malignancy_IL12RB1', 'malignancy_STAT1', 'malignancy_TYK2', 'malignancy_IRF8', 'malignancy_RORC', 'malignancy_ISG15', 'malignancy_IL12B',
         'malignancy_IL12RB2', 'malignancy_IL23', 'malignancy_SPPL2A', 'malignancy_JAK1', 'malignancy_STAT1GOF', 'malignancy_IL17F', 'malignancy_IL17RA', 'malignancy_IL17RC',
         'malignancy_IRAK4', 'malignancy_Myd88', 'malignancy_Others_specify', 'mutation_type', 'type_of_variant', 'zygosity', 'DNA_change', 'Protein_expressed_checked',
         'Protein_expressed', 'has_patient_received_replacement_therapy', 'is_patient_currently_replacement_therapy', 'Date_of_initiation_of_therapy_1', 'age1', 'Date_of_termination_of_therapy_2',
         'reaction', 'dose', 'route11', 'frequency', 'Has_patient_used_anti_infective_medication', 'courses_of_antibiotic_treatment_has_the_patient', 'drug_name', 'indication',
         'route', 'course', 'adverse_reaction', 'drug_name1', 'indication1', 'route1', 'course1', 'adverse_reaction1', 'drug_name2', 'indication2', 'route2', 'course2',
         'adverse_reaction2', 'drug_name3', 'indication3', 'route3', 'course3', 'adverse_reaction3', 'drug_name4', 'indication4', 'route4', 'course4', 'adverse_reaction4',
         'Immuno_modulator_medication_drug_name', 'imm_indication', 'imm_improvement', 'imm_adverse_reaction', 'Immuno_modulator_medication_drug_name1', 'imm_indication1', 'imm_improvement1',
         'imm_adverse_reaction1', 'Immuno_modulator_medication_drug_name2', 'imm_indication2', 'imm_improvement2', 'imm_adverse_reaction2', 'Immuno_modulator_medication_drug_name3',
         'imm_indication3', 'imm_improvement3', 'imm_adverse_reaction3', 'Immuno_modulator_medication_drug_name4', 'imm_indication4', 'imm_improvement4', 'imm_adverse_reaction4',
         'surgeries', 'Other_treatment', 'Has_patient_undergone_HSCT', 'type_of_transplant', 'outcome_alive', 'outcome_alive_no_date', 'outcome_alive_no_cause',
         'outcome_alive_no_cause_others_specify', ])

    users = profile_pid.objects.filter(user=request.user).prefetch_related('patient_pid').values_list('register_id__institute_name', 'uniqueId', 'pid_icmr_unique_no', 'pid_final_diagnosis', 'pid_date_of_record',
                                                                                      'pid_clinical_exam_date',
                                                                                  'pid_date_of_birth', 'pid_patient_name', 'pid_father_name', 'pid_mother_name', 'pid_paitent_id', 'pid_paitent_id_list',
                                                                                  'pid_patient_id_no', 'pid_father_mother_id', 'pid_father_mother_id_no', 'pid_permanent_addr', 'pid_state', 'pid_district',
                                                                                  'pid_city_name', 'pid_country_name', 'pid_land_line_no', 'pid_mother_mobile_no', 'pid_father_mobile_no', 'pid_email', 'pid_religion',
                                                                                  'pid_caste', 'pid_gender', 'pid_referred_status', 'pid_referred_by', 'pid_referred_by_desc', 'pid_consent_given', 'pid_consent_upload', 'pid_assent_given', 'pid_assent_upload', 'pid_hospital_name', 'pid_hospital_reg_no', 'profile_pid__pid_has_hiv_been_excluded', 'profile_pid__pid_date_onset_symptoms', 'profile_pid__pid_onset_date', 'profile_pid__age_onset_symptoms_years', 'profile_pid__age_onset_symptoms_months', 'profile_pid__pid_infections', 'profile_pid__pid_Meningitis_number_of_infection', 'profile_pid__pid_Meningitis_number_of_infection_last_year', 'profile_pid__Otitis_media', 'profile_pid__Otitis_media_last', 'profile_pid__Tonsillitis', 'profile_pid__Tonsillitis_last', 'profile_pid__Sinusitis', 'profile_pid__Sinusitis_last', 'profile_pid__Pneumonia_Bronchiectasis', 'profile_pid__Pneumonia_Bronchiectasis_last', 'profile_pid__pid_Gastroenteritis_number_of_infection', 'profile_pid__pid_Gastroenteritis_number_of_infection_last_year', 'profile_pid__pid_Urinary_tract_number_of_infection', 'profile_pid__pid_Urinary_tract_number_of_infection_last_year', 'profile_pid__tissue_infections', 'profile_pid__tissue_infections_last', 'profile_pid__Liver_abscess', 'profile_pid__Liver_abscess_last', 'profile_pid__pid_Septicemias_number_of_infection', 'profile_pid__pid_Septicemias_number_of_infection_last_year', 'profile_pid__Splenic_abscess', 'profile_pid__Splenic_abscess_last', 'profile_pid__pid_Thrush_or_fungal_number_of_infection', 'profile_pid__pid_Thrush_or_fungal_number_of_infection_last_year', 'profile_pid__pid_Vaccine_associated_complications', 'profile_pid__pid_bcg', 'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_age_onset', 'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_Axillary', 'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_Cervical', 'profile_pid__pid_Vaccine_associated_adenitis_Multiple_sites_yes_no', 'profile_pid__pid_Vaccine_associated_Multiple_sites', 'profile_pid__pid_bcg_options', 'profile_pid__pid_Vaccine_associated_complications_BCG_osis', 'profile_pid__pid_opv', 'profile_pid__pid_OPV_Date_Dose', 'profile_pid__pid_OPV_Flaccid_paralysis', 'profile_pid__pid_OPV_Poliovirus_isolation', 'profile_pid__pid_Rubella', 'profile_pid__pid_Rubella_Date_Vaccination', 'profile_pid__pid_Rubella_Symptoms_Fever', 'profile_pid__pid_Rubella_Symptoms_Enlarged_lymph_nodes', 'profile_pid__pid_Rubella_Symptoms_Measles_like_rash', 'profile_pid__pid_Measles', 'profile_pid__pid_Measles_Date_Vaccination', 'profile_pid__pid_Measles_fever', 'profile_pid__pid_Measles_EnlargedLymphNodes', 'profile_pid__pid_Measles_MeaslesLikeRash', 'profile_pid__pid_Failure_to_gain_weight', 'profile_pid__pid_autoimmunity_autoinflammation', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_temp', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_duration', 'profile_pid__pid_autoimmunity_Precipitated_cold', 'profile_pid__pid_autoimmunity_Precipitated_cold_frequency', 'profile_pid__pid_autoimmunity_AssociatedLymphadenopathy', 'profile_pid__pid_autoimmunity_AbdominalSymptoms', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_1', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_2', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_3', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_4', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_5', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_1', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_2', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_numberJoints', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_jointDeformity', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_Contractures', 'profile_pid__pid_autoimmunity_Osteomyelitis', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_1', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_2', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye3', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_4', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_5', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_6', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_7', 'profile_pid__pid_Skin_Mucosal', 'profile_pid__pid_Skin_Mucosal_1', 'profile_pid__pid_Skin_Mucosal_2', 'profile_pid__pid_Skin_Mucosal_3', 'profile_pid__pid_Skin_Mucosal_4', 'profile_pid__pid_Skin_Mucosal_5', 'profile_pid__pid_Skin_Mucosal_6', 'profile_pid__pid_Skin_Mucosal_7', 'profile_pid__pid_Skin_Mucosal_8', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_other', 'profile_pid__pid_ALLERGY_ATOPY', 'profile_pid__pid_ALLERGY_ATOPY_opn', 'profile_pid__pid_MALIGNANCY', 'profile_pid__pid_MALIGNANCY_diagnosis', 'profile_pid__pid_MALIGNANCY_diagnosis_present_before_diagnosis', 'profile_pid__pid_MALIGNANCY_diagnosis_options', 'profile_pid__pid_MALIGNANCY_diagnosis_Biologic', 'profile_pid__pid_ORGANISM_ISOLATED_viral', 'profile_pid__pid_ORGANISM_ISOLATED_viral_1', 'profile_pid__pid_ORGANISM_ISOLATED_viral_2', 'profile_pid__pid_ORGANISM_ISOLATED_viral_3', 'profile_pid__pid_ORGANISM_ISOLATED_viral_4', 'profile_pid__pid_ORGANISM_ISOLATED_viral_5', 'profile_pid__pid_ORGANISM_ISOLATED_viral_6', 'profile_pid__pid_ORGANISM_ISOLATED_viral_7', 'profile_pid__pid_ORGANISM_ISOLATED_viral_8', 'profile_pid__pid_ORGANISM_ISOLATED_viral_9', 'profile_pid__pid_ORGANISM_ISOLATED_viral_10', 'profile_pid__pid_ORGANISM_ISOLATED_viral_11', 'profile_pid__pid_ORGANISM_ISOLATED_viral_12', 'profile_pid__pid_ORGANISM_ISOLATED_viral_13', 'profile_pid__pid_ORGANISM_ISOLATED_viral_14', 'profile_pid__pid_ORGANISM_ISOLATED_viral_14_specify', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_1', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_2', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_3', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_4', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_5', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_6', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_7', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_8', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_9', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_10', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_11', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_12', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_13', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_14', 'profile_pid__pid_ORGANISM_ISOLATED_bacterial_14_specify', 'profile_pid__pid_Fungal', 'profile_pid__pid_Fungal_1', 'profile_pid__pid_Fungal_2', 'profile_pid__pid_Fungal_3', 'profile_pid__pid_Fungal_4', 'profile_pid__pid_Fungal_5', 'profile_pid__pid_Fungal_6', 'profile_pid__pid_Fungal_6_specify', 'profile_pid__pid_Mycobacterial', 'profile_pid__pid_Mycobacterial_1', 'profile_pid__pid_Mycobacterial_2', 'profile_pid__pid_Mycobacterial_3', 'profile_pid__pid_FamilyHistory_Consanguinity', 'profile_pid__pid_FamilyHistory_Consanguinity_degree', 'profile_pid__pid_FamilyHistory_HistoryYoung_Children', 'profile_pid__pid_FamilyHistory_HistoryYoung_Children_numberSiblingDeaths', 'profile_pid__pid_FamilyHistory_death_cause', 'profile_pid__pid_FamilyHistory_deaths_male_member', 'profile_pid__pid_FamilyHistory_deaths_male_member_relations', 'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID', 'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID_diagnosis', 'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID_relation', 'profile_pid__pid_FamilyHistory_diagnosed_PID_listed_registry', 'profile_pid__pid_FamilyHistory_reason_pid_evaluation', 'profile_pid__pid_clinical_exam_Anthropometry_wieght', 'profile_pid__pid_clinical_exam_Anthropometry_Height', 'profile_pid__pid_clinical_exam_Anthropometry_HeadCircumference', 'profile_pid__pid_DistinctivePhenotypeaDysmorphicFacies', 'profile_pid__pid_DistinctivePhenotypeaaHypoPigmentedHair', 'profile_pid__pid_DistinctivePhenotypeabTeethAbnormalities', 'profile_pid__pid_DistinctivePhenotypeacAbsentTonsil', 'profile_pid__pid_DistinctivePhenotypeadOralUlcers', 'profile_pid__pid_DistinctivePhenotypeadeSkinHypopigmentation', 'profile_pid__pid_DistinctivePhenotypeadefLymphAdenopathy', 'profile_pid__pid_DistinctivePhenotypeadefLymphAdenopathy_options', 'profile_pid__pid_DistinctivePhenotypegHepatosplenomegaly', 'profile_pid__pid_DistinctivePhenotypeSkeletalSystemAbnormalities', 'profile_pid__pid_DistinctivePhenotypeBCG_Scar', 'profile_pid__pid_DistinctivePhenotyFindingaRespiratory', 'profile_pid__pid_DistinctivePhenotyFindingCardiovascular', 'profile_pid__pid_DistinctivePhenotyFindingcAbdominal', 'profile_pid__pid_DistinctivePhenotyFindingdCNS', 'profile_pid__pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryImmunodeficiencyAffecting', 'profile_pid__pid_ImmunodeficiencyAffecting_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated', 'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated_Other_Specify', 'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody', 'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune', 'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects', 'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic', 'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory', 'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryComplementDeficiency_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryComplementDeficiency', 'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure', 'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryPhenocopies_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryPhenocopies', 'profile_pid__pid_BroadDiagnosisCategoryPhenocopies_other_specify', 'profile_pid__pid_CBC_Date', 'profile_pid__pid_CBC_Date1', 'profile_pid__pid_CBC_Date2', 'profile_pid__pid_CBC_Date3', 'profile_pid__pid_CBC_Hb', 'profile_pid__pid_CBC_Hb1', 'profile_pid__pid_CBC_Hb2', 'profile_pid__pid_CBC_Hb3', 'profile_pid__pid_CBC_wbc', 'profile_pid__pid_CBC_wbc1', 'profile_pid__pid_CBC_wbc2', 'profile_pid__pid_CBC_wbc3', 'profile_pid__pid_CBC_wbc_level', 'profile_pid__pid_CBC_wbc1_level', 'profile_pid__pid_CBC_wbc2_level', 'profile_pid__pid_CBC_wbc3_level', 'profile_pid__pid_CBC_Lymphcytes', 'profile_pid__pid_CBC_Lymphcytes1', 'profile_pid__pid_CBC_Lymphcytes2', 'profile_pid__pid_CBC_Lymphcytes3', 'profile_pid__pid_CBC_PMN', 'profile_pid__pid_CBC_PMN1', 'profile_pid__pid_CBC_PMN2', 'profile_pid__pid_CBC_PMN3', 'profile_pid__pid_CBC_Eosinophils', 'profile_pid__pid_CBC_Eosinophils1', 'profile_pid__pid_CBC_Eosinophils2', 'profile_pid__pid_CBC_Eosinophils3', 'profile_pid__pid_CBC_Basophils', 'profile_pid__pid_CBC_Basophils1', 'profile_pid__pid_CBC_Basophils2', 'profile_pid__pid_CBC_Basophils3', 'profile_pid__pid_CBC_Monocytes', 'profile_pid__pid_CBC_Monocytes1', 'profile_pid__pid_CBC_Monocytes2', 'profile_pid__pid_CBC_Monocytes3', 'profile_pid__pid_CBC_Platelets', 'profile_pid__pid_CBC_Platelets1', 'profile_pid__pid_CBC_Platelets2', 'profile_pid__pid_CBC_Platelets3', 'profile_pid__pid_M_Platelets', 'profile_pid__pid_M_Platelets1', 'profile_pid__pid_M_Platelets2', 'profile_pid__pid_M_Platelets3', 'profile_pid__pid_phenotype_Absolute_Lymphocyte_count', 'profile_pid__pid_phenotype_Absolute_Lymphocyte_count_level', 'profile_pid__pid_phenotype_CD3_T_cells', 'profile_pid__pid_phenotype_CD3_T_cells_level', 'profile_pid__pid_CD4_Helper_T', 'profile_pid__pid_CD4_Helper_T_level', 'profile_pid__pid_phenotype_CD8_Cytotoxic_T_cells', 'profile_pid__pid_phenotype_CD8_Cytotoxic_T_cells_level', 'profile_pid__pid_phenotype_CD19_B_cells', 'profile_pid__pid_phenotype_CD19_B_cells_level', 'profile_pid__pid_phenotype_CD20_B_cells', 'profile_pid__pid_phenotype_CD20_B_cells_level', 'profile_pid__pid_phenotype_CD56CD16_NK_cells', 'profile_pid__pid_phenotype_CD56CD16_NK_cells_level', 'profile_pid__pid_phenotype_CD25', 'profile_pid__pid_phenotype_CD25_level', 'profile_pid__pid_phenotype_Double_negative_T_cells', 'profile_pid__pid_phenotype_Double_negative_T_cells_level', 'profile_pid__Gamma_delta_T_cells', 'profile_pid__Gamma_delta_T_cells_level', 'profile_pid__pid_CD4_subset_panel_naive_cd4', 'profile_pid__pid_CD4_subset_panel_naive_cd4_level', 'profile_pid__pid_CD4_subset_panel_Total_Memory_CD4', 'profile_pid__pid_CD4_subset_panel_Total_Memory_CD4_level', 'profile_pid__CD4_CD45RA', 'profile_pid__CD4_CD45RA_level', 'profile_pid__CD4_CD45RO', 'profile_pid__CD4_CD45RO_level', 'profile_pid__pid_CD8_subset_panel_naive_cd8', 'profile_pid__pid_CD8_subset_panel_naive_cd8_level', 'profile_pid__pid_CD8_subset_panel_Total_Memory_CD8', 'profile_pid__pid_CD8_subset_panel_Total_Memory_CD8_level', 'profile_pid__CD8_CD45RA', 'profile_pid__CD8_CD45RA_level', 'profile_pid__CD8_CD45RO', 'profile_pid__CD8_CD45RO_level', 'profile_pid__pid_T_regulatory_cells', 'profile_pid__pid_T_regulatory_cells_level', 'profile_pid__pid_Naive_B_cells', 'profile_pid__pid_Naive_B_cells_level', 'profile_pid__pid_Naive_B_cells_Transitional_B_cells', 'profile_pid__pid_Naive_B_cells_Transitional_B_cells_level', 'profile_pid__cd27_B_cells', 'profile_pid__cd27_B_cells_level', 'profile_pid__cd27_igm_Bcells', 'profile_pid__cd27_igm_Bcells_level', 'profile_pid__cd27_igD_Bcells', 'profile_pid__cd27_igD_Bcells_level', 'profile_pid__pid_Immunoglobulin_IgG', 'profile_pid__pid_Immunoglobulin_IgG_level', 'profile_pid__pid_Immunoglobulin_IgG1', 'profile_pid__pid_Immunoglobulin_IgG1_level', 'profile_pid__pid_Immunoglobulin_IgG2', 'profile_pid__pid_Immunoglobulin_IgG2_level', 'profile_pid__pid_Immunoglobulin_IgG3', 'profile_pid__pid_Immunoglobulin_IgG3_level', 'profile_pid__pid_Immunoglobulin_IgG4', 'profile_pid__pid_Immunoglobulin_IgG4_level', 'profile_pid__pid_Immunoglobulin_IgA', 'profile_pid__pid_Immunoglobulin_IgA_level', 'profile_pid__pid_Immunoglobulin_IgM', 'profile_pid__pid_Immunoglobulin_IgM_level', 'profile_pid__pid_Immunoglobulin_IgE', 'profile_pid__pid_Immunoglobulin_IgE_level', 'profile_pid__pid_Immunoglobulin_IgD', 'profile_pid__pid_Immunoglobulin_IgD_level', 'profile_pid__pid_Vaccine_responses_tested', 'profile_pid__pid_Vaccine_responses_tested_Protein', 'profile_pid__diphtheria', 'profile_pid__tetanus', 'profile_pid__protien_conjugated_hib', 'profile_pid__Polysaccharide_hib', 'profile_pid__salmonella_typhi', 'profile_pid__PHI_174antigen', 'profile_pid__pid_Vaccine_responses_tested_Iso_hemagglutinin', 'profile_pid__Iso_hemagglutinin_antiA', 'profile_pid__Iso_hemagglutinin_antiB', 'profile_pid__pid_Vaccine_responses_tested_TREC_tested', 'profile_pid__if_yes', 'profile_pid__pid_Vaccine_responses_tested_Lymphocyte_functional_tests', 'profile_pid__pha', 'profile_pid__anti_cd', 'profile_pid__others', 'profile_pid__pid_eexpression_studies', 'profile_pid__pid_scid', 'profile_pid__pid_Expression_CD123', 'profile_pid__pid_hlh', 'profile_pid__pid_Expression_Perforin_expression', 'profile_pid__pid_Expression_CD107a_on_NK_cells', 'profile_pid__pid_Expression_CD107a_on_CD8_cells', 'profile_pid__pid_mxc2', 'profile_pid__pid_Expression_hda_hr_cells', 'profile_pid__pid_foxp3', 'profile_pid__pid_Expression_th1_cells', 'profile_pid__pid_xla', 'profile_pid__btk', 'profile_pid__pid_lad', 'profile_pid__cd18', 'profile_pid__cd11', 'profile_pid__pid_msmd', 'profile_pid__pid_cd212_lymphocytes', 'profile_pid__pid_cd119_monocytes', 'profile_pid__pid_ifn_gama_monocyte', 'profile_pid__pid_stati_monocyte', 'profile_pid__pid_stat4_monocyte', 'profile_pid__pid_higm', 'profile_pid__cd154', 'profile_pid__cd40', 'profile_pid__pid_was', 'profile_pid__wasp', 'profile_pid__pid_hige', 'profile_pid__DOCK8', 'profile_pid__STAT3', 'profile_pid__TH17', 'profile_pid__pid_Vaccine_responses_Complement_function', 'profile_pid__C2', 'profile_pid__C3', 'profile_pid__C4', 'profile_pid__Cq', 'profile_pid__CH50', 'profile_pid__AH50', 'profile_pid__factorD', 'profile_pid__factorH', 'profile_pid__factorI', 'profile_pid__Properdin', 'profile_pid__pid_Vaccine_responses_Beta_Repertoire_analysis', 'profile_pid__pid_Vaccine_responses_Beta_yesRepertoire_analysis', 'profile_pid__pid_Vaccine_responses_Auto_antibodies', 'profile_pid__ANA', 'profile_pid__Anti_neutrophil_antibody', 'profile_pid__Anti_platelet_antibody', 'profile_pid__Anti_C1q_antibody', 'profile_pid__Anti_C1_esterase_antibody', 'profile_pid__ada_enzyme', 'profile_pid__pnp_enzyme', 'profile_pid__NBT', 'profile_pid__pid_Vaccine_responses_DHR', 'profile_pid__yes', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_b558', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression1', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p67phox', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p40phox', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p22', 'profile_pid__Maternal_engraftment', 'profile_pid__Alfa_feto_protein', 'profile_pid__Alfa_feto_protein_yes', 'profile_pid__Karyotype', 'profile_pid__Karyotype_finding', 'profile_pid__Chromosomal', 'profile_pid__Chromosomal_finding', 'profile_pid__Radiological_investigation', 'profile_pid__Radiological_investigation_finding', 'profile_pid__FISH', 'profile_pid__FISH_finding', 'profile_pid__any_other', 'profile_pid__any_other_finding', 'profile_pid__pid_Vaccine_responses_Molecular_diagnosis', 'profile_pid__tb_Nscid', 'profile_pid__tb_Pscid', 'profile_pid__pid_malignancy_RFXANK', 'profile_pid__pid_malignancy_RFXANK', 'profile_pid__pid_malignancy_RFX5', 'profile_pid__pid_malignancy_RFXAP', 'profile_pid__pid_malignancy_DOCK8', 'profile_pid__pid_malignancy_CD40', 'profile_pid__pid_malignancy_CD40L', 'profile_pid__pid_malignancy_STAT3', 'profile_pid__pid_malignancy_PGM3', 'profile_pid__pid_malignancy_SPJNKS', 'profile_pid__pid_malignancy_WAS', 'profile_pid__pid_malignancy_ATM', 'profile_pid__pid_malignancy_LDC22', 'profile_pid__pid_malignancy_BtK', 'profile_pid__pid_malignancy_CVID', 'profile_pid__pid_malignancy_PRF1', 'profile_pid__pid_malignancy_STX11', 'profile_pid__pid_malignancy_UNC13D', 'profile_pid__pid_malignancy_STXBP2', 'profile_pid__pid_malignancy_FAAP24', 'profile_pid__pid_malignancy_SLC7A7', 'profile_pid__pid_hlh_others', 'profile_pid__pid_hlh_other', 'profile_pid__pid_malignancy_TNFRSF6', 'profile_pid__pid_malignancy_TNFSF6', 'profile_pid__pid_malignancy_CASP8', 'profile_pid__pid_malignancy_CASP10', 'profile_pid__pid_malignancy_FADD', 'profile_pid__pid_malignancy_LYST', 'profile_pid__pid_malignancy_RAB27A', 'profile_pid__pid_malignancy_CYBB', 'profile_pid__pid_malignancy_NCF1', 'profile_pid__pid_malignancy_CYBA', 'profile_pid__pid_malignancy_NCF2', 'profile_pid__pid_malignancy_NCF4', 'profile_pid__pid_malignancy_CYBC1', 'profile_pid__pid_malignancy_G6PD', 'profile_pid__pid_malignancy_ITGB2', 'profile_pid__pid_malignancy_SLC35C1', 'profile_pid__pid_malignancy_FERMT3', 'profile_pid__pid_malignancy_ELANE', 'profile_pid__pid_malignancy_HAX1', 'profile_pid__pid_malignancy_G6PC3', 'profile_pid__pid_malignancy_GFI1', 'profile_pid__pid_malignancy_VPS45', 'profile_pid__pid_malignancy_CFTR', 'profile_pid__pid_malignancy_IFNGR1', 'profile_pid__pid_malignancy_IFNGR2', 'profile_pid__pid_malignancy_IL12RB1', 'profile_pid__pid_malignancy_STAT1', 'profile_pid__pid_malignancy_TYK2', 'profile_pid__pid_malignancy_IRF8', 'profile_pid__pid_malignancy_RORC', 'profile_pid__pid_malignancy_ISG15', 'profile_pid__pid_malignancy_IL12B', 'profile_pid__pid_malignancy_IL12RB2', 'profile_pid__pid_malignancy_IL23', 'profile_pid__pid_malignancy_SPPL2A', 'profile_pid__pid_malignancy_JAK1', 'profile_pid__pid_malignancy_STAT1GOF', 'profile_pid__pid_malignancy_IL17F', 'profile_pid__pid_malignancy_IL17RA', 'profile_pid__pid_malignancy_IL17RC', 'profile_pid__pid_malignancy_IRAK4', 'profile_pid__pid_malignancy_Myd88', 'profile_pid__pid_malignancy_Others_specify', 'profile_pid__pid_mutation_type', 'profile_pid__pid_type_of_variant', 'profile_pid__pid_zygosity', 'profile_pid__pid_DNA_change', 'profile_pid__pid_Protein_expressed_checked', 'profile_pid__pid_Protein_expressed', 'profile_pid__pid_has_patient_received_replacement_therapy', 'profile_pid__pid_is_patient_currently_replacement_therapy', 'profile_pid__pid_Date_of_initiation_of_therapy_1', 'profile_pid__pid_age1', 'profile_pid__pid_Date_of_termination_of_therapy_2', 'profile_pid__pid_reaction', 'profile_pid__pid_dose', 'profile_pid__pid_route11', 'profile_pid__pid_frequency', 'profile_pid__pid_Has_patient_used_anti_infective_medication', 'profile_pid__pid_courses_of_antibiotic_treatment_has_the_patient', 'profile_pid__pid_drug_name', 'profile_pid__pid_indication', 'profile_pid__pid_route', 'profile_pid__pid_course', 'profile_pid__pid_adverse_reaction', 'profile_pid__pid_drug_name1', 'profile_pid__pid_indication1', 'profile_pid__pid_route1', 'profile_pid__pid_course1', 'profile_pid__pid_adverse_reaction1', 'profile_pid__pid_drug_name2', 'profile_pid__pid_indication2', 'profile_pid__pid_route2', 'profile_pid__pid_course2', 'profile_pid__pid_adverse_reaction2', 'profile_pid__pid_drug_name3', 'profile_pid__pid_indication3', 'profile_pid__pid_route3', 'profile_pid__pid_course3', 'profile_pid__pid_adverse_reaction3', 'profile_pid__pid_drug_name4', 'profile_pid__pid_indication4', 'profile_pid__pid_route4', 'profile_pid__pid_course4', 'profile_pid__pid_adverse_reaction4', 'profile_pid__pid_Immuno_modulator_medication_drug_name', 'profile_pid__pid_imm_indication', 'profile_pid__pid_imm_improvement', 'profile_pid__pid_imm_adverse_reaction', 'profile_pid__pid_Immuno_modulator_medication_drug_name1', 'profile_pid__pid_imm_indication1', 'profile_pid__pid_imm_improvement1', 'profile_pid__pid_imm_adverse_reaction1', 'profile_pid__pid_Immuno_modulator_medication_drug_name2', 'profile_pid__pid_imm_indication2', 'profile_pid__pid_imm_improvement2', 'profile_pid__pid_imm_adverse_reaction2', 'profile_pid__pid_Immuno_modulator_medication_drug_name3', 'profile_pid__pid_imm_indication3', 'profile_pid__pid_imm_improvement3', 'profile_pid__pid_imm_adverse_reaction3', 'profile_pid__pid_Immuno_modulator_medication_drug_name4', 'profile_pid__pid_imm_indication4', 'profile_pid__pid_imm_improvement4', 'profile_pid__pid_imm_adverse_reaction4', 'profile_pid__pid_surgeries', 'profile_pid__Other_treatment', 'profile_pid__pid_Has_patient_undergone_HSCT', 'profile_pid__pid_type_of_transplant', 'profile_pid__pid_outcome_alive', 'profile_pid__pid_outcome_alive_no_date', 'profile_pid__pid_outcome_alive_no_cause', 'profile_pid__pid_outcome_alive_no_cause_others_specify',)
    for user in users:
        writer.writerow(user)

    return response





@login_required(login_url='login')
def update_qa_qc_pid(request, pk):
    user = request.user
    register = Register.objects.get(user=request.user)
    patient = profile_pid.objects.get(id=pk)
    form2 = QApidForm(instance=patient)

    if request.method == 'POST':
        form2 = QApidForm(request.POST, request.FILES, instance=patient)
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
            return redirect('total_record_pid_admin')
        else:
            context = {'form2': form2, }
            return render(request, 'update_qa_qc_pid.html', context)

    context = {'form2': form2, }
    return render(request, 'update_qa_qc_pid.html', context)


@login_required(login_url='login')
def view_qa_qc_pid(request, pk):
    user = request.user
    patient = profile_pid.objects.get(id=pk)
    quality = patient.quality_result
    result = patient.quality_reason

    return HttpResponse(f"<h2><label>Quality result</label> </h2> <h2>{quality}</h2> <hr> <h2> <label >Remark </label></h2> <h2>{result}</h2>")
