from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_meta/', views.add_record_meta, name="add_record_meta"),
    path('view_profile_mt/<str:pk>/ ', views.view_profile_mt, name="view_profile_mt"),
    path('total_record_mt/', views.total_record_mt, name="total_record_mt"),
    path('delete_record_mt/<str:pk>/ ', views.delete_record_mt, name="delete_record_mt"),
    path('view_record_mt/<str:pk>/ ', views.view_record_mt, name="view_record_mt"),
    path('update_record_mt/<str:pk>/ ', views.update_record_mt, name="update_record_mt"),
    path('demographic_meta/<str:pk>/', views.demographic_meta, name="demographic_meta"),
    path('update_patient_record_meta/<str:pk>/', views.update_patient_record_meta, name="update_patient_record_meta"),
    path('update_qa_qc_iem/<str:pk>/', views.update_qa_qc_iem, name="update_qa_qc_iem"),
    path('view_qa_qc_iem/<str:pk>/', views.view_qa_qc_iem, name="view_qa_qc_iem"),

    path('total_record_mt_admin/', views.total_record_mt_admin, name="total_record_mt_admin"),
    path('export_iem/', views.export_iem_user_csv, name="export_iem"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
