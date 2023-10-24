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


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
