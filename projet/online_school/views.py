from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .models import CustomUser
from .forms import CustomUserCreationForm


def index(request):
    return render(request, 'online_school/index.html')


def about(request):
    return render(request, 'online_school/about.html')


def contact(request):
    return render(request, 'online_school/contact.html')


def courses(request):
    return render(request, 'online_school/courses.html')


def course_details(request):
    return render(request, 'online_school/course-details.html')


def events(request):
    return render(request, 'online_school/events.html')


def pricing(request):
    return render(request, 'online_school/pricing.html')


def starter_page(request):
    return render(request, 'online_school/starter-page.html')


def trainers(request):
    return render(request, 'online_school/trainers.html')


# ==============================
# 🔐 Authentification (Connexion, Inscription, Déconnexion)
# ==============================

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username.strip(), password=password)

        if user:
            login(request, user)
            # Vérifier les rôles de l'utilisateur
            if user.is_superuser:
                return redirect('login')
            else:
                return redirect('index')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'registration/login.html')


def deconnexion(request):
    logout(request)
    return redirect('index')


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Désactiver le compte jusqu'à activation
            user.role = "admin"  # Assigner le rôle "admin" directement
            user.is_superuser = True
            user.is_staff = True
            user.save()

            # Génération du lien d'activation
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            activation_link = f"http://{domain}/activate/{uid}/{token}/"

            # Contenu du mail
            subject = "Activation de votre compte"
            message = f"""
            Bonjour {user.username},

            Merci de vous être inscrit. Veuillez cliquer sur le lien ci-dessous pour activer votre compte :

            {activation_link}

            Si vous n'avez pas demandé cette inscription, ignorez cet email.

            Merci,
            L'équipe de support.
            """

            # Envoi du mail
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [user.email])
            email.send(fail_silently=False)
            return render(request, 'online_school/base.html')  # Redirige l'utilisateur

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        messages.error(request, "Le lien d'activation est invalide ou a expiré.")

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)  # Connexion automatique après activation
        return redirect("index")

    return render(request, "registration/activation_failed.html")  # Page d’erreur


from django.shortcuts import render, redirect
from .models import Cours, Evaluation


def ajouter(request):
    cours_list = Cours.objects,
    context = {
        'cours_list': cours_list,
    }
    return render(request, 'online_school/ajouter.html', context)

def add_cours(request):
    if request.method == 'POST':
        Cours.objects.create(
            titre=request.POST['titre_cours'],
            description=request.POST['description'],
            professeur=request.user
        )
        return redirect('ajouter')
    return redirect('ajouter')


def ajouter_devoir(request):
    if request.method == 'POST':
        Evaluation.objects.create(
            titre=request.POST['titre_devoir'],
            cours_id=request.POST['cours_id'],
            date_limite=request.POST['date_limite']
        )
        return redirect('ajouter')
    return redirect('ajouter')


def ajouter_evaluation(request):
    if request.method == 'POST':
        Evaluation.objects.create(
            titre=request.POST['titre_eval'],
            cours_id=request.POST['cours_id'],
            date=request.POST['date_eval'],
            note_max=request.POST['note_max']
        )
        return redirect('ajouter')
    return redirect('ajouter')


    