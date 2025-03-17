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


def contact(request):
    return render(request, 'online_school/contact.html')


def course_details(request):
    return render(request, 'online_school/course-details.html')


def starter_page(request):
    return render(request, 'online_school/starter-page.html')



# ==============================
# 🔐 Authentification (Connexion, Inscription, Déconnexion)
# ==============================

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username.strip(), password=password)

        if user:
            login(request, user)

            # Vérification des rôles et redirection
            if user.is_superuser:
                return redirect('index')  # Redirection admin

            if hasattr(user, 'role'):  # Vérifie si le champ "role" existe
                if user.role == 'etudiant':
                    return redirect('dashboard_etudiant')
                elif user.role == 'comptable':
                    return redirect('online_school/dashboard_comptable')
                else:
                    return redirect('index')  # Par défaut
            
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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Paiement, Comptable
from .forms import PaiementForm

@login_required
def create_payment(request):
    try:
        comptable = Comptable.objects.get(user=request.user)
    except Comptable.DoesNotExist:
        return HttpResponseForbidden("Vous devez être un comptable pour effectuer un paiement.")

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.accountant = comptable
            paiement.save()
            return redirect('liste_paiements')
    else:
        form = PaiementForm()

    return render(request, 'online_school/dashboard_comptable.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
@login_required
def comptable_dashboard(request):
    if request.user.role != 'comptable':
        return HttpResponseForbidden("Accès interdit")
    return render(request, 'online_school/dashboard_comptable.html')

def liste_paiements(request):

    if not request.user.is_authenticated or request.user.role != 'comptable':
        return HttpResponseForbidden("Accès interdit")  


    paiements = Paiement.objects.all()


    return render(request, 'online_school/liste_paiement.html', {'paiements': paiements})