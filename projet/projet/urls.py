from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('online_school.urls')),  # Inclure les URLs de l'application
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]
