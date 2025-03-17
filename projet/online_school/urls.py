from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import activate_account


urlpatterns = [
    path('', views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("courses/", views.courses, name="courses"),
    path("course-details/", views.course_details, name="course-details"),
    path("events/", views.events, name="events"),
    path("pricing/", views.pricing, name="pricing"),
    path("starter-page/", views.starter_page, name="starter-page"),
    path("trainers/", views.trainers, name="trainers"),
    path("ajouter/", views.ajouter, name="ajouter"),
    path("add_cours/", views.add_cours, name="add_cours"),

    

    path("login/", views.connexion, name="login"),
    path("register/", views.inscription, name="register"),
    path('activate/<uidb64>/<token>/',activate_account, name='activate_account'),

    # Gestion des mots de passe
    path('mot-de-passe-oublie/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name="password_reset"),
    path('mot-de-passe-oublie/confirme/',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
    path('mot-de-passe-oublie/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name="password_reset_confirm"),
    path('mot-de-passe-oublie/complet/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Gestion des fichiers médias en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
