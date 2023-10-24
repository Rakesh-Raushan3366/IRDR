from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_fb/', views.add_record_fb, name="add_record_fb"),
    path('view_profile_fb/<str:pk>/ ', views.view_profile_fb, name="view_profile_fb"),
    path('demographic_fb/<str:pk>/', views.demographic_fb, name="demographic_fb"),
    path('total_record_fb/', views.total_record_fb, name="total_record_fb"),
    path('view_record_fb/<str:pk>/ ', views.view_record_fb, name="view_record_fb"),
    path('update_record_fb/<str:pk>/ ', views.update_record_fb, name="update_record_fb"),
    path('delete_record_fb/<str:pk>/ ', views.delete_record_fb, name="delete_record_fb"),
    path('update_patient_record_fb/<str:pk>/ ', views.update_patient_record_fb, name="update_patient_record_fb"),
    path('view_qa_qc_fabry/<str:pk>/ ', views.view_qa_qc_fabry, name="view_qa_qc_fabry"),
    path('update_qa_qc_fabry/<str:pk>/ ', views.update_qa_qc_fabry, name="update_qa_qc_fabry"),
    path('total_record_fb_admin/', views.total_record_fb_admin, name="total_record_fb_admin"),
    path('export_fabry/', views.export_fabry_user_csv, name="export_fabry"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
