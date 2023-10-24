from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [

    path('add_record_nmd/', views.add_record_nmd, name="add_record_nmd"),
    path('demographic5/<str:pk>/', views.nmd_demographic, name="NMD_demographic"),
    path('total_record_nmd/', views.total_record_nmd, name="total_record_nmd"),
    path('view_record_nmd/<str:pk>/ ', views.view_record_nmd, name="view_record_nmd"),
    path('update_record_nmd/<str:pk>/ ', views.update_record_nmd, name="update_record_nmd"),
    path('delete_record_nmd/<str:pk>/ ', views.delete_record_nmd, name="delete_record_nmd"),
    path('update_patient_record_nmd/<str:pk>/ ', views.update_patient_record_nmd, name="update_patient_record_nmd"),
    path('view_profile_record_nmd/<str:pk>/ ', views.view_profile_record_nmd, name="view_profile_record_nmd"),
    path('update_qa_qc_nmd/<str:pk>/ ', views.update_qa_qc_nmd, name="update_qa_qc_nmd"),
    path('view_qa_qc_nmd/<str:pk>/ ', views.view_qa_qc_nmd, name="view_qa_qc_nmd"),
    path('total_record_nmd_admin/', views.total_record_nmd_admin, name="total_record_nmd_admin"),
    path('export_dystonmd_csv_user/', views.export_dystonmd_csv_user, name="export_dystonmd_csv_user"),
    path('export_spinalnmd_csv_user/', views.export_spinalnmd_csv_user, name="export_spinalnmd_csv_user"),
    path('export_limbnmd_csv_user/', views.export_limbnmd_csv_user, name="export_limbnmd_csv_user"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
