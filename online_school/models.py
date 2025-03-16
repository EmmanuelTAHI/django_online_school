from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Utilisateur générique
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='online_school_users',  # Change the related_name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='online_school_users',  # Change the related_name to avoid conflict
        blank=True
    )



# Admin
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Responsable Scolarité
class ResponsableScolarite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# Structure Académique
class StructureAcademique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()


# Cours et Matières
class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)


class Cours(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)


class FormatCours(models.Model):
    type_choices = [('texte', 'Texte'), ('image', 'Image'), ('pdf', 'PDF'), ('video', 'Vidéo')]
    type = models.CharField(max_length=10, choices=type_choices)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


class Lecon(models.Model):
    titre_lecon = models.CharField(max_length=255)
    num_lecon = models.IntegerField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


class Chapitre(models.Model):
    nom_chapitre = models.CharField(max_length=255)
    lecons = models.ManyToManyField(Lecon)


# Étudiant
class Etudiant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cours = models.ManyToManyField(Cours, through='Inscription')


class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


# Évaluation et Résultats
class Evaluation(models.Model):
    type_choices = [('quiz', 'Quiz'), ('devoir', 'Devoir')]
    type = models.CharField(max_length=10, choices=type_choices)
    date_limite = models.DateField()
    nombre_tentatives = models.IntegerField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


class Resultat(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    note = models.FloatField()


# Notes
class Notes(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    points = models.FloatField()


# Chat et Forum
class Chat(models.Model):
    participants = models.ManyToManyField(User)
    historique_message = models.TextField()


class Forum(models.Model):
    nom_du_forum = models.CharField(max_length=255)
    date_creation = models.DateField(auto_now_add=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


# Paiements et Comptabilité
class Paiement(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)


class Comptabilite(models.Model):
    paiements = models.ManyToManyField(Paiement)




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)  # Nouveau champ



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLES = (
        ('administrateur', 'Administrateur'),
        ('etudiant', 'Étudiant'),
        ('professeur', 'Professeur'),
        ('comptable', 'Comptable'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='etudiant')

    def __str__(self):
        return f"{self.user.username} - {self.role}"