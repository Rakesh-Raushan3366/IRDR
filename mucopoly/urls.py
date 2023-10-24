from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('add_record_mg/', views.add_record_mg, name="add_record_mg"),
    path('mg_demographic/<str:pk>/', views.mg_demographic, name="mg_demographic"),
    path('total_record_mg/', views.total_record_mg, name="total_record_mg"),
    path('view_record_mg/<str:pk>/ ', views.view_record_mg, name="view_record_mg"),
    path('update_record_mg/<str:pk>/ ', views.update_record_mg, name="update_record_mg"),
    path('update_patient_record_mg/<str:pk>/ ', views.update_patient_record_mg, name="update_patient_record_mg"),
    path('delete_record_mg/<str:pk>/ ', views.delete_record_mg, name="delete_record_mg"),
    path('view_profile_mg/<str:pk>/ ', views.view_profile_mg, name="view_profile_mg"),
    path('total_record_mg_admin/', views.total_record_mg_admin, name="total_record_mg_admin"),
    path('export_mucopoly/', views.export_mucopoly_user_csv, name="export_mucopoly"),
    path('mucopoly_qc/<str:pk>/', views.update_qa_qc_muco, name="update_qa_qc_muco"),
    path('view_qa_qc_muco/<str:pk>/', views.view_qa_qc_muco, name="view_qa_qc_muco"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
