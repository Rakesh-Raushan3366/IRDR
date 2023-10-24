from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from storage import views as views


urlpatterns = [

    path('storage_demographic/<str:pk>/', views.storage_demographic, name="storage_demographic"),
    path('total_record_sd/', views.total_record_sd, name="total_record_sd"),
    path('delete_record_sd/<str:pk>/ ', views.delete_record_sd, name="delete_record_sd"),
    path('update_storage_demographic/<str:pk>/', views.update_storage_demographic, name="update_storage_demographic"),
    path('view_storage_record/<str:pk>/', views.view_storage_record, name="view_storage_record"),
    path('update_patient_record_storage/<str:pk>/', views.update_patient_record_storage, name="update_patient_record_storage"),
    path('storage_total_record/', views.storage_total_record, name="storage_total_record"),
    path('total_record_sd_admin/', views.total_record_sd_admin, name="total_record_sd_admin"),
    path('view_profile_record_storage/<str:pk>/', views.view_profile_record_storage, name="view_profile_record_storage"),
    path('update_qa_qc_storage/<str:pk>/', views.update_qa_qc_storage, name="update_qa_qc_storage"),
    path('view_qa_qc_storage/<str:pk>/', views.view_qa_qc_storage, name="view_qa_qc_storage"),


    path('export_storage/', views.export_storage_user_csv, name="export_storage"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
