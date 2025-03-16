from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages

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

def student(request):
    return render(request,  'online_school/student_dashboard.html')

def teacher_dashboard(request):
    return render(request,'online_school/teacher_dashboard.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Récupérer le rôle depuis le modèle Profile
            try:
                profile = Profile.objects.get(user=user)
                role = profile.role
                # Rediriger selon le rôle
                if role == 'administrateur':
                    return redirect('admin_dashboard')
                elif role == 'etudiant':
                    return redirect('student_dashboard')
                elif role == 'professeur':
                    return redirect('teacher_dashboard')
                elif role == 'comptable':
                    return redirect('accountant_dashboard')
                else:
                    return redirect('home')  # Page par défaut
            except Profile.DoesNotExist:
                messages.error(request, "Erreur : Profil utilisateur non trouvé.")
                return render(request, 'online_school/login.html', {'username': username})
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'online_school/login.html', {'username': username})

    # Pour une requête GET, afficher le formulaire vide
    return render(request, 'online_school/login.html')



def logout_view(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('index')  # Redirige vers la page d'accueil


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        # Vérifier si les mots de passe correspondent
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'online_school/register.html', {
                'username': username,
                'email': email,
                'role': role,
            })

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'online_school/register.html', {
                'username': username,
                'email': email,
                'role': role,
            })

        # Vérifier si l'email existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'online_school/register.html', {
                'username': username,
                'email': email,
                'role': role,
            })

        # Créer l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        # Créer le profil associé avec le rôle
        Profile.objects.create(user=user, role=role)

        # Authentifier et connecter l'utilisateur
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            # Rediriger selon le rôle
            if role == 'administrateur':
                return redirect('admin_dashboard')
            elif role == 'etudiant':
                return redirect('index')
            elif role == 'professeur':
                return redirect('teacher_dashboard')
            elif role == 'comptable':
                return redirect('accountant_dashboard')
            else:
                return redirect('home')

    # Pour une requête GET, renvoyer le formulaire vide
    return render(request, 'online_school/register.html')

def password_reset(request):
    datas = {

    }
    return render(request,'password_reset.html', datas)



def activate_account(request, token):
    try:
        user_profile = UserProfile.objects.get(activation_token=token)
        user = user_profile.user
        user.is_active = True  # Activate the user
        user.save()
        messages.success(request, "Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.")
        return redirect("login.html")
    except UserProfile.DoesNotExist:
        messages.error(request, "Le lien d'activation est invalide ou expiré.")
        return redirect("register.html")



# Ajoutez ces fonctions à votre fichier views.py

def password_reset_confirm(request, uidb64, token):
    """Vue pour traiter le formulaire de nouveau mot de passe"""
    User = get_user_model()
    try:
        # Décodage de l'uidb64 pour obtenir l'ID utilisateur
        from django.utils.http import urlsafe_base64_decode
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        
        # Vérification du token
        from django.contrib.auth.tokens import default_token_generator
        validlink = default_token_generator.check_token(user, token)
        
        if request.method == "POST" and validlink:
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Votre mot de passe a été changé avec succès. Vous pouvez maintenant vous connecter.")
                return redirect('blog:password_reset_complete')
            else:
                # Formulaire invalide, afficher les erreurs
                return render(request, 'password_reset_confirm.html', {
                    'form': form,
                    'validlink': True,
                    'uidb64': uidb64,
                    'token': token
                })
        else:
            # Affichage initial du formulaire
            form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {
                'form': form,
                'validlink': validlink,
                'uidb64': uidb64,
                'token': token
            })
            
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # Lien invalide
        return render(request, 'password_reset_confirm.html', {
            'validlink': False
        })




from django.shortcuts import render

def admin_dashboard(request):
    return render(request, 'online_school/admin_dashboard.html', {'user': request.user})

def student_dashboard(request):
    return render(request, 'online_school/student_dashboard.html', {'user': request.user})

def teacher_dashboard(request):
    return render(request, 'online_school/teacher_dashboard.html', {'user': request.user})

def accountant_dashboard(request):
    return render(request, 'online_school/accountant_dashboard.html', {'user': request.user})

def home(request):
    return render(request, 'online_school/home.html', {'user': request.user})