from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_pid/', views.add_record_pid, name="add_record_pid"),
    path('demographic8/<str:pk>/', views.pid_demographic, name="pid_demographic"),
    path('total_record_pid/', views.total_record_pid, name="total_record_pid"),
    path('update_record_pid/<str:pk>/ ', views.update_record_pid, name="update_record_pid"),
    path('delete_record_pid/<str:pk>/ ', views.delete_record_pid, name="delete_record_pid"),
    path('view_record_pid/<str:pk>/ ', views.view_record_pid, name="view_record_pid"),
    path('update_patient_record_pid/<str:pk>/ ', views.update_patient_record_pid, name="update_patient_record_pid"),
    path('view_profile_pid/<str:pk>/ ', views.view_profile_pid, name="view_profile_pid"),
    path('update_qa_qc_pid/<str:pk>/ ', views.update_qa_qc_pid, name="update_qa_qc_pid"),
    path('view_qa_qc_pid/<str:pk>/ ', views.view_qa_qc_pid, name="view_qa_qc_pid"),
    path('total_record_pid_admin/', views.total_record_pid_admin, name="total_record_pid_admin"),
    path('export_pid/', views.export_pid_user_csv, name="export_pid"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
