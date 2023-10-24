from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_skeletal/', views.add_record_skeletal, name="add_record_skeletal"),
    path('skeletal_demographic/<str:pk>/', views.skeletal_demographic, name="skeletal_demographic"),
    path('update_skeletal_demographic/<str:pk>/', views.update_skeletal_demographic,
         name="update_skeletal_demographic"),
    path('view_skeletal_record/<str:pk>/', views.view_skeletal_record, name="view_skeletal_record"),
    path('total_record_skd/', views.total_record_skd, name="total_record_skd"),
    path('delete_record_skd/<str:pk>/ ', views.delete_record_skd, name="delete_record_skd"),
    path('update_patient_record_skeletal/<str:pk>/ ', views.update_patient_record_skeletal, name="update_patient_record_skeletal"),
    path('view_profile_record/<str:pk>/', views.view_profile_record, name="view_profile_record"),
    path('update_qa_qc_skeletal/<str:pk>/', views.update_qa_qc_skeletal, name="update_qa_qc_skeletal"),
    path('view_qa_qc_skeletal/<str:pk>/', views.view_qa_qc_skeletal, name="view_qa_qc_skeletal"),
    path('total_record_skd_admin/', views.total_record_skd_admin, name="total_record_skd_admin"),
    path('export_skeletal/', views.export_skeletal_user_csv, name="export_skeletal"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
