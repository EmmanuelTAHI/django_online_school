from django import forms
from .models import CustomUser
# from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()

"""
 class ArticleForm(forms.ModelForm):
    contenu = forms.CharField(widget=CKEditorWidget())  # Ajout de CKEditor

    class Meta:
        model = Article
        fields = ['titre', 'couverture', 'resume', 'contenu', 'auteur_id', 'categorie_id', 'tag_ids', 'est_publie', 'date_de_publication', 'slug', 'statut']
        widgets = {
            'date_publication': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ["contenu"]
"""
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Changez ici pour utiliser CustomUser
        fields = ["username", "email", "password1", "password2",  'role',]
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige vers une page de connexion ou un message de succès
            return redirect('login')  # Remplace 'login' par l'URL de ta page de connexion
        else:
            # Ajoute un message d'erreur ou d'autres actions selon besoin
            print(form.errors)  # Pour afficher les erreurs dans la console pendant le développement
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
