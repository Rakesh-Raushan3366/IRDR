from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers
from . import views
urlpatterns = [
    path('add_record_bd/', views.add_record_bd, name="add_record_bd"),
    path('view_profile_bd/<str:pk>/ ', views.view_profile_bd, name="view_profile_bd"),
    path('demographic_bd/<str:pk>/', views.demographic_bd, name="demographic_bd"),
    path('total_record_bd/', views.total_record_bd, name="total_record_bd"),
    path('view_record_bd/<str:pk>/ ', views.view_record_bd, name="view_record_bd"),
    path('update_patient_record_bd/<str:pk>/ ', views.update_patient_record_bd, name="update_patient_record_bd"),
    path('update_record_bd/<str:pk>/ ', views.update_record_bd, name="update_record_bd"),
    path('delete_record_bd/<str:pk>/ ', views.delete_record_bd, name="delete_record_bd"),
    path('update_qa_qc_bleeding/<str:pk>/ ', views.update_qa_qc_bleeding, name="update_qa_qc_bleeding"),
    path('view_qa_qc_bleeding/<str:pk>/ ', views.view_qa_qc_bleeding, name="view_qa_qc_bleeding"),
    path('total_record_bd_admin/', views.total_record_bd_admin, name="total_record_bd_admin"),
    path('export_bleeding/', views.export_bleeding_user_csv, name="export_bleeding"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
