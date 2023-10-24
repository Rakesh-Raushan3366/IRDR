from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_pompe/', views.add_record_pompe, name="add_record_pompe"),
    path('pompe_demographic/<str:pk>/', views.pompe_demographic, name="pompe_demographic"),
    path('pompe_total_record/', views.pompe_total_record, name="pompe_total_record"),
    path('update_pompe_demographic/<str:pk>/', views.update_pompe_demographic, name="update_pompe_demographic"),
    path('view_pompe_record/<str:pk>/', views.view_pompe_record, name="view_pompe_record"),
    path('delete_record_pm/<str:pk>/ ', views.delete_record_pm, name="delete_record_pm"),
    path('update_patient_record_pompe/<str:pk>/ ', views.update_patient_record_pompe, name="update_patient_record_pompe"),
    path('view_profile_pm/<str:pk>/ ', views.view_profile_pm, name="view_profile_pm"),
    path('update_qa_qc_pompe/<str:pk>/ ', views.update_qa_qc_pompe, name="update_qa_qc_pompe"),
    path('view_qa_qc_pompe/<str:pk>/ ', views.view_qa_qc_pompe, name="view_qa_qc_pompe"),



    path('pompe_total_record_admin/', views.pompe_total_record_admin, name="pompe_total_record_admin"),
    path('export_pompe/', views.export_pompe_user_csv, name="export_pompe"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
