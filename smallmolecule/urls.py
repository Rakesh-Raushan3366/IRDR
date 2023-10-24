from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_sm/', views.add_record_sm, name="add_record_sm"),
    path('demographic7/<str:pk>/', views.sm_demographic, name="sm_demographic"),
    path('total_record_sm/', views.total_record_sm, name="total_record_sm"),
    path('update_record_sm/<str:pk>/ ', views.update_record_sm, name="update_record_sm"),
    path('delete_record_sm/<str:pk>/ ', views.delete_record_sm, name="delete_record_sm"),
    path('view_record_sm/<str:pk>/ ', views.view_record_sm, name="view_record_sm"),
    path('update_patient_record_sm/<str:pk>/ ', views.update_patient_record_sm, name="update_patient_record_sm"),
    path('view_profile_sm/<str:pk>/ ', views.view_profile_sm, name="view_profile_sm"),
    path('update_qa_qc_small/<str:pk>/ ', views.update_qa_qc_small, name="update_qa_qc_small"),
    path('view_qa_qc_small/<str:pk>/ ', views.view_qa_qc_small, name="view_qa_qc_small"),
    path('total_record_sm_admin/', views.total_record_sm_admin, name="total_record_sm_admin"),
    path('export_smallmolecule/', views.export_smallmolecule_user_csv, name="export_smallmolecule"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
