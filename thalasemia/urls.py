from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_th/', views.add_record_th, name="add_record_th"),
    path('view_profile_th/<str:pk>/ ', views.view_profile_th, name="view_profile_th"),
    path('demographic_th/<str:pk>/', views.demographic_th, name="demographic_th"),
    path('total_record_th/', views.total_record_th, name="total_record_th"),
    path('view_record_th/<str:pk>/ ', views.view_record_th, name="view_record_th"),
    path('delete_record_th/<str:pk>/ ', views.delete_record_th, name="delete_record_th"),
    path('update_record_th/<str:pk>/ ', views.update_record_th, name="update_record_th"),

    path('update_patient_record_th/<str:pk>/ ', views.update_patient_record_th, name="update_patient_record_th"),
    path('total_record_th_admin/', views.total_record_th_admin, name="total_record_th_admin"),
    path('export_thalassemia_csv/<str:pk>/ ', views.export_thalassemia_csv_user, name="export_thalassemia_csv"),
    path('update_qa_qc_thalasemia/<str:pk>/ ', views.update_qa_qc_thalasemia, name="update_qa_qc_thalasemia"),
    path('view_qa_qc_thalasemia/<str:pk>/ ', views.view_qa_qc_thalasemia, name="view_qa_qc_thalasemia"),



]
