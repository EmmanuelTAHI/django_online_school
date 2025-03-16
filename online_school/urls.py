from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from online_school import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

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

    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("student_dashboard/",views.student,name="student_dashboard"),


    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='online_school/password_reset_form.html',
             email_template_name='online_school/password_reset_email.html',
             
             success_url='/password-reset/done/'  # URL explicite
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='online_school/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='online_school/password_reset_confirm.html',
             success_url='/reset/done/'  # URL explicite
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='online_school/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    path("activate/<uuid:token>/", views.activate_account, name="activate"),





    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('accountant_dashboard/', views.accountant_dashboard, name='accountant_dashboard'),
    path('home/', views.home, name='home'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Gestion des fichiers médias en mode debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
