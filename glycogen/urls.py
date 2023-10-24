from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [

    path('add_record_gl/', views.add_record_gl, name="add_record_gl"),
    path('view_profile_gl/<str:pk>/ ', views.view_profile_gl, name="view_profile_gl"),
    path('demographic_gl/<str:pk>/', views.demographic_gl, name="demographic_gl"),
    path('total_record_gl/', views.total_record_gl, name="total_record_gl"),
    path('delete_record_gl/<str:pk>/ ', views.delete_record_gl, name="delete_record_gl"),
    path('update_patient_record_gl/<str:pk>/ ', views.update_patient_record_gl, name="update_patient_record_gl"),
    path('view_record_gl/<str:pk>/ ', views.view_record_gl, name="view_record_gl"),
    path('update_record_gl/<str:pk>/ ', views.update_record_gl, name="update_record_gl"),
    path('total_record_gl_admin/', views.total_record_gl_admin, name="total_record_gl_admin"),
    path('export_gylcogen/ ', views.export_gylcogen_user_csv, name="export_gylcogen"),
    path('update_qa_qc_gsd/<str:pk>/ ', views.update_qa_qc_gsd, name="update_qa_qc_gsd"),
    path('view_qa_qc_gsd/<str:pk>/ ', views.view_qa_qc_gsd, name="view_qa_qc_gsd"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
