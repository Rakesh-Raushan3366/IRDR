from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

from fabry import views as fabry_view
from thalasemia import views as thalasemia_view
from glycogen import views as glycogen_view
from bleeding import views as bleeding_view
from smallmolecule import views as smallmolecule_view
from pid import views as pid_view
from nmd import views as nmd_view
from storage import views as storage_view
from skeletal import views as skeletal_view
from mucopoly import views as mucopoly_view
from pompe import views as pompe_view
from iem import views as iem_view

urlpatterns = [

    path('', views.info, name="info"),
    path('ajax/load_district/', views.load_district, name='load_district'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('info/', views.info, name="info"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('Facility1/', views.update_profile, name="Facility1"),
    path('view_facility/', views.view_facility, name="view_facility"),
    path('Opd_attendance/', views.Opd_attendance1, name="Opd_attendance"),
    path('Opd_attendance1/', views.Opd_attendance2, name="Opd_attendance1"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),

    path('add_record_th/', thalasemia_view.add_record_th, name="add_record_th"),

    path('add_record_gl/', glycogen_view.add_record_gl, name="add_record_gl"),

    path('add_record_fb/', fabry_view.add_record_fb, name="add_record_fb"),

    path('add_record_bd/', bleeding_view.add_record_bd, name="add_record_bd"),

    path('add_record_meta/', iem_view.add_record_meta, name="add_record_meta"),

    path('add_record_pompe/', pompe_view.add_record_pompe, name="add_record_pompe"),

    path('add_record_storage/', storage_view.add_record_storage, name="add_record_storage"),

    path('add_record_skeletal/', skeletal_view.add_record_skeletal, name="add_record_skeletal"),

    path('add_record_nmd/', nmd_view.add_record_nmd, name="add_record_nmd"),

    path('add_record_mg/', mucopoly_view.add_record_mg, name="add_record_mg"),

    path('add_record_sm/', smallmolecule_view.add_record_sm, name="add_record_sm"),

    path('add_record_pid/', pid_view.add_record_pid, name="add_record_pid"),




    #############
    path('total_record_th/', thalasemia_view.total_record_th, name="total_record_th"),

    path('total_record_gl/', glycogen_view.total_record_gl, name="total_record_gl"),

    path('total_record_fb/', fabry_view.total_record_fb, name="total_record_fb"),

    path('total_record_bd/', bleeding_view.total_record_bd, name="total_record_bd"),

    path('total_record_mt/', iem_view.total_record_mt, name="total_record_mt"),

    path('pompe_total_record/', pompe_view.pompe_total_record, name="pompe_total_record"),

    path('total_record_sd/', storage_view.total_record_sd, name="total_record_sd"),

    path('total_record_skd/', skeletal_view.total_record_skd, name="total_record_skd"),

    path('total_record_nmd/', nmd_view.total_record_nmd, name="total_record_nmd"),

    path('total_record_mg/', mucopoly_view.total_record_mg, name="total_record_mg"),

    path('total_record_sm/', smallmolecule_view.total_record_sm, name="total_record_sm"),

    path('total_record_pid/', pid_view.total_record_pid, name="total_record_pid"),
    path('total_record_pm/', pompe_view.total_record_pm, name="total_record_pm"),

    path('total_record_th_admin/', thalasemia_view.total_record_th_admin, name="total_record_th_admin"),
    path('total_record_gl_admin/', glycogen_view.total_record_gl_admin, name="total_record_gl_admin"),
    path('total_record_fb_admin/', fabry_view.total_record_fb_admin, name="total_record_fb_admin"),
    path('total_record_bd_admin/', bleeding_view.total_record_bd_admin, name="total_record_bd_admin"),
    path('total_record_mt_admin/', iem_view.total_record_mt_admin, name="total_record_mt_admin"),
    path('pompe_total_record_admin/', pompe_view.pompe_total_record_admin, name="pompe_total_record_admin"),
    path('total_record_sd_admin/', storage_view.total_record_sd_admin, name="total_record_sd_admin"),
    path('total_record_skd_admin/', skeletal_view.total_record_skd_admin, name="total_record_skd_admin"),
    path('total_record_nmd_admin/', nmd_view.total_record_nmd_admin, name="total_record_nmd_admin"),
    path('total_record_mg_admin/', mucopoly_view.total_record_mg_admin, name="total_record_mg_admin"),
    path('total_record_sm_admin/', smallmolecule_view.total_record_sm_admin, name="total_record_sm_admin"),
    path('total_record_pid_admin/', pid_view.total_record_pid_admin, name="total_record_pid_admin"),

    path('export_thalassemia_csv/', views.export_thalassemia_csv, name="export_thalassemia_csv"),
    path('export_thalassemia_qaqc/', views.export_thalassemia_qaqc, name="export_thalassemia_qaqc"),
    path('export_gylcogen_csv/', views.export_gylcogen_csv, name="export_gylcogen_csv"),
    path('export_gylcogen_qaqc/', views.export_gylcogen_qaqc, name="export_gylcogen_qaqc"),
    path('export_fabry_csv/', views.export_fabry_csv, name="export_fabry_csv"),
    path('export_fabry_qaqc/', views.export_fabry_qaqc, name="export_fabry_qaqc"),
    path('export_bleeding_csv/', views.export_bleeding_csv, name="export_bleeding_csv"),
    path('export_bleeding_qaqc/', views.export_bleeding_qaqc, name="export_bleeding_qaqc"),
    path('export_iem_csv/', views.export_iem_csv, name="export_iem_csv"),
    path('export_iem_qaqc/', views.export_iem_qaqc, name="export_iem_qaqc"),
    path('export_pompe_csv/', views.export_pompe_csv, name="export_pompe_csv"),
    path('export_pompe_qaqc/', views.export_pompe_qaqc, name="export_pompe_qaqc"),
    path('export_storage_csv/', views.export_storage_csv, name="export_storage_csv"),
    path('export_storage_qaqc/', views.export_storage_qaqc, name="export_storage_qaqc"),
    path('export_skeletal_csv/', views.export_skeletal_csv, name="export_skeletal_csv"),
    path('export_skeletal_qaqc/', views.export_skeletal_qaqc, name="export_skeletal_qaqc"),
    path('export_mucopoly_csv/', views.export_mucopoly_csv, name="export_mucopoly_csv"),
    path('export_mucopoly_qaqc/', views.export_mucopoly_qaqc, name="export_mucopoly_qaqc"),
    path('export_smallmolecule_csv/', views.export_smallmolecule_csv, name="export_smallmolecule_csv"),
    path('export_smallmolecule_qaqc/', views.export_smallmolecule_qaqc, name="export_smallmolecule_qaqc"),
    path('export_pid_csv/', views.export_pid_csv, name="export_pid_csv"),
    path('export_pid_qaqc/', views.export_pid_qaqc, name="export_pid_qaqc"),
    path('export_nmd_csv/', views.export_nmd_csv, name="export_nmd_csv"),

    path('export_dystonmd_csv/', views.export_dystonmd_csv, name="export_dystonmd_csv"),
    path('export_spinalnmd_csv/', views.export_spinalnmd_csv, name="export_spinalnmd_csv"),
    path('export_limbnmd_csv/', views.export_limbnmd_csv, name="export_limbnmd_csv"),
    path('export_dystonmd_qaqc/', views.export_dystonmd_qaqc, name="export_dystonmd_qaqc"),
    path('export_spinalnmd_qaqc/', views.export_spinalnmd_qaqc, name="export_spinalnmd_qaqc"),
    path('export_limbnmd_qaqc/', views.export_limbnmd_qaqc, name="export_limbnmd_qaqc"),

    path('institute/', views.institute, name="institute"),
    path('quality_control/', views.quality_control, name="quality_control"),
    path('post_collection/', views.post_collection, name="post_collection"),
    path('hello/', views.HelloView.as_view(), name='hello'),

    path('month_wise/', views.month_wise, name="month_wise"),
    path('export_opd_attendance/', views.export_opd_attendance, name="export_opd_attendance"),
    # path('update_profile/', views.update_profile, name="update_profile"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
