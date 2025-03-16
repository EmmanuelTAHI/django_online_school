from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses/", views.courses, name="courses"),
    path("course-details/", views.course_details, name="course-details"),
    path("events/", views.events, name="events"),
    path("pricing/", views.pricing, name="pricing"),
    path("starter-page/", views.starter_page, name="starter-page"),
    path("trainers/", views.trainers, name="trainers"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Gestion des fichiers médias en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
