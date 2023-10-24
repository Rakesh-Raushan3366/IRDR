import csv
from collections import OrderedDict
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
# import local data
from bleeding.models import *
from fabry.models import *
from glycogen.models import *
from iem.models import *
from mucopoly.models import *
from nmd.models import *
from pid.models import *
from pompe.models import *
from skeletal.models import *
from smallmolecule.models import *
from storage.models import *
from thalasemia.models import *
from .decorators import unauthenticated_user
from .forms import *


# import viewsets

@unauthenticated_user
def registerPage(request):
    form1 = CreateUserForm()

    if request.method == 'POST':
        form1 = CreateUserForm(request.POST)

        if form1.is_valid():
            form = form1.save()
            username = form1.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form1': form1, }
    return render(request, 'register.html', context)

# @unauthenticated_user
# def updatePage(request):
#     form1 = UpdateUserForm()
#
#     if request.method == 'POST':
#         form1 = UpdateUserForm(request.POST)
#
#         if form1.is_valid():
#             form = form1.save()
#             username = form1.cleaned_data.get('username')
#
#             messages.success(request, 'Account was updated for ' + username)
#             return redirect('login')
#
#     context = {'form1': form1, }
#     return render(request, 'update_profile.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        group1 = Group.objects.get(name='Admin')

        print(group1.user_set.all())
        print(group1.id)
        print(User.objects.all().prefetch_related('group').values('groups'))

        group_access = User.objects.filter(id=user.id).prefetch_related('group').values('groups')
        user1 = group_access[0]['groups']
        print(user1)

        if user is not None and user1 == group1.id:
            login(request, user)
            return redirect('institute')
        elif user is not None:
            login(request, user)
            return redirect('info')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)



@login_required(login_url='login')
def update_profile(request,):
    user = request.user
    register = Register.objects.get(user=request.user)
    form1 = RegisterForm(instance=register)
    if request.method == 'POST':
        form1 = RegisterForm(request.POST, request.FILES, instance=register)

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.register = register
            auth1.save()
            return redirect("/")
        else:
            context = {'form1': form1, }
            return render(request, 'update_profile.html', context)

    context = {'form1': form1, }
    return render(request, 'update_profile.html', context)

def load_district(request):
    town = request.GET.get('district_id')
    continent = District.objects.filter(state=town).all()
    context = {'continent': continent}
    return render(request, 'district.html', context)

def Opd_attendance1(request,):
    user = request.user
    Opd_attendance1 = Opd_attendance.objects.filter(user=request.user)
    form1 = Opd_attendanceForm()
    if request.method == 'POST':
        form1 = Opd_attendanceForm(request.POST, request.FILES)
        # no_of_cases  = form1.cleaned_data.get('no_of_cases')
        # no_of_opd_cases = form1.cleaned_data.get('no_of_opd_cases')
        # no_of_new_adminission = form1.cleaned_data.get('no_of_new_adminission')

        if form1.is_valid():
            auth1 = form1.save(commit=False)
            auth1.user = user
            auth1.pre_opd_att = auth1.no_of_cases / auth1.no_of_opd_cases * 100
            auth1.pre_new_admi = auth1.no_of_cases / auth1.no_of_new_adminission * 100
            auth1.pre_total = auth1.no_of_cases / (auth1.no_of_new_adminission + auth1.no_of_opd_cases) * 100
            # auth1.Opd_attendance = opd_attendance
            auth1.save()
            return redirect("Opd_attendance1")
        else:
            context = {'form1': form1, }
            return render(request, 'opd_attendance.html', context)

    context = {'form1': form1, 'Opd_attendance1': Opd_attendance1, }
    return render(request, 'opd_attendance.html', context)

def Opd_attendance2(request,):
    user = request.user
    Opd_attendance2 = Opd_attendance.objects.all()

    context = {'Opd_attendance2': Opd_attendance2, }
    return render(request, 'opd_1.html', context)

def view_facility(request,):
    Facility = Register.objects.all()

    context = {'Facility1': Facility, }
    return render(request, 'facility.html', context)


def load_district(request):
    town = request.GET.get('district_id')
    continent = District.objects.filter(state=town).all()
    context = {'continent': continent}
    return render(request, 'district.html', context)
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def info(request):
    context = {}
    return render(request, 'info.html', context)


@login_required(login_url='login')
def institute(request):
    register = User.objects.all()
    reg = Register.objects.filter(user__in=register,access='User').values_list('user_id')
    testing = User.objects.filter(id__in=reg)
    cars_list = []

    for i in testing:
        facality1 = Register.objects.get(user=i)
        facality2 = facality1.institute_name
        profile_fabry1 = profile_fabry.objects.filter(user=i, ).count()
        # profile_fabry1 = profile_fabry.objects.filter(user=i, complete='Yes').count()
        profile_thalassemia1 = profile_thalassemia.objects.filter(user=i, ).count()
        # profile_thalassemia1 = profile_thalassemia.objects.filter(user=i, complete='Yes').count()
        profile_glycogen1 = profile_glycogen.objects.filter(user=i, ).count()
        # profile_glycogen1 = profile_glycogen.objects.filter(user=i, complete='Yes').count()
        profile_bleeding1 = profile_bleeding.objects.filter(user=i, ).count()
        # profile_bleeding1 = profile_bleeding.objects.filter(user=i, complete='Yes').count()
        profile_metabolism1 = profile_metabolism.objects.filter(user=i,).count()
        # profile_metabolism1 = profile_metabolism.objects.filter(user=i, complete='Yes').count()
        profile_pompe1 = profile_pompe.objects.filter(user=i, ).count()
        # profile_pompe1 = profile_pompe.objects.filter(user=i, complete='Yes').count()
        profile_storage1 = profile_storage.objects.filter(user=i, ).count()
        # profile_storage1 = profile_storage.objects.filter(user=i, complete='Yes').count()
        profile_skeletal1 = profile_skeletal.objects.filter(user=i, ).count()
        # profile_skeletal1 = profile_skeletal.objects.filter(user=i, complete='Yes').count()
        profile_nmd1 = profile_nmd.objects.filter(user=i,).count()
        # profile_nmd1 = profile_nmd.objects.filter(user=i, complete='Yes').count()
        profile_mucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.filter(user=i, ).count()
        # profile_mucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.filter(user=i, complete='Yes').count()
        profile_smallmolecule1 = profile_smallmolecule.objects.filter(user=i, ).count()
        # profile_smallmolecule1 = profile_smallmolecule.objects.filter(user=i, complete='Yes').count()
        profile_pid1 = profile_pid.objects.filter(user=i, ).count()
        # profile_pid1 = profile_pid.objects.filter(user=i, complete='Yes').count()
        profile_total = profile_fabry1 + profile_thalassemia1 + profile_glycogen1 + profile_bleeding1 + profile_metabolism1 + profile_pompe1 + profile_storage1 + profile_skeletal1 + profile_nmd1 + \
                        profile_mucopolysaccharidosis1 + profile_smallmolecule1 + profile_pid1

        cars = OrderedDict()
        cars['institute_name'] = facality2
        cars['profile_fabry'] = profile_fabry1
        cars['profile_thalassemia'] = profile_thalassemia1
        cars['profile_glycogen'] = profile_glycogen1
        cars['profile_bleeding'] = profile_bleeding1
        cars['profile_metabolism'] = profile_metabolism1
        cars['profile_pompe'] = profile_pompe1
        cars['profile_storage'] = profile_storage1
        cars['profile_skeletal'] = profile_skeletal1
        cars['profile_nmd'] = profile_nmd1
        cars['profile_mucopolysaccharidosis'] = profile_mucopolysaccharidosis1
        cars['profile_smallmolecule'] = profile_smallmolecule1
        cars['profile_pid'] = profile_pid1
        cars['profile_total'] = profile_total

        profilefabry1 = profile_fabry.objects.filter( complete='Yes').count()
        profilefabry2 = profile_fabry.objects.filter( complete='No').count()
        profilefabry3 = profile_fabry.objects.filter( quality_result='Pass').count()
        profilefabry4 = profile_fabry.objects.filter( quality_result='Fail').count()
        profilefabry5 = profile_fabry.objects.all().count()

        profilethalassemia1 = profile_thalassemia.objects.filter( complete='Yes').count()
        profilethalassemia2 = profile_thalassemia.objects.filter( complete='No').count()
        profilethalassemia3 = profile_thalassemia.objects.filter( quality_result='Pass').count()
        profilethalassemia4 = profile_thalassemia.objects.filter( quality_result='Fail').count()
        profilethalassemia5 = profile_thalassemia.objects.all().count()

        profileglycogen1 = profile_glycogen.objects.filter( complete='Yes').count()
        profileglycogen2 = profile_glycogen.objects.filter( complete='No').count()
        profileglycogen3 = profile_glycogen.objects.filter( quality_result='Pass').count()
        profileglycogen4 = profile_glycogen.objects.filter( quality_result='Fail').count()
        profileglycogen5 = profile_glycogen.objects.all().count()

        profilebleeding1 = profile_bleeding.objects.filter( complete='Yes').count()
        profilebleeding2 = profile_bleeding.objects.filter( complete='No').count()
        profilebleeding3 = profile_bleeding.objects.filter( quality_result='Pass').count()
        profilebleeding4 = profile_bleeding.objects.filter( quality_result='Fail').count()
        profilebleeding5 = profile_bleeding.objects.all().count()

        profilemetabolism1 = profile_metabolism.objects.filter( complete='Yes').count()
        profilemetabolism2 = profile_metabolism.objects.filter( complete='No').count()
        profilemetabolism3 = profile_metabolism.objects.filter( quality_result='Pass').count()
        profilemetabolism4 = profile_metabolism.objects.filter( quality_result='Fail').count()
        profilemetabolism5 = profile_metabolism.objects.all().count()

        profilepompe1 = profile_pompe.objects.filter( complete='Yes').count()
        profilepompe2 = profile_pompe.objects.filter( complete='No').count()
        profilepompe3 = profile_pompe.objects.filter( quality_result='Pass').count()
        profilepompe4 = profile_pompe.objects.filter( quality_result='Fail').count()
        profilepompe5 = profile_pompe.objects.all().count()

        profilestorage1 = profile_storage.objects.filter( complete='Yes').count()
        profilestorage2 = profile_storage.objects.filter( complete='No').count()
        profilestorage3 = profile_storage.objects.filter( quality_result='Pass').count()
        profilestorage4 = profile_storage.objects.filter(quality_result='Fail').count()
        profilestorage5 = profile_storage.objects.all().count()

        profileskeletal1 = profile_skeletal.objects.filter( complete='Yes').count()
        profileskeletal2 = profile_skeletal.objects.filter( complete='No').count()
        profileskeletal3 = profile_skeletal.objects.filter( quality_result='Pass').count()
        profileskeletal4 = profile_skeletal.objects.filter(quality_result='Fail').count()
        profileskeletal5 = profile_skeletal.objects.all().count()

        profilenmd1 = profile_nmd.objects.filter( complete='Yes').count()
        profilenmd2 = profile_nmd.objects.filter( complete='No').count()
        profilenmd3 = profile_nmd.objects.filter(quality_result='Pass').count()
        profilenmd4 = profile_nmd.objects.filter(quality_result='Fail').count()
        profilenmd5 = profile_nmd.objects.all().count()

        profilemucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.filter( complete='Yes').count()
        profilemucopolysaccharidosis2 = profile_mucopolysaccharidosis.objects.filter( complete='No').count()
        profilemucopolysaccharidosis3 = profile_mucopolysaccharidosis.objects.filter(quality_result='Pass').count()
        profilemucopolysaccharidosis4 = profile_mucopolysaccharidosis.objects.filter(quality_result='Fail').count()
        profilemucopolysaccharidosis5 = profile_mucopolysaccharidosis.objects.all().count()

        profilesmallmolecule1 = profile_smallmolecule.objects.filter( complete='Yes').count()
        profilesmallmolecule2 = profile_smallmolecule.objects.filter( complete='No').count()
        profilesmallmolecule3 = profile_smallmolecule.objects.filter(quality_result='Pass').count()
        profilesmallmolecule4 = profile_smallmolecule.objects.filter(quality_result='Fail').count()
        profilesmallmolecule5 = profile_smallmolecule.objects.all().count()

        profilepid1 = profile_pid.objects.filter( complete='Yes').count()
        profilepid2 = profile_pid.objects.filter( complete='No').count()
        profilepid3 = profile_pid.objects.filter(quality_result='Pass').count()
        profilepid4 = profile_pid.objects.filter(quality_result='Fail').count()
        profilepid5 = profile_pid.objects.all().count()

        totalyes = profilefabry1 + profilethalassemia1 + profileglycogen1 + profilebleeding1 + profilemetabolism1 + profilepompe1 + profilestorage1 + profileskeletal1 + profilenmd1 + profilemucopolysaccharidosis1 + profilesmallmolecule1 + profilepid1

        totalno = profilefabry2 + profilethalassemia2 + profileglycogen2 + profilebleeding2 + profilemetabolism2 + profilepompe2 + profilestorage2 + profileskeletal2 + profilenmd2 + profilemucopolysaccharidosis2 + profilesmallmolecule2 + profilepid2

        total = profilefabry5 + profilethalassemia5 + profileglycogen5 + profilebleeding5 + profilemetabolism5 + profilepompe5 + profilestorage5 + profileskeletal5 + profilenmd5 + profilemucopolysaccharidosis5 + profilesmallmolecule5 + profilepid5

        cars_list.append(cars)


        # profile_fabry2 = profile_fabry.objects.annotate(month1=TruncMonth('fb_date_created')).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_fabry2 = profile_fabry.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id',  filter=Q(quality_result='Fail')), ).values('register__institute_name','count_yes',
                                                                                 'count_no','count_qapass', 'count_qafail','count_total',)

        # profile_thalassemia2 = profile_thalassemia.objects.annotate(month1=TruncMonth('date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_thalassemia2 = profile_thalassemia.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id',  filter=Q(quality_result='Fail')), ).values('register__institute_name','count_total', 'count_yes',
                                                                                 'count_no','count_qapass', 'count_qafail',)
        # profile_glycogen2 = profile_glycogen.objects.annotate(month1=TruncMonth('gl_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_glycogen2 = profile_glycogen.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id',  filter=Q(quality_result='Fail')), ).values('register__institute_name','count_total', 'count_yes',
                                                                                 'count_no','count_qapass', 'count_qafail',)
        # profile_bleeding2 = profile_bleeding.objects.annotate(month1=TruncMonth('bd_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_bleeding2 = profile_bleeding.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail', )
        # profile_metabolism2 = profile_metabolism.objects.annotate(month1=TruncMonth('mt_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_metabolism2 = profile_metabolism.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',
                                                                                )
        # profile_pompe2 = profile_pompe.objects.annotate(month1=TruncMonth('pmp_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_pompe2 = profile_pompe.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)
        # profile_storage2 = profile_storage.objects.annotate(month1=TruncMonth('sd_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_storage2 = profile_storage.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)
        # profile_skeletal2 = profile_skeletal.objects.annotate(month1=TruncMonth('sk_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_skeletal2 = profile_skeletal.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)
        # profile_nmd2 = profile_nmd.objects.annotate(month1=TruncMonth('nmd_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_nmd2 = profile_nmd.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)
        # profile_mucopolysaccharidosis2 = profile_mucopolysaccharidosis.objects.annotate(month1=TruncMonth('muco_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_mucopolysaccharidosis2 = profile_mucopolysaccharidosis.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)

        # profile_smallmolecule2 = profile_smallmolecule.objects.annotate(month1=TruncMonth('small_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_smallmolecule2 = profile_smallmolecule.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)

        # profile_pid2 = profile_pid.objects.annotate(month1=TruncMonth('pid_date_created', )).values('month1').annotate(
        #     count=Count('id',filter = Q(complete='No') )).values('month1', 'count', 'register__institute_name').order_by('month1')
        profile_pid2 = profile_pid.objects.values('register__institute_name').annotate(
            count_yes=Count('id', filter=Q(complete='Yes')), count_no=Count('id', filter=Q(complete='No')),
            count_total=Count('id'),
            count_qapass=Count('id', filter=Q(quality_result='Pass')),
            count_qafail=Count('id', filter=Q(quality_result='Fail')), ).values('register__institute_name', 'count_total', 'count_yes',
                                                                                'count_no', 'count_qapass',
                                                                                'count_qafail',)

        profile_fabry3 = profile_fabry.objects.annotate(month1=TruncMonth('fb_date_created')).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')

        profile_thalassemia3 = profile_thalassemia.objects.annotate(month1=TruncMonth('date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_glycogen3 = profile_glycogen.objects.annotate(month1=TruncMonth('gl_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_bleeding3 = profile_bleeding.objects.annotate(month1=TruncMonth('bd_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_metabolism3 = profile_metabolism.objects.annotate(month1=TruncMonth('mt_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_pompe3 = profile_pompe.objects.annotate(month1=TruncMonth('pmp_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_storage3 = profile_storage.objects.annotate(month1=TruncMonth('sd_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_skeletal3 = profile_skeletal.objects.annotate(month1=TruncMonth('sk_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_nmd3 = profile_nmd.objects.annotate(month1=TruncMonth('nmd_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_mucopolysaccharidosis3 = profile_mucopolysaccharidosis.objects.annotate(month1=TruncMonth('muco_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_smallmolecule3 = profile_smallmolecule.objects.annotate(month1=TruncMonth('small_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        profile_pid3 = profile_pid.objects.annotate(month1=TruncMonth('pid_date_created', )).values('month1').annotate(
            count=Count('id', )).values('month1', 'count', ).order_by('month1')
        print(profile_fabry2)
        time1 = date.today()
        print(time1.year, time1.month)
        date1 = date(2022, 5, 1)
        # d2 = date.strftime(date1, "%Y/%m/%d")
        # d3 = date1-time1
        # print(d3.months)

    # cars_list1 = []
    # for i in testing:
    #     facality11 = Register.objects.get(user=i)
    #     facality22 = facality11.institute_name
    #     profile_fabry11 = profile_fabry.objects.filter(user=i,).exclude(quality_result=None).count()
    #     profile_thalassemia11 = profile_thalassemia.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_glycogen11 = profile_glycogen.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_bleeding11 = profile_bleeding.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_metabolism11 = profile_metabolism.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_pompe11 = profile_pompe.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_storage11 = profile_storage.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_skeletal11 = profile_skeletal.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_nmd11 = profile_nmd.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_mucopolysaccharidosis11 = profile_mucopolysaccharidosis.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_smallmolecule11 = profile_smallmolecule.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_pid11 = profile_pid.objects.filter(user=i).exclude(quality_result=None).count()
    #     profile_total11 = profile_fabry11 + profile_thalassemia11 + profile_glycogen11 + profile_bleeding11 + profile_metabolism11 + profile_pompe11 + profile_storage11 + profile_skeletal11 + profile_nmd11 + \
    #                     profile_mucopolysaccharidosis11 + profile_smallmolecule11 + profile_pid11
    #
    #     cars1 = OrderedDict()
    #     cars1['institute_name'] = facality22
    #     cars1['profile_fabry'] = profile_fabry11
    #     cars1['profile_thalassemia'] = profile_thalassemia11
    #     cars1['profile_glycogen'] = profile_glycogen11
    #     cars1['profile_bleeding'] = profile_bleeding11
    #     cars1['profile_metabolism'] = profile_metabolism11
    #     cars1['profile_pompe'] = profile_pompe11
    #     cars1['profile_storage'] = profile_storage11
    #     cars1['profile_skeletal'] = profile_skeletal11
    #     cars1['profile_nmd'] = profile_nmd11
    #     cars1['profile_mucopolysaccharidosis'] = profile_mucopolysaccharidosis11
    #     cars1['profile_smallmolecule'] = profile_smallmolecule11
    #     cars1['profile_pid'] = profile_pid11
    #     cars1['profile_total'] = profile_total11
    #
    #     cars_list1.append(cars1)
    context = {'cars_list': cars_list, 'profilefabry1': profilefabry1, 'profilefabry2': profilefabry2, 'profilefabry3': profilefabry3,
                'profilefabry4': profilefabry4, 'profilefabry5': profilefabry5, 'profilethalassemia1': profilethalassemia1,
               'profilethalassemia2': profilethalassemia2, 'profilethalassemia3': profilethalassemia3, 'profilethalassemia4': profilethalassemia4,
               'profilethalassemia5': profilethalassemia5,
               'profileglycogen1': profileglycogen1,'profileglycogen2': profileglycogen2, 'profileglycogen3': profileglycogen3, 'profileglycogen4': profileglycogen4,
               'profileglycogen5': profileglycogen5, 'profilebleeding1': profilebleeding1, 'profilebleeding2': profilebleeding2, 'profilebleeding3': profilebleeding3,
               'profilebleeding4': profilebleeding4, 'profilebleeding5': profilebleeding5, 'profilemetabolism1': profilemetabolism1, 'profilemetabolism2': profilemetabolism2,
               'profilemetabolism3': profilemetabolism3, 'profilemetabolism4': profilemetabolism4, 'profilemetabolism5': profilemetabolism5,'profilepompe1': profilepompe1,
               'profilepompe2': profilepompe2, 'profilepompe3': profilepompe3, 'profilepompe4': profilepompe4, 'profilepompe5': profilepompe5, 'profilestorage1': profilestorage1,
                'profilestorage2': profilestorage2, 'profilestorage3': profilestorage3, 'profilestorage4': profilestorage4, 'profilestorage5': profilestorage5,'profileskeletal1': profileskeletal1,
               'profileskeletal2': profileskeletal2,'profileskeletal3': profileskeletal3, 'profileskeletal4': profileskeletal4, 'profileskeletal5': profileskeletal5,
               'profilenmd1': profilenmd1, 'profilenmd2': profilenmd2, 'profilenmd3': profilenmd3, 'profilenmd4': profilenmd4, 'profilenmd5': profilenmd5,'profilemucopolysaccharidosis1': profilemucopolysaccharidosis1,
               'profilemucopolysaccharidosis2': profilemucopolysaccharidosis2,'profilemucopolysaccharidosis3': profilemucopolysaccharidosis3,'profilemucopolysaccharidosis4': profilemucopolysaccharidosis4,
               'profilemucopolysaccharidosis5': profilemucopolysaccharidosis5, 'profilesmallmolecule1': profilesmallmolecule1,'profilesmallmolecule2': profilesmallmolecule2,'profilesmallmolecule3': profilesmallmolecule3,
               'profilesmallmolecule4': profilesmallmolecule4,'profilesmallmolecule5': profilesmallmolecule5, 'profilepid1': profilepid1, 'profilepid2': profilepid2, 'profilepid3': profilepid3,
               'profilepid4': profilepid4,'profilepid5': profilepid5,
               'total': total,'totalyes': totalyes,'totalno': totalno,

               'profile_fabry2': profile_fabry2,
               'profile_glycogen2': profile_glycogen2,
               'profile_thalassemia2': profile_thalassemia2, 'profile_bleeding2': profile_bleeding2, 'profile_metabolism2': profile_metabolism2,
               'profile_pompe2': profile_pompe2, 'profile_storage2': profile_storage2, 'profile_skeletal2': profile_skeletal2,
               'profile_nmd2': profile_nmd2, 'profile_mucopolysaccharidosis2': profile_mucopolysaccharidosis2, 'profile_smallmolecule2': profile_smallmolecule2,
               'profile_pid2': profile_pid2,
               'profile_fabry3': profile_fabry3, 'profile_thalassemia3': profile_thalassemia3, 'profile_glycogen3': profile_glycogen3,
               'profile_bleeding3': profile_bleeding3, 'profile_metabolism3': profile_metabolism3, 'profile_pompe3': profile_pompe3,
               'profile_storage3': profile_storage3, 'profile_skeletal3': profile_skeletal3, 'profile_nmd3': profile_nmd3,
               'profile_mucopolysaccharidosis3': profile_mucopolysaccharidosis3, 'profile_smallmolecule3': profile_smallmolecule3,
               'profile_pid3': profile_pid3

               }
    return render(request, "institute.html", context)

@login_required(login_url='login')
def quality_control(request):
    register = User.objects.all()
    reg = Register.objects.filter(user__in=register,access='User').values_list('user_id')
    testing = User.objects.filter(id__in=reg)
    cars_list = []
    cars_list1 = []
    for i in testing:
        facality1 = Register.objects.get(user=i)
        facality2 = facality1.institute_name
        profile_fabry1 = profile_fabry.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_thalassemia1 = profile_thalassemia.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_glycogen1 = profile_glycogen.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_bleeding1 = profile_bleeding.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_metabolism1 = profile_metabolism.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_pompe1 = profile_pompe.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_storage1 = profile_storage.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_skeletal1 = profile_skeletal.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_nmd1 = profile_nmd.objects.filter(user=i).filter(user=i,quality_result='Pass').count()
        profile_mucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.filter(user=i,quality_result='Pass').count()
        profile_smallmolecule1 = profile_smallmolecule.objects.filter(user=i,quality_result='Pass').count()
        profile_pid1 = profile_pid.objects.filter(user=i,quality_result='Pass').count()
        profile_total = profile_fabry1 + profile_thalassemia1 + profile_glycogen1 + profile_bleeding1 + profile_metabolism1 + profile_pompe1 + profile_storage1 + profile_skeletal1 + profile_nmd1 + \
                        profile_mucopolysaccharidosis1 + profile_smallmolecule1 + profile_pid1

        cars = OrderedDict()
        cars['institute_name'] = facality2
        cars['profile_fabry'] = profile_fabry1
        cars['profile_thalassemia'] = profile_thalassemia1
        cars['profile_glycogen'] = profile_glycogen1
        cars['profile_bleeding'] = profile_bleeding1
        cars['profile_metabolism'] = profile_metabolism1
        cars['profile_pompe'] = profile_pompe1
        cars['profile_storage'] = profile_storage1
        cars['profile_skeletal'] = profile_skeletal1
        cars['profile_nmd'] = profile_nmd1
        cars['profile_mucopolysaccharidosis'] = profile_mucopolysaccharidosis1
        cars['profile_smallmolecule'] = profile_smallmolecule1
        cars['profile_pid'] = profile_pid1
        cars['profile_total'] = profile_total

        profile_fabry1 = profile_fabry.objects.exclude(quality_result=None).count()
        profile_thalassemia1 = profile_thalassemia.objects.exclude(quality_result=None).count()
        profile_glycogen1 = profile_glycogen.objects.exclude(quality_result=None).count()
        profile_bleeding1 = profile_bleeding.objects.exclude(quality_result=None).count()
        profile_metabolism1 = profile_metabolism.objects.exclude(quality_result=None).count()
        profile_pompe1 = profile_pompe.objects.exclude(quality_result=None).count()
        profile_storage1 = profile_storage.objects.exclude(quality_result=None).count()
        profile_skeletal1 = profile_skeletal.objects.exclude(quality_result=None).count()
        profile_nmd1 = profile_nmd.objects.exclude(quality_result=None).count()
        profile_mucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.exclude(quality_result=None).count()
        profile_smallmolecule1 = profile_smallmolecule.objects.exclude(quality_result=None).count()
        profile_pid1 = profile_pid.objects.exclude(quality_result=None).count()
        total = profile_fabry1 + profile_thalassemia1 + profile_glycogen1 + profile_bleeding1 + profile_metabolism1 + profile_pompe1 + profile_storage1 + profile_skeletal1 + profile_nmd1 + profile_mucopolysaccharidosis1 + profile_smallmolecule1 + profile_pid1

        cars_list.append(cars)

    for i in testing:
        facality11 = Register.objects.get(user=i)
        facality22 = facality11.institute_name
        profile_fabry11 = profile_fabry.objects.filter(user=i,quality_result='Fail').count()
        profile_thalassemia11 = profile_thalassemia.objects.filter(user=i,quality_result='Fail').count()
        profile_glycogen11 = profile_glycogen.objects.filter(user=i,quality_result='Fail').count()
        profile_bleeding11 = profile_bleeding.objects.filter(user=i,quality_result='Fail').count()
        profile_metabolism11 = profile_metabolism.objects.filter(user=i,quality_result='Fail').count()
        profile_pompe11 = profile_pompe.objects.filter(user=i,quality_result='Fail').count()
        profile_storage11 = profile_storage.objects.filter(user=i,quality_result='Fail').count()
        profile_skeletal11 = profile_skeletal.objects.filter(user=i,quality_result='Fail').count()
        profile_nmd11 = profile_nmd.objects.filter(user=i,quality_result='Fail').count()
        profile_mucopolysaccharidosis11 = profile_mucopolysaccharidosis.objects.filter(user=i,quality_result='Fail').count()
        profile_smallmolecule11 = profile_smallmolecule.objects.filter(user=i,quality_result='Fail').count()
        profile_pid11 = profile_pid.objects.filter(user=i,quality_result='Fail').count()
        profile_total11 = profile_fabry11 + profile_thalassemia11 + profile_glycogen11 + profile_bleeding11 + profile_metabolism11 + profile_pompe11 + profile_storage11 + profile_skeletal11 + profile_nmd11 + \
                        profile_mucopolysaccharidosis11 + profile_smallmolecule11 + profile_pid11

        cars = OrderedDict()
        cars['institute_name'] = facality2
        cars['profile_fabry'] = profile_fabry11
        cars['profile_thalassemia'] = profile_thalassemia11
        cars['profile_glycogen'] = profile_glycogen11
        cars['profile_bleeding'] = profile_bleeding11
        cars['profile_metabolism'] = profile_metabolism11
        cars['profile_pompe'] = profile_pompe11
        cars['profile_storage'] = profile_storage11
        cars['profile_skeletal'] = profile_skeletal11
        cars['profile_nmd'] = profile_nmd11
        cars['profile_mucopolysaccharidosis'] = profile_mucopolysaccharidosis11
        cars['profile_smallmolecule'] = profile_smallmolecule11
        cars['profile_pid'] = profile_pid11
        cars['profile_total'] = profile_total11


        cars_list1.append(cars)

    context = {'cars_list': cars_list,'cars_list1': cars_list1, 'profile_fabry1': profile_fabry1, 'profile_thalassemia1': profile_thalassemia1,
               'profile_glycogen1': profile_glycogen1, 'profile_bleeding1': profile_bleeding1, 'profile_metabolism1': profile_metabolism1,
               'profile_mucopolysaccharidosis1': profile_mucopolysaccharidosis1, 'total': total,
               'profile_smallmolecule1': profile_smallmolecule1, 'profile_pid1': profile_pid1,
               'profile_pompe1': profile_pompe1, 'profile_storage1': profile_storage1, 'profile_skeletal1': profile_skeletal1, 'profile_nmd1': profile_nmd1,

               }
    return render(request, "quality_control.html", context)


def month_wise(request):
    profile_fabry3 = profile_fabry.objects.annotate(month1=TruncMonth('fb_date_created')).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')

    profile_thalassemia3 = profile_thalassemia.objects.annotate(month1=TruncMonth('date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_glycogen3 = profile_glycogen.objects.annotate(month1=TruncMonth('gl_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_bleeding3 = profile_bleeding.objects.annotate(month1=TruncMonth('bd_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_metabolism3 = profile_metabolism.objects.annotate(month1=TruncMonth('mt_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_pompe3 = profile_pompe.objects.annotate(month1=TruncMonth('pmp_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_storage3 = profile_storage.objects.annotate(month1=TruncMonth('sd_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_skeletal3 = profile_skeletal.objects.annotate(month1=TruncMonth('sk_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_nmd3 = profile_nmd.objects.annotate(month1=TruncMonth('nmd_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_mucopolysaccharidosis3 = profile_mucopolysaccharidosis.objects.annotate(month1=TruncMonth('muco_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_smallmolecule3 = profile_smallmolecule.objects.annotate(month1=TruncMonth('small_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    profile_pid3 = profile_pid.objects.annotate(month1=TruncMonth('pid_date_created', )).values('register__institute_name','month1').annotate(
        count=Count('id', )).values('register__institute_name','month1', 'count', ).order_by('month1')
    context = {'profile_fabry3': profile_fabry3, 'profile_thalassemia3': profile_thalassemia3, 'profile_glycogen3': profile_glycogen3,
               'profile_bleeding3': profile_bleeding3, 'profile_metabolism3': profile_metabolism3, 'profile_pompe3': profile_pompe3,
               'profile_storage3': profile_storage3, 'profile_skeletal3': profile_skeletal3, 'profile_nmd3': profile_nmd3,
               'profile_mucopolysaccharidosis3': profile_mucopolysaccharidosis3, 'profile_smallmolecule3': profile_smallmolecule3,
               'profile_pid3': profile_pid3

               }
    return render(request, "month_wise.html", context)


@login_required(login_url='login')
def export_thalassemia_csv(request):
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

    users = profile_thalassemia.objects.all().prefetch_related('patient_thalassemia').values_list('register_id__institute_name', 'uniqueId', 'th_icmr_unique_no', 'th_final_diagnosis', 'th_date_record',
                                                                                                  'date_clinical_examination',
                                                                                                  'th_date_of_birth', 'th_patient_name', 'th_father_name', 'th_mother_name', 'th_patient_adhaar_no',
                                                                                                  'th_paitent_id', 'th_patient_id_no', 'th_father_adhaar_no', 'th_father_id', 'th_father_id_no', 'th_permanent_addr',
                                                                                                  'th_state__name', 'th_district__name', 'th_city_name', 'th_country_name', 'th_land_line_no', 'th_mother_mobile_no',
                                                                                                  'th_father_mobile_no', 'th_email', 'th_religion', 'th_religion_other_specify', 'th_caste', 'th_caste_other_specify',
                                                                                                  'th_gender', 'th_referred_status', 'th_referred_by', 'th_referred_by_desc', 'th_consent_given', 'th_consent_upload',
                                                                                                  'th_assent_given', 'th_assent_upload', 'th_hospital_name', 'th_hospital_reg_no', 'th_nationality',
                                                                                                  'patient_thalassemia__th_patient_edu_status', 'patient_thalassemia__th_patient_occupation',
                                                                                                  'patient_thalassemia__th_father_edu_status', 'patient_thalassemia__th_father_occupation',
                                                                                                  'patient_thalassemia__th_mother_edu_status', 'patient_thalassemia__th_mother_occupation',
                                                                                                  'patient_thalassemia__th_monthly_income_status', 'patient_thalassemia__th_tribal',
                                                                                                  'patient_thalassemia__th_non_tribal_caste', 'patient_thalassemia__th_diagnosis_type',
                                                                                                  'patient_thalassemia__th_diagonosis_other_specify', 'patient_thalassemia__th_presentation_age',
                                                                                                  'patient_thalassemia__th_diagnosis_age', 'patient_thalassemia__th_pres_feature', 'patient_thalassemia__th_pres_pallor',
                                                                                                  'patient_thalassemia__th_pres_yellowness', 'patient_thalassemia__th_pres_rec_fever',
                                                                                                  'patient_thalassemia__th_pres_dist_abd', 'patient_thalassemia__th_pres_lethargy', 'patient_thalassemia__th_pres_fatigue',
                                                                                                  'patient_thalassemia__th_curr_child_age', 'patient_thalassemia__th_consanguinity', 'patient_thalassemia__th_sibling_aff',
                                                                                                  'patient_thalassemia__th_other_family_mem', 'patient_thalassemia__th_other_family_mem_details',
                                                                                                  'patient_thalassemia__th_pedigree_upload', 'patient_thalassemia__th_f_fatigue', 'patient_thalassemia__th_f_dyspnoea',
                                                                                                  'patient_thalassemia__th_f_rec_fever', 'patient_thalassemia__th_f_abdominal_pain', 'patient_thalassemia__th_f_chest_pain',
                                                                                                  'patient_thalassemia__th_f_bone_joint_pain', 'patient_thalassemia__th_f_any_other',
                                                                                                  'patient_thalassemia__th_f_any_other_specify', 'patient_thalassemia__th_f_past_hist',
                                                                                                  'patient_thalassemia__th_crisis_num', 'patient_thalassemia__th_crisis_num_last_12',
                                                                                                  'patient_thalassemia__th_acute_chest_syndrome', 'patient_thalassemia__th_crisis_hyperhemolyitc',
                                                                                                  'patient_thalassemia__th_crisis_pain_pr_yr_before_hydoxyurea',
                                                                                                  'patient_thalassemia__th_crisis_pain_pr_yr_before_hydoxyurea',
                                                                                                  'patient_thalassemia__th_crisis_pain_pr_yr_after_hydoxyurea', 'patient_thalassemia__th_other_illness',
                                                                                                  'patient_thalassemia__th_other_illness_name', 'patient_thalassemia__th_other_illness_age',
                                                                                                  'patient_thalassemia__th_other_illness_dur', 'patient_thalassemia__th_height', 'patient_thalassemia__th_height_z_score',
                                                                                                  'patient_thalassemia__th_weight', 'patient_thalassemia__th_weight_z_score', 'patient_thalassemia__th_hemolytic_facies',
                                                                                                  'patient_thalassemia__th_pallor', 'patient_thalassemia__th_jaundice', 'patient_thalassemia__th_edema',
                                                                                                  'patient_thalassemia__th_leg_ulcers', 'patient_thalassemia__th_hepatomegaly', 'patient_thalassemia__th_splenomegaly',
                                                                                                  'patient_thalassemia__th_any_systematic_anom', 'patient_thalassemia__th_any_sys_ab_specify',
                                                                                                  'patient_thalassemia__th_neurological_abnor', 'patient_thalassemia__th_neurological_abnor_option',
                                                                                                  'patient_thalassemia__th_neurological_abnor_option_other', 'patient_thalassemia__th_renal_involvement',
                                                                                                  'patient_thalassemia__th_renal_involvement_opts', 'patient_thalassemia__th_renal_involvement_opts_other',
                                                                                                  'patient_thalassemia__th_feet_swelling', 'patient_thalassemia__th_clin_leg_ulcers',
                                                                                                  'patient_thalassemia__th_clin_gallstones', 'patient_thalassemia__th_iron_overload_yes_no',
                                                                                                  'patient_thalassemia__th_iron_overload_cardiac', 'patient_thalassemia__th_iron_overload_Endocrine',
                                                                                                  'patient_thalassemia__th_iron_overload_Growth', 'patient_thalassemia__th_hist_infection',
                                                                                                  'patient_thalassemia__th_hist_infection_opt', 'patient_thalassemia__th_hist_infection_opt_other_specify',
                                                                                                  'patient_thalassemia__th_haem_wbc', 'patient_thalassemia__th_haem_hb', 'patient_thalassemia__th_haem_mcv',
                                                                                                  'patient_thalassemia__th_haem_mch', 'patient_thalassemia__th_haem_mchc', 'patient_thalassemia__th_haem_rbc_count',
                                                                                                  'patient_thalassemia__th_haem_rdw_per', 'patient_thalassemia__th_haem_plts', 'patient_thalassemia__th_haem_plts',
                                                                                                  'patient_thalassemia__th_haem_retic_count', 'patient_thalassemia__th_haem_hba', 'patient_thalassemia__th_haem_hbf',
                                                                                                  'patient_thalassemia__th_haem_hba2', 'patient_thalassemia__th_haem_hbf', 'patient_thalassemia__th_red_cell_morphology',
                                                                                                  'patient_thalassemia__th_red_cell_morphology_other_specify', 'patient_thalassemia__th_haem_unstable_haem',
                                                                                                  'patient_thalassemia__th_haem_var_hb', 'patient_thalassemia__th_haem_var_hb_hbs',
                                                                                                  'patient_thalassemia__th_haem_var_hb_hbe', 'patient_thalassemia__th_haem_var_hb_hbd',
                                                                                                  'patient_thalassemia__th_haem_var_hb_other_per', 'patient_thalassemia__th_haem_var_hb_retention_time',
                                                                                                  'patient_thalassemia__th_mol_alpha_thal', 'patient_thalassemia__th_mol_alpha_thal_opt',
                                                                                                  'patient_thalassemia__th_haem_hbh_incl', 'patient_thalassemia__th_mol_hbh_thal_opt',
                                                                                                  'patient_thalassemia__th_mol_alpha_thal_opt_other', 'patient_thalassemia__th_mol_beta_thal',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_1', 'patient_thalassemia__th_mol_beta_thal_opt_2',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_3', 'patient_thalassemia__th_mol_beta_thal_opt_4',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_5', 'patient_thalassemia__th_mol_beta_thal_opt_6',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_7', 'patient_thalassemia__th_mol_beta_thal_opt_8',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_other_spec', 'patient_thalassemia__th_mol_interpretaion',
                                                                                                  'patient_thalassemia__th_HPFH_test', 'patient_thalassemia__th_HPFH_test_result',
                                                                                                  'patient_thalassemia__th_mol_alpha_beta_test', 'patient_thalassemia__th_mol_alpha_beta_test_result',
                                                                                                  'patient_thalassemia__th_curr_invest_date', 'patient_thalassemia__th_curr_pretasnsfusion',
                                                                                                  'patient_thalassemia__th_curr_post_transfusion', 'patient_thalassemia__th_curr_hiv', 'patient_thalassemia__th_curr_hbsag',
                                                                                                  'patient_thalassemia__th_curr_hcv', 'patient_thalassemia__th_treat_recieved',
                                                                                                  'patient_thalassemia__th_bio_serum_ferritin', 'patient_thalassemia__th_bio_serum_dehyd',
                                                                                                  'patient_thalassemia__th_bio_vitamin_b12', 'patient_thalassemia__th_bio_folate_levels',
                                                                                                  'patient_thalassemia__th_bio_ser_bilirubin', 'patient_thalassemia__th_bio_alan_amino',
                                                                                                  'patient_thalassemia__th_bio_ser_alkline', 'patient_thalassemia__th_bio_ser_calc',
                                                                                                  'patient_thalassemia__th_bio_ser_calc_ionized', 'patient_thalassemia__th_bio_ser_phosp',
                                                                                                  'patient_thalassemia__th_bio_s_creatinine', 'patient_thalassemia__th_bio_t4', 'patient_thalassemia__th_bio_tsh',
                                                                                                  'patient_thalassemia__th_bio_s_cortisol_early', 'patient_thalassemia__th_bio_s_cortisol_stimulates',
                                                                                                  'patient_thalassemia__th_bio_blood_sugar_fast', 'patient_thalassemia__th_bio_blood_sugar_post_meal',
                                                                                                  'patient_thalassemia__th_ecg', 'patient_thalassemia__th_ECHOcardiography', 'patient_thalassemia__th_Any_other',
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
                                                                                                  'patient_thalassemia__th_comp_iron_overload_beta_thalassemia_detail', 'patient_thalassemia__th_comp_iron_overload',
                                                                                                  'patient_thalassemia__th_comp_iron_overload_detail', 'patient_thalassemia__th_impr_mngt',
                                                                                                  'patient_thalassemia__th_filled_by_deo_name', 'patient_thalassemia__th_filled_by_name',
                                                                                                  'patient_thalassemia__th_filled_date', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_thalassemia_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="thalassemia_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'th_final_diagnosis', 'th_date_record', 'date_clinical_examination',
         'th_presentation_age', 'th_diagnosis_age', 'th_hepatomegaly','th_splenomegaly','th_haem_hba','th_haem_hbf','th_haem_hba2', 'th_haem_var_hb','th_haem_var_hb_hbs', 'th_haem_var_hb_hbe', 'th_haem_var_hb_hbd',
         'th_mol_alpha_thal',  'th_mol_beta_thal','th_mol_beta_thal_opt_1', 'th_mol_beta_thal_opt_2', 'th_mol_beta_thal_opt_3', 'th_mol_beta_thal_opt_4', 'th_mol_beta_thal_opt_5',
         'th_mol_beta_thal_opt_6', 'th_mol_beta_thal_opt_7', 'th_mol_beta_thal_opt_8', 'th_mol_beta_thal_other_spec',  'th_bio_serum_ferritin', 'th_transfusion', 'th_transfusion_age',  'th_hydroxyurea', 'th_chelation_status',
          'th_final_diagnosis',  ])

    users = profile_thalassemia.objects.all().prefetch_related('patient_thalassemia').values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'th_icmr_unique_no', 'th_final_diagnosis', 'th_date_record',
                                                                                                  'date_clinical_examination', 'patient_thalassemia__th_presentation_age', 'patient_thalassemia__th_diagnosis_age',
                                                                                                  'patient_thalassemia__th_hepatomegaly', 'patient_thalassemia__th_splenomegaly','patient_thalassemia__th_haem_hba','patient_thalassemia__th_haem_hbf','patient_thalassemia__th_haem_hba2','patient_thalassemia__th_haem_var_hb',

                                                                                                  'patient_thalassemia__th_mol_alpha_thal',  'patient_thalassemia__th_mol_beta_thal',
                                                                                                  'patient_thalassemia__th_haem_var_hb_hbs',
                                                                                                  'patient_thalassemia__th_haem_var_hb_hbe',
                                                                                                  'patient_thalassemia__th_haem_var_hb_hbd',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_1',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_2',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_3',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_4',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_5',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_6',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_7',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_opt_8',
                                                                                                  'patient_thalassemia__th_mol_beta_thal_other_spec',
                                                                                                  'patient_thalassemia__th_bio_serum_ferritin', 'patient_thalassemia__th_transfusion',
                                                                                                  'patient_thalassemia__th_transfusion_age',
                                                                                                  'patient_thalassemia__th_hydroxyurea', 'patient_thalassemia__th_chelation_status',

                                                                                                  'patient_thalassemia__th_final_diagnosis', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_gylcogen_csv(request):
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
def export_gylcogen_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="glycogen_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name','quality_result','quality_reason', 'UniqueId', 'unique_no', 'gl_final_dignosis', 'gl_date_of_record', 'gl_clinical_exam_date', 'gl_date_of_birth',  'gl_anth_wght_pat', 'gl_anth_wght_per', 'gl_anth_wght_sd',

         'gl_anth_height_pat', 'gl_anth_height_per', 'gl_anth_height_sd', 'gl_anth_head_cir_pat', 'gl_anth_head_cir_perc', 'gl_anth_head_cir_sd',
         'gl_anth_head_cir_pat',
         'gl_anth_head_cir_perc', 'gl_anth_head_cir_sd',
         'patient_glycogen__gl_presenting_complaints_years',
         'gl_presenting_complaints_months',
         'gl_presenting_complaints_day',
         'gl_presenting_complaints_intrauterine',

         'gl_presenting_complaints_age_presentation_years',
         'gl_presenting_complaints_age_presentation_months',
         'gl_presenting_complaints_age_presentation_day',
         'gl_presenting_complaints_age_presentation_intrauterine',

         'gl_presenting_complaints_age_diagnosis_years',
         'gl_presenting_complaints_age_diagnosis_months',
         'gl_presenting_complaints_age_diagnosis_day',
         'gl_presenting_complaints_age_diagnosis_intrauterine',
         'gl_fam_hist_status',  'gl_cons_status', 'gl_morn_leth_seiz',
         'gl_dev_delay', 'gl_irritability', 'gl_tremors', 'gl_muscle_weak_floppy', 'gl_exerc_cramping', 'gl_abdominal_dist', 'gl_jaundice', 'gl_over_hunger', 'gl_vomiting', 'gl_diarrhia', 'gl_weight_gain_fail',
         'gl_oral_ulcers', 'gl_perianal_ulcar', 'gl_rec_infections', 'gl_rec_infections_type','gl_rec_infections_type_other', 'gl_bony_deforminty', 'gl_site_bleeding', 'gl_site_bleeding_type', 'gl_polyurea', 'gl_puberty_delay', 'gl_joint_pain',
         'gl_exertion_dyspnoea', 'gl_doll_like_face', 'gl_hepatomegaly',  'gl_splenomegaly',
          'gl_renal_enlargement', 'gl_rachitic_changes', 'gl_hypotonia', 'gl_iq_status',  'gl_cong_heart_fail', 'gl_core_pulomonable', 'gl_hypertension', 'gl_inv_hb', 'gl_inv_wbc',
         'gl_inv_anc', 'gl_inv_wbc', 'gl_inv_abs_neutrophil_count', 'gl_inv_ph', 'gl_inv_hco_3', 'gl_inv_lactate', 'gl_inv_s_cal', 'gl_inv_s_phosphorous', 'gl_inv_sgot', 'gl_inv_ggt', 'gl_inv_tg', 'gl_inv_tc',
         'gl_inv_vldl', 'gl_inv_hdl', 'gl_inv_ldl', 'gl_inv_vit_d',  'gl_inv_s_uric_acid', 'gl_inv_s_cpk', 'gl_inv_s_afp', 'gl_rad_ultrasono_type', 'gl_echocardiography_status',  'gl_enzyme_assay','gl_dna1',
         'gl_mol_diagnosis_desc_gene_seq',  'gl_treat_diet_alone',  'gl_supportive_therapy', 'gl_any_surgery', 'gl_any_surgery_specify', 'gl_any_organ_transplantation',
         'gl_any_organ_transplantation_specify', 'gl_Finaldiagnosis',
	     'gl_Finaldiagnosis_other',
	     'gl_Finaloutcomes',  ])

    users = profile_glycogen.objects.all().prefetch_related('patient_glycogen').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'gl_icmr_unique_no', 'gl_final_dignosis', 'gl_date_of_record',
                                                                                            'gl_clinical_exam_date','gl_date_of_birth',
                                                                                            'patient_glycogen__gl_anth_wght_pat', 'patient_glycogen__gl_anth_wght_per', 'patient_glycogen__gl_anth_wght_sd',
                                                                                            'patient_glycogen__gl_anth_height_pat', 'patient_glycogen__gl_anth_height_per', 'patient_glycogen__gl_anth_height_sd',
                                                                                            'patient_glycogen__gl_anth_head_cir_pat', 'patient_glycogen__gl_anth_head_cir_perc', 'patient_glycogen__gl_anth_head_cir_sd',

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
                                                                                            'patient_glycogen__gl_cons_status',
                                                                                            'patient_glycogen__gl_morn_leth_seiz', 'patient_glycogen__gl_dev_delay', 'patient_glycogen__gl_irritability',
                                                                                            'patient_glycogen__gl_tremors', 'patient_glycogen__gl_muscle_weak_floppy', 'patient_glycogen__gl_exerc_cramping',
                                                                                            'patient_glycogen__gl_abdominal_dist', 'patient_glycogen__gl_jaundice', 'patient_glycogen__gl_over_hunger',
                                                                                            'patient_glycogen__gl_vomiting', 'patient_glycogen__gl_diarrhia', 'patient_glycogen__gl_weight_gain_fail',
                                                                                            'patient_glycogen__gl_oral_ulcers', 'patient_glycogen__gl_perianal_ulcar', 'patient_glycogen__gl_rec_infections',
                                                                                            'patient_glycogen__gl_rec_infections_type','patient_glycogen__gl_rec_infections_type_other', 'patient_glycogen__gl_bony_deforminty', 'patient_glycogen__gl_site_bleeding',
                                                                                            'patient_glycogen__gl_site_bleeding_type', 'patient_glycogen__gl_polyurea', 'patient_glycogen__gl_puberty_delay',
                                                                                            'patient_glycogen__gl_joint_pain', 'patient_glycogen__gl_exertion_dyspnoea', 'patient_glycogen__gl_doll_like_face',
                                                                                            'patient_glycogen__gl_hepatomegaly',  'patient_glycogen__gl_splenomegaly',
                                                                                            'patient_glycogen__gl_renal_enlargement', 'patient_glycogen__gl_rachitic_changes', 'patient_glycogen__gl_hypotonia',
                                                                                            'patient_glycogen__gl_iq_status',  'patient_glycogen__gl_cong_heart_fail',
                                                                                            'patient_glycogen__gl_core_pulomonable', 'patient_glycogen__gl_hypertension', 'patient_glycogen__gl_inv_hb',
                                                                                            'patient_glycogen__gl_inv_wbc', 'patient_glycogen__gl_inv_anc', 'patient_glycogen__gl_inv_wbc',
                                                                                            'patient_glycogen__gl_inv_abs_neutrophil_count', 'patient_glycogen__gl_inv_ph', 'patient_glycogen__gl_inv_hco_3',
                                                                                            'patient_glycogen__gl_inv_lactate', 'patient_glycogen__gl_inv_s_cal', 'patient_glycogen__gl_inv_s_phosphorous',
                                                                                            'patient_glycogen__gl_inv_sgot', 'patient_glycogen__gl_inv_ggt', 'patient_glycogen__gl_inv_tg', 'patient_glycogen__gl_inv_tc',
                                                                                            'patient_glycogen__gl_inv_vldl', 'patient_glycogen__gl_inv_hdl', 'patient_glycogen__gl_inv_ldl',
                                                                                            'patient_glycogen__gl_inv_vit_d',  'patient_glycogen__gl_inv_s_uric_acid',
                                                                                            'patient_glycogen__gl_inv_s_cpk', 'patient_glycogen__gl_inv_s_afp', 'patient_glycogen__gl_rad_ultrasono_type',
                                                                                            'patient_glycogen__gl_echocardiography_status',  'patient_glycogen__gl_enzyme_assay','patient_glycogen__gl_dna1',

                                                                                            'patient_glycogen__gl_mol_diagnosis_desc_gene_seq',
                                                                                            'patient_glycogen__gl_treat_diet_alone',
                                                                                            'patient_glycogen__gl_supportive_therapy', 'patient_glycogen__gl_any_surgery', 'patient_glycogen__gl_any_surgery_specify',
                                                                                            'patient_glycogen__gl_any_organ_transplantation', 'patient_glycogen__gl_any_organ_transplantation_specify',
                                                                                            'patient_glycogen__gl_Finaldiagnosis',
                                                                                            'patient_glycogen__gl_Finaldiagnosis_other',
                                                                                            'patient_glycogen__gl_Finaloutcomes',
                                                                                            )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_fabry_csv(request):
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
         'patient_fabry__fb_any_other', 'patient_fabry__fb_treatment', 'patient_fabry__fb_Finaloutcomes',
         'patient_fabry__fb_filled_by_deo_name',
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
def export_fabry_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fabry_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'patient_fabry__fb_final_diagnosis', 'patient_fabry__fb_date_of_record', 'patient_fabry__fb_clinical_exam_date',
         'fb_anth_wght_pat', 'fb_anth_wght_per', 'fb_anth_wght_sd',
         'fb_anth_height_pat', 'fb_anth_height_per', 'fb_anth_height_sd',
         'fb_anth_head_cir_pat',
         'fb_anth_head_cir_perc', 'fb_anth_head_cir_sd','fb_presenting_complaints_years', 'fb_presenting_complaints_months', 'fb_presenting_complaints_day', 'fb_presenting_complaints_intrauterine', 'fb_presenting_complaints_age_presentation_years',
         'fb_presenting_complaints_age_presentation_months', 'fb_presenting_complaints_age_presentation_day', 'fb_presenting_complaints_age_presentation_intrauterine', 'fb_presenting_complaints_age_diagnosis_years',
         'fb_presenting_complaints_age_diagnosis_months', 'fb_presenting_complaints_age_diagnosis_day', 'fb_presenting_complaints_age_diagnosis_intrauterine', 'fb_fam_hist_status', 'fb_acroparesthesia',
         'fb_cardiac_symtoms', 'fb_neropsychiatric_symp', 'fb_proteinuria', 'fb_enzyme_assy_lab_name', 'fb_enzyme_assy_ref_range', 'fb_enzyme_assy_report_details', 'fb_cDNA_change1', 'fb_Finaloutcomes',])

    users = profile_fabry.objects.all().prefetch_related('patient_fabry').values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'fb_icmr_unique_no', 'fb_final_diagnosis',
                                                                                      'fb_date_of_record', 'fb_clinical_exam_date',
                                                                                      'patient_fabry__fb_anth_wght_pat',
                                                                                      'patient_fabry__fb_anth_wght_per',
                                                                                      'patient_fabry__fb_anth_wght_sd',
                                                                                      'patient_fabry__fb_anth_height_pat',
                                                                                      'patient_fabry__fb_anth_height_per',
                                                                                      'patient_fabry__fb_anth_height_sd',
                                                                                      'patient_fabry__fb_anth_head_cir_pat',
                                                                                      'patient_fabry__fb_anth_head_cir_perc',
                                                                                      'patient_fabry__fb_anth_head_cir_sd',
                                                                                      'patient_fabry__fb_presenting_complaints_years', 'patient_fabry__fb_presenting_complaints_months',
                                                                                      'patient_fabry__fb_presenting_complaints_day', 'patient_fabry__fb_presenting_complaints_intrauterine',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_years', 'patient_fabry__fb_presenting_complaints_age_presentation_months',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_day',
                                                                                      'patient_fabry__fb_presenting_complaints_age_presentation_intrauterine',
                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_years', 'patient_fabry__fb_presenting_complaints_age_diagnosis_months',
                                                                                      'patient_fabry__fb_presenting_complaints_age_diagnosis_day', 'patient_fabry__fb_presenting_complaints_age_diagnosis_intrauterine',
                                                                                      'patient_fabry__fb_fam_hist_status', 'patient_fabry__fb_acroparesthesia', 'patient_fabry__fb_cardiac_symtoms',
                                                                                      'patient_fabry__fb_neropsychiatric_symp', 'patient_fabry__fb_proteinuria', 'patient_fabry__fb_enzyme_assy_lab_name',
                                                                                      'patient_fabry__fb_enzyme_assy_ref_range', 'patient_fabry__fb_enzyme_assy_report_details', 'patient_fabry__fb_cDNA_change1',
                                                                                      'patient_fabry__fb_Finaloutcomes',)
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_bleeding_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bleeding.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_bleeding__bd_final_diagnosis', 'patient_bleeding__bd_date_of_record', 'patient_bleeding__bd_date_of_clinical_exam', 'patient_bleeding__bd_date_of_birth',
         'patient_bleeding__bd_patient_name', 'patient_bleeding__bd_father_name', 'patient_bleeding__bd_mother_name',
         'patient_bleeding__bd_paitent_id_yes_no', 'patient_bleeding__bd_paitent_id', 'patient_bleeding__bd_patient_id_no', 'patient_bleeding__bd_mother_father_id', 'patient_bleeding__bd_mother_father_id_no',
         'patient_bleeding__bd_permanent_addr', 'patient_bleeding__bd_state', 'patient_bleeding__bd_district', 'patient_bleeding__bd_city_name', 'patient_bleeding__bd_country_name', 'patient_bleeding__bd_land_line_no',
         'patient_bleeding__bd_mother_mobile_no', 'patient_bleeding__bd_father_mobile_no', 'patient_bleeding__bd_email', 'patient_bleeding__bd_religion', 'patient_bleeding__bd_caste', 'patient_bleeding__bd_gender',
         'patient_bleeding__bd_referred_status', 'patient_bleeding__bd_referred_by', 'patient_bleeding__bd_referred_by_desc', 'patient_bleeding__bd_consent_given', 'patient_bleeding__bd_consent_upload',
         'patient_bleeding__bd_assent_given', 'patient_bleeding__bd_assent_upload', 'patient_bleeding__bd_hospital_name', 'patient_bleeding__bd_hospital_reg_no', 'patient_bleeding__bd_patient_edu_status',
         'patient_bleeding__bd_patient_occupation', 'patient_bleeding__bd_father_edu_status', 'patient_bleeding__bd_father_occupation', 'patient_bleeding__bd_mother_edu_status',
         'patient_bleeding__bd_mother_occupation', 'patient_bleeding__bd_monthly_income_status', 'patient_bleeding__bd_diagnosis_type_1', 'patient_bleeding__bd_diagnosis_type_other', 'patient_bleeding__bd_anthr_weight',
         'patient_bleeding__bd_anthr_height', 'patient_bleeding__bd_anthr_head_circum', 'patient_bleeding__bd_diagnosis_age', 'patient_bleeding__bd_first_bleed_age',
         'patient_bleeding__bd_bleeding_site', 'patient_bleeding__bd_blood_pressure_type', 'patient_bleeding__bd_blooding_fam_hist', 'patient_bleeding__bd_fam_name', 'patient_bleeding__bd_fam_reln',
         'patient_bleeding__bd_fam_daignosis', 'patient_bleeding__bd_test_center_name', 'patient_bleeding__bd_diagnosis_method', 'patient_bleeding__bd_blood_group', 'patient_bleeding__bd_hiv_status',
         'patient_bleeding__bd_hbv_status', 'patient_bleeding__bd_hcv_status', 'patient_bleeding__bd_factory_deficiency', 'patient_bleeding__bd_factory_deficiency_other', 'patient_bleeding__bd_factory_level_per',
         'patient_bleeding__bd_factory_severity', 'patient_bleeding__bd_vwf_antigen_per', 'patient_bleeding__bd_vwf_method', 'patient_bleeding__bd_vwf_ris_cofactor',
         'patient_bleeding__bd_screening_test', 'patient_bleeding__bd_quant_assay', 'patient_bleeding__bd_inhibitor_method', 'patient_bleeding__bd_inhibitor_titer', 'patient_bleeding__bd_platelet_count',
         'patient_bleeding__bd_platelet_agregatin_Ristocetin_low_dose', 'patient_bleeding__bd_platelet_agregatin_Ristocetin_high_dose',
         'patient_bleeding__bd_platelet_agregatin_ADP', 'patient_bleeding__bd_platelet_agregatin_Collagen', 'patient_bleeding__bd_platelet_agregatin_Epinephrine',
         'patient_bleeding__bd_platelet_agregatin_Arachidonic_acid', 'patient_bleeding__bd_platelet_agregatin_others', 'patient_bleeding__bd_platelet_receptors_1',
         'patient_bleeding__bd_platelet_receptors_2', 'patient_bleeding__bd_platelet_receptors_3', 'patient_bleeding__bd_platelet_receptors_4', 'patient_bleeding__bd_platelet_receptors_5',
         'patient_bleeding__bd_platelet_receptors_6', 'patient_bleeding__bd_platelet_receptors_7', 'patient_bleeding__bd_platelet_receptors_8',
         'patient_bleeding__bd_platelet_receptors_9', 'patient_bleeding__bd_platelet_receptors_others', 'patient_bleeding__bd_mutation_identified', 'patient_bleeding__bd_mutation_type',
         'patient_bleeding__bd_final_diagnosis', 'patient_bleeding__bd_fam_pedigree', 'patient_bleeding__bd_diag_invest_report', 'patient_bleeding__bd_carrier_studies',
         'patient_bleeding__bd_carr_female_1_name', 'patient_bleeding__bd_carr_female_1_adhaar', 'patient_bleeding__bd_carr_female_1_dob', 'patient_bleeding__bd_carr_female_1_age',
         'patient_bleeding__bd_carr_female_1_rel_index', 'patient_bleeding__bd_carr_female_1_status', 'patient_bleeding__bd_carr_female_1_dos', 'patient_bleeding__bd_carr_female_2_name',
         'patient_bleeding__bd_carr_female_2_adhaar', 'patient_bleeding__bd_carr_female_2_dob', 'patient_bleeding__bd_carr_female_2_age', 'patient_bleeding__bd_carr_female_2_rel_index',
         'patient_bleeding__bd_carr_female_2_status', 'patient_bleeding__bd_carr_female_2_dos', 'patient_bleeding__bd_carr_any_other_details', 'patient_bleeding__bd_ante_female_1_name',
         'patient_bleeding__bd_ante_female_1_adhaar', 'patient_bleeding__bd_ante_female_1_dob', 'patient_bleeding__bd_ante_female_1_age', 'patient_bleeding__bd_ante_female_1_rel_index',
         'patient_bleeding__bd_ante_female_1_proc', 'patient_bleeding__bd_ante_female_1_per_by', 'patient_bleeding__bd_ante_female_1_dos', 'patient_bleeding__bd_ante_female_1_res',
         'patient_bleeding__bd_ante_other_info_1', 'patient_bleeding__bd_ante_female_2_name', 'patient_bleeding__bd_ante_female_2_adhaar', 'patient_bleeding__bd_ante_female_2_dob',
         'patient_bleeding__bd_ante_female_2_age', 'patient_bleeding__bd_ante_female_2_rel_index', 'patient_bleeding__bd_ante_female_2_proc', 'patient_bleeding__bd_ante_female_2_per_by',
         'patient_bleeding__bd_ante_female_2_dos', 'patient_bleeding__bd_ante_female_2_res', 'patient_bleeding__bd_ante_other_info_2', 'patient_bleeding__bd_bleed_past_12', 'patient_bleeding__bd_bleed_life_time',
         'patient_bleeding__bd_spontaneous_past_12', 'patient_bleeding__bd_spontaneous_life_time', 'patient_bleeding__bd_traumatic_past_12',
         'patient_bleeding__bd_traumatic_life_time', 'patient_bleeding__bd_haemorrhages_past_12', 'patient_bleeding__bd_haemorrhages_life_time', 'patient_bleeding__bd_cns_past_12', 'patient_bleeding__bd_cns_life_time',
         'patient_bleeding__bd_muscle_past_12', 'patient_bleeding__bd_muscle_life_time', 'patient_bleeding__bd_mucosal_past_12', 'patient_bleeding__bd_mucosal_life_time',
         'patient_bleeding__bd_chronic_def', 'patient_bleeding__bd_bleeds_others', 'patient_bleeding__bd_first_fact_age', 'patient_bleeding__bd_birth_exposure_days', 'patient_bleeding__bd_transfusion_product',
         'patient_bleeding__bd_transfusion_product_others', 'patient_bleeding__bd_curr_mode_treatment', 'patient_bleeding__bd_demand_bd_episodes',
         'patient_bleeding__bd_demand_bd_duration', 'patient_bleeding__bd_funding_source', 'patient_bleeding__bd_funding_source_other', 'patient_bleeding__bd_dose', 'patient_bleeding__bd_frequency',
         'patient_bleeding__bd_start_date', 'patient_bleeding__bd_end_date', 'patient_bleeding__bd_ongoing_status', 'patient_bleeding__bd_duration', 'patient_bleeding__bd_infusion_skill',
         'patient_bleeding__bd_inhibitor_status',
         'patient_bleeding__bd_any_other_info', 'patient_bleeding__bd_surgery_num', 'patient_bleeding__bd_surgery_1', 'patient_bleeding__bd_surgery_1_transfusin',
         'patient_bleeding__bd_surgery_1_transfusin_others', 'patient_bleeding__bd_surgery_2', 'patient_bleeding__bd_surgery_2_transfusin',
         'patient_bleeding__bd_surgery_2_transfusin_others', 'patient_bleeding__bd_surgery_3', 'patient_bleeding__bd_surgery_3_transfusin',
         'patient_bleeding__bd_surgery_3_transfusin_others', 'patient_bleeding__bd_physical_dis_status', 'patient_bleeding__bd_cronic_anthr', 'patient_bleeding__bd_joint', 'patient_bleeding__bd_target_joint', ])

    users = profile_bleeding.objects.all().prefetch_related('patient_bleeding').values_list('register_id__institute_name', 'uniqueId', 'bd_icmr_unique_no', 'bd_final_diagnosis',
                                                                                            'bd_date_of_record', 'bd_date_of_clinical_exam', 'bd_date_of_birth',
                                                                                            'bd_patient_name', 'bd_father_name', 'bd_mother_name', 'bd_paitent_id_yes_no',
                                                                                            'bd_paitent_id', 'bd_patient_id_no', 'bd_mother_father_id', 'bd_mother_father_id_no',
                                                                                            'bd_permanent_addr', 'bd_state', 'bd_district', 'bd_city_name', 'bd_country_name',
                                                                                            'bd_land_line_no', 'bd_mother_mobile_no', 'bd_father_mobile_no', 'bd_email',
                                                                                            'bd_religion', 'bd_caste', 'bd_gender', 'bd_referred_status', 'bd_referred_by',
                                                                                            'bd_referred_by_desc', 'bd_consent_given', 'bd_consent_upload', 'bd_assent_given',
                                                                                            'bd_assent_upload', 'bd_hospital_name', 'bd_hospital_reg_no', 'patient_bleeding__bd_patient_edu_status',
                                                                                            'patient_bleeding__bd_patient_occupation', 'patient_bleeding__bd_father_edu_status', 'patient_bleeding__bd_father_occupation',
                                                                                            'patient_bleeding__bd_mother_edu_status', 'patient_bleeding__bd_mother_occupation',
                                                                                            'patient_bleeding__bd_monthly_income_status', 'patient_bleeding__bd_diagnosis_type_1',
                                                                                            'patient_bleeding__bd_diagnosis_type_other', 'patient_bleeding__bd_anthr_weight', 'patient_bleeding__bd_anthr_height',
                                                                                            'patient_bleeding__bd_anthr_head_circum', 'patient_bleeding__bd_diagnosis_age', 'patient_bleeding__bd_first_bleed_age',
                                                                                            'patient_bleeding__bd_bleeding_site', 'patient_bleeding__bd_blood_pressure_type', 'patient_bleeding__bd_blooding_fam_hist',
                                                                                            'patient_bleeding__bd_fam_name', 'patient_bleeding__bd_fam_reln', 'patient_bleeding__bd_fam_daignosis',
                                                                                            'patient_bleeding__bd_test_center_name', 'patient_bleeding__bd_diagnosis_method', 'patient_bleeding__bd_blood_group',
                                                                                            'patient_bleeding__bd_hiv_status',
                                                                                            'patient_bleeding__bd_hbv_status', 'patient_bleeding__bd_hcv_status', 'patient_bleeding__bd_factory_deficiency',
                                                                                            'patient_bleeding__bd_factory_deficiency_other', 'patient_bleeding__bd_factory_level_per',
                                                                                            'patient_bleeding__bd_factory_severity', 'patient_bleeding__bd_vwf_antigen_per', 'patient_bleeding__bd_vwf_method',
                                                                                            'patient_bleeding__bd_vwf_ris_cofactor', 'patient_bleeding__bd_screening_test', 'patient_bleeding__bd_quant_assay',
                                                                                            'patient_bleeding__bd_inhibitor_method', 'patient_bleeding__bd_inhibitor_titer', 'patient_bleeding__bd_platelet_count',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Ristocetin_low_dose',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Ristocetin_high_dose', 'patient_bleeding__bd_platelet_agregatin_ADP',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Collagen',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Epinephrine', 'patient_bleeding__bd_platelet_agregatin_Arachidonic_acid',
                                                                                            'patient_bleeding__bd_platelet_agregatin_others',
                                                                                            'patient_bleeding__bd_platelet_receptors_1', 'patient_bleeding__bd_platelet_receptors_2',
                                                                                            'patient_bleeding__bd_platelet_receptors_3', 'patient_bleeding__bd_platelet_receptors_4',
                                                                                            'patient_bleeding__bd_platelet_receptors_5',
                                                                                            'patient_bleeding__bd_platelet_receptors_6', 'patient_bleeding__bd_platelet_receptors_7',
                                                                                            'patient_bleeding__bd_platelet_receptors_8', 'patient_bleeding__bd_platelet_receptors_9',
                                                                                            'patient_bleeding__bd_platelet_receptors_others', 'patient_bleeding__bd_mutation_identified',
                                                                                            'patient_bleeding__bd_mutation_type', 'patient_bleeding__bd_final_diagnosis', 'patient_bleeding__bd_fam_pedigree',
                                                                                            'patient_bleeding__bd_diag_invest_report', 'patient_bleeding__bd_carrier_studies', 'patient_bleeding__bd_carr_female_1_name',
                                                                                            'patient_bleeding__bd_carr_female_1_adhaar', 'patient_bleeding__bd_carr_female_1_dob',
                                                                                            'patient_bleeding__bd_carr_female_1_age', 'patient_bleeding__bd_carr_female_1_rel_index',
                                                                                            'patient_bleeding__bd_carr_female_1_status', 'patient_bleeding__bd_carr_female_1_dos',
                                                                                            'patient_bleeding__bd_carr_female_2_name',
                                                                                            'patient_bleeding__bd_carr_female_2_adhaar', 'patient_bleeding__bd_carr_female_2_dob', 'patient_bleeding__bd_carr_female_2_age',
                                                                                            'patient_bleeding__bd_carr_female_2_rel_index', 'patient_bleeding__bd_carr_female_2_status',
                                                                                            'patient_bleeding__bd_carr_female_2_dos', 'patient_bleeding__bd_carr_any_other_details',
                                                                                            'patient_bleeding__bd_ante_female_1_name', 'patient_bleeding__bd_ante_female_1_adhaar',
                                                                                            'patient_bleeding__bd_ante_female_1_dob',
                                                                                            'patient_bleeding__bd_ante_female_1_age', 'patient_bleeding__bd_ante_female_1_rel_index',
                                                                                            'patient_bleeding__bd_ante_female_1_proc', 'patient_bleeding__bd_ante_female_1_per_by',
                                                                                            'patient_bleeding__bd_ante_female_1_dos',
                                                                                            'patient_bleeding__bd_ante_female_1_res', 'patient_bleeding__bd_ante_other_info_1', 'patient_bleeding__bd_ante_female_2_name',
                                                                                            'patient_bleeding__bd_ante_female_2_adhaar', 'patient_bleeding__bd_ante_female_2_dob',
                                                                                            'patient_bleeding__bd_ante_female_2_age', 'patient_bleeding__bd_ante_female_2_rel_index',
                                                                                            'patient_bleeding__bd_ante_female_2_proc', 'patient_bleeding__bd_ante_female_2_per_by',
                                                                                            'patient_bleeding__bd_ante_female_2_dos',
                                                                                            'patient_bleeding__bd_ante_female_2_res', 'patient_bleeding__bd_ante_other_info_2', 'patient_bleeding__bd_bleed_past_12',
                                                                                            'patient_bleeding__bd_bleed_life_time', 'patient_bleeding__bd_spontaneous_past_12',
                                                                                            'patient_bleeding__bd_spontaneous_life_time', 'patient_bleeding__bd_traumatic_past_12',
                                                                                            'patient_bleeding__bd_traumatic_life_time', 'patient_bleeding__bd_haemorrhages_past_12',
                                                                                            'patient_bleeding__bd_haemorrhages_life_time',
                                                                                            'patient_bleeding__bd_cns_past_12', 'patient_bleeding__bd_cns_life_time', 'patient_bleeding__bd_muscle_past_12',
                                                                                            'patient_bleeding__bd_muscle_life_time', 'patient_bleeding__bd_mucosal_past_12', 'patient_bleeding__bd_mucosal_life_time',
                                                                                            'patient_bleeding__bd_chronic_def', 'patient_bleeding__bd_bleeds_others', 'patient_bleeding__bd_first_fact_age',
                                                                                            'patient_bleeding__bd_birth_exposure_days', 'patient_bleeding__bd_transfusion_product',
                                                                                            'patient_bleeding__bd_transfusion_product_others', 'patient_bleeding__bd_curr_mode_treatment',
                                                                                            'patient_bleeding__bd_demand_bd_episodes', 'patient_bleeding__bd_demand_bd_duration', 'patient_bleeding__bd_funding_source',
                                                                                            'patient_bleeding__bd_funding_source_other', 'patient_bleeding__bd_dose', 'patient_bleeding__bd_frequency',
                                                                                            'patient_bleeding__bd_start_date', 'patient_bleeding__bd_end_date', 'patient_bleeding__bd_ongoing_status',
                                                                                            'patient_bleeding__bd_duration',
                                                                                            'patient_bleeding__bd_infusion_skill', 'patient_bleeding__bd_inhibitor_status', 'patient_bleeding__bd_any_other_info',
                                                                                            'patient_bleeding__bd_surgery_num', 'patient_bleeding__bd_surgery_1',
                                                                                            'patient_bleeding__bd_surgery_1_transfusin', 'patient_bleeding__bd_surgery_1_transfusin_others',
                                                                                            'patient_bleeding__bd_surgery_2', 'patient_bleeding__bd_surgery_2_transfusin',
                                                                                            'patient_bleeding__bd_surgery_2_transfusin_others', 'patient_bleeding__bd_surgery_3',
                                                                                            'patient_bleeding__bd_surgery_3_transfusin', 'patient_bleeding__bd_surgery_3_transfusin_others',
                                                                                            'patient_bleeding__bd_physical_dis_status', 'patient_bleeding__bd_cronic_anthr', 'patient_bleeding__bd_joint',
                                                                                            'patient_bleeding__bd_target_joint', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_bleeding_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bleeding_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'patient_bleeding__bd_final_diagnosis', 'patient_bleeding__bd_date_of_record', 'patient_bleeding__bd_date_of_clinical_exam',
         'bd_diagnosis_type_1', 'bd_diagnosis_type_other', 'bd_test_center_name', 'bd_diagnosis_method', 'bd_factory_deficiency', 'bd_factory_deficiency_other', 'bd_factory_level_per', 'bd_factory_severity',
         'bd_vwf_antigen_per', 'bd_vwf_method', 'bd_vwf_ris_cofactor', 'bd_platelet_agregatin_Ristocetin_low_dose', 'bd_platelet_agregatin_Ristocetin_high_dose', 'bd_platelet_agregatin_ADP',
         'bd_platelet_agregatin_Collagen', 'bd_platelet_agregatin_Epinephrine', 'bd_platelet_agregatin_Arachidonic_acid', 'bd_platelet_agregatin_others', 'bd_platelet_receptors_1', 'bd_platelet_receptors_2',
         'bd_platelet_receptors_3', 'bd_platelet_receptors_4', 'bd_platelet_receptors_5', 'bd_platelet_receptors_6', 'bd_platelet_receptors_7', 'bd_platelet_receptors_8', 'bd_platelet_receptors_9',
         'bd_platelet_receptors_others', 'bd_mutation_identified', 'bd_mutation_type', 'bd_final_diagnosis', 'bd_bleed_past_12', 'bd_bleed_life_time', 'bd_spontaneous_past_12', 'bd_spontaneous_life_time',
         'bd_traumatic_past_12', 'bd_traumatic_life_time',  ])

    users = profile_bleeding.objects.all().prefetch_related('patient_bleeding').values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'bd_icmr_unique_no', 'bd_final_diagnosis',
                                                                                            'bd_date_of_record', 'bd_date_of_clinical_exam',
                                                                                            'patient_bleeding__bd_diagnosis_type_1', 'patient_bleeding__bd_diagnosis_type_other', 'patient_bleeding__bd_test_center_name',
                                                                                            'patient_bleeding__bd_diagnosis_method', 'patient_bleeding__bd_factory_deficiency',
                                                                                            'patient_bleeding__bd_factory_deficiency_other', 'patient_bleeding__bd_factory_level_per',
                                                                                            'patient_bleeding__bd_factory_severity', 'patient_bleeding__bd_vwf_antigen_per', 'patient_bleeding__bd_vwf_method',
                                                                                            'patient_bleeding__bd_vwf_ris_cofactor', 'patient_bleeding__bd_platelet_agregatin_Ristocetin_low_dose',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Ristocetin_high_dose', 'patient_bleeding__bd_platelet_agregatin_ADP',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Collagen', 'patient_bleeding__bd_platelet_agregatin_Epinephrine',
                                                                                            'patient_bleeding__bd_platelet_agregatin_Arachidonic_acid', 'patient_bleeding__bd_platelet_agregatin_others',
                                                                                            'patient_bleeding__bd_platelet_receptors_1', 'patient_bleeding__bd_platelet_receptors_2',
                                                                                            'patient_bleeding__bd_platelet_receptors_3', 'patient_bleeding__bd_platelet_receptors_4',
                                                                                            'patient_bleeding__bd_platelet_receptors_5', 'patient_bleeding__bd_platelet_receptors_6',
                                                                                            'patient_bleeding__bd_platelet_receptors_7', 'patient_bleeding__bd_platelet_receptors_8',
                                                                                            'patient_bleeding__bd_platelet_receptors_9', 'patient_bleeding__bd_platelet_receptors_others',
                                                                                            'patient_bleeding__bd_mutation_identified', 'patient_bleeding__bd_mutation_type', 'patient_bleeding__bd_final_diagnosis',
                                                                                            'patient_bleeding__bd_bleed_past_12', 'patient_bleeding__bd_bleed_life_time', 'patient_bleeding__bd_spontaneous_past_12',
                                                                                            'patient_bleeding__bd_spontaneous_life_time', 'patient_bleeding__bd_traumatic_past_12',
                                                                                            'patient_bleeding__bd_traumatic_life_time',  )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_iem_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iem.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_metabolism__mt_final_diagnosis',
         'patient_metabolism__mt_date_of_records', 'patient_metabolism__mt_date_of_clinical_exam',
         'patient_metabolism__mt_date_of_birth',
         'patient_metabolism__mt_patient_name', 'patient_metabolism__mt_father_name',
         'patient_metabolism__mt_mother_name',
         'patient_metabolism__mt_paitent_id_yes_no', 'patient_metabolism__mt_paitent_id',
         'patient_metabolism__mt_patient_id_no', 'patient_metabolism__mt_father_mother_id',
         'patient_metabolism__mt_mother_father_id_no',
         'patient_metabolism__mt_permanent_addr', 'patient_metabolism__mt_state', 'patient_metabolism__mt_district',
         'patient_metabolism__mt_city_name', 'patient_metabolism__mt_country_name',
         'patient_metabolism__mt_land_line_no',
         'patient_metabolism__mt_mother_mobile_no', 'patient_metabolism__mt_father_mobile_no',
         'patient_metabolism__mt_email', 'patient_metabolism__mt_religion',
         'patient_metabolism__mt_religion_other_specify',
         'patient_metabolism__mt_caste', 'patient_metabolism__mt_caste_other_specify', 'patient_metabolism__mt_gender',
         'patient_metabolism__mt_referred_status', 'patient_metabolism__mt_referred_by',
         'patient_metabolism__mt_referred_by_desc', 'patient_metabolism__mt_consent_given',
         'patient_metabolism__mt_consent_upload', 'patient_metabolism__mt_assent_given',
         'patient_metabolism__mt_assent_upload',
         'patient_metabolism__mt_hospital_name', 'patient_metabolism__mt_hospital_reg_no',
         'patient_metabolism__mt_patient_edu_status',
         'patient_metabolism__mt_patient_occupation',
         'patient_metabolism__mt_father_edu_status',
         'patient_metabolism__mt_father_occupation',
         'patient_metabolism__mt_mother_edu_status',
         'patient_metabolism__mt_mother_occupation',
         'patient_metabolism__mt_monthly_income_status',
         'patient_metabolism__mt_anthropometry_date',
         'patient_metabolism__mt_anth_wght_pat',
         'patient_metabolism__mt_anth_wght_per',
         'patient_metabolism__mt_anth_wght_sd',
         'patient_metabolism__mt_anth_height_pat',
         'patient_metabolism__mt_anth_height_per',
         'patient_metabolism__mt_anth_height_sd',
         'patient_metabolism__mt_lower_segment_patient',
         'patient_metabolism__mt_lower_segment_percemtile',
         'patient_metabolism__mt_lower_segment_sd',
         'patient_metabolism__mt_lower_us_ls_patient',
         'patient_metabolism__mt_lower_us_ls_percemtile',
         'patient_metabolism__mt_lower_us_ls_sd',
         'patient_metabolism__mt_anth_head_cir_pat',
         'patient_metabolism__mt_anth_head_cir_perc',
         'patient_metabolism__mt_anth_head_cir_sd',
         'patient_metabolism__mt_lower_arm_spam_patient',
         'patient_metabolism__mt_lower_arm_spam_percemtile',
         'patient_metabolism__mt_lower_arm_spam_sd',
         'patient_metabolism__mt_presenting_complaints_years',
         'patient_metabolism__mt_presenting_complaints_months',
         'patient_metabolism__mt_presenting_complaints_day',
         'patient_metabolism__mt_presenting_complaints_intrauterine',
         'patient_metabolism__mt_presenting_complaints_age_presentation_years',
         'patient_metabolism__mt_presenting_complaints_age_presentation_months',
         'patient_metabolism__mt_presenting_complaints_age_presentation_day',
         'patient_metabolism__mt_presenting_complaints_age_presentation_intrauterine',
         'patient_metabolism__mt_presenting_complaints_age_diagnosis_years',
         'patient_metabolism__mt_presenting_complaints_age_diagnosis_months',
         'patient_metabolism__mt_presenting_complaints_age_diagnosis_day',
         'patient_metabolism__mt_presenting_complaints_age_diagnosis_intrauterine',
         'patient_metabolism__mt_pedigree_upload',
         'patient_metabolism__mt_fam_hist_status',
         'patient_metabolism__mt_fam_hist_descr',
         'patient_metabolism__mt_cons_status',
         'patient_metabolism__mt_cons_degree_specify',
         'patient_metabolism__mt_Inbreeding',
         'patient_metabolism__mt_Inbreeding_specify_degree',
         'patient_metabolism__mt_Inbreeding_coefficient_degree',
         'patient_metabolism__mt_encephalopathic_presentation',
         'patient_metabolism__mt_encephalopathic_presentation_age_presentaion',
         'patient_metabolism__mt_encephalopathic_presentation_age_diagnosis',
         'patient_metabolism__mt_encephalopathic_presentation_duration',
         'patient_metabolism__mt_Presentation_neonatal_jaundice',
         'patient_metabolism__mt_Presentation_neonatal_jaundice_age_presentation',
         'patient_metabolism__mt_Presentation_neonatal_jaundice_ae_diagnosis',
         'patient_metabolism__mt_Presentation_neonatal_jaundice_duraions',
         'patient_metabolism__mt_Presentation_cardiac_symptoms',
         'patient_metabolism__mt_Presentation_cardiac_symptoms_age_presentation',
         'patient_metabolism__mt_Presentation_cardiac_symptoms_age_diagnosis',
         'patient_metabolism__mt_Presentation_cardiac_symptoms_duration',
         'patient_metabolism__mt_symptoms_after_long_normalcy',
         'patient_metabolism__mt_symptoms_after_long_normalcy_sugar',
         'patient_metabolism__mt_symptoms_after_long_normalcy_fruit_juice',
         'patient_metabolism__mt_symptoms_after_long_normalcy_fasting',
         'patient_metabolism__mt_symptoms_after_long_normalcy_protein_foods',
         'patient_metabolism__mt_symptoms_after_long_normalcy_febrile_illness',
         'patient_metabolism__mt_Presentation_refractory_epilepsy',
         'patient_metabolism__mt_Presentation_refractory_epilepsy_age_presentation',
         'patient_metabolism__mt_Presentation_refractory_epilepsy_age_diagnosis',
         'patient_metabolism__mt_Presentation_refractory_epilepsy_duration',
         'patient_metabolism__mt_mental_retardation_or_dev_delay',
         'patient_metabolism__mt_mental_retardation_Motor',
         'patient_metabolism__mt_mental_retardation_Cognitive',
         'patient_metabolism__mt_mental_retardation_Global',
         'patient_metabolism__mt_Neuroregression',
         'patient_metabolism__mt_Neuroregression_Motor',
         'patient_metabolism__mt_Neuroregression_Cognitive',
         'patient_metabolism__mt_Neuroregression_Global',
         'patient_metabolism__mt_Age_onset_regression',
         'patient_metabolism__mt_Vomiting',
         'patient_metabolism__mt_Aversion_sweet_protein',
         'patient_metabolism__mt_Loose_stools',
         'patient_metabolism__mt_Loose_stools_dropdown',
         'patient_metabolism__mt_Pneumonia',
         'patient_metabolism__mt_Pneumonia_dropdown',
         'patient_metabolism__mt_Fever',
         'patient_metabolism__mt_Fever_dropdown',
         'patient_metabolism__mt_Fever_type',
         'patient_metabolism__mt_Lethargy',
         'patient_metabolism__mt_Behavioral_problems',
         'patient_metabolism__mt_Excessive_crying',
         'patient_metabolism__mt_Decreased_attention_span',
         'patient_metabolism__mt_Speech_disturbances',
         'patient_metabolism__mt_Decline_school_performance',
         'patient_metabolism__mt_Clumsiness',
         'patient_metabolism__mt_Seizures',
         'patient_metabolism__mt_Seizures_Partial',
         'patient_metabolism__mt_Seizures_generalized',
         'patient_metabolism__mt_Seizures_myoclonic',
         'patient_metabolism__mt_Seizures_other',
         'patient_metabolism__mt_Seizures_other_specify',
         'patient_metabolism__mt_Seizures_frequency',
         'patient_metabolism__mt_AntiConvulsant_therapy',
         'patient_metabolism__mt_AntiConvulsant_Monotherapy',
         'patient_metabolism__mt_AntiConvulsant_Monotherapy_drug_name',
         'patient_metabolism__mt_AntiConvulsant_Monotherapy_dose',
         'patient_metabolism__mt_AntiConvulsant_Polytherapy',
         'patient_metabolism__mt_AntiConvulsant_Polytherapy_drug_name',
         'patient_metabolism__mt_AntiConvulsant_Polytherapy_dose',
         'patient_metabolism__mt_HistoryPreviousAdmission',
         'patient_metabolism__mt_history_nuroregression',
         'patient_metabolism__mt_history_nuroregression_text',
         'patient_metabolism__mt_history_diagnosis',
         'patient_metabolism__mt_history_diagnosis_text',
         'patient_metabolism__mt_history_mech_ventilation',
         'patient_metabolism__mt_history_mech_ventilation_text',
         'patient_metabolism__mt_history_mech_distention',
         'patient_metabolism__mt_history_mech_distention_text',
         'patient_metabolism__mt_any_surgery',
         'patient_metabolism__mt_any_surgery_specify',
         'patient_metabolism__mt_History_liver_dysfunction',
         'patient_metabolism__mt_History_liver_dysfunction_trimester_pregnancy',
         'patient_metabolism__mt_Ultrasound',
         'patient_metabolism__mt_Ultrasound_Polyhydramnios',
         'patient_metabolism__mt_Ultrasound_Oligoamnios',
         'patient_metabolism__mt_Ultrasound_Skeletal_anomalies',
         'patient_metabolism__mt_Ultrasound_Hydrops',
         'patient_metabolism__mt_Ultrasound_abnormal_specify',
         'patient_metabolism__mt_Delivery_type',
         'patient_metabolism__mt_Baby_cried_immediately_after_delivery',
         'patient_metabolism__mt_Resuscitation_required',
         'patient_metabolism__mt_NICU_Stay',
         'patient_metabolism__mt_Symptomatic_asymptomatic',
         'patient_metabolism__mt_Shock',
         'patient_metabolism__mt_Shock_catecholamine_sensitive',
         'patient_metabolism__mt_Shock_refractory',
         'patient_metabolism__mt_Ventilation',
         'patient_metabolism__mt_Ventilation_CPAP',
         'patient_metabolism__mt_Ventilation_NIV',
         'patient_metabolism__mt_Ventilation_MV',
         'patient_metabolism__mt_feeding_issues',
         'patient_metabolism__mt_feeding_issues_Regurgitation_oral_feed',
         'patient_metabolism__mt_feeding_issues_NG_feeding',
         'patient_metabolism__mt_feeding_issues_Parenteral',
         'patient_metabolism__mt_Neonatal_hyperbilurubinemia',
         'patient_metabolism__mt_Neonatal_hyperbilurubinemia_direct',
         'patient_metabolism__mt_Neonatal_hyperbilurubinemia_indirect',
         'patient_metabolism__mt_Neonatal_hyperbilurubinemia_total_bill_value',
         'patient_metabolism__mt_Sepsis',
         'patient_metabolism__mt_Sepsis_Organism',
         'patient_metabolism__mt_CRRT_PD_required',
         'patient_metabolism__mt_EEG_natel',
         'patient_metabolism__mt_EEG_BurstSuppressionPattern_natel',
         'patient_metabolism__mt_EEG_Hypsarrythmia_natel',
         'patient_metabolism__mt_EEG_GeneralizedSlowing_natel',
         'patient_metabolism__mt_EEG_Comb_like_pattern_natel',
         'patient_metabolism__mt_facial_dysmorphism',
         'patient_metabolism__mt_Facial_dysmorphism_upload_file',
         'patient_metabolism__mt_Skin_Pigmentation',
         'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_diffuse',
         'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_patchy',
         'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation',
         'patient_metabolism__mt_Hirsutism',
         'patient_metabolism__mt_Hirsutism_Facial',
         'patient_metabolism__mt_Hirsutism_generalised',
         'patient_metabolism__mt_Excessive_mongolion_spots',
         'patient_metabolism__mt_Ichthyosis',
         'patient_metabolism__mt_Telengiectasia',
         'patient_metabolism__mt_Edema',
         'patient_metabolism__mt_Hydrops',
         'patient_metabolism__mt_Inverted_nipples',
         'patient_metabolism__mt_fat_distribution_Lipodystrophy',
         'patient_metabolism__mt_Hemoglobinura',
         'patient_metabolism__mt_Encephalopathy',
         'patient_metabolism__mt_Hypotonia',
         'patient_metabolism__mt_Hypertonia',
         'patient_metabolism__mt_Brisk_reflexes',
         'patient_metabolism__mt_Hyporeflexia',
         'patient_metabolism__mt_Opisthotonus',
         'patient_metabolism__mt_Other_Abnormal_Movement',
         'patient_metabolism__mt_Tremor_chorea_athetosis',
         'patient_metabolism__mt_AnyOther_TremorJitteriness',
         'patient_metabolism__mt_AnyOther_chorea',
         'patient_metabolism__mt_AnyOther_athetosis',
         'patient_metabolism__mt_Gait_abnormalities',
         'patient_metabolism__mt_Optic_Nerve_atrophy',
         'patient_metabolism__mt_Retinal_degeneration',
         'patient_metabolism__mt_Cataract',
         'patient_metabolism__mt_Squint',
         'patient_metabolism__mt_Nystagmus_oculogyria',
         'patient_metabolism__mt_Fundus_Abnormal',
         'patient_metabolism__mt_Fundus_Abnormal_specify',
         'patient_metabolism__mt_cheery_red_spot',
         'patient_metabolism__mt_cheery_red_spot_specify',
         'patient_metabolism__mt_Murmur',
         'patient_metabolism__mt_Congestive_Heart_Failure',
         'patient_metabolism__mt_Cardio_myopathy',
         'patient_metabolism__mt_Hepatomegaly',
         'patient_metabolism__mt_Consistency',
         'patient_metabolism__mt_surface',
         'patient_metabolism__mt_margin',
         'patient_metabolism__mt_BCM_size',
         'patient_metabolism__mt_Span_cm',
         'patient_metabolism__mt_Splenomegaly',
         'patient_metabolism__mt_Splenomegaly_size_cm',
         'patient_metabolism__mt_IQ',
         'patient_metabolism__mt_IQ_value',
         'patient_metabolism__mt_DQ',
         'patient_metabolism__mt_DQ_value',
         'patient_metabolism__mt_Any_other_findings',
         'patient_metabolism__mt_Hb_gm_dl',
         'patient_metabolism__mt_wbc_tc_ul',
         'patient_metabolism__mt_wbc_dc_perc',
         'patient_metabolism__mt_Absolut_Neutrophil_count_mm_3',
         'patient_metabolism__mt_Platelet_count_ul',
         'patient_metabolism__mt_Acanthocytes',
         'patient_metabolism__mt_S_calcium_mg_dl',
         'patient_metabolism__mt_S_phosphorous_mg_dl',
         'patient_metabolism__mt_S_alkaline_phosphate_UI',
         'patient_metabolism__mt_S_acid_phosphatase_U_L',
         'patient_metabolism__mt_CPK_U_L_total',
         'patient_metabolism__mt_MM_MB',
         'patient_metabolism__mt_Blood_Urea',
         'patient_metabolism__mt_Blood_creatinine_mg_dl',
         'patient_metabolism__mt_Serum_sodium_meq_l',
         'patient_metabolism__mt_Serum_potassium_meq_l',
         'patient_metabolism__mt_Total_protein_g_dl',
         'patient_metabolism__mt_Serum_albumin_g_dl',
         'patient_metabolism__mt_SGPT_IU_L',
         'patient_metabolism__mt_SGOT_IU_L',
         'patient_metabolism__mt_PT_sec',
         'patient_metabolism__mt_APTT_sec',
         'patient_metabolism__mt_TSB_mg_dl',
         'patient_metabolism__mt_DSB_mg_dl',
         'patient_metabolism__mt_IRON_IU_L',
         'patient_metabolism__mt_TIBC_IU_L',
         'patient_metabolism__mt_Lactate_mmol_l',
         'patient_metabolism__mt_Uric_acid_mg_dl',
         'patient_metabolism__mt_Blood_sugar_mg_dl',
         'patient_metabolism__mt_HbA1C_per',
         'patient_metabolism__mt_Total_Cholesterol_mg_dl',
         'patient_metabolism__mt_TGs_mg_dl',
         'patient_metabolism__mt_HDL_mg_dl',
         'patient_metabolism__mt_LDL_mg_dl',
         'patient_metabolism__mt_VLDL_mg_dl',
         'patient_metabolism__mt_Homocysteine_uml_l',
         'patient_metabolism__mt_Prolactin_ng_ml',
         'patient_metabolism__mt_Ultrasonography',
         'patient_metabolism__mt_Ultrasonography_abnormal_Liver',
         'patient_metabolism__mt_Ultrasonography_abnormal_Kidney',
         'patient_metabolism__mt_Ultrasonography_abnormal_Spleen',
         'patient_metabolism__mt_Ultrasonography_abnormal_AnyAdenoma',
         'patient_metabolism__mt_Ultrasonography_abnormal_RenalCysts',
         'patient_metabolism__mt_Skeletal_survey',
         'patient_metabolism__mt_Skeletal_survey_Rickets',
         'patient_metabolism__mt_Skeletal_survey_DysostosisMultiplex',
         'patient_metabolism__mt_Skeletal_survey_ShortLimbs',
         'patient_metabolism__mt_Skeletal_survey_SpineAbnormalities',
         'patient_metabolism__mt_Skeletal_survey_ChondrodyplasiaPuncta',
         'patient_metabolism__mt_ctc_scan',
         'patient_metabolism__mt_ctc_scan_ThalamusHypointesity',
         'patient_metabolism__mt_ctc_scan_calcification',
         'patient_metabolism__mt_ctc_scan_ventriculomegaly',
         'patient_metabolism__mt_ctc_scan_cerebralAtrophy',
         'patient_metabolism__mt_ctc_scan_infarct',
         'patient_metabolism__mt_ctc_scan_hemorrhage',
         'patient_metabolism__mt_ctc_scan_cerebraledema',
         'patient_metabolism__mt_ctc_scan_cysts',
         'patient_metabolism__mt_mri_brain_status',
         'patient_metabolism__mt_mri_brain_corticalAtrophy',
         'patient_metabolism__mt_mri_brain_cerebellarAtrophy',
         'patient_metabolism__mt_mri_brain_ventriculomegaly',
         'patient_metabolism__mt_mri_brain_basalGangliaHypo',
         'patient_metabolism__mt_mri_brain_hyperintensity',
         'patient_metabolism__mt_mri_brain_deepGrayMatterHyperintensity',
         'patient_metabolism__mt_mri_brain_thalamicHypo',
         'patient_metabolism__mt_mri_brain_demyelinationDysmyelination',
         'patient_metabolism__mt_mri_brain_cerebralEdema',
         'patient_metabolism__mt_mri_brain_cysts',
         'patient_metabolism__mt_mri_brain_infarct',
         'patient_metabolism__mt_mri_brain_hemorrhage',
         'patient_metabolism__mt_mri_brain_other',
         'patient_metabolism__mt_mrs_done',
         'patient_metabolism__mt_mrs_LactatePeak',
         'patient_metabolism__mt_mrs_NAAPeak',
         'patient_metabolism__mt_mrs_LowCreatininePeak',
         'patient_metabolism__mt_mrs_CholinePeak',
         'patient_metabolism__mt_echocardiography',
         'patient_metabolism__mt_echocardiography_DialtedCardiomyopathy',
         'patient_metabolism__mt_echocardiography_hypertrophicCardiomyopathy',
         'patient_metabolism__mt_echocardiography_valvularAbnormality',
         'patient_metabolism__mt_echocardiography_structuralDefects',
         'patient_metabolism__mt_echocardiography_SpecifyStructuralDefect',
         'patient_metabolism__mt_echocardiography_EjectionFraction',
         'patient_metabolism__mt_eeg',
         'patient_metabolism__mt_eeg_BurstSuppressionPattern',
         'patient_metabolism__mt_eeg_Hypsarrythmia',
         'patient_metabolism__mt_eeg_GeneralizedSlowing',
         'patient_metabolism__mt_eeg_CombLikePattern',
         'patient_metabolism__mt_ocular_examination_slit',
         'patient_metabolism__mt_veps',
         'patient_metabolism__mt_veps_abnormal_latency',
         'patient_metabolism__mt_erg',
         'patient_metabolism__mt_erg_abnormal_specify',
         'patient_metabolism__mt_OAE_BERA',
         'patient_metabolism__mt_OAE_BERA_Unilateral',
         'patient_metabolism__mt_OAE_BERA_bilateral',
         'patient_metabolism__mt_OAE_BERA_mild',
         'patient_metabolism__mt_OAE_BERA_moderate',
         'patient_metabolism__mt_OAE_BERA_severe',
         'patient_metabolism__mt_OAE_BERA_profoundHearingLoss',
         'patient_metabolism__mt_nerve_conduction_study',
         'patient_metabolism__mt_nerve_conduction_study_motor',
         'patient_metabolism__mt_nerve_conduction_study_sensory',
         'patient_metabolism__mt_nerve_conduction_study_mixed',
         'patient_metabolism__mt_nerve_conduction_study_upperLimb',
         'patient_metabolism__mt_nerve_conduction_study_lowerLimb',
         'patient_metabolism__mt_nerve_conduction_study_reducedMUAPAmplitude',
         'patient_metabolism__mt_nerve_conduction_study_shortMUAPDuration',
         'patient_metabolism__mt_nerve_conduction_study_decreasedConductionVelocity',
         'patient_metabolism__mt_nerve_conduction_study_increasedDistalLatency',
         'patient_metabolism__mt_nerve_conduction_study_decreasedSNAP',
         'patient_metabolism__mt_nerve_conduction_study_increasedFwaveLatency',
         'patient_metabolism__mt_muscle_biopsy',
         'patient_metabolism__mt_Any_other_investigations',
         'patient_metabolism__mt_blood_gas_metabolism_acidosis',
         'patient_metabolism__mt_blood_gas_metabolism_acidosis_PH',
         'patient_metabolism__mt_blood_gas_metabolism_acidosis_HCO_3',
         'patient_metabolism__mt_blood_gas_metabolism_acidosis_Anion_gap',
         'patient_metabolism__mt_metabolic_alkalosis',
         'patient_metabolism__mt_Hyper_ammonemia',
         'patient_metabolism__mt_Hyper_ammonemia_value',
         'patient_metabolism__mt_Hyper_ammonemia_duration',
         'patient_metabolism__mt_high_lactate',
         'patient_metabolism__mt_high_lactate_value',
         'patient_metabolism__mt_high_lactate_csf',
         'patient_metabolism__mt_high_lactate_csf_value',
         'patient_metabolism__mt_ief_transferring_pattern_type',
         'patient_metabolism__mt_ief_transferring_pattern_type_tpye1',
         'patient_metabolism__mt_ief_transferring_pattern_type_tpye2',
         'patient_metabolism__mt_urine_ketones',
         'patient_metabolism__mt_urine_ketones_value',
         'patient_metabolism__mt_plasma_ketones',
         'patient_metabolism__mt_plasma_ketones_value',
         'patient_metabolism__mt_plasma_ketones_ffa_ratio',
         'patient_metabolism__mt_plasma_ketones_ffa_ratio_value',
         'patient_metabolism__mt_hplc',
         'patient_metabolism__mt_hplc_specify',
         'patient_metabolism__mt_hplc_value',
         'patient_metabolism__mt_tms_primary_analyte',
         'patient_metabolism__mt_tms_primary_analyte_specify_anlyte',
         'patient_metabolism__mt_tms_primary_analyte_value',
         'patient_metabolism__mt_gcms',
         'patient_metabolism__mt_gcms_abnormal_specify',
         'patient_metabolism__mt_gcms_abnormal_value',
         'patient_metabolism__mt_orotic_acid',
         'patient_metabolism__mt_vlcfa',
         'patient_metabolism__mt_vlcfa_abnormal_specify',
         'patient_metabolism__mt_succinyl_acetone_status',
         'patient_metabolism__mt_succinyl_acetone_abnormal_specify',
         'patient_metabolism__mt_csf',
         'patient_metabolism__mt_csf_amino_acid',
         'patient_metabolism__mt_csf_glucose',
         'patient_metabolism__mt_csf_lactose',
         'patient_metabolism__mt_csf_protien',
         'patient_metabolism__mt_csf_nurotransonitres',
         'patient_metabolism__mt_csf_porphyrins',
         'patient_metabolism__mt_csf_purine',
         'patient_metabolism__mt_csf_pyrinidies',
         'patient_metabolism__mt_csf_glycine',
         'patient_metabolism__mt_csf_others',
         'patient_metabolism__mt_enzyme_analusis',
         'patient_metabolism__mt_enzyme_analusis_ref_range',
         'patient_metabolism__mt_enzyme_analusis_lab_name',
         'patient_metabolism__mt_enzyme_analusis_normal_control',
         'patient_metabolism__mt_enzyme_analusis_normal_range',
         'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood',
         'patient_metabolism__mt_enzyme_analusis_upload_report',
         'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood_date',
         'patient_metabolism__mt_Causative_DNA_sequence_variat',
         'patient_metabolism__mt_molecular_upload',
         'patient_metabolism__mt_Gene_molecula',
         'patient_metabolism__mt_trans_molecul',
         'patient_metabolism__mt_mul_dna1',
         'patient_metabolism__mt_mul_pro1',
         'patient_metabolism__mt_mul_var1',
         'patient_metabolism__mt_mul_var_cla1',
         'patient_metabolism__mt_mul_zygo1',
         'patient_metabolism__mt_mul_dna2',
         'patient_metabolism__mt_mul_pro2',
         'patient_metabolism__mt_mul_var2',
         'patient_metabolism__mt_mul_var_cla2',
         'patient_metabolism__mt_mul_zygo2',
         'patient_metabolism__mt_mul_seg',
         'patient_metabolism__mt_father',
         'patient_metabolism__mt_mother',
         'patient_metabolism__mt_special_diet',
         'patient_metabolism__mt_dietary_managment_1',
         'patient_metabolism__mt_dietary_managment_2',
         'patient_metabolism__mt_dietary_managment_3',
         'patient_metabolism__mt_dietary_managment_4',
         'patient_metabolism__mt_dietary_managment_type_of_diet_1',
         'patient_metabolism__mt_dietary_managment_type_of_diet_2',
         'patient_metabolism__mt_dietary_managment_type_of_diet_3',
         'patient_metabolism__mt_dietary_managment_type_of_diet_4',
         'patient_metabolism__mt_dietary_managment_type_of_diet_5',
         'patient_metabolism__mt_dietary_managment_type_of_diet_6',
         'patient_metabolism__mt_liver_transplantation',
         'patient_metabolism__mt_kidney_transplantation',
         'patient_metabolism__mt_heart_transplantation',
         'patient_metabolism__mt_lung_transplantation',
         'patient_metabolism__mt_calcium_multivitamin_supplements',
         'patient_metabolism__mt_regular_physiotherapy',
         'patient_metabolism__mt_any_ocular_medication',
         'patient_metabolism__mt_CPAP_BiPAP_sleep_apnea',
         'patient_metabolism__mt_any_other_specify',
         'patient_metabolism__mt_any_other_special_drug',
         'patient_metabolism__mt_any_other_special_drug_1',
         'patient_metabolism__mt_any_other_special_drug_2',
         'patient_metabolism__mt_any_other_special_drug_3',
         'patient_metabolism__mt_any_other_special_drug_4',
         'patient_metabolism__mt_any_other_special_drug_5',
         'patient_metabolism__mt_any_other_special_drug_6',
         'patient_metabolism__mt_any_other_special_drug_7',
         'patient_metabolism__mt_any_other_special_drug_8',
         'patient_metabolism__mt_any_other_special_drug_9',
         'patient_metabolism__mt_any_other_special_drug_10',
         'patient_metabolism__mt_any_other_special_drug_11',
         'patient_metabolism__mt_any_other_special_drug_12',
         'patient_metabolism__mt_any_other_special_drug_13',
         'patient_metabolism__mt_any_other_special_drug_14',
         'patient_metabolism__mt_any_other_special_drug_specify',
         'patient_metabolism__mt_Final_Diagnosis',
         'patient_metabolism__organic_cat',
         'patient_metabolism__organic_cat_other',
         'patient_metabolism__aminoacidpathies_cat',
         'patient_metabolism__aminoacidpathies_cat_BCAA',
         'patient_metabolism__aminoacidpathies_cat_other',
         'patient_metabolism__urea_cat',
         'patient_metabolism__urea_cat_NAGS',
         'patient_metabolism__vitamin_cat',
         'patient_metabolism__vitamin_cobalamin',
         'patient_metabolism__vitamin_folate',
         'patient_metabolism__vitamin_biotin',
         'patient_metabolism__vitamin_pyridoxine',
         'patient_metabolism__vitamin_other',
         'patient_metabolism__fatty_cat',
         'patient_metabolism__fatty_cat_other',
         'patient_metabolism__metal_cat',
         'patient_metabolism__metal_cat_other',
         'patient_metabolism__carbohydrate_cat',
         'patient_metabolism__Carbohydrate_sub3',
         'patient_metabolism__Congenital_disorder',
         'patient_metabolism__Peroxisomal_disorder_specify',
         'patient_metabolism__mitochondrial_cat',
         'patient_metabolism__mitochondrial_nuclear',
         'patient_metabolism__mitochondrial_mitochondrial',
         'patient_metabolism__mitochondrial_other',
         'patient_metabolism__Neurotransmitter_cat',
         'patient_metabolism__Neurotransmitter_pterin',
         'patient_metabolism__Neurotransmitter_tyrosine',
         'patient_metabolism__Neurotransmitter_other',
         'patient_metabolism__mt_diag_other',
         'patient_metabolism__mt_Final_Outcome',
         'patient_metabolism__mt_death_cause',
         'patient_metabolism__mt_age_timedeath',
         'patient_metabolism__mt_filled_by_deo_name',
         'patient_metabolism__mt_clinician_name',
         'patient_metabolism__mt_date_filled',
         ])

    users = profile_metabolism.objects.all().prefetch_related('patient_metabolism').values_list(
        'register_id__institute_name', 'uniqueId', 'mt_icmr_unique_no',
        'mt_final_diagnosis',
        'mt_date_of_records', 'mt_date_of_clinical_exam', 'mt_date_of_birth',
        'mt_patient_name', 'mt_father_name', 'mt_mother_name', 'mt_paitent_id_yes_no',
        'mt_paitent_id', 'mt_patient_id_no', 'mt_father_mother_id', 'mt_mother_father_id_no',
        'mt_permanent_addr', 'mt_state', 'mt_district', 'mt_city_name', 'mt_country_name',
        'mt_land_line_no', 'mt_mother_mobile_no', 'mt_father_mobile_no', 'mt_email',
        'mt_religion', 'mt_religion_other_specify', 'mt_caste', 'mt_caste_other_specify',
        'mt_gender', 'mt_referred_status', 'mt_referred_by', 'mt_referred_by_desc',
        'mt_consent_given', 'mt_consent_upload', 'mt_assent_given', 'mt_assent_upload',
        'mt_hospital_name', 'mt_hospital_reg_no', 'patient_metabolism__mt_patient_edu_status',
        'patient_metabolism__mt_patient_occupation',
        'patient_metabolism__mt_father_edu_status',
        'patient_metabolism__mt_father_occupation',
        'patient_metabolism__mt_mother_edu_status',
        'patient_metabolism__mt_mother_occupation',
        'patient_metabolism__mt_monthly_income_status',
        'patient_metabolism__mt_anthropometry_date',
        'patient_metabolism__mt_anth_wght_pat',
        'patient_metabolism__mt_anth_wght_per',
        'patient_metabolism__mt_anth_wght_sd',
        'patient_metabolism__mt_anth_height_pat',
        'patient_metabolism__mt_anth_height_per',
        'patient_metabolism__mt_anth_height_sd',
        'patient_metabolism__mt_lower_segment_patient',
        'patient_metabolism__mt_lower_segment_percemtile',
        'patient_metabolism__mt_lower_segment_sd',
        'patient_metabolism__mt_lower_us_ls_patient',
        'patient_metabolism__mt_lower_us_ls_percemtile',
        'patient_metabolism__mt_lower_us_ls_sd',
        'patient_metabolism__mt_anth_head_cir_pat',
        'patient_metabolism__mt_anth_head_cir_perc',
        'patient_metabolism__mt_anth_head_cir_sd',
        'patient_metabolism__mt_lower_arm_spam_patient',
        'patient_metabolism__mt_lower_arm_spam_percemtile',
        'patient_metabolism__mt_lower_arm_spam_sd',
        'patient_metabolism__mt_presenting_complaints_years',
        'patient_metabolism__mt_presenting_complaints_months',
        'patient_metabolism__mt_presenting_complaints_day',
        'patient_metabolism__mt_presenting_complaints_intrauterine',
        'patient_metabolism__mt_presenting_complaints_age_presentation_years',
        'patient_metabolism__mt_presenting_complaints_age_presentation_months',
        'patient_metabolism__mt_presenting_complaints_age_presentation_day',
        'patient_metabolism__mt_presenting_complaints_age_presentation_intrauterine',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_years',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_months',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_day',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_intrauterine',
        'patient_metabolism__mt_pedigree_upload',
        'patient_metabolism__mt_fam_hist_status',
        'patient_metabolism__mt_fam_hist_descr',
        'patient_metabolism__mt_cons_status',
        'patient_metabolism__mt_cons_degree_specify',
        'patient_metabolism__mt_Inbreeding',
        'patient_metabolism__mt_Inbreeding_specify_degree',
        'patient_metabolism__mt_Inbreeding_coefficient_degree',
        'patient_metabolism__mt_encephalopathic_presentation',
        'patient_metabolism__mt_encephalopathic_presentation_age_presentaion',
        'patient_metabolism__mt_encephalopathic_presentation_age_diagnosis',
        'patient_metabolism__mt_encephalopathic_presentation_duration',
        'patient_metabolism__mt_Presentation_neonatal_jaundice',
        'patient_metabolism__mt_Presentation_neonatal_jaundice_age_presentation',
        'patient_metabolism__mt_Presentation_neonatal_jaundice_ae_diagnosis',
        'patient_metabolism__mt_Presentation_neonatal_jaundice_duraions',
        'patient_metabolism__mt_Presentation_cardiac_symptoms',
        'patient_metabolism__mt_Presentation_cardiac_symptoms_age_presentation',
        'patient_metabolism__mt_Presentation_cardiac_symptoms_age_diagnosis',
        'patient_metabolism__mt_Presentation_cardiac_symptoms_duration',
        'patient_metabolism__mt_symptoms_after_long_normalcy',
        'patient_metabolism__mt_symptoms_after_long_normalcy_sugar',
        'patient_metabolism__mt_symptoms_after_long_normalcy_fruit_juice',
        'patient_metabolism__mt_symptoms_after_long_normalcy_fasting',
        'patient_metabolism__mt_symptoms_after_long_normalcy_protein_foods',
        'patient_metabolism__mt_symptoms_after_long_normalcy_febrile_illness',
        'patient_metabolism__mt_Presentation_refractory_epilepsy',
        'patient_metabolism__mt_Presentation_refractory_epilepsy_age_presentation',
        'patient_metabolism__mt_Presentation_refractory_epilepsy_age_diagnosis',
        'patient_metabolism__mt_Presentation_refractory_epilepsy_duration',
        'patient_metabolism__mt_mental_retardation_or_dev_delay',
        'patient_metabolism__mt_mental_retardation_Motor',
        'patient_metabolism__mt_mental_retardation_Cognitive',
        'patient_metabolism__mt_mental_retardation_Global',
        'patient_metabolism__mt_Neuroregression',
        'patient_metabolism__mt_Neuroregression_Motor',
        'patient_metabolism__mt_Neuroregression_Cognitive',
        'patient_metabolism__mt_Neuroregression_Global',
        'patient_metabolism__mt_Age_onset_regression',
        'patient_metabolism__mt_Vomiting',
        'patient_metabolism__mt_Aversion_sweet_protein',
        'patient_metabolism__mt_Loose_stools',
        'patient_metabolism__mt_Loose_stools_dropdown',
        'patient_metabolism__mt_Pneumonia',
        'patient_metabolism__mt_Pneumonia_dropdown',
        'patient_metabolism__mt_Fever',
        'patient_metabolism__mt_Fever_dropdown',
        'patient_metabolism__mt_Fever_type',
        'patient_metabolism__mt_Lethargy',
        'patient_metabolism__mt_Behavioral_problems',
        'patient_metabolism__mt_Excessive_crying',
        'patient_metabolism__mt_Decreased_attention_span',
        'patient_metabolism__mt_Speech_disturbances',
        'patient_metabolism__mt_Decline_school_performance',
        'patient_metabolism__mt_Clumsiness',
        'patient_metabolism__mt_Seizures',
        'patient_metabolism__mt_Seizures_Partial',
        'patient_metabolism__mt_Seizures_generalized',
        'patient_metabolism__mt_Seizures_myoclonic',
        'patient_metabolism__mt_Seizures_other',
        'patient_metabolism__mt_Seizures_other_specify',
        'patient_metabolism__mt_Seizures_frequency',
        'patient_metabolism__mt_AntiConvulsant_therapy',
        'patient_metabolism__mt_AntiConvulsant_Monotherapy',
        'patient_metabolism__mt_AntiConvulsant_Monotherapy_drug_name',
        'patient_metabolism__mt_AntiConvulsant_Monotherapy_dose',
        'patient_metabolism__mt_AntiConvulsant_Polytherapy',
        'patient_metabolism__mt_AntiConvulsant_Polytherapy_drug_name',
        'patient_metabolism__mt_AntiConvulsant_Polytherapy_dose',
        'patient_metabolism__mt_HistoryPreviousAdmission',
        'patient_metabolism__mt_history_nuroregression',
        'patient_metabolism__mt_history_nuroregression_text',
        'patient_metabolism__mt_history_diagnosis',
        'patient_metabolism__mt_history_diagnosis_text',
        'patient_metabolism__mt_history_mech_ventilation',
        'patient_metabolism__mt_history_mech_ventilation_text',
        'patient_metabolism__mt_history_mech_distention',
        'patient_metabolism__mt_history_mech_distention_text',
        'patient_metabolism__mt_any_surgery',
        'patient_metabolism__mt_any_surgery_specify',
        'patient_metabolism__mt_History_liver_dysfunction',
        'patient_metabolism__mt_History_liver_dysfunction_trimester_pregnancy',
        'patient_metabolism__mt_Ultrasound',
        'patient_metabolism__mt_Ultrasound_Polyhydramnios',
        'patient_metabolism__mt_Ultrasound_Oligoamnios',
        'patient_metabolism__mt_Ultrasound_Skeletal_anomalies',
        'patient_metabolism__mt_Ultrasound_Hydrops',
        'patient_metabolism__mt_Ultrasound_abnormal_specify',
        'patient_metabolism__mt_Delivery_type',
        'patient_metabolism__mt_Baby_cried_immediately_after_delivery',
        'patient_metabolism__mt_Resuscitation_required',
        'patient_metabolism__mt_NICU_Stay',
        'patient_metabolism__mt_Symptomatic_asymptomatic',
        'patient_metabolism__mt_Shock',
        'patient_metabolism__mt_Shock_catecholamine_sensitive',
        'patient_metabolism__mt_Shock_refractory',
        'patient_metabolism__mt_Ventilation',
        'patient_metabolism__mt_Ventilation_CPAP',
        'patient_metabolism__mt_Ventilation_NIV',
        'patient_metabolism__mt_Ventilation_MV',
        'patient_metabolism__mt_feeding_issues',
        'patient_metabolism__mt_feeding_issues_Regurgitation_oral_feed',
        'patient_metabolism__mt_feeding_issues_NG_feeding',
        'patient_metabolism__mt_feeding_issues_Parenteral',
        'patient_metabolism__mt_Neonatal_hyperbilurubinemia',
        'patient_metabolism__mt_Neonatal_hyperbilurubinemia_direct',
        'patient_metabolism__mt_Neonatal_hyperbilurubinemia_indirect',
        'patient_metabolism__mt_Neonatal_hyperbilurubinemia_total_bill_value',
        'patient_metabolism__mt_Sepsis',
        'patient_metabolism__mt_Sepsis_Organism',
        'patient_metabolism__mt_CRRT_PD_required',
        'patient_metabolism__mt_EEG_natel',
        'patient_metabolism__mt_EEG_BurstSuppressionPattern_natel',
        'patient_metabolism__mt_EEG_Hypsarrythmia_natel',
        'patient_metabolism__mt_EEG_GeneralizedSlowing_natel',
        'patient_metabolism__mt_EEG_Comb_like_pattern_natel',
        'patient_metabolism__mt_facial_dysmorphism',
        'patient_metabolism__mt_Facial_dysmorphism_upload_file',
        'patient_metabolism__mt_Skin_Pigmentation',
        'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_diffuse',
        'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation_patchy',
        'patient_metabolism__mt_Skin_Pigmentation_Hypopigmentation',
        'patient_metabolism__mt_Hirsutism',
        'patient_metabolism__mt_Hirsutism_Facial',
        'patient_metabolism__mt_Hirsutism_generalised',
        'patient_metabolism__mt_Excessive_mongolion_spots',
        'patient_metabolism__mt_Ichthyosis',
        'patient_metabolism__mt_Telengiectasia',
        'patient_metabolism__mt_Edema',
        'patient_metabolism__mt_Hydrops',
        'patient_metabolism__mt_Inverted_nipples',
        'patient_metabolism__mt_fat_distribution_Lipodystrophy',
        'patient_metabolism__mt_Hemoglobinura',
        'patient_metabolism__mt_Encephalopathy',
        'patient_metabolism__mt_Hypotonia',
        'patient_metabolism__mt_Hypertonia',
        'patient_metabolism__mt_Brisk_reflexes',
        'patient_metabolism__mt_Hyporeflexia',
        'patient_metabolism__mt_Opisthotonus',
        'patient_metabolism__mt_Other_Abnormal_Movement',
        'patient_metabolism__mt_Tremor_chorea_athetosis',
        'patient_metabolism__mt_AnyOther_TremorJitteriness',
        'patient_metabolism__mt_AnyOther_chorea',
        'patient_metabolism__mt_AnyOther_athetosis',
        'patient_metabolism__mt_Gait_abnormalities',
        'patient_metabolism__mt_Optic_Nerve_atrophy',
        'patient_metabolism__mt_Retinal_degeneration',
        'patient_metabolism__mt_Cataract',
        'patient_metabolism__mt_Squint',
        'patient_metabolism__mt_Nystagmus_oculogyria',
        'patient_metabolism__mt_Fundus_Abnormal',
        'patient_metabolism__mt_Fundus_Abnormal_specify',
        'patient_metabolism__mt_cheery_red_spot',
        'patient_metabolism__mt_cheery_red_spot_specify',
        'patient_metabolism__mt_Murmur',
        'patient_metabolism__mt_Congestive_Heart_Failure',
        'patient_metabolism__mt_Cardio_myopathy',
        'patient_metabolism__mt_Hepatomegaly',
        'patient_metabolism__mt_Consistency',
        'patient_metabolism__mt_surface',
        'patient_metabolism__mt_margin',
        'patient_metabolism__mt_BCM_size',
        'patient_metabolism__mt_Span_cm',
        'patient_metabolism__mt_Splenomegaly',
        'patient_metabolism__mt_Splenomegaly_size_cm',
        'patient_metabolism__mt_IQ',
        'patient_metabolism__mt_IQ_value',
        'patient_metabolism__mt_DQ',
        'patient_metabolism__mt_DQ_value',
        'patient_metabolism__mt_Any_other_findings',
        'patient_metabolism__mt_Hb_gm_dl',
        'patient_metabolism__mt_wbc_tc_ul',
        'patient_metabolism__mt_wbc_dc_perc',
        'patient_metabolism__mt_Absolut_Neutrophil_count_mm_3',
        'patient_metabolism__mt_Platelet_count_ul',
        'patient_metabolism__mt_Acanthocytes',
        'patient_metabolism__mt_S_calcium_mg_dl',
        'patient_metabolism__mt_S_phosphorous_mg_dl',
        'patient_metabolism__mt_S_alkaline_phosphate_UI',
        'patient_metabolism__mt_S_acid_phosphatase_U_L',
        'patient_metabolism__mt_CPK_U_L_total',
        'patient_metabolism__mt_MM_MB',
        'patient_metabolism__mt_Blood_Urea',
        'patient_metabolism__mt_Blood_creatinine_mg_dl',
        'patient_metabolism__mt_Serum_sodium_meq_l',
        'patient_metabolism__mt_Serum_potassium_meq_l',
        'patient_metabolism__mt_Total_protein_g_dl',
        'patient_metabolism__mt_Serum_albumin_g_dl',
        'patient_metabolism__mt_SGPT_IU_L',
        'patient_metabolism__mt_SGOT_IU_L',
        'patient_metabolism__mt_PT_sec',
        'patient_metabolism__mt_APTT_sec',
        'patient_metabolism__mt_TSB_mg_dl',
        'patient_metabolism__mt_DSB_mg_dl',
        'patient_metabolism__mt_IRON_IU_L',
        'patient_metabolism__mt_TIBC_IU_L',
        'patient_metabolism__mt_Lactate_mmol_l',
        'patient_metabolism__mt_Uric_acid_mg_dl',
        'patient_metabolism__mt_Blood_sugar_mg_dl',
        'patient_metabolism__mt_HbA1C_per',
        'patient_metabolism__mt_Total_Cholesterol_mg_dl',
        'patient_metabolism__mt_TGs_mg_dl',
        'patient_metabolism__mt_HDL_mg_dl',
        'patient_metabolism__mt_LDL_mg_dl',
        'patient_metabolism__mt_VLDL_mg_dl',
        'patient_metabolism__mt_Homocysteine_uml_l',
        'patient_metabolism__mt_Prolactin_ng_ml',
        'patient_metabolism__mt_Ultrasonography',
        'patient_metabolism__mt_Ultrasonography_abnormal_Liver',
        'patient_metabolism__mt_Ultrasonography_abnormal_Kidney',
        'patient_metabolism__mt_Ultrasonography_abnormal_Spleen',
        'patient_metabolism__mt_Ultrasonography_abnormal_AnyAdenoma',
        'patient_metabolism__mt_Ultrasonography_abnormal_RenalCysts',
        'patient_metabolism__mt_Skeletal_survey',
        'patient_metabolism__mt_Skeletal_survey_Rickets',
        'patient_metabolism__mt_Skeletal_survey_DysostosisMultiplex',
        'patient_metabolism__mt_Skeletal_survey_ShortLimbs',
        'patient_metabolism__mt_Skeletal_survey_SpineAbnormalities',
        'patient_metabolism__mt_Skeletal_survey_ChondrodyplasiaPuncta',
        'patient_metabolism__mt_ctc_scan',
        'patient_metabolism__mt_ctc_scan_ThalamusHypointesity',
        'patient_metabolism__mt_ctc_scan_calcification',
        'patient_metabolism__mt_ctc_scan_ventriculomegaly',
        'patient_metabolism__mt_ctc_scan_cerebralAtrophy',
        'patient_metabolism__mt_ctc_scan_infarct',
        'patient_metabolism__mt_ctc_scan_hemorrhage',
        'patient_metabolism__mt_ctc_scan_cerebraledema',
        'patient_metabolism__mt_ctc_scan_cysts',
        'patient_metabolism__mt_mri_brain_status',
        'patient_metabolism__mt_mri_brain_corticalAtrophy',
        'patient_metabolism__mt_mri_brain_cerebellarAtrophy',
        'patient_metabolism__mt_mri_brain_ventriculomegaly',
        'patient_metabolism__mt_mri_brain_basalGangliaHypo',
        'patient_metabolism__mt_mri_brain_hyperintensity',
        'patient_metabolism__mt_mri_brain_deepGrayMatterHyperintensity',
        'patient_metabolism__mt_mri_brain_thalamicHypo',
        'patient_metabolism__mt_mri_brain_demyelinationDysmyelination',
        'patient_metabolism__mt_mri_brain_cerebralEdema',
        'patient_metabolism__mt_mri_brain_cysts',
        'patient_metabolism__mt_mri_brain_infarct',
        'patient_metabolism__mt_mri_brain_hemorrhage',
        'patient_metabolism__mt_mri_brain_other',
        'patient_metabolism__mt_mrs_done',
        'patient_metabolism__mt_mrs_LactatePeak',
        'patient_metabolism__mt_mrs_NAAPeak',
        'patient_metabolism__mt_mrs_LowCreatininePeak',
        'patient_metabolism__mt_mrs_CholinePeak',
        'patient_metabolism__mt_echocardiography',
        'patient_metabolism__mt_echocardiography_DialtedCardiomyopathy',
        'patient_metabolism__mt_echocardiography_hypertrophicCardiomyopathy',
        'patient_metabolism__mt_echocardiography_valvularAbnormality',
        'patient_metabolism__mt_echocardiography_structuralDefects',
        'patient_metabolism__mt_echocardiography_SpecifyStructuralDefect',
        'patient_metabolism__mt_echocardiography_EjectionFraction',
        'patient_metabolism__mt_eeg',
        'patient_metabolism__mt_eeg_BurstSuppressionPattern',
        'patient_metabolism__mt_eeg_Hypsarrythmia',
        'patient_metabolism__mt_eeg_GeneralizedSlowing',
        'patient_metabolism__mt_eeg_CombLikePattern',
        'patient_metabolism__mt_ocular_examination_slit',
        'patient_metabolism__mt_veps',
        'patient_metabolism__mt_veps_abnormal_latency',
        'patient_metabolism__mt_erg',
        'patient_metabolism__mt_erg_abnormal_specify',
        'patient_metabolism__mt_OAE_BERA',
        'patient_metabolism__mt_OAE_BERA_Unilateral',
        'patient_metabolism__mt_OAE_BERA_bilateral',
        'patient_metabolism__mt_OAE_BERA_mild',
        'patient_metabolism__mt_OAE_BERA_moderate',
        'patient_metabolism__mt_OAE_BERA_severe',
        'patient_metabolism__mt_OAE_BERA_profoundHearingLoss',
        'patient_metabolism__mt_nerve_conduction_study',
        'patient_metabolism__mt_nerve_conduction_study_motor',
        'patient_metabolism__mt_nerve_conduction_study_sensory',
        'patient_metabolism__mt_nerve_conduction_study_mixed',
        'patient_metabolism__mt_nerve_conduction_study_upperLimb',
        'patient_metabolism__mt_nerve_conduction_study_lowerLimb',
        'patient_metabolism__mt_nerve_conduction_study_reducedMUAPAmplitude',
        'patient_metabolism__mt_nerve_conduction_study_shortMUAPDuration',
        'patient_metabolism__mt_nerve_conduction_study_decreasedConductionVelocity',
        'patient_metabolism__mt_nerve_conduction_study_increasedDistalLatency',
        'patient_metabolism__mt_nerve_conduction_study_decreasedSNAP',
        'patient_metabolism__mt_nerve_conduction_study_increasedFwaveLatency',
        'patient_metabolism__mt_muscle_biopsy',
        'patient_metabolism__mt_Any_other_investigations',
        'patient_metabolism__mt_blood_gas_metabolism_acidosis',
        'patient_metabolism__mt_blood_gas_metabolism_acidosis_PH',
        'patient_metabolism__mt_blood_gas_metabolism_acidosis_HCO_3',
        'patient_metabolism__mt_blood_gas_metabolism_acidosis_Anion_gap',
        'patient_metabolism__mt_metabolic_alkalosis',
        'patient_metabolism__mt_Hyper_ammonemia',
        'patient_metabolism__mt_Hyper_ammonemia_value',
        'patient_metabolism__mt_Hyper_ammonemia_duration',
        'patient_metabolism__mt_high_lactate',
        'patient_metabolism__mt_high_lactate_value',
        'patient_metabolism__mt_high_lactate_csf',
        'patient_metabolism__mt_high_lactate_csf_value',
        'patient_metabolism__mt_ief_transferring_pattern_type',
        'patient_metabolism__mt_ief_transferring_pattern_type_tpye1',
        'patient_metabolism__mt_ief_transferring_pattern_type_tpye2',
        'patient_metabolism__mt_urine_ketones',
        'patient_metabolism__mt_urine_ketones_value',
        'patient_metabolism__mt_plasma_ketones',
        'patient_metabolism__mt_plasma_ketones_value',
        'patient_metabolism__mt_plasma_ketones_ffa_ratio',
        'patient_metabolism__mt_plasma_ketones_ffa_ratio_value',
        'patient_metabolism__mt_hplc',
        'patient_metabolism__mt_hplc_specify',
        'patient_metabolism__mt_hplc_value',
        'patient_metabolism__mt_tms_primary_analyte',
        'patient_metabolism__mt_tms_primary_analyte_specify_anlyte',
        'patient_metabolism__mt_tms_primary_analyte_value',
        'patient_metabolism__mt_gcms',
        'patient_metabolism__mt_gcms_abnormal_specify',
        'patient_metabolism__mt_gcms_abnormal_value',
        'patient_metabolism__mt_orotic_acid',
        'patient_metabolism__mt_vlcfa',
        'patient_metabolism__mt_vlcfa_abnormal_specify',
        'patient_metabolism__mt_succinyl_acetone_status',
        'patient_metabolism__mt_succinyl_acetone_abnormal_specify',
        'patient_metabolism__mt_csf',
        'patient_metabolism__mt_csf_amino_acid',
        'patient_metabolism__mt_csf_glucose',
        'patient_metabolism__mt_csf_lactose',
        'patient_metabolism__mt_csf_protien',
        'patient_metabolism__mt_csf_nurotransonitres',
        'patient_metabolism__mt_csf_porphyrins',
        'patient_metabolism__mt_csf_purine',
        'patient_metabolism__mt_csf_pyrinidies',
        'patient_metabolism__mt_csf_glycine',
        'patient_metabolism__mt_csf_others',
        'patient_metabolism__mt_enzyme_analusis',
        'patient_metabolism__mt_enzyme_analusis_ref_range',
        'patient_metabolism__mt_enzyme_analusis_lab_name',
        'patient_metabolism__mt_enzyme_analusis_normal_control',
        'patient_metabolism__mt_enzyme_analusis_normal_range',
        'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood',
        'patient_metabolism__mt_enzyme_analusis_upload_report',
        'patient_metabolism__mt_enzyme_analusis_sample_dbs_blood_date',
        'patient_metabolism__mt_Causative_DNA_sequence_variat',
        'patient_metabolism__mt_molecular_upload',
        'patient_metabolism__mt_Gene_molecula',
        'patient_metabolism__mt_trans_molecul',
        'patient_metabolism__mt_mul_dna1',
        'patient_metabolism__mt_mul_pro1',
        'patient_metabolism__mt_mul_var1',
        'patient_metabolism__mt_mul_var_cla1',
        'patient_metabolism__mt_mul_zygo1',
        'patient_metabolism__mt_mul_dna2',
        'patient_metabolism__mt_mul_pro2',
        'patient_metabolism__mt_mul_var2',
        'patient_metabolism__mt_mul_var_cla2',
        'patient_metabolism__mt_mul_zygo2',
        'patient_metabolism__mt_mul_seg',
        'patient_metabolism__mt_father',
        'patient_metabolism__mt_mother',
        'patient_metabolism__mt_special_diet',
        'patient_metabolism__mt_dietary_managment_1',
        'patient_metabolism__mt_dietary_managment_2',
        'patient_metabolism__mt_dietary_managment_3',
        'patient_metabolism__mt_dietary_managment_4',
        'patient_metabolism__mt_dietary_managment_type_of_diet_1',
        'patient_metabolism__mt_dietary_managment_type_of_diet_2',
        'patient_metabolism__mt_dietary_managment_type_of_diet_3',
        'patient_metabolism__mt_dietary_managment_type_of_diet_4',
        'patient_metabolism__mt_dietary_managment_type_of_diet_5',
        'patient_metabolism__mt_dietary_managment_type_of_diet_6',
        'patient_metabolism__mt_liver_transplantation',
        'patient_metabolism__mt_kidney_transplantation',
        'patient_metabolism__mt_heart_transplantation',
        'patient_metabolism__mt_lung_transplantation',
        'patient_metabolism__mt_calcium_multivitamin_supplements',
        'patient_metabolism__mt_regular_physiotherapy',
        'patient_metabolism__mt_any_ocular_medication',
        'patient_metabolism__mt_CPAP_BiPAP_sleep_apnea',
        'patient_metabolism__mt_any_other_specify',
        'patient_metabolism__mt_any_other_special_drug',
        'patient_metabolism__mt_any_other_special_drug_1',
        'patient_metabolism__mt_any_other_special_drug_2',
        'patient_metabolism__mt_any_other_special_drug_3',
        'patient_metabolism__mt_any_other_special_drug_4',
        'patient_metabolism__mt_any_other_special_drug_5',
        'patient_metabolism__mt_any_other_special_drug_6',
        'patient_metabolism__mt_any_other_special_drug_7',
        'patient_metabolism__mt_any_other_special_drug_8',
        'patient_metabolism__mt_any_other_special_drug_9',
        'patient_metabolism__mt_any_other_special_drug_10',
        'patient_metabolism__mt_any_other_special_drug_11',
        'patient_metabolism__mt_any_other_special_drug_12',
        'patient_metabolism__mt_any_other_special_drug_13',
        'patient_metabolism__mt_any_other_special_drug_14',
        'patient_metabolism__mt_any_other_special_drug_specify',
        'patient_metabolism__mt_Final_Diagnosis',
        'patient_metabolism__organic_cat',
        'patient_metabolism__organic_cat_other',
        'patient_metabolism__aminoacidpathies_cat',
        'patient_metabolism__aminoacidpathies_cat_BCAA',
        'patient_metabolism__aminoacidpathies_cat_other',
        'patient_metabolism__urea_cat',
        'patient_metabolism__urea_cat_NAGS',
        'patient_metabolism__vitamin_cat',
        'patient_metabolism__vitamin_cobalamin',
        'patient_metabolism__vitamin_folate',
        'patient_metabolism__vitamin_biotin',
        'patient_metabolism__vitamin_pyridoxine',
        'patient_metabolism__vitamin_other',
        'patient_metabolism__fatty_cat',
        'patient_metabolism__fatty_cat_other',
        'patient_metabolism__metal_cat',
        'patient_metabolism__metal_cat_other',
        'patient_metabolism__carbohydrate_cat',
        'patient_metabolism__Carbohydrate_sub3',
        'patient_metabolism__Congenital_disorder',
        'patient_metabolism__Peroxisomal_disorder_specify',
        'patient_metabolism__mitochondrial_cat',
        'patient_metabolism__mitochondrial_nuclear',
        'patient_metabolism__mitochondrial_mitochondrial',
        'patient_metabolism__mitochondrial_other',
        'patient_metabolism__Neurotransmitter_cat',
        'patient_metabolism__Neurotransmitter_pterin',
        'patient_metabolism__Neurotransmitter_tyrosine',
        'patient_metabolism__Neurotransmitter_other',
        'patient_metabolism__mt_diag_other',
        'patient_metabolism__mt_Final_Outcome',
        'patient_metabolism__mt_death_cause',
        'patient_metabolism__mt_age_timedeath',
        'patient_metabolism__mt_filled_by_deo_name',
        'patient_metabolism__mt_clinician_name',
        'patient_metabolism__mt_date_filled',
        )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_iem_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iem_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result', 'quality_reason', 'UniqueId', 'unique_no',
         'mt_anth_wght_pat',
         'mt_anth_wght_per',
         'mt_anth_wght_sd',
         'mt_anth_height_pat',
         'mt_anth_height_per',
         'mt_anth_height_sd',
         'mt_lower_segment_patient',
         'mt_lower_segment_percemtile',
         'mt_lower_segment_sd',
         'mt_lower_us_ls_patient',
         'mt_lower_us_ls_percemtile',
         'mt_lower_us_ls_sd',
         'mt_anth_head_cir_pat',
         'mt_anth_head_cir_perc',
         'mt_anth_head_cir_sd',
         'mt_lower_arm_spam_patient',
         'mt_lower_arm_spam_percemtile',
         'mt_lower_arm_spam_sd',
         'mt_presenting_complaints_years',
         'mt_presenting_complaints_months',
         'mt_presenting_complaints_day',
         'mt_presenting_complaints_intrauterine',
         'mt_presenting_complaints_age_presentation_years',
         'mt_presenting_complaints_age_presentation_months',
         'mt_presenting_complaints_age_presentation_day',
         'mt_presenting_complaints_age_presentation_intrauterine',
         'mt_presenting_complaints_age_diagnosis_years',
         'mt_presenting_complaints_age_diagnosis_months',
         'mt_presenting_complaints_age_diagnosis_day',
         'mt_presenting_complaints_age_diagnosis_intrauterine',
         'mt_fam_hist_status',
         'mt_encephalopathic_presentation',
         'mt_Presentation_neonatal_jaundice',
         'mt_Presentation_refractory_epilepsy',
         'mt_mental_retardation_or_dev_delay',
         'mt_Seizures',
         'mt_CRRT_PD_required',
         'mt_Encephalopathy',
         'mt_Lactate_mmol_l',
         'mt_Homocysteine_uml_l',
         'mt_ctc_scan',
         'mt_mri_brain_status',
         'mt_mrs_done',
         'mt_echocardiography',
         'mt_eeg',
         'mt_blood_gas_metabolism_acidosis',
         'mt_Hyper_ammonemia',
         'mt_high_lactate',
         'mt_urine_ketones',
         'mt_tms_primary_analyte',
         'mt_gcms',
         'mt_Causative_DNA_sequence_variat',
         'mt_mul_dna1',
         'mt_special_diet',
         'mt_Final_Diagnosis',
         'mt_Final_Outcome', ])

    users = profile_metabolism.objects.all().prefetch_related('patient_metabolism').values_list(
        'register_id__institute_name', 'quality_result', 'quality_reason', 'uniqueId', 'mt_icmr_unique_no',
        'patient_metabolism__mt_anth_wght_pat',
        'patient_metabolism__mt_anth_wght_per',
        'patient_metabolism__mt_anth_wght_sd',
        'patient_metabolism__mt_anth_height_pat',
        'patient_metabolism__mt_anth_height_per',
        'patient_metabolism__mt_anth_height_sd',
        'patient_metabolism__mt_lower_segment_patient',
        'patient_metabolism__mt_lower_segment_percemtile',
        'patient_metabolism__mt_lower_segment_sd',
        'patient_metabolism__mt_lower_us_ls_patient',
        'patient_metabolism__mt_lower_us_ls_percemtile',
        'patient_metabolism__mt_lower_us_ls_sd',
        'patient_metabolism__mt_anth_head_cir_pat',
        'patient_metabolism__mt_anth_head_cir_perc',
        'patient_metabolism__mt_anth_head_cir_sd',
        'patient_metabolism__mt_lower_arm_spam_patient',
        'patient_metabolism__mt_lower_arm_spam_percemtile',
        'patient_metabolism__mt_lower_arm_spam_sd',
        'patient_metabolism__mt_presenting_complaints_years',
        'patient_metabolism__mt_presenting_complaints_months',
        'patient_metabolism__mt_presenting_complaints_day',
        'patient_metabolism__mt_presenting_complaints_intrauterine',
        'patient_metabolism__mt_presenting_complaints_age_presentation_years',
        'patient_metabolism__mt_presenting_complaints_age_presentation_months',
        'patient_metabolism__mt_presenting_complaints_age_presentation_day',
        'patient_metabolism__mt_presenting_complaints_age_presentation_intrauterine',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_years',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_months',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_day',
        'patient_metabolism__mt_presenting_complaints_age_diagnosis_intrauterine',
        'patient_metabolism__mt_fam_hist_status',
        'patient_metabolism__mt_encephalopathic_presentation',
        'patient_metabolism__mt_Presentation_neonatal_jaundice',
        'patient_metabolism__mt_Presentation_refractory_epilepsy',
        'patient_metabolism__mt_mental_retardation_or_dev_delay',
        'patient_metabolism__mt_Seizures',
        'patient_metabolism__mt_CRRT_PD_required',
        'patient_metabolism__mt_Encephalopathy',
        'patient_metabolism__mt_Lactate_mmol_l',
        'patient_metabolism__mt_Homocysteine_uml_l',
        'patient_metabolism__mt_ctc_scan',
        'patient_metabolism__mt_mri_brain_status',
        'patient_metabolism__mt_mrs_done',
        'patient_metabolism__mt_echocardiography',
        'patient_metabolism__mt_eeg',
        'patient_metabolism__mt_blood_gas_metabolism_acidosis',
        'patient_metabolism__mt_Hyper_ammonemia',
        'patient_metabolism__mt_high_lactate',
        'patient_metabolism__mt_urine_ketones',
        'patient_metabolism__mt_tms_primary_analyte',
        'patient_metabolism__mt_gcms',
        'patient_metabolism__mt_Causative_DNA_sequence_variat',
        'patient_metabolism__mt_mul_dna1',
        'patient_metabolism__mt_special_diet',
        'patient_metabolism__mt_Final_Diagnosis',
        'patient_metabolism__mt_Final_Outcome', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_pompe_csv(request):
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
         'patient_pompe__pd_Enzyme_analysis_done', 'patient_pompe__pd_Sample_date_done','patient_pompe__pd_patien',
         'patient_pompe__pd_contro','patient_pompe__pd_nor_ran',
         'patient_pompe__pd_CRIM_Status',
         'patient_pompe__pd_Enzyme_analysis_uploaded','patient_pompe__pd_Causative_DNA_sequence_variat',
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

    users = profile_pompe.objects.all().prefetch_related('patient_pompe').values_list('register_id__institute_name', 'uniqueId', 'pmp_icmr_unique_no', 'pmp_final_diagnosis',
                                                                                      'pmp_date_of_records', 'pmp_date_of_clinical_exam', 'pmp_date_of_birth',
                                                                                      'pmp_patient_name', 'pmp_father_name', 'pmp_mother_name', 'pmp_paitent_id_yes_no',
                                                                                      'pmp_paitent_id', 'pmp_patient_id_no', 'pmp_father_mother_id', 'pmp_father_mother_id_no',
                                                                                      'pmp_permanent_addr', 'pmp_state', 'pmp_district', 'pmp_city_name', 'pmp_country_name',
                                                                                      'pmp_land_line_no', 'pmp_mother_mobile_no', 'pmp_father_mobile_no', 'pmp_email',
                                                                                      'pmp_religion', 'pmp_caste', 'pmp_gender', 'pmp_referred_status', 'pmp_referred_by',
                                                                                      'pmp_referred_by_desc', 'pmp_consent_given', 'pmp_consent_upload', 'pmp_assent_given',
                                                                                      'pmp_assent_upload', 'pmp_hospital_name', 'pmp_hospital_reg_no', 'patient_pompe__pd_Patient_education',
                                                                                      'patient_pompe__pd_Patient_occupation', 'patient_pompe__pd_Father_education', 'patient_pompe__pd_Father_occupation',
                                                                                      'patient_pompe__pd_Mother_education', 'patient_pompe__pd_Mother_occupation',
                                                                                      'patient_pompe__pd_Monthly_family_income', 'patient_pompe__pd_weight_patient', 'patient_pompe__pd_weight_percentile',
                                                                                      'patient_pompe__pd_weight_SD', 'patient_pompe__pd_height_patient', 'patient_pompe__pd_height_percentile',
                                                                                      'patient_pompe__pd_height_SD', 'patient_pompe__pd_Head_circumference_patient', 'patient_pompe__pd_Head_circumference_percentile',
                                                                                      'patient_pompe__pd_Head_circumference_sd',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_year', 'patient_pompe__pd_Age_at_onset_of_symptoms_month',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_day',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_Intrauterine', 'patient_pompe__pd_Age_at_presentation_year',
                                                                                      'patient_pompe__pd_Age_at_presentation_month',
                                                                                      'patient_pompe__pd_Age_at_presentation_day', 'patient_pompe__pd_Age_at_presentation_Intrauterine',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_year', 'patient_pompe__pd_Age_at_diagnosis_month',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_day', 'patient_pompe__pd_Age_at_diagnosis_Intrauterine',
                                                                                      'patient_pompe__pd_Pedigree_to_be_uploaded', 'patient_pompe__pd_positive_family_history',
                                                                                      'patient_pompe__pd_family_history_specify', 'patient_pompe__pd_Consanguinity', 'patient_pompe__pd_Consanguinity_specify',
                                                                                      'patient_pompe__pd_Ultrasound_findings', 'patient_pompe__pd_Polyhydramnios',
                                                                                      'patient_pompe__pd_Fetal_echocardiography', 'patient_pompe__pd_Natal_History_Type_of_delivery',
                                                                                      'patient_pompe__pd_Natal_History_Baby_cried_immediately_after_delivery',
                                                                                      'patient_pompe__pd_Natal_History_Resuscitation_required', 'patient_pompe__pd_Natal_History_ventilater',
                                                                                      'patient_pompe__pd_Natal_History_o_2_Cpap',
                                                                                      'patient_pompe__pd_Natal_History_Nursery_stay', 'patient_pompe__pd_Birth_weight', 'patient_pompe__pd_Development_milestones',
                                                                                      'patient_pompe__pd_if_delayed_Motor', 'patient_pompe__pd_if_delayed_Global',
                                                                                      'patient_pompe__pd_if_delayed_Cognitive', 'patient_pompe__pd_head', 'patient_pompe__pd_face', 'patient_pompe__pd_Eyes_Ptosis',
                                                                                      'patient_pompe__pd_Large_tongue', 'patient_pompe__pd_Others_specify',
                                                                                      'patient_pompe__pd_Ever_had_respiratory_distress', 'patient_pompe__pd_No_of_episode',
                                                                                      'patient_pompe__pd_Ventilator_or_other_respiratory_support', 'patient_pompe__pd_Mode_of_ventilation',
                                                                                      'patient_pompe__pd_Age_at_ventilator', 'patient_pompe__pd_Tracheostomy', 'patient_pompe__pd_Was_weaning_off_from_ventilator_possible',
                                                                                      'patient_pompe__pd_Feeding_difficulties', 'patient_pompe__pd_Feeding',
                                                                                       'patient_pompe__pd_Protuberantabdomen', 'patient_pompe__pd_Hepatomegaly',
                                                                                      'patient_pompe__pd_Size_BCM', 'patient_pompe__pd_Span', 'patient_pompe__pd_Hernia', 'patient_pompe__pd_Others',
                                                                                      'patient_pompe__pd_Edema',
                                                                                      'patient_pompe__pd_Cyanosis', 'patient_pompe__pd_Cardiac_medications_date_started', 'patient_pompe__pd_Cardiac_medications_dose',
                                                                                      'patient_pompe__pd_Heart_rate', 'patient_pompe__pd_Gallop', 'patient_pompe__pd_arrythmia',
                                                                                      'patient_pompe__pd_Muscle_weakness', 'patient_pompe__pd_Age_at_Onset_of_weakness', 'patient_pompe__pd_Onset_of_weakness',
                                                                                      'patient_pompe__pd_Difficulty_in_sitting_from_lying_position',
                                                                                      'patient_pompe__pd_Difficulty_in_standing_from_standing_position', 'patient_pompe__pd_Wheelchair_bound',
                                                                                      'patient_pompe__pd_Age_at_Wheelchair_bound',
                                                                                      'patient_pompe__pd_Sleep_disturbances_apnea', 'patient_pompe__pd_Hypotonia',
                                                                                      'patient_pompe__pd_Proximal_muscle_weakness_in_upper_extremities',
                                                                                      'patient_pompe__pd_Distal_muscle_weakness_in_upper_extremities', 'patient_pompe__pd_Proximal_muscle_weakness_in_lower_extremities',
                                                                                      'patient_pompe__pd_Distal_muscle_weakness_in_lower_extremities', 'patient_pompe__pd_Neck_muscle_weakness',
                                                                                      'patient_pompe__pd_Muscle_weakness_in_trunk', 'patient_pompe__pd_Reflexes',
                                                                                      'patient_pompe__pd_Gower_positive', 'patient_pompe__pd_Contractures', 'patient_pompe__pd_Abnormal_Gait',
                                                                                      'patient_pompe__pd_Muscles_of_respiration_involved', 'patient_pompe__pd_bulbar_and_lingual_weakness',
                                                                                      'patient_pompe__pd_if_yes', 'patient_pompe__pd_Rigid_spine', 'patient_pompe__pd_Higher_mental_functions',
                                                                                      'patient_pompe__pd_Cranial_nerve_involvement', 'patient_pompe__pd_Altered_or_reduced_visual_acuity',
                                                                                      'patient_pompe__pd_Hearing_loss', 'patient_pompe__pd_Foot_drop', 'patient_pompe__pd_Radiography_of_chest_to_assess_for_cardiomegaly',
                                                                                      'patient_pompe__pd_ECG', 'patient_pompe__pd_Short_PR',
                                                                                      'patient_pompe__pd_Tall_broad_QRS', 'patient_pompe__pd_ECHO_date', 'patient_pompe__pd_ECHO', 'patient_pompe__pd_PFT_date',
                                                                                      'patient_pompe__pd_PFT', 'patient_pompe__pd_ECHO_specify', 'patient_pompe__pd_PFT_Supine_FVC', 'patient_pompe__pd_PFT_Sitting_FVC',
                                                                                      'patient_pompe__pd_PFT_Supine_FEV1', 'patient_pompe__pd_PFT_Sitting_FEV1', 'patient_pompe__pd_PFT_Mean_Inspiratory_Pressure',
                                                                                      'patient_pompe__pd_PFT_Mean_Expiratory_Pressure',
                                                                                      'patient_pompe__pd_Swallow_study', 'patient_pompe__pd_Swallow_study_specify', 'patient_pompe__pd_CK', 'patient_pompe__pd_CK_MB',
                                                                                      'patient_pompe__pd_AST', 'patient_pompe__pd_ALT', 'patient_pompe__pd_LDH',
                                                                                      'patient_pompe__pd_Enzyme_analysis_done', 'patient_pompe__pd_Sample_date_done',
                                                                                      'patient_pompe__pd_patien',
                                                                                      'patient_pompe__pd_contro',
                                                                                      'patient_pompe__pd_nor_ran',
                                                                                      'patient_pompe__pd_CRIM_Status',
                                                                                      'patient_pompe__pd_Enzyme_analysis_uploaded','patient_pompe__pd_Causative_DNA_sequence_variat',
                                                                                      'patient_pompe__pd_molecular_upload','patient_pompe__pd_Patient_molecular','patient_pompe__pd_Gene_molecula',
                                                                                      'patient_pompe__pd_trans_molecul','patient_pompe__pd_mul_dna1','patient_pompe__pd_mul_pro1',
                                                                                      'patient_pompe__pd_mul_var1','patient_pompe__pd_mul_zygo1',
                                                                                      'patient_pompe__pd_mul_var_cla1',
                                                                                      'patient_pompe__pd_mul_dna2',
                                                                                      'patient_pompe__pd_mul_pro2',
                                                                                      'patient_pompe__pd_mul_var2',
                                                                                      'patient_pompe__pd_mul_zygo2',

                                                                                      'patient_pompe__pd_mul_var_cla2',
                                                                                      'patient_pompe__pd_mul_seg','patient_pompe__pd_father','patient_pompe__pd_mother',
                                                                                      'patient_pompe__pd_ERT','patient_pompe__pd_name_of_com', 'patient_pompe__pd_ERT_enz', 'patient_pompe__pd_Date_Initiation',
                                                                                      'patient_pompe__pd_Age_of_Start', 'patient_pompe__pd_Dosage', 'patient_pompe__pd_Duration',
                                                                                      'patient_pompe__pd_Adverse_events', 'patient_pompe__pd_Adverse_events_specify', 'patient_pompe__pd_Response',
                                                                                      'patient_pompe__pd_Immunomodulation','patient_pompe__pd_Immunomodulation_methotrexate','patient_pompe__pd_Immunomodulation_rituximab',
                                                                                      'patient_pompe__pd_Immunomodulation_ivig',
                                                                                      'patient_pompe__pd_Current_ERT_Status', 'patient_pompe__pd_Ongoing','patient_pompe__pd_moto_sca', 'patient_pompe__pd_Any_interruption',
                                                                                      'patient_pompe__pd_Reason_for_interruption', 'patient_pompe__pd_Duration_of_interruption',
                                                                                      'patient_pompe__pd_Physiotherapy_date','patient_pompe__pd_moto_qmft','patient_pompe__pd_moto_gsgc',
                                                                                      'patient_pompe__pd_moto_wlk_ts',
                                                                                      'patient_pompe__pd_Finaldiagnosis','patient_pompe__pd_Finaloutcomes',
                                                                                      'patient_pompe__pd_filed_by_DEO_name', 'patient_pompe__pd_clinician_name',
                                                                                      'patient_pompe__pd_filled_date', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_pompe_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pompe_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'pmp_final_diagnosis', 'pmp_date_of_records', 'pmp_date_of_clinical_exam',
         'pd_weight_patient',
         'pd_weight_percentile', 'pd_weight_SD', 'pd_height_patient',
         'pd_height_percentile',
         'pd_height_SD', 'pd_Head_circumference_patient',
         'pd_Head_circumference_percentile', 'pd_Head_circumference_sd',
         'pd_Age_at_onset_of_symptoms_year', 'pd_Age_at_onset_of_symptoms_month', 'pd_Age_at_onset_of_symptoms_day', 'pd_Age_at_onset_of_symptoms_Intrauterine', 'pd_Age_at_presentation_year',
         'pd_Age_at_presentation_month', 'pd_Age_at_presentation_day', 'pd_Age_at_presentation_Intrauterine', 'pd_Age_at_diagnosis_year', 'pd_Age_at_diagnosis_month', 'pd_Age_at_diagnosis_day',
         'pd_Age_at_diagnosis_Intrauterine', 'pd_positive_family_history', 'pd_Ever_had_respiratory_distress', 'pd_Muscle_weakness', 'pd_ECHO',  'pd_PFT','pd_patien','pd_mul_dna1',

         'pd_Enzyme_analysis_done',  'pd_ERT','pd_Finaldiagnosis','pd_Finaloutcomes', ])

    users = profile_pompe.objects.all().prefetch_related('patient_pompe').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'pmp_icmr_unique_no', 'pmp_final_diagnosis',
                                                                                      'pmp_date_of_records', 'pmp_date_of_clinical_exam',
                                                                                      'patient_pompe__pd_weight_patient',
                                                                                      'patient_pompe__pd_weight_percentile',
                                                                                      'patient_pompe__pd_weight_SD',
                                                                                      'patient_pompe__pd_height_patient',
                                                                                      'patient_pompe__pd_height_percentile',
                                                                                      'patient_pompe__pd_height_SD',
                                                                                      'patient_pompe__pd_Head_circumference_patient',
                                                                                      'patient_pompe__pd_Head_circumference_percentile',
                                                                                      'patient_pompe__pd_Head_circumference_sd',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_year', 'patient_pompe__pd_Age_at_onset_of_symptoms_month',
                                                                                      'patient_pompe__pd_Age_at_onset_of_symptoms_day', 'patient_pompe__pd_Age_at_onset_of_symptoms_Intrauterine',
                                                                                      'patient_pompe__pd_Age_at_presentation_year', 'patient_pompe__pd_Age_at_presentation_month',
                                                                                      'patient_pompe__pd_Age_at_presentation_day', 'patient_pompe__pd_Age_at_presentation_Intrauterine',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_year', 'patient_pompe__pd_Age_at_diagnosis_month', 'patient_pompe__pd_Age_at_diagnosis_day',
                                                                                      'patient_pompe__pd_Age_at_diagnosis_Intrauterine', 'patient_pompe__pd_positive_family_history',
                                                                                      'patient_pompe__pd_Ever_had_respiratory_distress', 'patient_pompe__pd_Muscle_weakness', 'patient_pompe__pd_ECHO',
                                                                                      'patient_pompe__pd_PFT',
                                                                                      'patient_pompe__pd_patien',
                                                                                      'patient_pompe__pd_mul_dna1',
                                                                                      'patient_pompe__pd_Enzyme_analysis_done', 'patient_pompe__pd_ERT',
                                                                                      'patient_pompe__pd_Finaldiagnosis','patient_pompe__pd_Finaloutcomes',)
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_storage_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="storage.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_storage__sd_final_diagnosis',
         'patient_storage__sd_date_of_records', 'patient_storage__sd_date_of_clinical_exam',
         'patient_storage__sd_date_of_birth',
         'patient_storage__sd_Patient_name', 'patient_storage__sd_Father_name',
         'patient_storage__sd_Mother_name',
         'patient_storage__sd_paitent_id_yes_no', 'patient_storage__sd_paitent_id', 'patient_storage__sd_patient_id_no',
         'patient_storage__sd_Father_mother_id', 'patient_storage__sd_Father_mother_id_no',
         'patient_storage__sd_permanent_addr', 'patient_storage__sd_state', 'patient_storage__sd_district',
         'patient_storage__sd_city_name', 'patient_storage__sd_country_name',
         'patient_storage__sd_land_line_number', 'patient_storage__sd_Mother_mobile_no',
         'patient_storage__sd_Father_mobile_no', 'patient_storage__sd_email', 'patient_storage__sd_religion',
         'patient_storage__sd_cast',
         'patient_storage__sd_gender', 'patient_storage__sd_referred_status', 'patient_storage__sd_referred_by',
         'patient_storage__sd_referred_by_desc', 'patient_storage__sd_consent_given',
         'patient_storage__sd_consent_upload', 'patient_storage__sd_assent_given', 'patient_storage__sd_assent_upload',
         'patient_storage__sd_hospital_name', 'patient_storage__sd_hospital_reg_no',
         'patient_storage__sd_Patient_education', 'patient_storage__sd_Patient_occupation',
         'patient_storage__sd_Father_education', 'patient_storage__sd_Father_occupation',
         'patient_storage__sd_Mother_education', 'patient_storage__sd_Mother_occupation',
         'patient_storage__sd_Monthly_family_income', 'patient_storage__sd_weight_patient',
         'patient_storage__sd_weight_percentile', 'patient_storage__sd_weight_SD', 'patient_storage__sd_height_patient',
         'patient_storage__sd_height_percentile', 'patient_storage__sd_height_SD',
         'patient_storage__sd_Head_circumference_patient', 'patient_storage__sd_Head_circumference_percentile',
         'patient_storage__sd_Head_circumference_sd',
         'patient_storage__sd_Age_at_onset_of_symptoms_year',
         'patient_storage__sd_Age_at_onset_of_symptoms_month',
         'patient_storage__sd_Age_at_onset_of_symptoms_day',
         'patient_storage__sd_Age_at_onset_of_symptoms_Intrauterine',
         'patient_storage__sd_Age_at_presentation_year',
         'patient_storage__sd_Age_at_presentation_month',
         'patient_storage__sd_Age_at_presentation_day',
         'patient_storage__sd_Age_at_presentation_Intrauterine',
         'patient_storage__sd_Age_at_diagnosis_year',
         'patient_storage__sd_Age_at_diagnosis_month',
         'patient_storage__sd_Age_at_diagnosis_day',
         'patient_storage__sd_Age_at_diagnosis_Intrauterine',
         'patient_storage__sd_Pedigree_to_be_uploaded',
         'patient_storage__sd_positive_family_history',
         'patient_storage__sd_family_history_specify',
         'patient_storage__sd_Consanguinity',
         'patient_storage__sd_Consanguinity_specify',
         'patient_storage__sd_Antenatal_Ultrasound',
         'patient_storage__sd_Polyhydramnios',
         'patient_storage__sd_Hydrops',
         'patient_storage__sd_Hydrops_specify',
         'patient_storage__sd_Type_of_delivery',
         'patient_storage__sd_Baby_cried_immediately_after_delivery',
         'patient_storage__sd_Resuscitation_required',
         'patient_storage__sk_Resuscitation_specify',
         'patient_storage__sd_Resuscitation_ventilation',
         'patient_storage__sd_NICU_stay',
         'patient_storage__sd_NICU_specify',
         'patient_storage__sd_NICU_stay_other',
         'patient_storage__sd_Birth_weight',
         'patient_storage__sd_Development_milestones',
         'patient_storage__sd_delayed_Motor',
         'patient_storage__sd_delayed_Global',
         'patient_storage__sd_delayed_Cognitive',
         'patient_storage__sd_Abdominal_distentesion',
         'patient_storage__sd_Increasing_pallor',
         'patient_storage__sd_Bleeding',
         'patient_storage__sd_Developmental_Delay',
         'patient_storage__sd_Neuroregression',
         'patient_storage__sd_Behavioral_problems',
         'patient_storage__sd_Hyperactivity',
         'patient_storage__sd_Psychomotor_arrest',
         'patient_storage__sd_Seizures',
         'patient_storage__sd_Seizures_specify',
         'patient_storage__sd_On_some_antiepileptics_drugs',
         'patient_storage__sd_antiepileptics_specify',
         'patient_storage__sd_Decreased_attention_span',
         'patient_storage__sd_Stiffness',
         'patient_storage__sd_Poor_feeding',
         'patient_storage__sd_Choking',
         'patient_storage__sd_Loss_of_Vision',
         'patient_storage__sd_Hearing_loss',
         'patient_storage__sd_Recurrent_persistent_upper_respiratory_symptoms',
         'patient_storage__sd_Fractures',
         'patient_storage__sd_Gait_disturbances',
         'patient_storage__sd_Speech_disturbances',
         'patient_storage__sd_Any_surgery',
         'patient_storage__sd_Surgery',
         'patient_storage__sd_Surgery_age_history',
         'patient_storage__sd_Surgery_other_specify',
         'patient_storage__sd_Functional_status',
         'patient_storage__sd_Head_shape_Abnormal',
         'patient_storage__sd_Mongolian_spots_at_back',
         'patient_storage__sd_Ichthyosis',
         'patient_storage__sd_Stiff_Thick_skin',
         'patient_storage__sd_Telangiectasia',
         'patient_storage__sd_Edema',
         'patient_storage__sd_Hydrops1',
         'patient_storage__sd_Angiokeratomas',
         'patient_storage__sd_Exaggerated_startle_reflex',
         'patient_storage__sd_Hypotonia',
         'patient_storage__sd_Hypertonia',
         'patient_storage__sd_Brisk_reflexes',
         'patient_storage__sd_Hyporeflexia',
         'patient_storage__sd_Gait_abnormalities',
         'patient_storage__sd_Opisthotonus',
         'patient_storage__sd_Dystonia',
         'patient_storage__sd_IQ_done',
         'patient_storage__sd_IQ_done_value',
         'patient_storage__sd_DQ_done',
         'patient_storage__sd_DQ_done_value',
         'patient_storage__sd_gaze_palsy',
         'patient_storage__sd_Ophthalmology',
         'patient_storage__sd_Epilepsy',
         'patient_storage__sd_Age_seizure',
         'patient_storage__sd_Development_Cognitive_ability',
         'patient_storage__sd_Ataxia_of_gait',
         'patient_storage__sd_Cerebellar_tremor',
         'patient_storage__sd_Pyramidal',
         'patient_storage__sd_Extrapyramidal',
         'patient_storage__sd_Swallowing_difficulties_Oral_bulbar_function',
         'patient_storage__sd_Speech',
         'patient_storage__sd_Spinal_alignement',
         'patient_storage__sd_final_diagnosis_other',
         'patient_storage__sd_Oculomotor_apraxia',
         'patient_storage__sd_Saccades',
         'patient_storage__sd_Corneal_clouding_opacity',
         'patient_storage__sd_Glaucoma',
         'patient_storage__sd_Optic_Nerve_atrophy',
         'patient_storage__sd_Retinal_degeneration_pigmentation',
         'patient_storage__sd_Cataract',
         'patient_storage__sd_Squint',
         'patient_storage__sd_Nystagmus',
         'patient_storage__sd_Supranuclear_gaze_palsy',
         'patient_storage__sd_Fundus_abnormal',
         'patient_storage__sd_Cherry_Red_Spot',
         'patient_storage__sd_Pigmentary_changes',
         'patient_storage__sd_Cardiovascular_Congestive_Heart_Failure',
         'patient_storage__sd_Cardiovascular_Cor_Pulomonale',
         'patient_storage__sd_Respiratory_Enlarged_tonsils',
         'patient_storage__sd_Respiratory_Sleep_apnea',
         'patient_storage__sd_Respiratory_Reactive_Airway_Disease',
         'patient_storage__sd_Respiratory_Dyspnea',
         'patient_storage__sd_Hepatomegaly',
         'patient_storage__sd_if_yes_size_bcm',
         'patient_storage__sd_if_yes_span',
         'patient_storage__sd_if_yes_Consistency',
         'patient_storage__sd_if_yes_surface',
         'patient_storage__sd_if_yes_margin',
         'patient_storage__sd_Splenomegaly',
         'patient_storage__sd_if_Splenomegaly',
         'patient_storage__sd_Joint_stiffness',
         'patient_storage__sd_Scoliosis',
         'patient_storage__sd_Kyphosis_Gibbus',
         'patient_storage__sd_Genu_valgum',
         'patient_storage__sd_Pes_Cavus',
         'patient_storage__sd_Toe_Walking',
         'patient_storage__sd_Hb',
         'patient_storage__sd_WBC_Total_Count',
         'patient_storage__sd_Platelet_Count',
         'patient_storage__sd_WBC_Differnetial',
         'patient_storage__sd_Absolute_neutrophil_counts',
         'patient_storage__sd_PT_sec',
         'patient_storage__sd_APTT_sec',
         'patient_storage__sd_S_calcium_mg_dl',
         'patient_storage__sd_S_Phosphorus_mg_dl',
         'patient_storage__sd_S_alkaline_phosphatise_IU',
         'patient_storage__sd_S_Acid_phosphatise_IU',
         'patient_storage__sd_S_Total_protein_g_dl',
         'patient_storage__sd_S_Serum_albumin_g_dl',
         'patient_storage__sd_SGPT_IU',
         'patient_storage__sd_GGT',
         'patient_storage__sd_GGT',
         'patient_storage__sd_IRON_mg_dl',
         'patient_storage__sd_TIBC_mg_dl',
         'patient_storage__sd_Vit_B12_pg_ml',
         'patient_storage__sd_Vit_D_ng_ml',
         'patient_storage__sd_PTH_ng_ml',
         'patient_storage__sd_Skeletal_survey',
         'patient_storage__sd_Erlenmeyer_flask_deformity',
         'patient_storage__sd_Osteopenia',
         'patient_storage__sd_Skeletal_Scoliosis',
         'patient_storage__sd_Dysostosis_multiplex',
         'patient_storage__sd_Dexa_Z_Score',
         'patient_storage__sd_xray_bone_age',
         'patient_storage__sd_Pulmonary_function_test',
         'patient_storage__sd_sitting_FEV1',
         'patient_storage__sd_sittingFVC',
         'patient_storage__sd_Supine_FEV1',
         'patient_storage__sd_SupineFVC',
         'patient_storage__sd_rad_ultrasono_type',
         'patient_storage__sd_rad_liversize',
         'patient_storage__sd_rad_liverEchotexture',
         'patient_storage__sd_rad_hepatic',
         'patient_storage__sd_rad_Kidney',
         'patient_storage__sd_rad_kidney_size',
         'patient_storage__sd_rad_kidney_size',
         'patient_storage__sd_rad_lymphnodes_size',
         'patient_storage__sd_rad_portal_vien_dia',
         'patient_storage__sd_rad_adenoma',
         'patient_storage__sd_renal_par_pathalogy',
         'patient_storage__sd_renal_par_pathalogy_specify',
         'patient_storage__sd_nephrocalcinosis',
         'patient_storage__sd_pancreatitis',
         'patient_storage__sd_cholethiasis',
         'patient_storage__sd_CT_scan',
         'patient_storage__sd_CT_scan_specify',
         'patient_storage__sd_MRI_Brain',
         'patient_storage__cerebral_atrophy',
         'patient_storage__hydrocephalus',
         'patient_storage__basal_ganglia_hypo',
         'patient_storage__hyperintensity',
         'patient_storage__thalamic',
         'patient_storage__dysmyelination',
         'patient_storage__Any_other_MRI',
         'patient_storage__sd_MRI_Spine_limbs_pelvis',
         'patient_storage__sd_Osteonecrosis',
         'patient_storage__sd_Compression_spine_deformity_fractures',
         'patient_storage__sd_Marrow_infiltration',
         'patient_storage__sd_marrow_Any_other',
         'patient_storage__sd_MRI_abdomen',
         'patient_storage__sd_Liver_volume',
         'patient_storage__sd_Spleen_volume',
         'patient_storage__sd_Gaucher_related_nodules',
         'patient_storage__sd_Echocardiography_test',
         'patient_storage__sd_Specify_findings_Cardiomyopathy',
         'patient_storage__Cardiomyopathy',
         'patient_storage__sd_Cardiomyopathy',
         'patient_storage__sd_Mention_LVMI',
         'patient_storage__sd_Valvular_involvement',
         'patient_storage__Valvular_Stenosis_mitral',
         'patient_storage__Valvular_Stenosis_tricuspid',
         'patient_storage__Valvular_Stenosis_aortic',
         'patient_storage__Valvular_Stenosis_pulmonary',
         'patient_storage__sd_Valvular_Regurgitation',
         'patient_storage__Valvular_Regurgitation_mitral',
         'patient_storage__Valvular_Regurgitation_tricuspid',
         'patient_storage__Valvular_Regurgitation_aortic',
         'patient_storage__Valvular_Regurgitation_pulmonary',
         'patient_storage__sd_Ejection_fraction',
         'patient_storage__sd_EEG',
         'patient_storage__sd_EEG_specify_Findings',
         'patient_storage__sd_Sleep_Studies',
         'patient_storage__sd_Sleep_Studies_Findings',
         'patient_storage__sd_SLIT_lamp_examination',
         'patient_storage__sd_VEP',
         'patient_storage__sd_ved_specify',
         'patient_storage__sd_Opthalmological_Examination',
         'patient_storage__sd_Describe_if_abnormal',
         'patient_storage__sd_SLIT_Lamp',
         'patient_storage__sd_BERA_Audiogram',
         'patient_storage__sd_BERA_Describe_if_abnormal',
         'patient_storage__sd_Servirity',
         'patient_storage__sd_Unilat_bilat',
         'patient_storage__sd_Nerve_Conduction_Study',
         'patient_storage__sd_Nerve_Describe_if_abnormal',
         'patient_storage__sd_Chitrotriosidase_Study',
         'patient_storage__sd_Chitrotriosidase_if_abnormal',
         'patient_storage__Any_Other_Biomarker2',
         'patient_storage__sd_Biomarker_if_abnormal',
         'patient_storage__sd_Enzyme_assay',
         'patient_storage__sd_Sample_used',
         'patient_storage__sd_Enzyme',
         'patient_storage__sd_Enzyme_other',
         'patient_storage__mt_enzyme_patient_control',
         'patient_storage__mt_enzyme_control_range',
         'patient_storage__mt_enzyme_normal_range',
         'patient_storage__sd_Enzyme_upload',
         'patient_storage__sd_Causative_DNA_sequence_variat',
         'patient_storage__sd_molecular_upload',
         'patient_storage__sd_Gene_molecula',
         'patient_storage__sd_trans_molecul',
         'patient_storage__sd_mul_dna1',
         'patient_storage__sd_mul_pro1',
         'patient_storage__sd_mul_var1',
         'patient_storage__sd_mul_var_cla1',
         'patient_storage__sd_mul_zygo1',
         'patient_storage__sd_mul_dna2',
         'patient_storage__sd_mul_pro2',
         'patient_storage__sd_mul_var2',
         'patient_storage__sd_mul_var_cla2',
         'patient_storage__sd_mul_zygo2',
         'patient_storage__sd_mul_seg',
         'patient_storage__sd_father',
         'patient_storage__sd_mother',
         'patient_storage__sd_ERT',
         'patient_storage__sd_Date_of_initiation',
         'patient_storage__sd_age_of_start',
         'patient_storage__sd_Dosage',
         'patient_storage__sd_Duration',
         'patient_storage__sd_Adverse_events',
         'patient_storage__sd_Adverse_events_specify',
         'patient_storage__sd_ERT_Status',
         'patient_storage__sd_Response_to_therapy',
         'patient_storage__sd_Any_interruption',
         'patient_storage__sd_Reason_interruption',
         'patient_storage__sd_Duration_interruption',
         'patient_storage__sd_Bone_Marrow_Transplantation',
         'patient_storage__sd_Bone_Marrow_Date',
         'patient_storage__sd_Donor',
         'patient_storage__sd_Hospital',
         'patient_storage__sd_Response',
         'patient_storage__sd_Surgery1',
         'patient_storage__Surgery_Splenectomy',
         'patient_storage__Surgery_Hernia',
         'patient_storage__Surgery_others',
         'patient_storage__Surgery_others_text',
         'patient_storage__sd_Surgery_age',
         'patient_storage__sd_Calcium_and_multivitamin_supplements',
         'patient_storage__sd_Regular_Physiotherapy',
         'patient_storage__sd_Antiepileptics',
         'patient_storage__sd_Blood_Transfusion',
         'patient_storage__sd_BL_freq',
         'patient_storage__sd_BL_Trans',
         'patient_storage__sd_Platlet_Transfusion',
         'patient_storage__sd_PL_freq',
         'patient_storage__sd_PL_Trans',
         'patient_storage__PL_Any_other',
         'patient_storage__sd_final_diagnosis',
         'patient_storage__sd_final_diagnosis_other',
         'patient_storage__sd_Final_Outcome',
         'patient_storage__sd_death_cause',
         'patient_storage__sd_age_timedeath',
         'patient_storage__sd_filed_by_DEO_name',
         'patient_storage__sd_clinician_name',
         'patient_storage__sd_filled_date',
         ])

    users = profile_storage.objects.all().prefetch_related('patient_storage').values_list('register_id__institute_name',
                                                                                          'uniqueId',
                                                                                          'sd_icmr_unique_no',
                                                                                          'sd_final_diagnosis',
                                                                                          'sd_date_of_records',
                                                                                          'sd_date_of_clinical_exam',
                                                                                          'sd_date_of_birth',

                                                                                          'sd_Patient_name',
                                                                                          'sd_Father_name',
                                                                                          'sd_Mother_name',
                                                                                          'sd_paitent_id_yes_no',
                                                                                          'sd_paitent_id',
                                                                                          'sd_patient_id_no',
                                                                                          'sd_Father_mother_id',
                                                                                          'sd_Father_mother_id_no',
                                                                                          'sd_permanent_addr',
                                                                                          'sd_state', 'sd_district',
                                                                                          'sd_city_name',
                                                                                          'sd_country_name',
                                                                                          'sd_land_line_number',
                                                                                          'sd_Mother_mobile_no',
                                                                                          'sd_Father_mobile_no',
                                                                                          'sd_email',
                                                                                          'sd_religion', 'sd_cast',
                                                                                          'sd_gender',
                                                                                          'sd_referred_status',
                                                                                          'sd_referred_by',
                                                                                          'sd_referred_by_desc',
                                                                                          'sd_consent_given',
                                                                                          'sd_consent_upload',
                                                                                          'sd_assent_given',
                                                                                          'sd_assent_upload',
                                                                                          'sd_hospital_name',
                                                                                          'sd_hospital_reg_no',
                                                                                          'patient_storage__sd_Patient_education',
                                                                                          'patient_storage__sd_Patient_occupation',
                                                                                          'patient_storage__sd_Father_education',
                                                                                          'patient_storage__sd_Father_occupation',
                                                                                          'patient_storage__sd_Mother_education',
                                                                                          'patient_storage__sd_Mother_occupation',
                                                                                          'patient_storage__sd_Monthly_family_income',
                                                                                          'patient_storage__sd_weight_patient',
                                                                                          'patient_storage__sd_weight_percentile',
                                                                                          'patient_storage__sd_weight_SD',
                                                                                          'patient_storage__sd_height_patient',
                                                                                          'patient_storage__sd_height_percentile',
                                                                                          'patient_storage__sd_height_SD',
                                                                                          'patient_storage__sd_Head_circumference_patient',
                                                                                          'patient_storage__sd_Head_circumference_percentile',
                                                                                          'patient_storage__sd_Head_circumference_sd',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_year',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_month',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_day',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_Intrauterine',
                                                                                          'patient_storage__sd_Age_at_presentation_year',
                                                                                          'patient_storage__sd_Age_at_presentation_month',
                                                                                          'patient_storage__sd_Age_at_presentation_day',
                                                                                          'patient_storage__sd_Age_at_presentation_Intrauterine',
                                                                                          'patient_storage__sd_Age_at_diagnosis_year',
                                                                                          'patient_storage__sd_Age_at_diagnosis_month',
                                                                                          'patient_storage__sd_Age_at_diagnosis_day',
                                                                                          'patient_storage__sd_Age_at_diagnosis_Intrauterine',
                                                                                          'patient_storage__sd_Pedigree_to_be_uploaded',
                                                                                          'patient_storage__sd_positive_family_history',
                                                                                          'patient_storage__sd_family_history_specify',
                                                                                          'patient_storage__sd_Consanguinity',
                                                                                          'patient_storage__sd_Consanguinity_specify',
                                                                                          'patient_storage__sd_Antenatal_Ultrasound',
                                                                                          'patient_storage__sd_Polyhydramnios',
                                                                                          'patient_storage__sd_Hydrops',
                                                                                          'patient_storage__sd_Hydrops_specify',
                                                                                          'patient_storage__sd_Type_of_delivery',
                                                                                          'patient_storage__sd_Baby_cried_immediately_after_delivery',
                                                                                          'patient_storage__sd_Resuscitation_required',
                                                                                          'patient_storage__sk_Resuscitation_specify',
                                                                                          'patient_storage__sd_Resuscitation_ventilation',
                                                                                          'patient_storage__sd_NICU_stay',
                                                                                          'patient_storage__sd_NICU_specify',
                                                                                          'patient_storage__sd_NICU_stay_other',
                                                                                          'patient_storage__sd_Birth_weight',
                                                                                          'patient_storage__sd_Development_milestones',
                                                                                          'patient_storage__sd_delayed_Motor',
                                                                                          'patient_storage__sd_delayed_Global',
                                                                                          'patient_storage__sd_delayed_Cognitive',
                                                                                          'patient_storage__sd_Abdominal_distentesion',
                                                                                          'patient_storage__sd_Increasing_pallor',
                                                                                          'patient_storage__sd_Bleeding',
                                                                                          'patient_storage__sd_Developmental_Delay',
                                                                                          'patient_storage__sd_Neuroregression',
                                                                                          'patient_storage__sd_Behavioral_problems',
                                                                                          'patient_storage__sd_Hyperactivity',
                                                                                          'patient_storage__sd_Psychomotor_arrest',
                                                                                          'patient_storage__sd_Seizures',
                                                                                          'patient_storage__sd_Seizures_specify',
                                                                                          'patient_storage__sd_On_some_antiepileptics_drugs',
                                                                                          'patient_storage__sd_antiepileptics_specify',
                                                                                          'patient_storage__sd_Decreased_attention_span',
                                                                                          'patient_storage__sd_Stiffness',
                                                                                          'patient_storage__sd_Poor_feeding',
                                                                                          'patient_storage__sd_Choking',
                                                                                          'patient_storage__sd_Loss_of_Vision',
                                                                                          'patient_storage__sd_Hearing_loss',
                                                                                          'patient_storage__sd_Recurrent_persistent_upper_respiratory_symptoms',
                                                                                          'patient_storage__sd_Fractures',
                                                                                          'patient_storage__sd_Gait_disturbances',
                                                                                          'patient_storage__sd_Speech_disturbances',
                                                                                          'patient_storage__sd_Any_surgery',
                                                                                          'patient_storage__sd_Surgery',
                                                                                          'patient_storage__sd_Surgery_age_history',
                                                                                          'patient_storage__sd_Surgery_other_specify',
                                                                                          'patient_storage__sd_Functional_status',
                                                                                          'patient_storage__sd_Head_shape_Abnormal',
                                                                                          'patient_storage__sd_Mongolian_spots_at_back',
                                                                                          'patient_storage__sd_Ichthyosis',
                                                                                          'patient_storage__sd_Stiff_Thick_skin',
                                                                                          'patient_storage__sd_Telangiectasia',
                                                                                          'patient_storage__sd_Edema',
                                                                                          'patient_storage__sd_Hydrops1',
                                                                                          'patient_storage__sd_Angiokeratomas',
                                                                                          'patient_storage__sd_Exaggerated_startle_reflex',
                                                                                          'patient_storage__sd_Hypotonia',
                                                                                          'patient_storage__sd_Hypertonia',
                                                                                          'patient_storage__sd_Brisk_reflexes',
                                                                                          'patient_storage__sd_Hyporeflexia',
                                                                                          'patient_storage__sd_Gait_abnormalities',
                                                                                          'patient_storage__sd_Opisthotonus',
                                                                                          'patient_storage__sd_Dystonia',
                                                                                          'patient_storage__sd_IQ_done',
                                                                                          'patient_storage__sd_IQ_done_value',
                                                                                          'patient_storage__sd_DQ_done',
                                                                                          'patient_storage__sd_DQ_done_value',
                                                                                          'patient_storage__sd_gaze_palsy',
                                                                                          'patient_storage__sd_Ophthalmology',
                                                                                          'patient_storage__sd_Epilepsy',
                                                                                          'patient_storage__sd_Age_seizure',
                                                                                          'patient_storage__sd_Development_Cognitive_ability',
                                                                                          'patient_storage__sd_Ataxia_of_gait',
                                                                                          'patient_storage__sd_Cerebellar_tremor',
                                                                                          'patient_storage__sd_Pyramidal',
                                                                                          'patient_storage__sd_Extrapyramidal',
                                                                                          'patient_storage__sd_Swallowing_difficulties_Oral_bulbar_function',
                                                                                          'patient_storage__sd_Speech',
                                                                                          'patient_storage__sd_Spinal_alignement',
                                                                                          'patient_storage__sd_final_diagnosis_other',
                                                                                          'patient_storage__sd_Oculomotor_apraxia',
                                                                                          'patient_storage__sd_Saccades',
                                                                                          'patient_storage__sd_Corneal_clouding_opacity',
                                                                                          'patient_storage__sd_Glaucoma',
                                                                                          'patient_storage__sd_Optic_Nerve_atrophy',
                                                                                          'patient_storage__sd_Retinal_degeneration_pigmentation',
                                                                                          'patient_storage__sd_Cataract',
                                                                                          'patient_storage__sd_Squint',
                                                                                          'patient_storage__sd_Nystagmus',
                                                                                          'patient_storage__sd_Supranuclear_gaze_palsy',
                                                                                          'patient_storage__sd_Fundus_abnormal',
                                                                                          'patient_storage__sd_Cherry_Red_Spot',
                                                                                          'patient_storage__sd_Pigmentary_changes',
                                                                                          'patient_storage__sd_Cardiovascular_Congestive_Heart_Failure',
                                                                                          'patient_storage__sd_Cardiovascular_Cor_Pulomonale',
                                                                                          'patient_storage__sd_Respiratory_Enlarged_tonsils',
                                                                                          'patient_storage__sd_Respiratory_Sleep_apnea',
                                                                                          'patient_storage__sd_Respiratory_Reactive_Airway_Disease',
                                                                                          'patient_storage__sd_Respiratory_Dyspnea',
                                                                                          'patient_storage__sd_Hepatomegaly',
                                                                                          'patient_storage__sd_if_yes_size_bcm',
                                                                                          'patient_storage__sd_if_yes_span',
                                                                                          'patient_storage__sd_if_yes_Consistency',
                                                                                          'patient_storage__sd_if_yes_surface',
                                                                                          'patient_storage__sd_if_yes_margin',
                                                                                          'patient_storage__sd_Splenomegaly',
                                                                                          'patient_storage__sd_if_Splenomegaly',
                                                                                          'patient_storage__sd_Joint_stiffness',
                                                                                          'patient_storage__sd_Scoliosis',
                                                                                          'patient_storage__sd_Kyphosis_Gibbus',
                                                                                          'patient_storage__sd_Genu_valgum',
                                                                                          'patient_storage__sd_Pes_Cavus',
                                                                                          'patient_storage__sd_Toe_Walking',
                                                                                          'patient_storage__sd_Hb',
                                                                                          'patient_storage__sd_WBC_Total_Count',
                                                                                          'patient_storage__sd_Platelet_Count',
                                                                                          'patient_storage__sd_WBC_Differnetial',
                                                                                          'patient_storage__sd_Absolute_neutrophil_counts',
                                                                                          'patient_storage__sd_PT_sec',
                                                                                          'patient_storage__sd_APTT_sec',
                                                                                          'patient_storage__sd_S_calcium_mg_dl',
                                                                                          'patient_storage__sd_S_Phosphorus_mg_dl',
                                                                                          'patient_storage__sd_S_alkaline_phosphatise_IU',
                                                                                          'patient_storage__sd_S_Acid_phosphatise_IU',
                                                                                          'patient_storage__sd_S_Total_protein_g_dl',
                                                                                          'patient_storage__sd_S_Serum_albumin_g_dl',
                                                                                          'patient_storage__sd_SGPT_IU',
                                                                                          'patient_storage__sd_GGT',
                                                                                          'patient_storage__sd_GGT',
                                                                                          'patient_storage__sd_IRON_mg_dl',
                                                                                          'patient_storage__sd_TIBC_mg_dl',
                                                                                          'patient_storage__sd_Vit_B12_pg_ml',
                                                                                          'patient_storage__sd_Vit_D_ng_ml',
                                                                                          'patient_storage__sd_PTH_ng_ml',
                                                                                          'patient_storage__sd_Skeletal_survey',
                                                                                          'patient_storage__sd_Erlenmeyer_flask_deformity',
                                                                                          'patient_storage__sd_Osteopenia',
                                                                                          'patient_storage__sd_Skeletal_Scoliosis',
                                                                                          'patient_storage__sd_Dysostosis_multiplex',
                                                                                          'patient_storage__sd_Dexa_Z_Score',
                                                                                          'patient_storage__sd_xray_bone_age',
                                                                                          'patient_storage__sd_Pulmonary_function_test',
                                                                                          'patient_storage__sd_sitting_FEV1',
                                                                                          'patient_storage__sd_sittingFVC',
                                                                                          'patient_storage__sd_Supine_FEV1',
                                                                                          'patient_storage__sd_SupineFVC',
                                                                                          'patient_storage__sd_rad_ultrasono_type',
                                                                                          'patient_storage__sd_rad_liversize',
                                                                                          'patient_storage__sd_rad_liverEchotexture',
                                                                                          'patient_storage__sd_rad_hepatic',
                                                                                          'patient_storage__sd_rad_Kidney',
                                                                                          'patient_storage__sd_rad_kidney_size',
                                                                                          'patient_storage__sd_rad_kidney_size',
                                                                                          'patient_storage__sd_rad_lymphnodes_size',
                                                                                          'patient_storage__sd_rad_portal_vien_dia',
                                                                                          'patient_storage__sd_rad_adenoma',
                                                                                          'patient_storage__sd_renal_par_pathalogy',
                                                                                          'patient_storage__sd_renal_par_pathalogy_specify',
                                                                                          'patient_storage__sd_nephrocalcinosis',
                                                                                          'patient_storage__sd_pancreatitis',
                                                                                          'patient_storage__sd_cholethiasis',
                                                                                          'patient_storage__sd_CT_scan',
                                                                                          'patient_storage__sd_CT_scan_specify',
                                                                                          'patient_storage__sd_MRI_Brain',
                                                                                          'patient_storage__cerebral_atrophy',
                                                                                          'patient_storage__hydrocephalus',
                                                                                          'patient_storage__basal_ganglia_hypo',
                                                                                          'patient_storage__hyperintensity',
                                                                                          'patient_storage__thalamic',
                                                                                          'patient_storage__dysmyelination',
                                                                                          'patient_storage__Any_other_MRI',
                                                                                          'patient_storage__sd_MRI_Spine_limbs_pelvis',
                                                                                          'patient_storage__sd_Osteonecrosis',
                                                                                          'patient_storage__sd_Compression_spine_deformity_fractures',
                                                                                          'patient_storage__sd_Marrow_infiltration',
                                                                                          'patient_storage__sd_marrow_Any_other',
                                                                                          'patient_storage__sd_MRI_abdomen',
                                                                                          'patient_storage__sd_Liver_volume',
                                                                                          'patient_storage__sd_Spleen_volume',
                                                                                          'patient_storage__sd_Gaucher_related_nodules',
                                                                                          'patient_storage__sd_Echocardiography_test',
                                                                                          'patient_storage__sd_Specify_findings_Cardiomyopathy',
                                                                                          'patient_storage__Cardiomyopathy',
                                                                                          'patient_storage__sd_Cardiomyopathy',
                                                                                          'patient_storage__sd_Mention_LVMI',
                                                                                          'patient_storage__sd_Valvular_involvement',
                                                                                          'patient_storage__Valvular_Stenosis_mitral',
                                                                                          'patient_storage__Valvular_Stenosis_tricuspid',
                                                                                          'patient_storage__Valvular_Stenosis_aortic',
                                                                                          'patient_storage__Valvular_Stenosis_pulmonary',
                                                                                          'patient_storage__sd_Valvular_Regurgitation',
                                                                                          'patient_storage__Valvular_Regurgitation_mitral',
                                                                                          'patient_storage__Valvular_Regurgitation_tricuspid',
                                                                                          'patient_storage__Valvular_Regurgitation_aortic',
                                                                                          'patient_storage__Valvular_Regurgitation_pulmonary',
                                                                                          'patient_storage__sd_Ejection_fraction',
                                                                                          'patient_storage__sd_EEG',
                                                                                          'patient_storage__sd_EEG_specify_Findings',
                                                                                          'patient_storage__sd_Sleep_Studies',
                                                                                          'patient_storage__sd_Sleep_Studies_Findings',
                                                                                          'patient_storage__sd_SLIT_lamp_examination',
                                                                                          'patient_storage__sd_VEP',
                                                                                          'patient_storage__sd_ved_specify',
                                                                                          'patient_storage__sd_Opthalmological_Examination',
                                                                                          'patient_storage__sd_Describe_if_abnormal',
                                                                                          'patient_storage__sd_SLIT_Lamp',
                                                                                          'patient_storage__sd_BERA_Audiogram',
                                                                                          'patient_storage__sd_BERA_Describe_if_abnormal',
                                                                                          'patient_storage__sd_Servirity',
                                                                                          'patient_storage__sd_Unilat_bilat',
                                                                                          'patient_storage__sd_Nerve_Conduction_Study',
                                                                                          'patient_storage__sd_Nerve_Describe_if_abnormal',
                                                                                          'patient_storage__sd_Chitrotriosidase_Study',
                                                                                          'patient_storage__sd_Chitrotriosidase_if_abnormal',
                                                                                          'patient_storage__Any_Other_Biomarker2',
                                                                                          'patient_storage__sd_Biomarker_if_abnormal',
                                                                                          'patient_storage__sd_Enzyme_assay',
                                                                                          'patient_storage__sd_Sample_used',
                                                                                          'patient_storage__sd_Enzyme',
                                                                                          'patient_storage__sd_Enzyme_other',
                                                                                          'patient_storage__mt_enzyme_patient_control',
                                                                                          'patient_storage__mt_enzyme_control_range',
                                                                                          'patient_storage__mt_enzyme_normal_range',
                                                                                          'patient_storage__sd_Enzyme_upload',
                                                                                          'patient_storage__sd_Causative_DNA_sequence_variat',
                                                                                          'patient_storage__sd_molecular_upload',
                                                                                          'patient_storage__sd_Gene_molecula',
                                                                                          'patient_storage__sd_trans_molecul',
                                                                                          'patient_storage__sd_mul_dna1',
                                                                                          'patient_storage__sd_mul_pro1',
                                                                                          'patient_storage__sd_mul_var1',
                                                                                          'patient_storage__sd_mul_var_cla1',
                                                                                          'patient_storage__sd_mul_zygo1',
                                                                                          'patient_storage__sd_mul_dna2',
                                                                                          'patient_storage__sd_mul_pro2',
                                                                                          'patient_storage__sd_mul_var2',
                                                                                          'patient_storage__sd_mul_var_cla2',
                                                                                          'patient_storage__sd_mul_zygo2',
                                                                                          'patient_storage__sd_mul_seg',
                                                                                          'patient_storage__sd_father',
                                                                                          'patient_storage__sd_mother',
                                                                                          'patient_storage__sd_ERT',
                                                                                          'patient_storage__sd_Date_of_initiation',
                                                                                          'patient_storage__sd_age_of_start',
                                                                                          'patient_storage__sd_Dosage',
                                                                                          'patient_storage__sd_Duration',
                                                                                          'patient_storage__sd_Adverse_events',
                                                                                          'patient_storage__sd_Adverse_events_specify',
                                                                                          'patient_storage__sd_ERT_Status',
                                                                                          'patient_storage__sd_Response_to_therapy',
                                                                                          'patient_storage__sd_Any_interruption',
                                                                                          'patient_storage__sd_Reason_interruption',
                                                                                          'patient_storage__sd_Duration_interruption',
                                                                                          'patient_storage__sd_Bone_Marrow_Transplantation',
                                                                                          'patient_storage__sd_Bone_Marrow_Date',
                                                                                          'patient_storage__sd_Donor',
                                                                                          'patient_storage__sd_Hospital',
                                                                                          'patient_storage__sd_Response',
                                                                                          'patient_storage__sd_Surgery1',
                                                                                          'patient_storage__Surgery_Splenectomy',
                                                                                          'patient_storage__Surgery_Hernia',
                                                                                          'patient_storage__Surgery_others',
                                                                                          'patient_storage__Surgery_others_text',
                                                                                          'patient_storage__sd_Surgery_age',
                                                                                          'patient_storage__sd_Calcium_and_multivitamin_supplements',
                                                                                          'patient_storage__sd_Regular_Physiotherapy',
                                                                                          'patient_storage__sd_Antiepileptics',
                                                                                          'patient_storage__sd_Blood_Transfusion',
                                                                                          'patient_storage__sd_BL_freq',
                                                                                          'patient_storage__sd_BL_Trans',
                                                                                          'patient_storage__sd_Platlet_Transfusion',
                                                                                          'patient_storage__sd_PL_freq',
                                                                                          'patient_storage__sd_PL_Trans',
                                                                                          'patient_storage__PL_Any_other',
                                                                                          'patient_storage__sd_final_diagnosis',
                                                                                          'patient_storage__sd_final_diagnosis_other',
                                                                                          'patient_storage__sd_Final_Outcome',
                                                                                          'patient_storage__sd_death_cause',
                                                                                          'patient_storage__sd_age_timedeath',
                                                                                          'patient_storage__sd_filed_by_DEO_name',
                                                                                          'patient_storage__sd_clinician_name',
                                                                                          'patient_storage__sd_filled_date', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_storage_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="storage_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result', 'quality_reason', 'UniqueId', 'unique_no', 'sd_weight_patient',
         'sd_weight_percentile',
         'sd_weight_SD',
         'sd_height_patient',
         'sd_height_percentile',
         'sd_height_SD',
         'sd_Head_circumference_patient',
         'sd_Head_circumference_percentile',
         'sd_Head_circumference_sd',
         'sd_Age_at_onset_of_symptoms_year',
         'sd_Age_at_onset_of_symptoms_month',
         'sd_Age_at_onset_of_symptoms_day',
         'sd_Age_at_onset_of_symptoms_Intrauterine',
         'sd_Age_at_presentation_year',
         'sd_Age_at_presentation_month',
         'sd_Age_at_presentation_day',
         'sd_Age_at_presentation_Intrauterine',
         'sd_Age_at_diagnosis_year',
         'sd_Age_at_diagnosis_month',
         'sd_Age_at_diagnosis_day',
         'sd_Age_at_diagnosis_Intrauterine',
         'sd_positive_family_history',
         'sd_Abdominal_distentesion',
         'sd_Developmental_Delay',
         'sd_Seizures',
         'sd_Hepatomegaly',
         'sd_Splenomegaly',
         'sd_Hb',
         'sd_Platelet_Count',
         'sd_Skeletal_survey',
         'sd_Erlenmeyer_flask_deformity',
         'sd_Osteopenia',
         'sd_Skeletal_Scoliosis',
         'sd_Dysostosis_multiplex',
         'sd_Pulmonary_function_test',
         'sd_rad_ultrasono_type',
         'sd_Chitrotriosidase_Study',
         'sd_Enzyme_assay',
         'mt_enzyme_patient_control',
         'sd_Causative_DNA_sequence_variat',
         'sd_mul_dna1',
         'sd_ERT',
         'sd_final_diagnosis',
         'sd_Final_Outcome', ])

    users = profile_storage.objects.all().prefetch_related('patient_storage').values_list('register_id__institute_name',
                                                                                          'quality_result',
                                                                                          'quality_reason', 'uniqueId',
                                                                                          'sd_icmr_unique_no',
                                                                                          'patient_storage__sd_weight_patient',
                                                                                          'patient_storage__sd_weight_percentile',
                                                                                          'patient_storage__sd_weight_SD',
                                                                                          'patient_storage__sd_height_patient',
                                                                                          'patient_storage__sd_height_percentile',
                                                                                          'patient_storage__sd_height_SD',
                                                                                          'patient_storage__sd_Head_circumference_patient',
                                                                                          'patient_storage__sd_Head_circumference_percentile',
                                                                                          'patient_storage__sd_Head_circumference_sd',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_year',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_month',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_day',
                                                                                          'patient_storage__sd_Age_at_onset_of_symptoms_Intrauterine',
                                                                                          'patient_storage__sd_Age_at_presentation_year',
                                                                                          'patient_storage__sd_Age_at_presentation_month',
                                                                                          'patient_storage__sd_Age_at_presentation_day',
                                                                                          'patient_storage__sd_Age_at_presentation_Intrauterine',
                                                                                          'patient_storage__sd_Age_at_diagnosis_year',
                                                                                          'patient_storage__sd_Age_at_diagnosis_month',
                                                                                          'patient_storage__sd_Age_at_diagnosis_day',
                                                                                          'patient_storage__sd_Age_at_diagnosis_Intrauterine',
                                                                                          'patient_storage__sd_positive_family_history',
                                                                                          'patient_storage__sd_Abdominal_distentesion',
                                                                                          'patient_storage__sd_Developmental_Delay',
                                                                                          'patient_storage__sd_Seizures',
                                                                                          'patient_storage__sd_Hepatomegaly',
                                                                                          'patient_storage__sd_Splenomegaly',
                                                                                          'patient_storage__sd_Hb',
                                                                                          'patient_storage__sd_Platelet_Count',
                                                                                          'patient_storage__sd_Skeletal_survey',
                                                                                          'patient_storage__sd_Erlenmeyer_flask_deformity',
                                                                                          'patient_storage__sd_Osteopenia',
                                                                                          'patient_storage__sd_Skeletal_Scoliosis',
                                                                                          'patient_storage__sd_Dysostosis_multiplex',
                                                                                          'patient_storage__sd_Pulmonary_function_test',
                                                                                          'patient_storage__sd_rad_ultrasono_type',
                                                                                          'patient_storage__sd_Chitrotriosidase_Study',
                                                                                          'patient_storage__sd_Enzyme_assay',
                                                                                          'patient_storage__mt_enzyme_patient_control',
                                                                                          'patient_storage__sd_Causative_DNA_sequence_variat',
                                                                                          'patient_storage__sd_mul_dna1',
                                                                                          'patient_storage__sd_ERT',
                                                                                          'patient_storage__sd_final_diagnosis',
                                                                                          'patient_storage__sd_Final_Outcome', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_skeletal_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skeletal.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'patient_skeletal_sk_final_diagnosis',
         'patient_skeletal_sk_date_of_records', 'patient_skeletal_sk_date_of_clinical_exam',
         'patient_skeletal_sk_date_of_birth',
         'patient_skeletal_sk_patient_age', 'patient_skeletal_sk_patient_name', 'patient_skeletal_sk_father_name',
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
        'sk_date_of_records', 'sk_date_of_clinical_exam', 'sk_date_of_birth', 'sk_patient_age',
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
def export_skeletal_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="skeletal_qaqc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'patient_skeletal_sk_final_diagnosis', 'patient_skeletal_sk_date_of_records', 'patient_skeletal_sk_date_of_clinical_exam',
         'sk_weight_patient', 'sk_weight_percentile', 'sk_weight_sd', 'sk_height_patient', 'sk_height_percentile', 'sk_height_sd', 'sk_Lower_segment_patient', 'sk_Lower_segment_percentile', 'sk_Lower_segment_sd',
         'sk_US_LS_Ratio_patient', 'sk_US_LS_Ratio_percentile', 'sk_US_LS_Ratio_sd', 'sk_Head_circumference_patient', 'sk_Head_circumference_percentile', 'sk_Head_circumference_sd', 'sk_Arm_span_patient',
         'sk_Arm_span_percentile', 'sk_Arm_span_sd', 'sk_Age_at_onset_of_symptoms_year', 'sk_Age_at_onset_of_symptoms_month', 'sk_Age_at_onset_of_symptoms_day', 'sk_Age_at_onset_of_symptoms_Intrauterine',
         'sk_Age_at_presentation_year', 'sk_Age_at_presentation_month', 'sk_Age_at_presentation_day', 'sk_Age_at_presentation_Intrauterine','sk_Age_at_diagnosis_year',
        'sk_Age_at_diagnosis_month',
        'sk_Age_at_diagnosis_day',
        'sk_Age_at_diagnosis_Intrauterine', 'sk_positive_family_history', 'sk_history','sk_Any_Fractures', 'sk_Upper_limb_Trident_hand', 'sk_Upper_limb_Trident_hand_right',
         'sk_Upper_limb_Trident_hand_left', 'sk_Upper_limb_Deformities', 'sk_Upper_limb_Deformities_right', 'sk_Upper_limb_Deformities_left', 'sk_Lower_limb_Deformities', 'sk_Lower_limb_Deformities_right',
         'sk_Lower_limb_Deformities_left', 'sk_DEXA_Scan_Z_score', 'sk_x_ray_findings_Date', 'sk_Dorso_lumbar_Spine_AP', 'sk_X_ray_cervical_spine_in_extension_and_flexion_AP', 'sk_genetic_analysis_performed',
         'sk_mul_dna1',
         'sk_Final_diagnosis', 'sk_Final_outcome',
         ])

    users = profile_skeletal.objects.all().prefetch_related('patient_skeletal').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'sk_icmr_unique_no', 'sk_final_diagnosis',
                                                                                            'sk_date_of_records', 'sk_date_of_clinical_exam',
                                                                                            'patient_skeletal__sk_weight_patient', 'patient_skeletal__sk_weight_percentile', 'patient_skeletal__sk_weight_sd',
                                                                                            'patient_skeletal__sk_height_patient', 'patient_skeletal__sk_height_percentile', 'patient_skeletal__sk_height_sd',
                                                                                            'patient_skeletal__sk_Lower_segment_patient', 'patient_skeletal__sk_Lower_segment_percentile',
                                                                                            'patient_skeletal__sk_Lower_segment_sd', 'patient_skeletal__sk_US_LS_Ratio_patient',
                                                                                            'patient_skeletal__sk_US_LS_Ratio_percentile', 'patient_skeletal__sk_US_LS_Ratio_sd',
                                                                                            'patient_skeletal__sk_Head_circumference_patient', 'patient_skeletal__sk_Head_circumference_percentile',
                                                                                            'patient_skeletal__sk_Head_circumference_sd', 'patient_skeletal__sk_Arm_span_patient',
                                                                                            'patient_skeletal__sk_Arm_span_percentile', 'patient_skeletal__sk_Arm_span_sd',
                                                                                            'patient_skeletal__sk_Age_at_onset_of_symptoms_year', 'patient_skeletal__sk_Age_at_onset_of_symptoms_month',
                                                                                            'patient_skeletal__sk_Age_at_onset_of_symptoms_day', 'patient_skeletal__sk_Age_at_onset_of_symptoms_Intrauterine',
                                                                                            'patient_skeletal__sk_Age_at_presentation_year', 'patient_skeletal__sk_Age_at_presentation_month',
                                                                                            'patient_skeletal__sk_Age_at_presentation_day', 'patient_skeletal__sk_Age_at_presentation_Intrauterine',
                                                                                            'patient_skeletal__sk_Age_at_diagnosis_year',
                                                                                            'patient_skeletal__sk_Age_at_diagnosis_month',
                                                                                            'patient_skeletal__sk_Age_at_diagnosis_day',
                                                                                            'patient_skeletal__sk_Age_at_diagnosis_Intrauterine',
                                                                                            'patient_skeletal__sk_positive_family_history','patient_skeletal__sk_history','patient_skeletal__sk_Any_Fractures',
                                                                                            'patient_skeletal__sk_Upper_limb_Trident_hand', 'patient_skeletal__sk_Upper_limb_Trident_hand_right',
                                                                                            'patient_skeletal__sk_Upper_limb_Trident_hand_left', 'patient_skeletal__sk_Upper_limb_Deformities',
                                                                                            'patient_skeletal__sk_Upper_limb_Deformities_right', 'patient_skeletal__sk_Upper_limb_Deformities_left',
                                                                                            'patient_skeletal__sk_Lower_limb_Deformities', 'patient_skeletal__sk_Lower_limb_Deformities_right',
                                                                                            'patient_skeletal__sk_Lower_limb_Deformities_left', 'patient_skeletal__sk_DEXA_Scan_Z_score',
                                                                                            'patient_skeletal__sk_x_ray_findings_Date', 'patient_skeletal__sk_Dorso_lumbar_Spine_AP',
                                                                                            'patient_skeletal__sk_X_ray_cervical_spine_in_extension_and_flexion_AP', 'patient_skeletal__sk_genetic_analysis_performed',
                                                                                            'patient_skeletal__sk_mul_dna1',
                                                                                            'patient_skeletal__sk_Final_diagnosis', 'patient_skeletal__sk_Final_outcome',)
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_mucopoly_csv(request):
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
def export_mucopoly_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Mucopoly_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'muco_final_diagnosis', 'muco_date_of_records', 'muco_date_of_clinical_exam',
         'anth_wght_pat',
         'anth_wght_per', 'anth_wght_sd',
         'anth_height_pat',
         'anth_height_per',
         'anth_height_sd',
         'anth_head_cir_pat',
         'anth_head_cir_per', 'anth_head_cir_sd',
         'Age_at_Onset_of_symptoms_years', 'Age_at_Onset_of_symptoms_months',
         'Age_at_Onset_of_symptoms_day', 'Age_at_Onset_of_symptoms_intrauterine',

         'Age_at_Presentation_years', 'Age_at_Presentation_months',
         'Age_at_Presentation_day', 'Age_at_Presentation_intrauterine',

         'Age_at_diagnosis_years', 'Age_at_diagnosis_months',
         'Age_at_diagnosis_day', 'Age_at_diagnosis_intrauterine',
            'developmental_milestones', 'motor', 'globall', 'cognitive', 'cognitive', 'behavioural_problems', 'face_coarse',
         'corneal_clouding', 'Valvular_involvement', 'hepatomegaly', 'size_hepatomegaly', 'span_hepatomegaly', 'Splenomegaly', 'size_splenomegaly', 'Joint_Contractures','Joint_arthritis', 'Joint_laxity', 'CT_Scan',
         'Specify_findings_if_abnormall', 'MRI_Brain', 'Specify_findings_if_abnormal_mri', 'EEG', 'Specify_findings_if_abnormal_eeg', 'Hearing_Assessment', 'if_abnormal', 'enzyme_var', 'enzyme_sam',
          'Patient_enzyme', 'mul_dna1','Finaldiagnosis','Finaloutcomes',])

    users = profile_mucopolysaccharidosis.objects.all().prefetch_related('patient_mucopoly').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'muco_icmr_unique_no', 'muco_final_diagnosis',
                                                                                                         'muco_date_of_records', 'muco_date_of_clinical_exam',
                                                                                                         'patient_mucopoly__gl_anth_wght_pat',
                                                                                                         'patient_mucopoly__gl_anth_wght_per',
                                                                                                         'patient_mucopoly__gl_anth_wght_sd',
                                                                                                         'patient_mucopoly__gl_anth_height_pat',
                                                                                                         'patient_mucopoly__gl_anth_height_per',
                                                                                                         'patient_mucopoly__gl_anth_height_sd',
                                                                                                         'patient_mucopoly__gl_anth_head_cir_pat',
                                                                                                         'patient_mucopoly__gl_anth_head_cir_per',
                                                                                                         'patient_mucopoly__gl_anth_head_cir_sd',
                                                                                                         'patient_mucopoly__Age_at_Onset_of_symptoms_years',
                                                                                                         'patient_mucopoly__Age_at_Onset_of_symptoms_months',
                                                                                                         'patient_mucopoly__Age_at_Onset_of_symptoms_day',
                                                                                                         'patient_mucopoly__Age_at_Onset_of_symptoms_intrauterine',

                                                                                                         'patient_mucopoly__Age_at_Presentation_years',
                                                                                                         'patient_mucopoly__Age_at_Presentation_months',
                                                                                                         'patient_mucopoly__Age_at_Presentation_day',
                                                                                                         'patient_mucopoly__Age_at_Presentation_intrauterine',

                                                                                                         'patient_mucopoly__Age_at_diagnosis_years',
                                                                                                         'patient_mucopoly__Age_at_diagnosis_months',
                                                                                                         'patient_mucopoly__Age_at_diagnosis_day',
                                                                                                         'patient_mucopoly__Age_at_diagnosis_intrauterine',
                                                                                                         'patient_mucopoly__developmental_milestones', 'patient_mucopoly__motor',
                                                                                                         'patient_mucopoly__globall', 'patient_mucopoly__cognitive', 'patient_mucopoly__cognitive',
                                                                                                         'patient_mucopoly__behavioural_problems', 'patient_mucopoly__face_coarse', 'patient_mucopoly__corneal_clouding',
                                                                                                         'patient_mucopoly__Valvular_involvement', 'patient_mucopoly__hepatomegaly', 'patient_mucopoly__size_hepatomegaly',
                                                                                                         'patient_mucopoly__span_hepatomegaly', 'patient_mucopoly__Splenomegaly', 'patient_mucopoly__size_splenomegaly',
                                                                                                         'patient_mucopoly__Joint_Contractures','patient_mucopoly__Joint_arthritis', 'patient_mucopoly__Joint_laxity', 'patient_mucopoly__CT_Scan',
                                                                                                         'patient_mucopoly__Specify_findings_if_abnormall', 'patient_mucopoly__MRI_Brain',
                                                                                                         'patient_mucopoly__Specify_findings_if_abnormal_mri', 'patient_mucopoly__EEG',
                                                                                                         'patient_mucopoly__Specify_findings_if_abnormal_eeg', 'patient_mucopoly__Hearing_Assessment',
                                                                                                         'patient_mucopoly__if_abnormal', 'patient_mucopoly__enzyme_var', 'patient_mucopoly__enzyme_sam',
                                                                                                         'patient_mucopoly__Patient_enzyme','patient_mucopoly__mul_dna1','patient_mucopoly__Finaldiagnosis','patient_mucopoly__Finaloutcomes', )

    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_smallmolecule_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="smallmolecule.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'small_final_diagnosis', 'small_date_of_records', 'small_date_of_clinical_exam', 'small_date_of_birth', 'small_patient_name', 'small_father_name',
         'small_mother_name', 'small_paitent_id_yes_no', 'small_paitent_id', 'small_patient_id_no', 'small_father_mother_id', 'small_father_mother_no', 'small_permanent_addr', 'small_state', 'small_district',
         'small_city_name', 'small_country_name', 'small_land_line_no', 'small_mother_mobile_no', 'small_father_mobile_no', 'small_email', 'small_religion', 'small_caste', 'small_gender', 'small_referred_status',
         'small_referred_by', 'small_referred_by_desc', 'small_consent_given', 'small_consent_upload', 'small_assent_given', 'small_assent_upload', 'small_hospital_name', 'small_hospital_reg_no', 'head_circumference',
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

    users = profile_smallmolecule.objects.all().prefetch_related('patient_small').values_list('register_id__institute_name', 'uniqueId', 'small_icmr_unique_no', 'small_final_diagnosis', 'small_date_of_records',
                                                                                              'small_date_of_clinical_exam', 'small_date_of_birth', 'small_patient_name', 'small_father_name',
                                                                                              'small_mother_name', 'small_paitent_id_yes_no', 'small_paitent_id', 'small_patient_id_no', 'small_father_mother_id',
                                                                                              'small_father_mother_no', 'small_permanent_addr', 'small_state', 'small_district', 'small_city_name', 'small_country_name',
                                                                                              'small_land_line_no', 'small_mother_mobile_no', 'small_father_mobile_no', 'small_email', 'small_religion', 'small_caste',
                                                                                              'small_gender', 'small_referred_status', 'small_referred_by', 'small_referred_by_desc', 'small_consent_given',
                                                                                              'small_consent_upload', 'small_assent_given', 'small_assent_upload', 'small_hospital_name', 'small_hospital_reg_no',
                                                                                              'patient_small__head_circumference', 'patient_small__age_at_first_symptom', 'patient_small__visual_problem',
                                                                                              'patient_small__any_malformation', 'patient_small__developmental_delay', 'patient_small__developmental_findings',
                                                                                              'patient_small__vomiting', 'patient_small__vomiting_finding', 'patient_small__loose_stools', 'patient_small__stools_findings',
                                                                                              'patient_small__pneumonia', 'patient_small__pneumonia_findings', 'patient_small__fever', 'patient_small__fever_findings',
                                                                                              'patient_small__lethargy', 'patient_small__lethargy_findings', 'patient_small__seizures', 'patient_small__seizures_findings',
                                                                                              'patient_small__abdominal_distention', 'patient_small__abdominal_distention_findings', 'patient_small__history_admission',
                                                                                              'patient_small__history_findings', 'patient_small__any_surgery', 'patient_small__surgery_findings',
                                                                                              'patient_small__aversion_sweet_protein', 'patient_small__sweet_protein_findings', 'patient_small__encephalopathy',
                                                                                              'patient_small__encephalopathy_findings', 'patient_small__deafness', 'patient_small__deafness_findings',
                                                                                              'patient_small__extra_pyramidal_symp', 'patient_small__extra_pyramidal_symp_findings', 'patient_small__hypotonia',
                                                                                              'patient_small__hypotonia_findings', 'patient_small__hypertonia', 'patient_small__hypertonia_findings',
                                                                                              'patient_small__facial_dysmorphism', 'patient_small__facial_dysmorphism_findings', 'patient_small__congential_heart_disease',
                                                                                              'patient_small__congential_heart_disease_findings', 'patient_small__cardiomyopathy', 'patient_small__cardiomyopathy_findings',
                                                                                              'patient_small__hepatomegaly', 'patient_small__hepatomegaly_findings', 'patient_small__splenomegaly',
                                                                                              'patient_small__splenomegaly_findings', 'patient_small__pigmentary', 'patient_small__pigmentary_findings',
                                                                                              'patient_small__deranged_LFT', 'patient_small__deranged_LFT_findings', 'patient_small__deranged_RFT',
                                                                                              'patient_small__deranged_RFT_findings', 'patient_small__hypoglycemia', 'patient_small__hypoglycemia_findings',
                                                                                              'patient_small__metabolic_acidosis', 'patient_small__metabolic_acidosis_findings', 'patient_small__metabolic_alkalosis',
                                                                                              'patient_small__metabolic_alkalosis_findings', 'patient_small__hyper_ammonia', 'patient_small__hyper_ammonia_findings',
                                                                                              'patient_small__high_lactate', 'patient_small__high_lactate_findings', 'patient_small__urine_ketones',
                                                                                              'patient_small__urine_ketones_findings', 'patient_small__cherry_red_spot', 'patient_small__cherry_red_spot_findings',
                                                                                              'patient_small__retinitis_pigmentosa', 'patient_small__retinitis_pigmentosa_findings', 'patient_small__optic_atrophy',
                                                                                              'patient_small__optic_atrophy_findings', 'patient_small__mechanical_ventilation',
                                                                                              'patient_small__mechanical_ventilation_findings', 'patient_small__dialysis', 'patient_small__dialysis_findings',
                                                                                              'patient_small__regression', 'patient_small__regression_findings', 'patient_small__distonia_abnormal_movement',
                                                                                              'patient_small__distonia_abnormal_findings', 'patient_small__high_cpk', 'patient_small__high_cpk_findings',
                                                                                              'patient_small__generic_analysis', 'patient_small__generic_analysis_findings', 'patient_small__final_dagnosis',
                                                                                              'patient_small__final_dagnosis_findings', 'patient_small__dna_storage', 'patient_small__dna_storage_findings',
                                                                                              'patient_small__CT_brain', 'patient_small__CT_brain_date', 'patient_small__CT_brain_age', 'patient_small__mri_brain',
                                                                                              'patient_small__mri_brain_date', 'patient_small__mri_brain_age', 'patient_small__mrs_brain', 'patient_small__mrs_brain_date',
                                                                                              'patient_small__mrs_brain_age', 'patient_small__ms_ms', 'patient_small__ms_date', 'patient_small__ms_age',
                                                                                              'patient_small__gcms', 'patient_small__gcms_date', 'patient_small__gcms_age', 'patient_small__enzyme_assay',
                                                                                              'patient_small__enzyme_assay_date', 'patient_small__enzyme_assay_age', 'patient_small__quantitative_plasma',
                                                                                              'patient_small__quantitative_plasma_date', 'patient_small__quantitative_plasma_age', 'patient_small__quantitative_csf',
                                                                                              'patient_small__quantitative_csf_date', 'patient_small__quantitative_csf_age', 'patient_small__muscle_biopsy',
                                                                                              'patient_small__muscle_biopsy_date', 'patient_small__muscle_biopsy_age', 'patient_small__ncv', 'patient_small__ncv_date',
                                                                                              'patient_small__ncv_age', 'patient_small__ief_cdg', 'patient_small__ief_cdg_date', 'patient_small__ief_cdg_age',
                                                                                              'patient_small__glycine', 'patient_small__glycine_date', 'patient_small__glycine_age', 'patient_small__other_info',
                                                                                              'patient_small__other_info_date', 'patient_small__other_info_age', 'patient_small__tms', 'patient_small__tms_date',
                                                                                              'patient_small__tms_age', 'patient_small__photos', 'patient_small__photos_specify', 'patient_small__molecular_studies',
                                                                                              'patient_small__molecular_studies_date', 'patient_small__molecular_studies_place', 'patient_small__upload_studies',
                                                                                              'patient_small__Final_Outcome', 'patient_small__death_cause', 'patient_small__age_timedeath', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_smallmolecule_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="smallmolecule_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'small_final_diagnosis', 'small_date_of_records', 'small_date_of_clinical_exam', 'head_circumference',
          'visual_problem', 'any_malformation',  'Final_Outcome', 'death_cause',  ])

    users = profile_smallmolecule.objects.all().prefetch_related('patient_small').values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'small_icmr_unique_no', 'small_final_diagnosis', 'small_date_of_records',
                                                                                              'small_date_of_clinical_exam',
                                                                                              'patient_small__head_circumference', 'patient_small__age_at_first_symptom', 'patient_small__visual_problem',
                                                                                              'patient_small__any_malformation',
                                                                                              'patient_small__Final_Outcome', 'patient_small__death_cause',  )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_pid_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pid.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'pid_final_diagnosis', 'pid_date_of_record', 'pid_clinical_exam_date', 'pid_date_of_birth', 'pid_patient_name', 'pid_father_name', 'pid_mother_name',
         'pid_paitent_id', 'pid_paitent_id_list', 'pid_patient_id_no', 'pid_father_mother_id', 'pid_father_mother_id_no', 'pid_permanent_addr', 'pid_state', 'pid_district', 'pid_city_name', 'pid_country_name',
         'pid_land_line_no', 'pid_mother_mobile_no', 'pid_father_mobile_no', 'pid_email', 'pid_religion', 'pid_caste', 'pid_gender', 'pid_referred_status', 'pid_referred_by', 'pid_referred_by_desc', 'pid_consent_given',
         'pid_consent_upload', 'pid_assent_given', 'pid_assent_upload', 'pid_hospital_name', 'pid_hospital_reg_no', 'pid_has_hiv_been_excluded', 'pid_date_onset_symptoms', 'pid_onset_date', 'age_onset_symptoms_years',
         'age_onset_symptoms_months', 'pid_infections', 'pid_Meningitis_number_of_infection', 'pid_Meningitis_number_of_infection_last_year', 'Otitis_media', 'Otitis_media_last', 'Tonsillitis', 'Tonsillitis_last',
         'Sinusitis', 'Sinusitis_last', 'Pneumonia_Bronchiectasis', 'Pneumonia_Bronchiectasis_last', 'pid_Gastroenteritis_number_of_infection', 'pid_Gastroenteritis_number_of_infection_last_year',
         'pid_Urinary_tract_number_of_infection', 'pid_Urinary_tract_number_of_infection_last_year', 'tissue_infections', 'tissue_infections_last', 'Liver_abscess', 'Liver_abscess_last',
         'pid_Septicemias_number_of_infection', 'pid_Septicemias_number_of_infection_last_year', 'Splenic_abscess', 'Splenic_abscess_last', 'pid_Thrush_or_fungal_number_of_infection',
         'pid_Thrush_or_fungal_number_of_infection_last_year', 'pid_Vaccine_associated_complications', 'pid_bcg', 'pid_Vaccine_associated_complications_BCG_adenitis_age_onset',
         'pid_Vaccine_associated_complications_BCG_adenitis_Axillary', 'pid_Vaccine_associated_complications_BCG_adenitis_Cervical', 'pid_Vaccine_associated_adenitis_Multiple_sites_yes_no',
         'pid_Vaccine_associated_Multiple_sites', 'pid_bcg_options', 'pid_Vaccine_associated_complications_BCG_osis', 'pid_opv', 'pid_OPV_Date_Dose', 'pid_OPV_Flaccid_paralysis', 'pid_OPV_Poliovirus_isolation',
         'pid_Rubella', 'pid_Rubella_Date_Vaccination', 'pid_Rubella_Symptoms_Fever', 'pid_Rubella_Symptoms_Enlarged_lymph_nodes', 'pid_Rubella_Symptoms_Measles_like_rash', 'pid_Measles', 'pid_Measles_Date_Vaccination',
         'pid_Measles_fever', 'pid_Measles_EnlargedLymphNodes', 'pid_Measles_MeaslesLikeRash', 'pid_Failure_to_gain_weight', 'pid_autoimmunity_autoinflammation', 'pid_autoimmunity_autoinflammation_type_symptoms_fever',
         'pid_autoimmunity_autoinflammation_type_symptoms_fever_temp', 'pid_autoimmunity_autoinflammation_type_symptoms_fever_duration', 'pid_autoimmunity_Precipitated_cold',
         'pid_autoimmunity_Precipitated_cold_frequency', 'pid_autoimmunity_AssociatedLymphadenopathy', 'pid_autoimmunity_AbdominalSymptoms', 'pid_autoimmunity_AbdominalSymptoms_1', 'pid_autoimmunity_AbdominalSymptoms_2',
         'pid_autoimmunity_AbdominalSymptoms_3', 'pid_autoimmunity_AbdominalSymptoms_4', 'pid_autoimmunity_AbdominalSymptoms_5', 'pid_autoimmunity_MusculoskeletalSymptoms', 'pid_autoimmunity_MusculoskeletalSymptoms_1',
         'pid_autoimmunity_MusculoskeletalSymptoms_2', 'pid_autoimmunity_MusculoskeletalSymptoms_3', 'pid_autoimmunity_MusculoskeletalSymptoms_3_numberJoints',
         'pid_autoimmunity_MusculoskeletalSymptoms_3_jointDeformity', 'pid_autoimmunity_MusculoskeletalSymptoms_3_Contractures', 'pid_autoimmunity_Osteomyelitis', 'pid_autoimmunity_CNS_Ear_Eye',
         'pid_autoimmunity_CNS_Ear_Eye_1', 'pid_autoimmunity_CNS_Ear_Eye_2', 'pid_autoimmunity_CNS_Ear_Eye_3', 'pid_autoimmunity_CNS_Ear_Eye_4', 'pid_autoimmunity_CNS_Ear_Eye_5', 'pid_autoimmunity_CNS_Ear_Eye_6',
         'pid_autoimmunity_CNS_Ear_Eye_7', 'pid_Skin_Mucosal', 'pid_Skin_Mucosal_1', 'pid_Skin_Mucosal_2', 'pid_Skin_Mucosal_3', 'pid_Skin_Mucosal_4', 'pid_Skin_Mucosal_5', 'pid_Skin_Mucosal_6', 'pid_Skin_Mucosal_7',
         'pid_Skin_Mucosal_8', 'pid_autoimmunity_autoinflammation_type_symptoms_fever_other', 'pid_ALLERGY_ATOPY', 'pid_ALLERGY_ATOPY_opn', 'pid_MALIGNANCY', 'pid_MALIGNANCY_diagnosis',
         'pid_MALIGNANCY_diagnosis_present_before_diagnosis', 'pid_MALIGNANCY_diagnosis_options', 'pid_MALIGNANCY_diagnosis_Biologic', 'pid_ORGANISM_ISOLATED_viral', 'pid_ORGANISM_ISOLATED_viral_1',
         'pid_ORGANISM_ISOLATED_viral_2', 'pid_ORGANISM_ISOLATED_viral_3', 'pid_ORGANISM_ISOLATED_viral_4', 'pid_ORGANISM_ISOLATED_viral_5', 'pid_ORGANISM_ISOLATED_viral_6', 'pid_ORGANISM_ISOLATED_viral_7',
         'pid_ORGANISM_ISOLATED_viral_8', 'pid_ORGANISM_ISOLATED_viral_9', 'pid_ORGANISM_ISOLATED_viral_10', 'pid_ORGANISM_ISOLATED_viral_11', 'pid_ORGANISM_ISOLATED_viral_12', 'pid_ORGANISM_ISOLATED_viral_13',
         'pid_ORGANISM_ISOLATED_viral_14', 'pid_ORGANISM_ISOLATED_viral_14_specify', 'pid_ORGANISM_ISOLATED_Bacterial', 'pid_ORGANISM_ISOLATED_Bacterial_1', 'pid_ORGANISM_ISOLATED_Bacterial_2',
         'pid_ORGANISM_ISOLATED_Bacterial_3', 'pid_ORGANISM_ISOLATED_Bacterial_4', 'pid_ORGANISM_ISOLATED_Bacterial_5', 'pid_ORGANISM_ISOLATED_Bacterial_6', 'pid_ORGANISM_ISOLATED_Bacterial_7',
         'pid_ORGANISM_ISOLATED_Bacterial_8', 'pid_ORGANISM_ISOLATED_Bacterial_9', 'pid_ORGANISM_ISOLATED_Bacterial_10', 'pid_ORGANISM_ISOLATED_Bacterial_11', 'pid_ORGANISM_ISOLATED_Bacterial_12',
         'pid_ORGANISM_ISOLATED_Bacterial_13', 'pid_ORGANISM_ISOLATED_Bacterial_14', 'pid_ORGANISM_ISOLATED_bacterial_14_specify', 'pid_Fungal', 'pid_Fungal_1', 'pid_Fungal_2', 'pid_Fungal_3', 'pid_Fungal_4',
         'pid_Fungal_5', 'pid_Fungal_6', 'pid_Fungal_6_specify', 'pid_Mycobacterial', 'pid_Mycobacterial_1', 'pid_Mycobacterial_2', 'pid_Mycobacterial_3', 'pid_FamilyHistory_Consanguinity',
         'pid_FamilyHistory_Consanguinity_degree', 'pid_FamilyHistory_HistoryYoung_Children', 'pid_FamilyHistory_HistoryYoung_Children_numberSiblingDeaths', 'pid_FamilyHistory_death_cause',
         'pid_FamilyHistory_deaths_male_member', 'pid_FamilyHistory_deaths_male_member_relations', 'pid_FamilyHistory_deaths_male_member_diagnosed_PID', 'pid_FamilyHistory_deaths_male_member_diagnosed_PID_diagnosis',
         'pid_FamilyHistory_deaths_male_member_diagnosed_PID_relation', 'pid_FamilyHistory_diagnosed_PID_listed_registry', 'pid_FamilyHistory_reason_pid_evaluation', 'pid_clinical_exam_Anthropometry_wieght',
         'pid_clinical_exam_Anthropometry_Height', 'pid_clinical_exam_Anthropometry_HeadCircumference', 'pid_DistinctivePhenotypeaDysmorphicFacies', 'pid_DistinctivePhenotypeaaHypoPigmentedHair',
         'pid_DistinctivePhenotypeabTeethAbnormalities', 'pid_DistinctivePhenotypeacAbsentTonsil', 'pid_DistinctivePhenotypeadOralUlcers', 'pid_DistinctivePhenotypeadeSkinHypopigmentation',
         'pid_DistinctivePhenotypeadefLymphAdenopathy', 'pid_DistinctivePhenotypeadefLymphAdenopathy_options', 'pid_DistinctivePhenotypegHepatosplenomegaly', 'pid_DistinctivePhenotypeSkeletalSystemAbnormalities',
         'pid_DistinctivePhenotypeBCG_Scar', 'pid_DistinctivePhenotyFindingaRespiratory', 'pid_DistinctivePhenotyFindingCardiovascular', 'pid_DistinctivePhenotyFindingcAbdominal', 'pid_DistinctivePhenotyFindingdCNS',
         'pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no', 'pid_BroadDiagnosisCategoryImmunodeficiencyAffecting', 'pid_ImmunodeficiencyAffecting_other_specify',
         'pid_BroadDiagnosisCategoryCIDAssociated_yes_no', 'pid_BroadDiagnosisCategoryCIDAssociated', 'pid_BroadDiagnosisCategoryCIDAssociated_Other_Specify', 'pid_BroadDiagnosisCategoryPredominantAntibody_yes_no',
         'pid_BroadDiagnosisCategoryPredominantAntibody', 'pid_BroadDiagnosisCategoryPredominantAntibody_other_specify', 'pid_BroadDiagnosisCategoryDiseasesImmune_yes_no', 'pid_BroadDiagnosisCategoryDiseasesImmune',
         'pid_BroadDiagnosisCategoryDiseasesImmune_other_specify', 'pid_BroadDiagnosisCategoryCongenitalDefects_yes_no', 'pid_BroadDiagnosisCategoryCongenitalDefects',
         'pid_BroadDiagnosisCategoryCongenitalDefects_other_specify', 'pid_BroadDiagnosisCategoryDefectsIntrinsic_yes_no', 'pid_BroadDiagnosisCategoryDefectsIntrinsic',
         'pid_BroadDiagnosisCategoryDefectsIntrinsic_other_specify', 'pid_BroadDiagnosisCategoryAutoinflammatory_yes_no', 'pid_BroadDiagnosisCategoryAutoinflammatory',
         'pid_BroadDiagnosisCategoryAutoinflammatory_other_specify', 'pid_BroadDiagnosisCategoryComplementDeficiency_yes_no', 'pid_BroadDiagnosisCategoryComplementDeficiency',
         'pid_BroadDiagnosisCategoryMarrowFailure_yes_no', 'pid_BroadDiagnosisCategoryMarrowFailure', 'pid_BroadDiagnosisCategoryMarrowFailure_other_specify', 'pid_BroadDiagnosisCategoryPhenocopies_yes_no',
         'pid_BroadDiagnosisCategoryPhenocopies', 'pid_BroadDiagnosisCategoryPhenocopies_other_specify', 'pid_CBC_Date', 'pid_CBC_Date1', 'pid_CBC_Date2', 'pid_CBC_Date3', 'pid_CBC_Hb', 'pid_CBC_Hb1', 'pid_CBC_Hb2',
         'pid_CBC_Hb3', 'pid_CBC_wbc', 'pid_CBC_wbc1', 'pid_CBC_wbc2', 'pid_CBC_wbc3', 'pid_CBC_wbc_level', 'pid_CBC_wbc1_level', 'pid_CBC_wbc2_level', 'pid_CBC_wbc3_level', 'pid_CBC_Lymphcytes', 'pid_CBC_Lymphcytes1',
         'pid_CBC_Lymphcytes2', 'pid_CBC_Lymphcytes3', 'pid_CBC_PMN', 'pid_CBC_PMN1', 'pid_CBC_PMN2', 'pid_CBC_PMN3', 'pid_CBC_Eosinophils', 'pid_CBC_Eosinophils1', 'pid_CBC_Eosinophils2', 'pid_CBC_Eosinophils3',
         'pid_CBC_Basophils', 'pid_CBC_Basophils1', 'pid_CBC_Basophils2', 'pid_CBC_Basophils3', 'pid_CBC_Monocytes', 'pid_CBC_Monocytes1', 'pid_CBC_Monocytes2', 'pid_CBC_Monocytes3', 'pid_CBC_Platelets',
         'pid_CBC_Platelets1', 'pid_CBC_Platelets2', 'pid_CBC_Platelets3', 'pid_M_Platelets', 'pid_M_Platelets1', 'pid_M_Platelets2', 'pid_M_Platelets3', 'pid_phenotype_Absolute_Lymphocyte_count',
         'pid_phenotype_Absolute_Lymphocyte_count_level', 'pid_phenotype_CD3_T_cells', 'pid_phenotype_CD3_T_cells_level', 'pid_CD4_Helper_T', 'pid_CD4_Helper_T_level', 'pid_phenotype_CD8_Cytotoxic_T_cells',
         'pid_phenotype_CD8_Cytotoxic_T_cells_level', 'pid_phenotype_CD19_B_cells', 'pid_phenotype_CD19_B_cells_level', 'pid_phenotype_CD20_B_cells', 'pid_phenotype_CD20_B_cells_level', 'pid_phenotype_CD56CD16_NK_cells',
         'pid_phenotype_CD56CD16_NK_cells_level', 'pid_phenotype_CD25', 'pid_phenotype_CD25_level', 'pid_phenotype_Double_negative_T_cells', 'pid_phenotype_Double_negative_T_cells_level', 'Gamma_delta_T_cells',
         'Gamma_delta_T_cells_level', 'pid_CD4_subset_panel_naive_cd4', 'pid_CD4_subset_panel_naive_cd4_level', 'pid_CD4_subset_panel_Total_Memory_CD4', 'pid_CD4_subset_panel_Total_Memory_CD4_level', 'CD4_CD45RA',
         'CD4_CD45RA_level', 'CD4_CD45RO', 'CD4_CD45RO_level', 'pid_CD8_subset_panel_naive_cd8', 'pid_CD8_subset_panel_naive_cd8_level', 'pid_CD8_subset_panel_Total_Memory_CD8',
         'pid_CD8_subset_panel_Total_Memory_CD8_level', 'CD8_CD45RA', 'CD8_CD45RA_level', 'CD8_CD45RO', 'CD8_CD45RO_level', 'pid_T_regulatory_cells', 'pid_T_regulatory_cells_level', 'pid_Naive_B_cells',
         'pid_Naive_B_cells_level', 'pid_Naive_B_cells_Transitional_B_cells', 'pid_Naive_B_cells_Transitional_B_cells_level', 'cd27_B_cells', 'cd27_B_cells_level', 'cd27_igm_Bcells', 'cd27_igm_Bcells_level',
         'cd27_igD_Bcells', 'cd27_igD_Bcells_level', 'pid_Immunoglobulin_IgG', 'pid_Immunoglobulin_IgG_level', 'pid_Immunoglobulin_IgG1', 'pid_Immunoglobulin_IgG1_level', 'pid_Immunoglobulin_IgG2',
         'pid_Immunoglobulin_IgG2_level', 'pid_Immunoglobulin_IgG3', 'pid_Immunoglobulin_IgG3_level', 'pid_Immunoglobulin_IgG4', 'pid_Immunoglobulin_IgG4_level', 'pid_Immunoglobulin_IgA', 'pid_Immunoglobulin_IgA_level',
         'pid_Immunoglobulin_IgM', 'pid_Immunoglobulin_IgM_level', 'pid_Immunoglobulin_IgE', 'pid_Immunoglobulin_IgE_level', 'pid_Immunoglobulin_IgD', 'pid_Immunoglobulin_IgD_level', 'pid_Vaccine_responses_tested',
         'pid_Vaccine_responses_tested_Protein', 'diphtheria', 'tetanus', 'protien_conjugated_hib', 'Polysaccharide_hib', 'salmonella_typhi', 'PHI_174antigen', 'pid_Vaccine_responses_tested_Iso_hemagglutinin',
         'Iso_hemagglutinin_antiA', 'Iso_hemagglutinin_antiB', 'pid_Vaccine_responses_tested_TREC_tested', 'if_yes', 'pid_Vaccine_responses_tested_Lymphocyte_functional_tests', 'pha', 'anti_cd', 'others',
         'pid_eexpression_studies', 'pid_scid', 'pid_Expression_CD123', 'pid_hlh', 'pid_Expression_Perforin_expression', 'pid_Expression_CD107a_on_NK_cells', 'pid_Expression_CD107a_on_CD8_cells', 'pid_mxc2',
         'pid_Expression_hda_hr_cells', 'pid_foxp3', 'pid_Expression_th1_cells', 'pid_xla', 'btk', 'pid_lad', 'cd18', 'cd11', 'pid_msmd', 'pid_cd212_lymphocytes', 'pid_cd119_monocytes', 'pid_ifn_gama_monocyte',
         'pid_stati_monocyte', 'pid_stat4_monocyte', 'pid_higm', 'cd154', 'cd40', 'pid_was', 'wasp', 'pid_hige', 'DOCK8', 'STAT3', 'TH17', 'pid_Vaccine_responses_Complement_function', 'C2', 'C3', 'C4', 'Cq', 'CH50',
         'AH50', 'factorD', 'factorH', 'factorI', 'Properdin', 'pid_Vaccine_responses_Beta_Repertoire_analysis', 'pid_Vaccine_responses_Beta_yesRepertoire_analysis', 'pid_Vaccine_responses_Auto_antibodies', 'ANA',
         'Anti_neutrophil_antibody', 'Anti_platelet_antibody', 'Anti_C1q_antibody', 'Anti_C1_esterase_antibody', 'ada_enzyme', 'pnp_enzyme', 'NBT', 'pid_Vaccine_responses_DHR', 'yes',
         'pid_Vaccine_responses_Flow_cytometric_expression_b558', 'pid_Vaccine_responses_Flow_cytometric_expression1', 'pid_Vaccine_responses_Flow_cytometric_expression_p67phox',
         'pid_Vaccine_responses_Flow_cytometric_expression_p40phox', 'pid_Vaccine_responses_Flow_cytometric_expression_p22', 'Maternal_engraftment', 'Alfa_feto_protein', 'Alfa_feto_protein_yes', 'Karyotype',
         'Karyotype_finding', 'Chromosomal', 'Chromosomal_finding', 'Radiological_investigation', 'Radiological_investigation_finding', 'FISH', 'FISH_finding', 'any_other', 'any_other_finding',
         'pid_Vaccine_responses_Molecular_diagnosis', 'tb_Nscid', 'tb_Pscid', 'pid_malignancy_RFXANK', 'pid_malignancy_RFXANK', 'pid_malignancy_RFX5', 'pid_malignancy_RFXAP', 'pid_malignancy_DOCK8',
         'pid_malignancy_CD40', 'pid_malignancy_CD40L', 'pid_malignancy_STAT3', 'pid_malignancy_PGM3', 'pid_malignancy_SPJNKS', 'pid_malignancy_WAS', 'pid_malignancy_ATM', 'pid_malignancy_LDC22', 'pid_malignancy_BtK',
         'pid_malignancy_CVID', 'pid_malignancy_PRF1', 'pid_malignancy_STX11', 'pid_malignancy_UNC13D', 'pid_malignancy_STXBP2', 'pid_malignancy_FAAP24', 'pid_malignancy_SLC7A7', 'pid_hlh_others', 'pid_hlh_other',
         'pid_malignancy_TNFRSF6', 'pid_malignancy_TNFSF6', 'pid_malignancy_CASP8', 'pid_malignancy_CASP10', 'pid_malignancy_FADD', 'pid_malignancy_LYST', 'pid_malignancy_RAB27A', 'pid_malignancy_CYBB',
         'pid_malignancy_NCF1', 'pid_malignancy_CYBA', 'pid_malignancy_NCF2', 'pid_malignancy_NCF4', 'pid_malignancy_CYBC1', 'pid_malignancy_G6PD', 'pid_malignancy_ITGB2', 'pid_malignancy_SLC35C1',
         'pid_malignancy_FERMT3', 'pid_malignancy_ELANE', 'pid_malignancy_HAX1', 'pid_malignancy_G6PC3', 'pid_malignancy_GFI1', 'pid_malignancy_VPS45', 'pid_malignancy_CFTR', 'pid_malignancy_IFNGR1',
         'pid_malignancy_IFNGR2', 'pid_malignancy_IL12RB1', 'pid_malignancy_STAT1', 'pid_malignancy_TYK2', 'pid_malignancy_IRF8', 'pid_malignancy_RORC', 'pid_malignancy_ISG15', 'pid_malignancy_IL12B',
         'pid_malignancy_IL12RB2', 'pid_malignancy_IL23', 'pid_malignancy_SPPL2A', 'pid_malignancy_JAK1', 'pid_malignancy_STAT1GOF', 'pid_malignancy_IL17F', 'pid_malignancy_IL17RA', 'pid_malignancy_IL17RC',
         'pid_malignancy_IRAK4', 'pid_malignancy_Myd88', 'pid_malignancy_Others_specify', 'pid_mutation_type', 'pid_type_of_variant', 'pid_zygosity', 'pid_DNA_change', 'pid_Protein_expressed_checked',
         'pid_Protein_expressed', 'pid_has_patient_received_replacement_therapy', 'pid_is_patient_currently_replacement_therapy', 'pid_Date_of_initiation_of_therapy_1', 'pid_age1', 'pid_Date_of_termination_of_therapy_2',
         'pid_reaction', 'pid_dose', 'pid_route11', 'pid_frequency', 'pid_Has_patient_used_anti_infective_medication', 'pid_courses_of_antibiotic_treatment_has_the_patient', 'pid_drug_name', 'pid_indication',
         'pid_route', 'pid_course', 'pid_adverse_reaction', 'pid_drug_name1', 'pid_indication1', 'pid_route1', 'pid_course1', 'pid_adverse_reaction1', 'pid_drug_name2', 'pid_indication2', 'pid_route2', 'pid_course2',
         'pid_adverse_reaction2', 'pid_drug_name3', 'pid_indication3', 'pid_route3', 'pid_course3', 'pid_adverse_reaction3', 'pid_drug_name4', 'pid_indication4', 'pid_route4', 'pid_course4', 'pid_adverse_reaction4',
         'pid_Immuno_modulator_medication_drug_name', 'pid_imm_indication', 'pid_imm_improvement', 'pid_imm_adverse_reaction', 'pid_Immuno_modulator_medication_drug_name1', 'pid_imm_indication1', 'pid_imm_improvement1',
         'pid_imm_adverse_reaction1', 'pid_Immuno_modulator_medication_drug_name2', 'pid_imm_indication2', 'pid_imm_improvement2', 'pid_imm_adverse_reaction2', 'pid_Immuno_modulator_medication_drug_name3',
         'pid_imm_indication3', 'pid_imm_improvement3', 'pid_imm_adverse_reaction3', 'pid_Immuno_modulator_medication_drug_name4', 'pid_imm_indication4', 'pid_imm_improvement4', 'pid_imm_adverse_reaction4',
         'pid_surgeries', 'Other_treatment', 'pid_Has_patient_undergone_HSCT', 'pid_type_of_transplant', 'pid_outcome_alive', 'pid_outcome_alive_no_date', 'pid_outcome_alive_no_cause',
         'pid_outcome_alive_no_cause_others_specify', ])

    users = profile_pid.objects.all().prefetch_related('patient_pid').values_list('register_id__institute_name', 'uniqueId', 'pid_icmr_unique_no', 'pid_final_diagnosis', 'pid_date_of_record', 'pid_clinical_exam_date',
                                                                                  'pid_date_of_birth', 'pid_patient_name', 'pid_father_name', 'pid_mother_name', 'pid_paitent_id', 'pid_paitent_id_list',
                                                                                  'pid_patient_id_no', 'pid_father_mother_id', 'pid_father_mother_id_no', 'pid_permanent_addr', 'pid_state', 'pid_district',
                                                                                  'pid_city_name', 'pid_country_name', 'pid_land_line_no', 'pid_mother_mobile_no', 'pid_father_mobile_no', 'pid_email', 'pid_religion',
                                                                                  'pid_caste', 'pid_gender', 'pid_referred_status', 'pid_referred_by', 'pid_referred_by_desc', 'pid_consent_given', 'pid_consent_upload',
                                                                                  'pid_assent_given', 'pid_assent_upload', 'pid_hospital_name', 'pid_hospital_reg_no', 'profile_pid__pid_has_hiv_been_excluded',
                                                                                  'profile_pid__pid_date_onset_symptoms', 'profile_pid__pid_onset_date', 'profile_pid__age_onset_symptoms_years',
                                                                                  'profile_pid__age_onset_symptoms_months', 'profile_pid__pid_infections', 'profile_pid__pid_Meningitis_number_of_infection',
                                                                                  'profile_pid__pid_Meningitis_number_of_infection_last_year', 'profile_pid__Otitis_media', 'profile_pid__Otitis_media_last',
                                                                                  'profile_pid__Tonsillitis', 'profile_pid__Tonsillitis_last', 'profile_pid__Sinusitis', 'profile_pid__Sinusitis_last',
                                                                                  'profile_pid__Pneumonia_Bronchiectasis', 'profile_pid__Pneumonia_Bronchiectasis_last',
                                                                                  'profile_pid__pid_Gastroenteritis_number_of_infection', 'profile_pid__pid_Gastroenteritis_number_of_infection_last_year',
                                                                                  'profile_pid__pid_Urinary_tract_number_of_infection', 'profile_pid__pid_Urinary_tract_number_of_infection_last_year',
                                                                                  'profile_pid__tissue_infections', 'profile_pid__tissue_infections_last', 'profile_pid__Liver_abscess', 'profile_pid__Liver_abscess_last',
                                                                                  'profile_pid__pid_Septicemias_number_of_infection', 'profile_pid__pid_Septicemias_number_of_infection_last_year',
                                                                                  'profile_pid__Splenic_abscess', 'profile_pid__Splenic_abscess_last', 'profile_pid__pid_Thrush_or_fungal_number_of_infection',
                                                                                  'profile_pid__pid_Thrush_or_fungal_number_of_infection_last_year', 'profile_pid__pid_Vaccine_associated_complications',
                                                                                  'profile_pid__pid_bcg', 'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_age_onset',
                                                                                  'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_Axillary',
                                                                                  'profile_pid__pid_Vaccine_associated_complications_BCG_adenitis_Cervical',
                                                                                  'profile_pid__pid_Vaccine_associated_adenitis_Multiple_sites_yes_no', 'profile_pid__pid_Vaccine_associated_Multiple_sites',
                                                                                  'profile_pid__pid_bcg_options', 'profile_pid__pid_Vaccine_associated_complications_BCG_osis', 'profile_pid__pid_opv',
                                                                                  'profile_pid__pid_OPV_Date_Dose', 'profile_pid__pid_OPV_Flaccid_paralysis', 'profile_pid__pid_OPV_Poliovirus_isolation',
                                                                                  'profile_pid__pid_Rubella', 'profile_pid__pid_Rubella_Date_Vaccination', 'profile_pid__pid_Rubella_Symptoms_Fever',
                                                                                  'profile_pid__pid_Rubella_Symptoms_Enlarged_lymph_nodes', 'profile_pid__pid_Rubella_Symptoms_Measles_like_rash',
                                                                                  'profile_pid__pid_Measles', 'profile_pid__pid_Measles_Date_Vaccination', 'profile_pid__pid_Measles_fever',
                                                                                  'profile_pid__pid_Measles_EnlargedLymphNodes', 'profile_pid__pid_Measles_MeaslesLikeRash', 'profile_pid__pid_Failure_to_gain_weight',
                                                                                  'profile_pid__pid_autoimmunity_autoinflammation', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever',
                                                                                  'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_temp',
                                                                                  'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_duration', 'profile_pid__pid_autoimmunity_Precipitated_cold',
                                                                                  'profile_pid__pid_autoimmunity_Precipitated_cold_frequency', 'profile_pid__pid_autoimmunity_AssociatedLymphadenopathy',
                                                                                  'profile_pid__pid_autoimmunity_AbdominalSymptoms', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_1',
                                                                                  'profile_pid__pid_autoimmunity_AbdominalSymptoms_2', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_3',
                                                                                  'profile_pid__pid_autoimmunity_AbdominalSymptoms_4', 'profile_pid__pid_autoimmunity_AbdominalSymptoms_5',
                                                                                  'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_1',
                                                                                  'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_2', 'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3',
                                                                                  'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_numberJoints',
                                                                                  'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_jointDeformity',
                                                                                  'profile_pid__pid_autoimmunity_MusculoskeletalSymptoms_3_Contractures', 'profile_pid__pid_autoimmunity_Osteomyelitis',
                                                                                  'profile_pid__pid_autoimmunity_CNS_Ear_Eye', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_1', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_2',
                                                                                  'profile_pid__pid_autoimmunity_CNS_Ear_Eye3', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_4',
                                                                                  'profile_pid__pid_autoimmunity_CNS_Ear_Eye_5', 'profile_pid__pid_autoimmunity_CNS_Ear_Eye_6',
                                                                                  'profile_pid__pid_autoimmunity_CNS_Ear_Eye_7', 'profile_pid__pid_Skin_Mucosal', 'profile_pid__pid_Skin_Mucosal_1',
                                                                                  'profile_pid__pid_Skin_Mucosal_2', 'profile_pid__pid_Skin_Mucosal_3', 'profile_pid__pid_Skin_Mucosal_4',
                                                                                  'profile_pid__pid_Skin_Mucosal_5', 'profile_pid__pid_Skin_Mucosal_6', 'profile_pid__pid_Skin_Mucosal_7',
                                                                                  'profile_pid__pid_Skin_Mucosal_8', 'profile_pid__pid_autoimmunity_autoinflammation_type_symptoms_fever_other',
                                                                                  'profile_pid__pid_ALLERGY_ATOPY', 'profile_pid__pid_ALLERGY_ATOPY_opn', 'profile_pid__pid_MALIGNANCY',
                                                                                  'profile_pid__pid_MALIGNANCY_diagnosis', 'profile_pid__pid_MALIGNANCY_diagnosis_present_before_diagnosis',
                                                                                  'profile_pid__pid_MALIGNANCY_diagnosis_options', 'profile_pid__pid_MALIGNANCY_diagnosis_Biologic',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral', 'profile_pid__pid_ORGANISM_ISOLATED_viral_1', 'profile_pid__pid_ORGANISM_ISOLATED_viral_2',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_3', 'profile_pid__pid_ORGANISM_ISOLATED_viral_4', 'profile_pid__pid_ORGANISM_ISOLATED_viral_5',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_6', 'profile_pid__pid_ORGANISM_ISOLATED_viral_7', 'profile_pid__pid_ORGANISM_ISOLATED_viral_8',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_9', 'profile_pid__pid_ORGANISM_ISOLATED_viral_10',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_11', 'profile_pid__pid_ORGANISM_ISOLATED_viral_12',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_13', 'profile_pid__pid_ORGANISM_ISOLATED_viral_14',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_viral_14_specify', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_1', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_2',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_3', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_4',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_5', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_6',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_7', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_8',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_9', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_10',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_11', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_12',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_13', 'profile_pid__pid_ORGANISM_ISOLATED_Bacterial_14',
                                                                                  'profile_pid__pid_ORGANISM_ISOLATED_bacterial_14_specify', 'profile_pid__pid_Fungal', 'profile_pid__pid_Fungal_1',
                                                                                  'profile_pid__pid_Fungal_2', 'profile_pid__pid_Fungal_3', 'profile_pid__pid_Fungal_4', 'profile_pid__pid_Fungal_5',
                                                                                  'profile_pid__pid_Fungal_6', 'profile_pid__pid_Fungal_6_specify', 'profile_pid__pid_Mycobacterial', 'profile_pid__pid_Mycobacterial_1',
                                                                                  'profile_pid__pid_Mycobacterial_2', 'profile_pid__pid_Mycobacterial_3', 'profile_pid__pid_FamilyHistory_Consanguinity',
                                                                                  'profile_pid__pid_FamilyHistory_Consanguinity_degree', 'profile_pid__pid_FamilyHistory_HistoryYoung_Children',
                                                                                  'profile_pid__pid_FamilyHistory_HistoryYoung_Children_numberSiblingDeaths', 'profile_pid__pid_FamilyHistory_death_cause',
                                                                                  'profile_pid__pid_FamilyHistory_deaths_male_member', 'profile_pid__pid_FamilyHistory_deaths_male_member_relations',
                                                                                  'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID',
                                                                                  'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID_diagnosis',
                                                                                  'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID_relation',
                                                                                  'profile_pid__pid_FamilyHistory_diagnosed_PID_listed_registry', 'profile_pid__pid_FamilyHistory_reason_pid_evaluation',
                                                                                  'profile_pid__pid_clinical_exam_Anthropometry_wieght', 'profile_pid__pid_clinical_exam_Anthropometry_Height',
                                                                                  'profile_pid__pid_clinical_exam_Anthropometry_HeadCircumference', 'profile_pid__pid_DistinctivePhenotypeaDysmorphicFacies',
                                                                                  'profile_pid__pid_DistinctivePhenotypeaaHypoPigmentedHair', 'profile_pid__pid_DistinctivePhenotypeabTeethAbnormalities',
                                                                                  'profile_pid__pid_DistinctivePhenotypeacAbsentTonsil', 'profile_pid__pid_DistinctivePhenotypeadOralUlcers',
                                                                                  'profile_pid__pid_DistinctivePhenotypeadeSkinHypopigmentation', 'profile_pid__pid_DistinctivePhenotypeadefLymphAdenopathy',
                                                                                  'profile_pid__pid_DistinctivePhenotypeadefLymphAdenopathy_options', 'profile_pid__pid_DistinctivePhenotypegHepatosplenomegaly',
                                                                                  'profile_pid__pid_DistinctivePhenotypeSkeletalSystemAbnormalities', 'profile_pid__pid_DistinctivePhenotypeBCG_Scar',
                                                                                  'profile_pid__pid_DistinctivePhenotyFindingaRespiratory', 'profile_pid__pid_DistinctivePhenotyFindingCardiovascular',
                                                                                  'profile_pid__pid_DistinctivePhenotyFindingcAbdominal', 'profile_pid__pid_DistinctivePhenotyFindingdCNS',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryImmunodeficiencyAffecting', 'profile_pid__pid_ImmunodeficiencyAffecting_other_specify',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryCIDAssociated_Other_Specify', 'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody_yes_no',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody', 'profile_pid__pid_BroadDiagnosisCategoryPredominantAntibody_other_specify',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryDiseasesImmune_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects_yes_no',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects', 'profile_pid__pid_BroadDiagnosisCategoryCongenitalDefects_other_specify',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryDefectsIntrinsic_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory_yes_no',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory', 'profile_pid__pid_BroadDiagnosisCategoryAutoinflammatory_other_specify',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryComplementDeficiency_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryComplementDeficiency',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure_yes_no', 'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryMarrowFailure_other_specify', 'profile_pid__pid_BroadDiagnosisCategoryPhenocopies_yes_no',
                                                                                  'profile_pid__pid_BroadDiagnosisCategoryPhenocopies', 'profile_pid__pid_BroadDiagnosisCategoryPhenocopies_other_specify',
                                                                                  'profile_pid__pid_CBC_Date', 'profile_pid__pid_CBC_Date1', 'profile_pid__pid_CBC_Date2', 'profile_pid__pid_CBC_Date3',
                                                                                  'profile_pid__pid_CBC_Hb', 'profile_pid__pid_CBC_Hb1', 'profile_pid__pid_CBC_Hb2', 'profile_pid__pid_CBC_Hb3', 'profile_pid__pid_CBC_wbc',
                                                                                  'profile_pid__pid_CBC_wbc1', 'profile_pid__pid_CBC_wbc2', 'profile_pid__pid_CBC_wbc3', 'profile_pid__pid_CBC_wbc_level',
                                                                                  'profile_pid__pid_CBC_wbc1_level', 'profile_pid__pid_CBC_wbc2_level', 'profile_pid__pid_CBC_wbc3_level',
                                                                                  'profile_pid__pid_CBC_Lymphcytes', 'profile_pid__pid_CBC_Lymphcytes1', 'profile_pid__pid_CBC_Lymphcytes2',
                                                                                  'profile_pid__pid_CBC_Lymphcytes3', 'profile_pid__pid_CBC_PMN', 'profile_pid__pid_CBC_PMN1', 'profile_pid__pid_CBC_PMN2',
                                                                                  'profile_pid__pid_CBC_PMN3', 'profile_pid__pid_CBC_Eosinophils', 'profile_pid__pid_CBC_Eosinophils1', 'profile_pid__pid_CBC_Eosinophils2',
                                                                                  'profile_pid__pid_CBC_Eosinophils3', 'profile_pid__pid_CBC_Basophils', 'profile_pid__pid_CBC_Basophils1',
                                                                                  'profile_pid__pid_CBC_Basophils2', 'profile_pid__pid_CBC_Basophils3', 'profile_pid__pid_CBC_Monocytes', 'profile_pid__pid_CBC_Monocytes1',
                                                                                  'profile_pid__pid_CBC_Monocytes2', 'profile_pid__pid_CBC_Monocytes3', 'profile_pid__pid_CBC_Platelets', 'profile_pid__pid_CBC_Platelets1',
                                                                                  'profile_pid__pid_CBC_Platelets2', 'profile_pid__pid_CBC_Platelets3', 'profile_pid__pid_M_Platelets', 'profile_pid__pid_M_Platelets1',
                                                                                  'profile_pid__pid_M_Platelets2', 'profile_pid__pid_M_Platelets3', 'profile_pid__pid_phenotype_Absolute_Lymphocyte_count',
                                                                                  'profile_pid__pid_phenotype_Absolute_Lymphocyte_count_level', 'profile_pid__pid_phenotype_CD3_T_cells',
                                                                                  'profile_pid__pid_phenotype_CD3_T_cells_level', 'profile_pid__pid_CD4_Helper_T', 'profile_pid__pid_CD4_Helper_T_level',
                                                                                  'profile_pid__pid_phenotype_CD8_Cytotoxic_T_cells', 'profile_pid__pid_phenotype_CD8_Cytotoxic_T_cells_level',
                                                                                  'profile_pid__pid_phenotype_CD19_B_cells', 'profile_pid__pid_phenotype_CD19_B_cells_level', 'profile_pid__pid_phenotype_CD20_B_cells',
                                                                                  'profile_pid__pid_phenotype_CD20_B_cells_level', 'profile_pid__pid_phenotype_CD56CD16_NK_cells',
                                                                                  'profile_pid__pid_phenotype_CD56CD16_NK_cells_level', 'profile_pid__pid_phenotype_CD25', 'profile_pid__pid_phenotype_CD25_level',
                                                                                  'profile_pid__pid_phenotype_Double_negative_T_cells', 'profile_pid__pid_phenotype_Double_negative_T_cells_level',
                                                                                  'profile_pid__Gamma_delta_T_cells', 'profile_pid__Gamma_delta_T_cells_level', 'profile_pid__pid_CD4_subset_panel_naive_cd4',
                                                                                  'profile_pid__pid_CD4_subset_panel_naive_cd4_level', 'profile_pid__pid_CD4_subset_panel_Total_Memory_CD4',
                                                                                  'profile_pid__pid_CD4_subset_panel_Total_Memory_CD4_level', 'profile_pid__CD4_CD45RA', 'profile_pid__CD4_CD45RA_level',
                                                                                  'profile_pid__CD4_CD45RO', 'profile_pid__CD4_CD45RO_level', 'profile_pid__pid_CD8_subset_panel_naive_cd8',
                                                                                  'profile_pid__pid_CD8_subset_panel_naive_cd8_level', 'profile_pid__pid_CD8_subset_panel_Total_Memory_CD8',
                                                                                  'profile_pid__pid_CD8_subset_panel_Total_Memory_CD8_level', 'profile_pid__CD8_CD45RA', 'profile_pid__CD8_CD45RA_level',
                                                                                  'profile_pid__CD8_CD45RO', 'profile_pid__CD8_CD45RO_level', 'profile_pid__pid_T_regulatory_cells',
                                                                                  'profile_pid__pid_T_regulatory_cells_level', 'profile_pid__pid_Naive_B_cells', 'profile_pid__pid_Naive_B_cells_level',
                                                                                  'profile_pid__pid_Naive_B_cells_Transitional_B_cells', 'profile_pid__pid_Naive_B_cells_Transitional_B_cells_level',
                                                                                  'profile_pid__cd27_B_cells', 'profile_pid__cd27_B_cells_level', 'profile_pid__cd27_igm_Bcells', 'profile_pid__cd27_igm_Bcells_level',
                                                                                  'profile_pid__cd27_igD_Bcells', 'profile_pid__cd27_igD_Bcells_level', 'profile_pid__pid_Immunoglobulin_IgG',
                                                                                  'profile_pid__pid_Immunoglobulin_IgG_level', 'profile_pid__pid_Immunoglobulin_IgG1', 'profile_pid__pid_Immunoglobulin_IgG1_level',
                                                                                  'profile_pid__pid_Immunoglobulin_IgG2', 'profile_pid__pid_Immunoglobulin_IgG2_level', 'profile_pid__pid_Immunoglobulin_IgG3',
                                                                                  'profile_pid__pid_Immunoglobulin_IgG3_level', 'profile_pid__pid_Immunoglobulin_IgG4', 'profile_pid__pid_Immunoglobulin_IgG4_level',
                                                                                  'profile_pid__pid_Immunoglobulin_IgA', 'profile_pid__pid_Immunoglobulin_IgA_level', 'profile_pid__pid_Immunoglobulin_IgM',
                                                                                  'profile_pid__pid_Immunoglobulin_IgM_level', 'profile_pid__pid_Immunoglobulin_IgE', 'profile_pid__pid_Immunoglobulin_IgE_level',
                                                                                  'profile_pid__pid_Immunoglobulin_IgD', 'profile_pid__pid_Immunoglobulin_IgD_level', 'profile_pid__pid_Vaccine_responses_tested',
                                                                                  'profile_pid__pid_Vaccine_responses_tested_Protein', 'profile_pid__diphtheria', 'profile_pid__tetanus',
                                                                                  'profile_pid__protien_conjugated_hib', 'profile_pid__Polysaccharide_hib', 'profile_pid__salmonella_typhi', 'profile_pid__PHI_174antigen',
                                                                                  'profile_pid__pid_Vaccine_responses_tested_Iso_hemagglutinin', 'profile_pid__Iso_hemagglutinin_antiA',
                                                                                  'profile_pid__Iso_hemagglutinin_antiB', 'profile_pid__pid_Vaccine_responses_tested_TREC_tested', 'profile_pid__if_yes',
                                                                                  'profile_pid__pid_Vaccine_responses_tested_Lymphocyte_functional_tests', 'profile_pid__pha', 'profile_pid__anti_cd',
                                                                                  'profile_pid__others', 'profile_pid__pid_eexpression_studies', 'profile_pid__pid_scid', 'profile_pid__pid_Expression_CD123',
                                                                                  'profile_pid__pid_hlh', 'profile_pid__pid_Expression_Perforin_expression', 'profile_pid__pid_Expression_CD107a_on_NK_cells',
                                                                                  'profile_pid__pid_Expression_CD107a_on_CD8_cells', 'profile_pid__pid_mxc2', 'profile_pid__pid_Expression_hda_hr_cells',
                                                                                  'profile_pid__pid_foxp3', 'profile_pid__pid_Expression_th1_cells', 'profile_pid__pid_xla', 'profile_pid__btk', 'profile_pid__pid_lad',
                                                                                  'profile_pid__cd18', 'profile_pid__cd11', 'profile_pid__pid_msmd', 'profile_pid__pid_cd212_lymphocytes',
                                                                                  'profile_pid__pid_cd119_monocytes', 'profile_pid__pid_ifn_gama_monocyte', 'profile_pid__pid_stati_monocyte',
                                                                                  'profile_pid__pid_stat4_monocyte', 'profile_pid__pid_higm', 'profile_pid__cd154', 'profile_pid__cd40', 'profile_pid__pid_was',
                                                                                  'profile_pid__wasp', 'profile_pid__pid_hige', 'profile_pid__DOCK8', 'profile_pid__STAT3', 'profile_pid__TH17',
                                                                                  'profile_pid__pid_Vaccine_responses_Complement_function', 'profile_pid__C2', 'profile_pid__C3', 'profile_pid__C4', 'profile_pid__Cq',
                                                                                  'profile_pid__CH50', 'profile_pid__AH50', 'profile_pid__factorD', 'profile_pid__factorH', 'profile_pid__factorI',
                                                                                  'profile_pid__Properdin', 'profile_pid__pid_Vaccine_responses_Beta_Repertoire_analysis',
                                                                                  'profile_pid__pid_Vaccine_responses_Beta_yesRepertoire_analysis', 'profile_pid__pid_Vaccine_responses_Auto_antibodies',
                                                                                  'profile_pid__ANA', 'profile_pid__Anti_neutrophil_antibody', 'profile_pid__Anti_platelet_antibody', 'profile_pid__Anti_C1q_antibody',
                                                                                  'profile_pid__Anti_C1_esterase_antibody', 'profile_pid__ada_enzyme', 'profile_pid__pnp_enzyme', 'profile_pid__NBT',
                                                                                  'profile_pid__pid_Vaccine_responses_DHR', 'profile_pid__yes', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_b558',
                                                                                  'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression1', 'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p67phox',
                                                                                  'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p40phox',
                                                                                  'profile_pid__pid_Vaccine_responses_Flow_cytometric_expression_p22', 'profile_pid__Maternal_engraftment',
                                                                                  'profile_pid__Alfa_feto_protein', 'profile_pid__Alfa_feto_protein_yes', 'profile_pid__Karyotype', 'profile_pid__Karyotype_finding',
                                                                                  'profile_pid__Chromosomal', 'profile_pid__Chromosomal_finding', 'profile_pid__Radiological_investigation',
                                                                                  'profile_pid__Radiological_investigation_finding', 'profile_pid__FISH', 'profile_pid__FISH_finding', 'profile_pid__any_other',
                                                                                  'profile_pid__any_other_finding', 'profile_pid__pid_Vaccine_responses_Molecular_diagnosis', 'profile_pid__tb_Nscid',
                                                                                  'profile_pid__tb_Pscid', 'profile_pid__pid_malignancy_RFXANK', 'profile_pid__pid_malignancy_RFXANK', 'profile_pid__pid_malignancy_RFX5',
                                                                                  'profile_pid__pid_malignancy_RFXAP', 'profile_pid__pid_malignancy_DOCK8', 'profile_pid__pid_malignancy_CD40',
                                                                                  'profile_pid__pid_malignancy_CD40L', 'profile_pid__pid_malignancy_STAT3', 'profile_pid__pid_malignancy_PGM3',
                                                                                  'profile_pid__pid_malignancy_SPJNKS', 'profile_pid__pid_malignancy_WAS', 'profile_pid__pid_malignancy_ATM',
                                                                                  'profile_pid__pid_malignancy_LDC22', 'profile_pid__pid_malignancy_BtK', 'profile_pid__pid_malignancy_CVID',
                                                                                  'profile_pid__pid_malignancy_PRF1', 'profile_pid__pid_malignancy_STX11', 'profile_pid__pid_malignancy_UNC13D',
                                                                                  'profile_pid__pid_malignancy_STXBP2', 'profile_pid__pid_malignancy_FAAP24', 'profile_pid__pid_malignancy_SLC7A7',
                                                                                  'profile_pid__pid_hlh_others', 'profile_pid__pid_hlh_other', 'profile_pid__pid_malignancy_TNFRSF6', 'profile_pid__pid_malignancy_TNFSF6',
                                                                                  'profile_pid__pid_malignancy_CASP8', 'profile_pid__pid_malignancy_CASP10', 'profile_pid__pid_malignancy_FADD',
                                                                                  'profile_pid__pid_malignancy_LYST', 'profile_pid__pid_malignancy_RAB27A', 'profile_pid__pid_malignancy_CYBB',
                                                                                  'profile_pid__pid_malignancy_NCF1', 'profile_pid__pid_malignancy_CYBA', 'profile_pid__pid_malignancy_NCF2',
                                                                                  'profile_pid__pid_malignancy_NCF4', 'profile_pid__pid_malignancy_CYBC1', 'profile_pid__pid_malignancy_G6PD',
                                                                                  'profile_pid__pid_malignancy_ITGB2', 'profile_pid__pid_malignancy_SLC35C1', 'profile_pid__pid_malignancy_FERMT3',
                                                                                  'profile_pid__pid_malignancy_ELANE', 'profile_pid__pid_malignancy_HAX1', 'profile_pid__pid_malignancy_G6PC3',
                                                                                  'profile_pid__pid_malignancy_GFI1', 'profile_pid__pid_malignancy_VPS45', 'profile_pid__pid_malignancy_CFTR',
                                                                                  'profile_pid__pid_malignancy_IFNGR1', 'profile_pid__pid_malignancy_IFNGR2', 'profile_pid__pid_malignancy_IL12RB1',
                                                                                  'profile_pid__pid_malignancy_STAT1', 'profile_pid__pid_malignancy_TYK2', 'profile_pid__pid_malignancy_IRF8',
                                                                                  'profile_pid__pid_malignancy_RORC', 'profile_pid__pid_malignancy_ISG15', 'profile_pid__pid_malignancy_IL12B',
                                                                                  'profile_pid__pid_malignancy_IL12RB2', 'profile_pid__pid_malignancy_IL23', 'profile_pid__pid_malignancy_SPPL2A',
                                                                                  'profile_pid__pid_malignancy_JAK1', 'profile_pid__pid_malignancy_STAT1GOF', 'profile_pid__pid_malignancy_IL17F',
                                                                                  'profile_pid__pid_malignancy_IL17RA', 'profile_pid__pid_malignancy_IL17RC', 'profile_pid__pid_malignancy_IRAK4',
                                                                                  'profile_pid__pid_malignancy_Myd88', 'profile_pid__pid_malignancy_Others_specify', 'profile_pid__pid_mutation_type',
                                                                                  'profile_pid__pid_type_of_variant', 'profile_pid__pid_zygosity', 'profile_pid__pid_DNA_change',
                                                                                  'profile_pid__pid_Protein_expressed_checked', 'profile_pid__pid_Protein_expressed',
                                                                                  'profile_pid__pid_has_patient_received_replacement_therapy', 'profile_pid__pid_is_patient_currently_replacement_therapy',
                                                                                  'profile_pid__pid_Date_of_initiation_of_therapy_1', 'profile_pid__pid_age1', 'profile_pid__pid_Date_of_termination_of_therapy_2',
                                                                                  'profile_pid__pid_reaction', 'profile_pid__pid_dose', 'profile_pid__pid_route11', 'profile_pid__pid_frequency',
                                                                                  'profile_pid__pid_Has_patient_used_anti_infective_medication', 'profile_pid__pid_courses_of_antibiotic_treatment_has_the_patient',
                                                                                  'profile_pid__pid_drug_name', 'profile_pid__pid_indication', 'profile_pid__pid_route', 'profile_pid__pid_course',
                                                                                  'profile_pid__pid_adverse_reaction', 'profile_pid__pid_drug_name1', 'profile_pid__pid_indication1', 'profile_pid__pid_route1',
                                                                                  'profile_pid__pid_course1', 'profile_pid__pid_adverse_reaction1', 'profile_pid__pid_drug_name2', 'profile_pid__pid_indication2',
                                                                                  'profile_pid__pid_route2', 'profile_pid__pid_course2', 'profile_pid__pid_adverse_reaction2', 'profile_pid__pid_drug_name3',
                                                                                  'profile_pid__pid_indication3', 'profile_pid__pid_route3', 'profile_pid__pid_course3', 'profile_pid__pid_adverse_reaction3',
                                                                                  'profile_pid__pid_drug_name4', 'profile_pid__pid_indication4', 'profile_pid__pid_route4', 'profile_pid__pid_course4',
                                                                                  'profile_pid__pid_adverse_reaction4', 'profile_pid__pid_Immuno_modulator_medication_drug_name', 'profile_pid__pid_imm_indication',
                                                                                  'profile_pid__pid_imm_improvement', 'profile_pid__pid_imm_adverse_reaction', 'profile_pid__pid_Immuno_modulator_medication_drug_name1',
                                                                                  'profile_pid__pid_imm_indication1', 'profile_pid__pid_imm_improvement1', 'profile_pid__pid_imm_adverse_reaction1',
                                                                                  'profile_pid__pid_Immuno_modulator_medication_drug_name2', 'profile_pid__pid_imm_indication2', 'profile_pid__pid_imm_improvement2',
                                                                                  'profile_pid__pid_imm_adverse_reaction2', 'profile_pid__pid_Immuno_modulator_medication_drug_name3', 'profile_pid__pid_imm_indication3',
                                                                                  'profile_pid__pid_imm_improvement3', 'profile_pid__pid_imm_adverse_reaction3', 'profile_pid__pid_Immuno_modulator_medication_drug_name4',
                                                                                  'profile_pid__pid_imm_indication4', 'profile_pid__pid_imm_improvement4', 'profile_pid__pid_imm_adverse_reaction4',
                                                                                  'profile_pid__pid_surgeries', 'profile_pid__Other_treatment', 'profile_pid__pid_Has_patient_undergone_HSCT',
                                                                                  'profile_pid__pid_type_of_transplant', 'profile_pid__pid_outcome_alive', 'profile_pid__pid_outcome_alive_no_date',
                                                                                  'profile_pid__pid_outcome_alive_no_cause', 'profile_pid__pid_outcome_alive_no_cause_others_specify', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_pid_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pid_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'pid_final_diagnosis', 'pid_date_of_record', 'pid_clinical_exam_date',
         'pid_has_hiv_been_excluded', 'pid_date_onset_symptoms', 'pid_onset_date', 'age_onset_symptoms_years', 'age_onset_symptoms_months', 'pid_infections',
         'pid_Meningitis_number_of_infection', 'pid_Meningitis_number_of_infection_last_year', 'Otitis_media', 'Otitis_media_last', 'Tonsillitis',
         'Tonsillitis_last', 'Sinusitis', 'Sinusitis_last', 'Pneumonia_Bronchiectasis', 'Pneumonia_Bronchiectasis_last', 'pid_Gastroenteritis_number_of_infection',
         'pid_Gastroenteritis_number_of_infection_last_year', 'pid_Urinary_tract_number_of_infection', 'pid_Urinary_tract_number_of_infection_last_year', 'tissue_infections',
         'tissue_infections_last', 'Liver_abscess', 'Liver_abscess_last', 'pid_Septicemias_number_of_infection', 'pid_Septicemias_number_of_infection_last_year', 'Splenic_abscess',
         'Splenic_abscess_last', 'pid_Thrush_or_fungal_number_of_infection', 'pid_Thrush_or_fungal_number_of_infection_last_year', 'pid_Vaccine_associated_complications',
          'pid_Failure_to_gain_weight', 'pid_no_times_hospitalised', 'pid_autoimmunity_autoinflammation',
          'pid_ALLERGY_ATOPY', 'pid_ALLERGY_ATOPY_opn',
         'pid_MALIGNANCY','pid_ORGANISM_ISOLATED_viral',
          'pid_ORGANISM_ISOLATED_Bacterial',  'pid_Fungal',  'pid_Mycobacterial',  'pid_FamilyHistory_Consanguinity',  'pid_FamilyHistory_HistoryYoung_Children',
          'pid_FamilyHistory_deaths_male_member',  'pid_FamilyHistory_deaths_male_member_diagnosed_PID',

         'pid_FamilyHistory_reason_pid_evaluation', 'pid_DistinctivePhenotypeacAbsentTonsil', 'pid_DistinctivePhenotypeadefLymphAdenopathy',

         'pid_DistinctivePhenotypegHepatosplenomegaly', 'pid_DistinctivePhenotypeBCG_Scar', 'pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no', 'pid_CBC_Date',  'pid_CBC_Hb',   'pid_CBC_wbc','pid_CBC_wbc_level',
          'pid_CBC_Lymphcytes',  'pid_CBC_PMN',
          'pid_CBC_Platelets',  'pid_M_Platelets',  'pid_phenotype_Absolute_Lymphocyte_count',  'pid_phenotype_CD3_T_cells',
          'pid_CD4_Helper_T',  'pid_phenotype_CD8_Cytotoxic_T_cells', 'pid_phenotype_CD19_B_cells',
          'pid_phenotype_CD20_B_cells',  'pid_phenotype_CD56CD16_NK_cells',
         'pid_Immunoglobulin_IgG',
          'pid_Immunoglobulin_IgA',
         'pid_Immunoglobulin_IgM', 'pid_Immunoglobulin_IgE',  'pid_Immunoglobulin_IgD',

         'NBT',  'pid_Vaccine_responses_Molecular_diagnosis', 'pid_Immuno_modulator_medication_drug_name',
          'pid_Has_patient_undergone_HSCT', 'pid_type_of_transplant', 'pid_outcome_alive', ])

    users = profile_pid.objects.all().prefetch_related('patient_pid').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'pid_icmr_unique_no', 'pid_final_diagnosis', 'pid_date_of_record', 'pid_clinical_exam_date',         'profile_pid__pid_has_hiv_been_excluded', 'profile_pid__pid_date_onset_symptoms',
	'profile_pid__pid_onset_date', 'profile_pid__age_onset_symptoms_years', 'profile_pid__age_onset_symptoms_months', 'profile_pid__pid_infections',
         'profile_pid__pid_Meningitis_number_of_infection', 'profile_pid__pid_Meningitis_number_of_infection_last_year', 'profile_pid__Otitis_media', 'profile_pid__Otitis_media_last', 'profile_pid__Tonsillitis',
         'profile_pid__Tonsillitis_last', 'profile_pid__Sinusitis', 'profile_pid__Sinusitis_last', 'profile_pid__Pneumonia_Bronchiectasis', 'profile_pid__Pneumonia_Bronchiectasis_last', 'profile_pid__pid_Gastroenteritis_number_of_infection',
         'profile_pid__pid_Gastroenteritis_number_of_infection_last_year', 'profile_pid__pid_Urinary_tract_number_of_infection', 'profile_pid__pid_Urinary_tract_number_of_infection_last_year', 'profile_pid__tissue_infections',

         'profile_pid__tissue_infections_last', 'profile_pid__Liver_abscess', 'profile_pid__Liver_abscess_last', 'profile_pid__pid_Septicemias_number_of_infection', 'profile_pid__pid_Septicemias_number_of_infection_last_year', 'profile_pid__Splenic_abscess',
         'profile_pid__Splenic_abscess_last', 'profile_pid__pid_Thrush_or_fungal_number_of_infection', 'profile_pid__pid_Thrush_or_fungal_number_of_infection_last_year', 'profile_pid__pid_Vaccine_associated_complications',
          'profile_pid__pid_Failure_to_gain_weight', 'profile_pid__pid_no_times_hospitalised', 'profile_pid__pid_autoimmunity_autoinflammation',
          'profile_pid__pid_ALLERGY_ATOPY', 'profile_pid__pid_ALLERGY_ATOPY_opn',
         'profile_pid__pid_MALIGNANCY','profile_pid__pid_ORGANISM_ISOLATED_viral',
          'profile_pid__pid_ORGANISM_ISOLATED_Bacterial',  'profile_pid__pid_Fungal',  'profile_pid__pid_Mycobacterial',  'profile_pid__pid_FamilyHistory_Consanguinity',  'profile_pid__pid_FamilyHistory_HistoryYoung_Children',
          'profile_pid__pid_FamilyHistory_deaths_male_member',  'profile_pid__pid_FamilyHistory_deaths_male_member_diagnosed_PID',

         'profile_pid__pid_FamilyHistory_reason_pid_evaluation', 'profile_pid__pid_DistinctivePhenotypeacAbsentTonsil', 'profile_pid__pid_DistinctivePhenotypeadefLymphAdenopathy',

         'profile_pid__pid_DistinctivePhenotypegHepatosplenomegaly', 'profile_pid__pid_DistinctivePhenotypeBCG_Scar', 'profile_pid__pid_BroadDiagnosisCategoryImmunodeficiencyAffecting_yes_no', 'profile_pid__pid_CBC_Date',
	 'profile_pid__pid_CBC_Hb',   'profile_pid__pid_CBC_wbc','profile_pid__pid_CBC_wbc_level',
          'profile_pid__pid_CBC_Lymphcytes',  'profile_pid__pid_CBC_PMN',
          'profile_pid__pid_CBC_Platelets',  'profile_pid__pid_M_Platelets',  'profile_pid__pid_phenotype_Absolute_Lymphocyte_count',  'profile_pid__pid_phenotype_CD3_T_cells',
          'profile_pid__pid_CD4_Helper_T',  'profile_pid__pid_phenotype_CD8_Cytotoxic_T_cells', 'profile_pid__pid_phenotype_CD19_B_cells',
          'profile_pid__pid_phenotype_CD20_B_cells',  'profile_pid__pid_phenotype_CD56CD16_NK_cells',
         'profile_pid__pid_Immunoglobulin_IgG',
          'profile_pid__pid_Immunoglobulin_IgA',
         'profile_pid__pid_Immunoglobulin_IgM', 'profile_pid__pid_Immunoglobulin_IgE',  'profile_pid__pid_Immunoglobulin_IgD',

         'profile_pid__NBT',  'profile_pid__pid_Vaccine_responses_Molecular_diagnosis', 'profile_pid__pid_Immuno_modulator_medication_drug_name',
          'profile_pid__pid_Has_patient_undergone_HSCT', 'profile_pid__pid_type_of_transplant', 'profile_pid__pid_outcome_alive',)
    for user in users:
        writer.writerow(user)

    return response

@login_required(login_url='login')
def export_nmd_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam', 'nmd_date_of_birth', 'nmd_patient_name', 'nmd_father_name',
         'nmd_mother_name', 'nmd_paitent_id_yes_no', 'nmd_paitent_id', 'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district', 'nmd_city_name',
         'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion', 'nmd_caste', 'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc',
         'nmd_consent_given', 'nmd_consent_upload', 'nmd_assent_given', 'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no', 'NMD_patient_education', 'NMD_patient_occupation', 'NMD_father_edu_status',
         'NMD_father_occupation', 'NMD_mother_edu_status', 'NMD_mother_occupation', 'NMD_monthly_income_status', 'NMD_diagnosis_type', 'NMD_enrollment_status', 'diagnosis_age', 'aproximate_age', 'symptoms_age_onset',
         'onset_age', 'pedigree', 'positive_family_hist', 'positive_family_siblings', 'positive_family_sibling_nubmer_affected', 'positive_family_cousins', 'positive_family_sCousins_nubmer_affected',
         'positive_family_Maternal_uncles', 'positive_family_Maternal_uncles_nubmer_affected', 'positive_family_Grand_materna', 'positive_family_Grand_materna_affected', 'positive_family_mothers',
         'difficulty_running_walking_fast', 'unable_rise_low_chair_floor', 'repeated_false', 'muscle_hypertrophy', 'mental_sub_normality', 'learning_disability', 'delayed_motor_milestrones',
         'symtoms_signs_other_specify', 'CEF_anthropometric_wieght', 'CEF_anthropometric_height', 'CEF_anthropometric_head_circumference', 'MP_MRC_grade_upperlimb_proximal_muscles',
         'MP_MRC_grade_upperlimb_distal_muscles', 'MP_MRC_grade_lowerlimb_proximal_muscles', 'MP_MRC_grade_lowerlimb_distal_muscles', 'functional_status_Independently_ambulant',
         'functional_status_NeedsPhysicalAssistance', 'functional_status_AmbulantHome', 'functional_status_WheelchairBound', 'functional_status_WheelchairBound_age', 'functional_status_BedBound',
         'functional_status_BedBound_age', 'functional_status_FunctionalScoreAvailable', 'functional_status_BrookeScale', 'functional_status_VignosScale', 'intelligent_quotient_tested',
         'intelligent_quotient_tested_if_yes', 'autism', 'Contractures', 'Contractures_ankle', 'Contractures_knee', 'Contractures_hips', 'Contractures_elbows', 'Scoliosis', 'Kyphosis', 'Respiratory_difficulty',
         'LaboratoryInvestigation_serum_ck_lvel', 'LaboratoryInvestigation_Cardiac_Evaluation', 'LaboratoryInvestigation_ecg_status', 'LaboratoryInvestigation_ecg_normal_abnormal', 'NMD_diagnosis_type',
         'LaboratoryInvestigation_2DECHO_status', 'LaboratoryInvestigation_2DECHO_normal_abnormal', 'NMD_diagnosis_type', 'pulmonary_function_tests', 'pulmonary_function_tests_normal_abnormal',
         'pulmonary_function_forced_vital_capacity', 'genetic_diagnosis_confirmed_mPCR', 'genetic_diagnosis_confirmed_MLPA', 'genetic_diagnosis_confirmed_MicroArray', 'genetic_diagnosis_confirmed_SangerSequencing',
         'genetic_diagnosis_confirmed_next_generation', 'genetic_diagnosis_next_generation', 'enetic_diagnosis_next_generation_TargetedPanel', 'enetic_diagnosis_next_generation_WholeExomeSequencing',
         'enetic_diagnosis_next_generation_WholeGenomeSequencing', 'upload_genetic_report', 'NMD_diagnosis_type', 'inframe_outframe', 'list_of_deleted_exons', 'list_of_duplicate_exons', 'mutation_identified_Missense',
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
         'mother_carrier_status', 'mother_carrier_status_outcome', 'sister_carrier_status', 'sister_carrier_status_outcome', 'gender', 'born_consanguineous_parents', 'consanguineous_parents_if_yes',
         'familyHistory_sibling_affected', 'familyHistory_sibling_affected_number', 'upload_pedegree', 'age_first_evaluation', 'age_at_onset', 'age_onset_options', 'age_onset_options_yes_no', 'ConditionBirth_cry',
         'conditionBirth_feedingDifficulty', 'conditionBirth_RespiratoryDistress', 'conditionBirth_ReceivedOxygen', 'conditionBirth_KeptIncubator', 'arthrogryposisBirth', 'RecurrentLowerRespiratory', 'Scoliosis',
         'Kyphosis', 'Contractures', 'HipDislocation', 'Fractures', 'MotorSystemExam_Minipolymyoclonus', 'MotorSystemExam_TongueFasciculations', 'MotorSystemExam_MotorPower_ModifiedMRCgrade',
         'MotorSystemExam_UpperLimb_ProximalMuscles', 'MotorSystemExam_UpperLimb_DistalMuscles', 'MotorSystemExam_lowerLimb_ProximalMuscles', 'MotorSystemExam_lowerLimb_DistalMuscles', 'LimbWeakness',
         'LimbWeakness_if_yes_UpperLimb_ProximalGrade', 'LimbWeakness_if_yes_UpperLimb_DistalGrade', 'LimbWeakness_if_yes_LowerLimb_ProximalGrade', 'LimbWeakness_if_yes_LowerLimb_DistalGrade', 'currentMotor_ability',
         'currentMotor_WheelchairBound', 'currentMotor_WheelchairBound_if_yes_age', 'currentMotor_BedBound', 'currentMotor_BedBound_age', 'HMAS', 'HMAS_score', 'clinicalDiagnosis_SMA0', 'clinicalDiagnosis_SMA1',
         'clinicalDiagnosis_SMA2', 'clinicalDiagnosis_SMA3', 'clinicalDiagnosis_SMA4', 'LaboratoryInvestigation_CK_Level', 'geneticDiagnosis', 'NAIP_deletion', 'geneticFindings_gene', 'geneticFindings_Location',
         'geneticFindings_Variant', 'geneticFindings_Zygosity', 'geneticFindings_Disease', 'geneticFindings_Inheritance', 'geneticFindings_classification', 'geneticDiagnosis2', 'final_diagnosis_1',
         'genetic_report_upload', 'Treatment_RespiratorySupport', 'Treatment_RespiratorySupport_ifyes_BIPAP', 'Treatment_RespiratorySupport_ifyes_IPPR', 'Treatment_RespiratorySupport_ifyes_Ventilation', 'Feeding_Oral',
         'Feeding_Nasogastric', 'Feeding_PEG', 'OperatedScoliosis', 'OperatedScoliosis_ifyes_age', 'CurrentPastTreatment_ReceivedNusinersin', 'CurrentPastTreatment_ReceivedNusinersin_if_yes',
         'CurrentPastTreatment_ReceivedRisdiplam', 'CurrentPastTreatment_ReceivedRisdiplam_if_yes_age', 'CurrentPastTreatment_ReceivedZolgensma', 'CurrentPastTreatment_ReceivedZolgensma_if_yes_age', 'finalOutcome',
         'finalOutcome_if_dead_age', 'finalOutcome_death_place1', 'finalOutcome_deathCause', 'finalOutcome_deathCause_known', 'finalOutcome_death_place2', 'carrier_testing_parents', 'prenatal_testing',
         'prenatal_testing_if_yes', 'limb_gender', 'evaluation_age', 'limb_symptoms_onset_age', 'limb_born_consanguineous_parents', 'limb_consanguineous_parents_if_yes', 'MuscleHypertrophy', 'MuscleWasting',
         'Contractures_3', 'Contractures_3_ankle', 'Contractures_3_knee', 'Contractures_3_hip', 'Contractures_3_elbow', 'Contractures_3_neck', 'limb_weakness', 'limb_weakness_UpperlimbProximal',
         'limb_weakness_UpperlimbDistal', 'limb_weakness_LowerlimbProximal', 'limb_weakness_lowerlimbDistal', 'BulbarWeakness', 'BulbarWeakness_if_yes', 'CardiacSymptoms', 'cardiac_symptoms_options',
         'RespiratorySymptoms', 'RespiratorySymptoms_options', 'InheritancePattern', 'PositiveFamilyHistory', 'PositiveFamilyHistory_SiblingsAffected', 'PositiveFamilyHistory_SiblingsAffected_number',
         'PositiveFamilyHistory_MotherAffected', 'PositiveFamilyHistory_FatherAffected', 'PositiveFamilyHistory_GrandmotherAffected', 'PositiveFamilyHistory_GrandFatherAffected', 'PositiveFamilyHistory_CousinsAffected',
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

    users = profile_nmd.objects.all().prefetch_related('demographicnmd', 'dystonmd', 'spinalnmd', 'limbnmd').values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis',
                                                                                                                         'nmd_date_of_records',
                                                                                                                         'nmd_date_of_clinical_exam',
                                                                                                                         'nmd_date_of_birth', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name',
                                                                                                                         'nmd_paitent_id_yes_no', 'nmd_paitent_id',
                                                                                                                         'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr',
                                                                                                                         'nmd_state', 'nmd_district', 'nmd_city_name',
                                                                                                                         'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no',
                                                                                                                         'nmd_email', 'nmd_religion', 'nmd_caste',
                                                                                                                         'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc',
                                                                                                                         'nmd_consent_given', 'nmd_consent_upload', 'nmd_assent_given',
                                                                                                                         'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                                                         'demographicnmd__NMD_patient_education',
                                                                                                                         'demographicnmd__NMD_patient_occupation', 'demographicnmd__NMD_father_edu_status',
                                                                                                                         'demographicnmd__NMD_father_occupation',
                                                                                                                         'demographicnmd__NMD_mother_edu_status', 'demographicnmd__NMD_mother_occupation',
                                                                                                                         'demographicnmd__NMD_monthly_income_status',
                                                                                                                         'dystonmd__NMD_diagnosis_type', 'dystonmd__NMD_enrollment_status', 'dystonmd__diagnosis_age',
                                                                                                                         'dystonmd__aproximate_age',
                                                                                                                         'dystonmd__symptoms_age_onset', 'dystonmd__onset_age', 'dystonmd__pedigree',
                                                                                                                         'dystonmd__positive_family_hist',
                                                                                                                         'dystonmd__positive_family_siblings', 'dystonmd__positive_family_sibling_nubmer_affected',
                                                                                                                         'dystonmd__positive_family_cousins',
                                                                                                                         'dystonmd__positive_family_sCousins_nubmer_affected', 'dystonmd__positive_family_Maternal_uncles',
                                                                                                                         'dystonmd__positive_family_Maternal_uncles_nubmer_affected',
                                                                                                                         'dystonmd__positive_family_Grand_materna',
                                                                                                                         'dystonmd__positive_family_Grand_materna_affected', 'dystonmd__positive_family_mothers',
                                                                                                                         'dystonmd__difficulty_running_walking_fast',
                                                                                                                         'dystonmd__unable_rise_low_chair_floor', 'dystonmd__repeated_false',
                                                                                                                         'dystonmd__muscle_hypertrophy', 'dystonmd__mental_sub_normality',
                                                                                                                         'dystonmd__learning_disability', 'dystonmd__delayed_motor_milestrones',
                                                                                                                         'dystonmd__symtoms_signs_other_specify',
                                                                                                                         'dystonmd__CEF_anthropometric_wieght', 'dystonmd__CEF_anthropometric_height',
                                                                                                                         'dystonmd__CEF_anthropometric_head_circumference',
                                                                                                                         'dystonmd__MP_MRC_grade_upperlimb_proximal_muscles',
                                                                                                                         'dystonmd__MP_MRC_grade_upperlimb_distal_muscles',
                                                                                                                         'dystonmd__MP_MRC_grade_lowerlimb_proximal_muscles',
                                                                                                                         'dystonmd__MP_MRC_grade_lowerlimb_distal_muscles',
                                                                                                                         'dystonmd__functional_status_Independently_ambulant',
                                                                                                                         'dystonmd__functional_status_NeedsPhysicalAssistance',
                                                                                                                         'dystonmd__functional_status_AmbulantHome', 'dystonmd__functional_status_WheelchairBound',
                                                                                                                         'dystonmd__functional_status_WheelchairBound_age', 'dystonmd__functional_status_BedBound',
                                                                                                                         'dystonmd__functional_status_BedBound_age',
                                                                                                                         'dystonmd__functional_status_FunctionalScoreAvailable', 'dystonmd__functional_status_BrookeScale',
                                                                                                                         'dystonmd__functional_status_VignosScale', 'dystonmd__intelligent_quotient_tested',
                                                                                                                         'dystonmd__intelligent_quotient_tested_if_yes',
                                                                                                                         'dystonmd__autism', 'dystonmd__Contractures_dmd', 'dystonmd__Contractures_ankle',
                                                                                                                         'dystonmd__Contractures_knee', 'dystonmd__Contractures_hips',
                                                                                                                         'dystonmd__Contractures_elbows', 'dystonmd__Scoliosis_dmd', 'dystonmd__Kyphosis_dmd',
                                                                                                                         'dystonmd__Respiratory_difficulty',
                                                                                                                         'dystonmd__LaboratoryInvestigation_serum_ck_lvel',
                                                                                                                         'dystonmd__LaboratoryInvestigation_Cardiac_Evaluation',
                                                                                                                         'dystonmd__LaboratoryInvestigation_ecg_status',
                                                                                                                         'dystonmd__LaboratoryInvestigation_ecg_normal_abnormal', 'dystonmd__NMD_diagnosis_type',
                                                                                                                         'dystonmd__LaboratoryInvestigation_2DECHO_status',
                                                                                                                         'dystonmd__LaboratoryInvestigation_2DECHO_normal_abnormal', 'dystonmd__NMD_diagnosis_type',
                                                                                                                         'dystonmd__pulmonary_function_tests', 'dystonmd__pulmonary_function_tests_normal_abnormal',
                                                                                                                         'dystonmd__pulmonary_function_forced_vital_capacity', 'dystonmd__genetic_diagnosis_confirmed_mPCR',
                                                                                                                         'dystonmd__genetic_diagnosis_confirmed_MLPA', 'dystonmd__genetic_diagnosis_confirmed_MicroArray',
                                                                                                                         'dystonmd__genetic_diagnosis_confirmed_SangerSequencing',
                                                                                                                         'dystonmd__genetic_diagnosis_confirmed_next_generation',
                                                                                                                         'dystonmd__genetic_diagnosis_next_generation',
                                                                                                                         'dystonmd__enetic_diagnosis_next_generation_TargetedPanel',
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
                                                                                                                         'dystonmd__mutation_identified_Splicesite_mutation',
                                                                                                                         'dystonmd__mutation_identified_InframeInsertion',
                                                                                                                         'dystonmd__mutation_identified_InframeInsertion_mutation',
                                                                                                                         'dystonmd__mutation_identified_InframeDeletion',
                                                                                                                         'dystonmd__mutation_identified_InframeDeletion_mutation', 'dystonmd__mutation_identified_INDEL',
                                                                                                                         'dystonmd__mutation_identified_INDEL_mutation', 'dystonmd__mutation_identified_Others',
                                                                                                                         'dystonmd__mutation_identified_Others_mutation',
                                                                                                                         'dystonmd__gene_location', 'dystonmd__gene_variant', 'dystonmd__gene_Zygosity',
                                                                                                                         'dystonmd__gene_Disease', 'dystonmd__gene_Inheritance',
                                                                                                                         'dystonmd__gene_classification', 'dystonmd__Muscle_Biopsy',
                                                                                                                         'dystonmd__Muscle_Biopsy_MuscleImmunohistochemistry',
                                                                                                                         'dystonmd__Muscle_Biopsy_MuscleImmunohistochemistry_if_yes', 'dystonmd__final_diagnosis',
                                                                                                                         'dystonmd__current_past_treatment_Steroids',
                                                                                                                         'dystonmd__current_past_treatment_Steroids_starting_age',
                                                                                                                         'dystonmd__current_past_treatment_Prednisone', 'dystonmd__current_past_treatment_1',
                                                                                                                         'dystonmd__current_past_treatment_2', 'dystonmd__current_past_treatment_Deflazacort',
                                                                                                                         'dystonmd__current_past_treatment_Deflazacort_1',
                                                                                                                         'dystonmd__current_past_treatment_Deflazacort_anyother_specify',
                                                                                                                         'dystonmd__current_past_treatment_Supplements',
                                                                                                                         'dystonmd__current_past_treatment_Supplements_calcium',
                                                                                                                         'dystonmd__current_past_treatment_Supplements_vit_D',
                                                                                                                         'dystonmd__Respiratoryassistance_BiPAP', 'dystonmd__Respiratoryassistance_BiPAP_age',
                                                                                                                         'dystonmd__Respiratoryassistance_Ventilator',
                                                                                                                         'dystonmd__Respiratoryassistance_Ventilator_age', 'dystonmd__Tendon_lengthening_surgery',
                                                                                                                         'dystonmd__Tendon_lengthening_surgery_if_yes_age',
                                                                                                                         'dystonmd__Surgicalcorrectionscoliosis', 'dystonmd__Surgicalcorrectionscoliosis_if_yes_age',
                                                                                                                         'dystonmd__last_follow_up',
                                                                                                                         'dystonmd__last_follow_up_if_yes', 'dystonmd__last_follow_up_if_yes_age',
                                                                                                                         'dystonmd__Functionalstatus', 'dystonmd__functional_status_options',
                                                                                                                         'dystonmd__functional_score', 'dystonmd__functional_score_brooks_grade',
                                                                                                                         'dystonmd__functional_score_vignos_grade', 'dystonmd__outcome',
                                                                                                                         'dystonmd__outcome_age', 'dystonmd__oucome_cause_of_death', 'dystonmd__outcome_death_cause',
                                                                                                                         'dystonmd__death_place',
                                                                                                                         'dystonmd__mother_carrier_status', 'dystonmd__mother_carrier_status_outcome',
                                                                                                                         'dystonmd__sister_carrier_status',
                                                                                                                         'dystonmd__sister_carrier_status_outcome', 'spinalnmd__gender',
                                                                                                                         'spinalnmd__born_consanguineous_parents',
                                                                                                                         'spinalnmd__consanguineous_parents_if_yes', 'spinalnmd__familyHistory_sibling_affected',
                                                                                                                         'spinalnmd__familyHistory_sibling_affected_number',
                                                                                                                         'spinalnmd__upload_pedegree', 'spinalnmd__age_first_evaluation', 'spinalnmd__age_at_onset',
                                                                                                                         'spinalnmd__age_onset_options',
                                                                                                                         'spinalnmd__age_onset_options_yes_no', 'spinalnmd__ConditionBirth_cry',
                                                                                                                         'spinalnmd__conditionBirth_feedingDifficulty',
                                                                                                                         'spinalnmd__conditionBirth_RespiratoryDistress', 'spinalnmd__conditionBirth_ReceivedOxygen',
                                                                                                                         'spinalnmd__conditionBirth_KeptIncubator',
                                                                                                                         'spinalnmd__arthrogryposisBirth', 'spinalnmd__RecurrentLowerRespiratory',
                                                                                                                         'spinalnmd__Scoliosis_sma',
                                                                                                                         'spinalnmd__Kyphosis_sma',
                                                                                                                         'spinalnmd__Contractures', 'spinalnmd__HipDislocation', 'spinalnmd__Fractures',
                                                                                                                         'spinalnmd__MotorSystemExam_Minipolymyoclonus',
                                                                                                                         'spinalnmd__MotorSystemExam_TongueFasciculations',
                                                                                                                         'spinalnmd__MotorSystemExam_MotorPower_ModifiedMRCgrade',
                                                                                                                         'spinalnmd__MotorSystemExam_UpperLimb_ProximalMuscles',
                                                                                                                         'spinalnmd__MotorSystemExam_UpperLimb_DistalMuscles',
                                                                                                                         'spinalnmd__MotorSystemExam_lowerLimb_ProximalMuscles',
                                                                                                                         'spinalnmd__MotorSystemExam_lowerLimb_DistalMuscles', 'spinalnmd__LimbWeakness',
                                                                                                                         'spinalnmd__LimbWeakness_if_yes_UpperLimb_ProximalGrade',
                                                                                                                         'spinalnmd__LimbWeakness_if_yes_UpperLimb_DistalGrade',
                                                                                                                         'spinalnmd__LimbWeakness_if_yes_LowerLimb_ProximalGrade',
                                                                                                                         'spinalnmd__LimbWeakness_if_yes_LowerLimb_DistalGrade',
                                                                                                                         'spinalnmd__currentMotor_ability', 'spinalnmd__currentMotor_WheelchairBound',
                                                                                                                         'spinalnmd__currentMotor_WheelchairBound_if_yes_age',
                                                                                                                         'spinalnmd__currentMotor_BedBound', 'spinalnmd__currentMotor_BedBound_age', 'spinalnmd__HMAS',
                                                                                                                         'spinalnmd__HMAS_score',
                                                                                                                         'spinalnmd__clinicalDiagnosis_SMA0', 'spinalnmd__clinicalDiagnosis_SMA1',
                                                                                                                         'spinalnmd__clinicalDiagnosis_SMA2',
                                                                                                                         'spinalnmd__clinicalDiagnosis_SMA3', 'spinalnmd__clinicalDiagnosis_SMA4',
                                                                                                                         'spinalnmd__LaboratoryInvestigation_CK_Level',
                                                                                                                         'spinalnmd__geneticDiagnosis', 'spinalnmd__NAIP_deletion', 'spinalnmd__geneticFindings_gene',
                                                                                                                         'spinalnmd__geneticFindings_Location',
                                                                                                                         'spinalnmd__geneticFindings_Variant', 'spinalnmd__geneticFindings_Zygosity',
                                                                                                                         'spinalnmd__geneticFindings_Disease',
                                                                                                                         'spinalnmd__geneticFindings_Inheritance', 'spinalnmd__geneticFindings_classification',
                                                                                                                         'spinalnmd__geneticDiagnosis2',
                                                                                                                         'spinalnmd__final_diagnosis_1', 'spinalnmd__genetic_report_upload',
                                                                                                                         'spinalnmd__Treatment_RespiratorySupport',
                                                                                                                         'spinalnmd__Treatment_RespiratorySupport_ifyes_BIPAP',
                                                                                                                         'spinalnmd__Treatment_RespiratorySupport_ifyes_IPPR',
                                                                                                                         'spinalnmd__Treatment_RespiratorySupport_ifyes_Ventilation', 'spinalnmd__Feeding_Oral',
                                                                                                                         'spinalnmd__Feeding_Nasogastric',
                                                                                                                         'spinalnmd__Feeding_PEG', 'spinalnmd__OperatedScoliosis', 'spinalnmd__OperatedScoliosis_ifyes_age',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedNusinersin',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedNusinersin_if_yes',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam_if_yes_age',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedZolgensma',
                                                                                                                         'spinalnmd__CurrentPastTreatment_ReceivedZolgensma_if_yes_age',
                                                                                                                         'spinalnmd__finalOutcome', 'spinalnmd__finalOutcome_if_dead_age',
                                                                                                                         'spinalnmd__finalOutcome_death_place1',
                                                                                                                         'spinalnmd__finalOutcome_deathCause', 'spinalnmd__finalOutcome_deathCause_known',
                                                                                                                         'spinalnmd__finalOutcome_death_place2',
                                                                                                                         'spinalnmd__carrier_testing_parents', 'spinalnmd__prenatal_testing',
                                                                                                                         'spinalnmd__prenatal_testing_if_yes', 'limbnmd__limb_gender',
                                                                                                                         'limbnmd__evaluation_age', 'limbnmd__limb_symptoms_onset_age',
                                                                                                                         'limbnmd__limb_born_consanguineous_parents',
                                                                                                                         'limbnmd__limb_consanguineous_parents_if_yes', 'limbnmd__MuscleHypertrophy',
                                                                                                                         'limbnmd__MuscleWasting', 'limbnmd__Contractures_3',
                                                                                                                         'limbnmd__Contractures_3_ankle', 'limbnmd__Contractures_3_knee', 'limbnmd__Contractures_3_hip',
                                                                                                                         'limbnmd__Contractures_3_elbow',
                                                                                                                         'limbnmd__Contractures_3_neck', 'limbnmd__limb_weakness',
                                                                                                                         'limbnmd__limb_weakness_UpperlimbProximal',
                                                                                                                         'limbnmd__limb_weakness_UpperlimbDistal', 'limbnmd__limb_weakness_LowerlimbProximal',
                                                                                                                         'limbnmd__limb_weakness_lowerlimbDistal',
                                                                                                                         'limbnmd__BulbarWeakness', 'limbnmd__BulbarWeakness_if_yes', 'limbnmd__CardiacSymptoms',
                                                                                                                         'limbnmd__cardiac_symptoms_options',
                                                                                                                         'limbnmd__RespiratorySymptoms', 'limbnmd__RespiratorySymptoms_options',
                                                                                                                         'limbnmd__InheritancePattern', 'limbnmd__PositiveFamilyHistory',
                                                                                                                         'limbnmd__PositiveFamilyHistory_SiblingsAffected',
                                                                                                                         'limbnmd__PositiveFamilyHistory_SiblingsAffected_number',
                                                                                                                         'limbnmd__PositiveFamilyHistory_MotherAffected', 'limbnmd__PositiveFamilyHistory_FatherAffected',
                                                                                                                         'limbnmd__PositiveFamilyHistory_GrandmotherAffected',
                                                                                                                         'limbnmd__PositiveFamilyHistory_GrandFatherAffected',
                                                                                                                         'limbnmd__PositiveFamilyHistory_CousinsAffected',
                                                                                                                         'limbnmd__PositiveFamilyHistory_CousinsAffected_number',
                                                                                                                         'limbnmd__PositiveFamilyHistory_AnyOther', 'limbnmd__PositiveFamilyHistory_AnyOther_specify',
                                                                                                                         'limbnmd__PositiveFamilyHistory_AnyOther_Specify_names',
                                                                                                                         'limbnmd__PositiveFamilyHistory_upload_pedidegree', 'limbnmd__current_motor',
                                                                                                                         'limbnmd__CurrentMotor_yes_no', 'limbnmd__CurrentMotor_if_yes_age',
                                                                                                                         'limbnmd__LaboratoryInvestigations_CK_level',
                                                                                                                         'limbnmd__NerveConductionStudies', 'limbnmd__NerveConductionStudies_options',
                                                                                                                         'limbnmd__CardiacEvaluation', 'limbnmd__CardiacEvaluation_ECG',
                                                                                                                         'limbnmd__CardiacEvaluation_ECG_status',
                                                                                                                         'limbnmd__CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia',
                                                                                                                         'limbnmd__CardiacEvaluation_ECG_status_if_abnormal_Arrhythmia_if_yes', 'limbnmd__limb_2DECHO',
                                                                                                                         'limbnmd__limb_2DECHO_status',
                                                                                                                         'limbnmd__limb_2DECHO_if_abnormal', 'limbnmd__limb_2DECHO_yes_no', 'limbnmd__limb_2DECHO_AnyOther',
                                                                                                                         'limbnmd__MuscleBiopsy',
                                                                                                                         'limbnmd__MuscleBiopsy_Immunohistochemistry', 'limbnmd__MuscleBiopsy_if_yes',
                                                                                                                         'limbnmd__DiagnosisConfirmed_sanger',
                                                                                                                         'limbnmd__DiagnosisConfirmed_nextGenerationSeq_options',
                                                                                                                         'limbnmd__DiagnosisConfirmed_nextGenerationSeq_options',
                                                                                                                         'limbnmd__upload_genetic_report', 'limbnmd__limb_mutation', 'limbnmd__mutationDetails_Missense',
                                                                                                                         'limbnmd__mutationDetails_Missense_mutation', 'limbnmd__mutationDetails_Nonsense',
                                                                                                                         'limbnmd__mutationDetails_Nonsense_mutation',
                                                                                                                         'limbnmd__mutationDetails_SpliceSite', 'limbnmd__mutationDetails_SpliceSite_mutation',
                                                                                                                         'limbnmd__mutationDetails_Insertion',
                                                                                                                         'limbnmd__mutationDetails_Insertion_mutation', 'limbnmd__mutationDetails_Deletions',
                                                                                                                         'limbnmd__mutationDetails_Deletions_mutation',
                                                                                                                         'limbnmd__mutationDetails_AnyOther_specify', 'limbnmd__mutationDetails_AnyOther_mutation',
                                                                                                                         'limbnmd__MutationDetected_Homozygous',
                                                                                                                         'limbnmd__MutationDetected_CompoundHeterozygous', 'limbnmd__MutationDetected_Heterozygous',
                                                                                                                         'limbnmd__MutationDetected_VariantUnknownSignificance', 'limbnmd__gene_Location',
                                                                                                                         'limbnmd__gene_Variant', 'limbnmd__gene_Zygosity',
                                                                                                                         'limbnmd__gene_Disease', 'limbnmd__gene_Inheritance', 'limbnmd__gene_classification',
                                                                                                                         'limbnmd__AR_LGMD_type', 'limbnmd__ADLGMD_type',
                                                                                                                         'limbnmd__SegregationPattern_Father', 'limbnmd__SegregationPattern_Mother',
                                                                                                                         'limbnmd__TreatmentReceived_TendonLengthening',
                                                                                                                         'limbnmd__TreatmentReceived_TendonLengthening_age', 'limbnmd__Scoliosis_limb',
                                                                                                                         'limbnmd__Scoliosis_SurgicalCorrection',
                                                                                                                         'limbnmd__Scoliosis_SurgicalCorrection_age', 'limbnmd__CardiacAbnormalities_pacemaker',
                                                                                                                         'limbnmd__CardiacAbnormalities_Prophylactic',
                                                                                                                         'limbnmd__CardiacAbnormalities_CardiacTransplant', 'limbnmd__RespiratoryAssistance',
                                                                                                                         'limbnmd__RespiratoryAssistance_BiPAP',
                                                                                                                         'limbnmd__RespiratoryAssistance_BiPAP_age', 'limbnmd__RespiratoryAssistance_Ventilator',
                                                                                                                         'limbnmd__RespiratoryAssistance_Ventilator_age',
                                                                                                                         'limbnmd__Final_Outcome_last_followup_Date', 'limbnmd__Final_Outcome_status',
                                                                                                                         'limbnmd__Final_Outcome_if_death_age',
                                                                                                                         'limbnmd__Final_Outcome_death_cause', 'limbnmd__Final_Outcome_Cardiac',
                                                                                                                         'limbnmd__Final_Outcome_death_place',
                                                                                                                         'limbnmd__Final_Outcome_Respiratory', 'limbnmd__Final_Outcome_Respiratory_place', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_dystonmd_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam', 'nmd_date_of_birth', 'nmd_patient_name', 'nmd_father_name',
         'nmd_mother_name', 'nmd_paitent_id_yes_no', 'nmd_paitent_id', 'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district', 'nmd_city_name',
         'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion', 'nmd_caste', 'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc',
         'nmd_consent_given', 'nmd_consent_upload', 'nmd_assent_given', 'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no', 'NMD_diagnosis_type', 'NMD_enrollment_status', 'diagnosis_age', 'aproximate_age',
         'symptoms_age_onset',
         'onset_age', 'pedigree', 'positive_family_hist', 'positive_family_siblings', 'positive_family_sibling_nubmer_affected', 'positive_family_cousins', 'positive_family_sCousins_nubmer_affected',
         'positive_family_Maternal_uncles', 'positive_family_Maternal_uncles_nubmer_affected', 'positive_family_Grand_materna', 'positive_family_Grand_materna_affected', 'positive_family_mothers',
         'difficulty_running_walking_fast', 'unable_rise_low_chair_floor', 'repeated_false', 'muscle_hypertrophy', 'mental_sub_normality', 'learning_disability', 'delayed_motor_milestrones',
         'symtoms_signs_other_specify', 'CEF_anthropometric_wieght', 'CEF_anthropometric_height', 'CEF_anthropometric_head_circumference', 'MP_MRC_grade_upperlimb_proximal_muscles',
         'MP_MRC_grade_upperlimb_distal_muscles', 'MP_MRC_grade_lowerlimb_proximal_muscles', 'MP_MRC_grade_lowerlimb_distal_muscles', 'functional_status_Independently_ambulant',
         'functional_status_NeedsPhysicalAssistance', 'functional_status_AmbulantHome', 'functional_status_WheelchairBound', 'functional_status_WheelchairBound_age', 'functional_status_BedBound',
         'functional_status_BedBound_age', 'functional_status_FunctionalScoreAvailable', 'functional_status_BrookeScale', 'functional_status_VignosScale', 'intelligent_quotient_tested',
         'intelligent_quotient_tested_if_yes', 'autism', 'Contractures', 'Contractures_ankle', 'Contractures_knee', 'Contractures_hips', 'Contractures_elbows', 'Scoliosis', 'Kyphosis', 'Respiratory_difficulty',
         'LaboratoryInvestigation_serum_ck_lvel', 'LaboratoryInvestigation_Cardiac_Evaluation', 'LaboratoryInvestigation_ecg_status', 'LaboratoryInvestigation_ecg_normal_abnormal', 'NMD_diagnosis_type',
         'LaboratoryInvestigation_2DECHO_status', 'LaboratoryInvestigation_2DECHO_normal_abnormal', 'NMD_diagnosis_type', 'pulmonary_function_tests', 'pulmonary_function_tests_normal_abnormal',
         'pulmonary_function_forced_vital_capacity', 'genetic_diagnosis_confirmed_mPCR', 'genetic_diagnosis_confirmed_MLPA', 'genetic_diagnosis_confirmed_MicroArray', 'genetic_diagnosis_confirmed_SangerSequencing',
         'genetic_diagnosis_confirmed_next_generation', 'genetic_diagnosis_next_generation', 'enetic_diagnosis_next_generation_TargetedPanel', 'enetic_diagnosis_next_generation_WholeExomeSequencing',
         'enetic_diagnosis_next_generation_WholeGenomeSequencing', 'upload_genetic_report', 'NMD_diagnosis_type', 'inframe_outframe', 'list_of_deleted_exons', 'list_of_duplicate_exons', 'mutation_identified_Missense',
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

    users = profile_nmd.objects.all().prefetch_related('dystonmd', ).values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                 'nmd_date_of_clinical_exam',
                                                                                 'nmd_date_of_birth', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name', 'nmd_paitent_id_yes_no',
                                                                                 'nmd_paitent_id',
                                                                                 'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                 'nmd_city_name',
                                                                                 'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                 'nmd_caste',
                                                                                 'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given', 'nmd_consent_upload',
                                                                                 'nmd_assent_given',
                                                                                 'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                 'dystonmd__NMD_diagnosis_type', 'dystonmd__NMD_enrollment_status', 'dystonmd__diagnosis_age', 'dystonmd__aproximate_age',
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
                                                                                 'dystonmd__Contractures_knee', 'dystonmd__Contractures_hips', 'dystonmd__Contractures_elbows', 'dystonmd__Scoliosis_dmd',
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
                                                                                 'dystonmd__Surgicalcorrectionscoliosis', 'dystonmd__Surgicalcorrectionscoliosis_if_yes_age', 'dystonmd__last_follow_up',
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


@login_required(login_url='login')
def export_spinalnmd_csv(request):
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

    users = profile_nmd.objects.all().prefetch_related('spinalnmd').values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                'nmd_date_of_clinical_exam',
                                                                                'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name', 'nmd_paitent_id_yes_no',
                                                                                'nmd_paitent_id',
                                                                                'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                'nmd_city_name',
                                                                                'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                'nmd_caste',
                                                                                'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given', 'nmd_consent_upload',
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
                                                                                'spinalnmd__RecurrentLowerRespiratory', 'spinalnmd__Scoliosis_sma', 'spinalnmd__Kyphosis_sma', 'spinalnmd__Contractures',
                                                                                'spinalnmd__HipDislocation',
                                                                                'spinalnmd__Fractures', 'spinalnmd__MotorSystemExam_Minipolymyoclonus', 'spinalnmd__MotorSystemExam_TongueFasciculations',
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
                                                                                'spinalnmd__Treatment_RespiratorySupport_ifyes_Ventilation', 'spinalnmd__Feeding_Oral', 'spinalnmd__Feeding_Nasogastric',
                                                                                'spinalnmd__Feeding_PEG', 'spinalnmd__OperatedScoliosis', 'spinalnmd__OperatedScoliosis_ifyes_age',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedNusinersin', 'spinalnmd__CurrentPastTreatment_ReceivedNusinersin_if_yes',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam', 'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam_if_yes_age',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedZolgensma', 'spinalnmd__CurrentPastTreatment_ReceivedZolgensma_if_yes_age',
                                                                                'spinalnmd__finalOutcome', 'spinalnmd__finalOutcome_if_dead_age', 'spinalnmd__finalOutcome_death_place1',
                                                                                'spinalnmd__finalOutcome_deathCause', 'spinalnmd__finalOutcome_deathCause_known', 'spinalnmd__finalOutcome_death_place2',
                                                                                'spinalnmd__carrier_testing_parents', 'spinalnmd__prenatal_testing', 'spinalnmd__prenatal_testing_if_yes', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_limbnmd_csv(request):
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

    users = profile_nmd.objects.all().prefetch_related('limbnmd', ).values_list('register_id__institute_name', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                'nmd_date_of_clinical_exam',
                                                                                'nmd_date_of_birth', 'nmd_patient_age', 'nmd_patient_name', 'nmd_father_name', 'nmd_mother_name', 'nmd_paitent_id_yes_no',
                                                                                'nmd_paitent_id',
                                                                                'nmd_patient_id_no', 'nmd_father_mother_id', 'nmd_mother_father_no', 'nmd_permanent_addr', 'nmd_state', 'nmd_district',
                                                                                'nmd_city_name',
                                                                                'nmd_country_name', 'nmd_land_line_no', 'nmd_mother_mobile_no', 'nmd_father_mobile_no', 'nmd_email', 'nmd_religion',
                                                                                'nmd_caste',
                                                                                'nmd_gender', 'nmd_referred_status', 'nmd_referred_by', 'nmd_referred_by_desc', 'nmd_consent_given', 'nmd_consent_upload',
                                                                                'nmd_assent_given',
                                                                                'nmd_assent_upload', 'nmd_hospital_name', 'nmd_hospital_reg_no',
                                                                                'limbnmd__limb_gender', 'limbnmd__evaluation_age', 'limbnmd__limb_symptoms_onset_age',
                                                                                'limbnmd__limb_born_consanguineous_parents', 'limbnmd__limb_consanguineous_parents_if_yes', 'limbnmd__MuscleHypertrophy',
                                                                                'limbnmd__MuscleWasting', 'limbnmd__Contractures_3', 'limbnmd__Contractures_3_ankle', 'limbnmd__Contractures_3_knee',
                                                                                'limbnmd__Contractures_3_hip', 'limbnmd__Contractures_3_elbow', 'limbnmd__Contractures_3_neck', 'limbnmd__limb_weakness',
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
                                                                                'limbnmd__AR_LGMD_type', 'limbnmd__ADLGMD_type', 'limbnmd__SegregationPattern_Father', 'limbnmd__SegregationPattern_Mother',
                                                                                'limbnmd__TreatmentReceived_TendonLengthening', 'limbnmd__TreatmentReceived_TendonLengthening_age', 'limbnmd__Scoliosis_limb',
                                                                                'limbnmd__Scoliosis_SurgicalCorrection', 'limbnmd__Scoliosis_SurgicalCorrection_age',
                                                                                'limbnmd__CardiacAbnormalities_pacemaker', 'limbnmd__CardiacAbnormalities_Prophylactic',
                                                                                'limbnmd__CardiacAbnormalities_CardiacTransplant', 'limbnmd__RespiratoryAssistance', 'limbnmd__RespiratoryAssistance_BiPAP',
                                                                                'limbnmd__RespiratoryAssistance_BiPAP_age', 'limbnmd__RespiratoryAssistance_Ventilator',
                                                                                'limbnmd__RespiratoryAssistance_Ventilator_age', 'limbnmd__Final_Outcome_last_followup_Date',
                                                                                'limbnmd__Final_Outcome_status', 'limbnmd__Final_Outcome_if_death_age', 'limbnmd__Final_Outcome_death_cause',
                                                                                'limbnmd__Final_Outcome_Cardiac', 'limbnmd__Final_Outcome_death_place', 'limbnmd__Final_Outcome_Respiratory',
                                                                                'limbnmd__Final_Outcome_Respiratory_place', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_dystonmd_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam', 'NMD_enrollment_status', 'diagnosis_age', 'aproximate_age',
         'symptoms_age_onset',
         'onset_age', 'pedigree', 'positive_family_hist', 'positive_family_siblings', 'positive_family_sibling_nubmer_affected', 'positive_family_cousins', 'positive_family_sCousins_nubmer_affected',
         'positive_family_Maternal_uncles', 'positive_family_Maternal_uncles_nubmer_affected', 'positive_family_Grand_materna', 'positive_family_Grand_materna_affected', 'positive_family_mothers',
         'difficulty_running_walking_fast', 'unable_rise_low_chair_floor', 'repeated_false', 'muscle_hypertrophy', 'mental_sub_normality', 'learning_disability', 'delayed_motor_milestrones',
         'symtoms_signs_other_specify', 'CEF_anthropometric_wieght', 'CEF_anthropometric_height', 'CEF_anthropometric_head_circumference', 'MP_MRC_grade_upperlimb_proximal_muscles',
         'MP_MRC_grade_upperlimb_distal_muscles', 'MP_MRC_grade_lowerlimb_proximal_muscles', 'MP_MRC_grade_lowerlimb_distal_muscles', 'functional_status_Independently_ambulant',
         'functional_status_NeedsPhysicalAssistance', 'functional_status_AmbulantHome', 'functional_status_WheelchairBound', 'functional_status_WheelchairBound_age', 'functional_status_BedBound',
         'functional_status_BedBound_age', 'functional_status_FunctionalScoreAvailable', 'functional_status_BrookeScale', 'functional_status_VignosScale', 'intelligent_quotient_tested',
         'intelligent_quotient_tested_if_yes', 'autism', 'Contractures', 'Contractures_ankle', 'Contractures_knee', 'Contractures_hips', 'Contractures_elbows', 'Scoliosis', 'Kyphosis', 'Respiratory_difficulty',
         'LaboratoryInvestigation_serum_ck_lvel', 'LaboratoryInvestigation_Cardiac_Evaluation', 'LaboratoryInvestigation_ecg_status', 'LaboratoryInvestigation_ecg_normal_abnormal', 'NMD_diagnosis_type',
         'LaboratoryInvestigation_2DECHO_status', 'LaboratoryInvestigation_2DECHO_normal_abnormal', 'NMD_diagnosis_type', 'pulmonary_function_tests', 'pulmonary_function_tests_normal_abnormal',
         'pulmonary_function_forced_vital_capacity', 'genetic_diagnosis_confirmed_mPCR', 'genetic_diagnosis_confirmed_MLPA', 'genetic_diagnosis_confirmed_MicroArray', 'genetic_diagnosis_confirmed_SangerSequencing',
         'genetic_diagnosis_confirmed_next_generation', 'genetic_diagnosis_next_generation', 'enetic_diagnosis_next_generation_TargetedPanel', 'enetic_diagnosis_next_generation_WholeExomeSequencing',
         'enetic_diagnosis_next_generation_WholeGenomeSequencing', 'upload_genetic_report', 'NMD_diagnosis_type', 'inframe_outframe', 'list_of_deleted_exons', 'list_of_duplicate_exons', 'mutation_identified_Missense',
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

    users = profile_nmd.objects.all().prefetch_related('dystonmd', ).values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                 'nmd_date_of_clinical_exam',

                                                                                 'dystonmd__NMD_diagnosis_type', 'dystonmd__NMD_enrollment_status', 'dystonmd__diagnosis_age', 'dystonmd__aproximate_age',
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
                                                                                 'dystonmd__Contractures_knee', 'dystonmd__Contractures_hips', 'dystonmd__Contractures_elbows', 'dystonmd__Scoliosis_dmd',
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
                                                                                 'dystonmd__Surgicalcorrectionscoliosis', 'dystonmd__Surgicalcorrectionscoliosis_if_yes_age', 'dystonmd__last_follow_up',
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


@login_required(login_url='login')
def export_spinalnmd_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam',
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

    users = profile_nmd.objects.all().prefetch_related('spinalnmd').values_list('register_id__institute_name','quality_result','quality_reason', 'uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                'nmd_date_of_clinical_exam',
                                                                                'spinalnmd__gender', 'spinalnmd__born_consanguineous_parents', 'spinalnmd__consanguineous_parents_if_yes',
                                                                                'spinalnmd__familyHistory_sibling_affected', 'spinalnmd__familyHistory_sibling_affected_number',
                                                                                'spinalnmd__upload_pedegree',
                                                                                'spinalnmd__age_first_evaluation', 'spinalnmd__age_at_onset', 'spinalnmd__age_onset_options',
                                                                                'spinalnmd__age_onset_options_yes_no',
                                                                                'spinalnmd__ConditionBirth_cry', 'spinalnmd__conditionBirth_feedingDifficulty',
                                                                                'spinalnmd__conditionBirth_RespiratoryDistress',
                                                                                'spinalnmd__conditionBirth_ReceivedOxygen', 'spinalnmd__conditionBirth_KeptIncubator', 'spinalnmd__arthrogryposisBirth',
                                                                                'spinalnmd__RecurrentLowerRespiratory', 'spinalnmd__Scoliosis_sma', 'spinalnmd__Kyphosis_sma', 'spinalnmd__Contractures',
                                                                                'spinalnmd__HipDislocation',
                                                                                'spinalnmd__Fractures', 'spinalnmd__MotorSystemExam_Minipolymyoclonus', 'spinalnmd__MotorSystemExam_TongueFasciculations',
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
                                                                                'spinalnmd__Treatment_RespiratorySupport_ifyes_Ventilation', 'spinalnmd__Feeding_Oral', 'spinalnmd__Feeding_Nasogastric',
                                                                                'spinalnmd__Feeding_PEG', 'spinalnmd__OperatedScoliosis', 'spinalnmd__OperatedScoliosis_ifyes_age',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedNusinersin', 'spinalnmd__CurrentPastTreatment_ReceivedNusinersin_if_yes',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam', 'spinalnmd__CurrentPastTreatment_ReceivedRisdiplam_if_yes_age',
                                                                                'spinalnmd__CurrentPastTreatment_ReceivedZolgensma', 'spinalnmd__CurrentPastTreatment_ReceivedZolgensma_if_yes_age',
                                                                                'spinalnmd__finalOutcome', 'spinalnmd__finalOutcome_if_dead_age', 'spinalnmd__finalOutcome_death_place1',
                                                                                'spinalnmd__finalOutcome_deathCause', 'spinalnmd__finalOutcome_deathCause_known', 'spinalnmd__finalOutcome_death_place2',
                                                                                'spinalnmd__carrier_testing_parents', 'spinalnmd__prenatal_testing', 'spinalnmd__prenatal_testing_if_yes', )
    for user in users:
        writer.writerow(user)

    return response


@login_required(login_url='login')
def export_limbnmd_qaqc(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nmd_qc.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Institute name', 'quality_result','quality_reason','UniqueId', 'unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records', 'nmd_date_of_clinical_exam',
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

    users = profile_nmd.objects.all().prefetch_related('limbnmd', ).values_list('register_id__institute_name', 'quality_result','quality_reason','uniqueId', 'nmd_icmr_unique_no', 'nmd_final_diagnosis', 'nmd_date_of_records',
                                                                                'nmd_date_of_clinical_exam',

                                                                                'limbnmd__limb_gender', 'limbnmd__evaluation_age', 'limbnmd__limb_symptoms_onset_age',
                                                                                'limbnmd__limb_born_consanguineous_parents', 'limbnmd__limb_consanguineous_parents_if_yes', 'limbnmd__MuscleHypertrophy',
                                                                                'limbnmd__MuscleWasting', 'limbnmd__Contractures_3', 'limbnmd__Contractures_3_ankle', 'limbnmd__Contractures_3_knee',
                                                                                'limbnmd__Contractures_3_hip', 'limbnmd__Contractures_3_elbow', 'limbnmd__Contractures_3_neck', 'limbnmd__limb_weakness',
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
                                                                                'limbnmd__AR_LGMD_type', 'limbnmd__ADLGMD_type', 'limbnmd__SegregationPattern_Father', 'limbnmd__SegregationPattern_Mother',
                                                                                'limbnmd__TreatmentReceived_TendonLengthening', 'limbnmd__TreatmentReceived_TendonLengthening_age', 'limbnmd__Scoliosis_limb',
                                                                                'limbnmd__Scoliosis_SurgicalCorrection', 'limbnmd__Scoliosis_SurgicalCorrection_age',
                                                                                'limbnmd__CardiacAbnormalities_pacemaker', 'limbnmd__CardiacAbnormalities_Prophylactic',
                                                                                'limbnmd__CardiacAbnormalities_CardiacTransplant', 'limbnmd__RespiratoryAssistance', 'limbnmd__RespiratoryAssistance_BiPAP',
                                                                                'limbnmd__RespiratoryAssistance_BiPAP_age', 'limbnmd__RespiratoryAssistance_Ventilator',
                                                                                'limbnmd__RespiratoryAssistance_Ventilator_age', 'limbnmd__Final_Outcome_last_followup_Date',
                                                                                'limbnmd__Final_Outcome_status', 'limbnmd__Final_Outcome_if_death_age', 'limbnmd__Final_Outcome_death_cause',
                                                                                'limbnmd__Final_Outcome_Cardiac', 'limbnmd__Final_Outcome_death_place', 'limbnmd__Final_Outcome_Respiratory',
                                                                                'limbnmd__Final_Outcome_Respiratory_place', )
    for user in users:
        writer.writerow(user)

    return response



@login_required(login_url='login')
def export_opd_attendance(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="opd.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['user','date','name_of_rdei','no_of_cases','no_of_opd_cases','no_of_new_adminission','pre_opd_att','pre_new_admi' ])

    users = Opd_attendance.objects.values_list('user','date','name_of_rdei','no_of_cases','no_of_opd_cases','no_of_new_adminission','pre_opd_att','pre_new_admi'  )
    for user in users:
        writer.writerow(user)

    return response


@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        profile_bleeding1 = profile_bleeding.objects.all().count()
        profile_fabry1 = profile_fabry.objects.all().count()
        profile_glycogen1 = profile_glycogen.objects.all().count()
        profile_metabolism1 = profile_metabolism.objects.all().count()
        profile_mucopolysaccharidosis1 = profile_mucopolysaccharidosis.objects.all().count()
        profile_nmd1 = profile_nmd.objects.all().count()
        profile_pid1 = profile_pid.objects.all().count()
        profile_pompe1 = profile_pompe.objects.all().count()
        profile_skeletal1 = profile_skeletal.objects.all().count()
        profile_smallmolecule1 = profile_smallmolecule.objects.all().count()
        profile_storage1 = profile_storage.objects.all().count()
        profile_thalassemia1 = profile_thalassemia.objects.all().count()
        total_count = int(profile_bleeding1) + int(profile_fabry1) + int(profile_glycogen1) + int(profile_metabolism1) + int(profile_mucopolysaccharidosis1) + \
                      int(profile_nmd1) + int(profile_pid1) + int(profile_pompe1) + int(profile_skeletal1) + int(profile_smallmolecule1) + int(profile_storage1) + int(profile_thalassemia1)
        data = {
            'count': total_count, 'profile_bleeding1': profile_bleeding1, 'profile_fabry1': profile_fabry1, 'profile_glycogen1': profile_glycogen1, 'profile_metabolism1': profile_metabolism1,
            'profile_mucopolysaccharidosis1': profile_mucopolysaccharidosis1, 'profile_nmd1': profile_nmd1, 'profile_pid1': profile_pid1,
            'profile_pompe1': profile_pompe1, 'profile_skeletal1': profile_skeletal1, 'profile_smallmolecule1': profile_smallmolecule1, 'profile_storage1': profile_storage1, 'profile_thalassemia1': profile_thalassemia1,

            }
        return JsonResponse(data)


# class HelloView(APIView):
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)





