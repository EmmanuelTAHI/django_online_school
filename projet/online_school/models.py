from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = [
        ('admin', 'Admin'),
        ('responsable_scolarite', 'Responsable Scolarité'),
        ('enseignant', 'Enseignant'),
        ('etudiant', 'Étudiant'),
        ('comptable', 'Comptable'),
    ]
    role = models.CharField(max_length=25, choices=role_choices, default='etudiant')

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
        blank=True,
        help_text='Les groupes auxquels cet utilisateur appartient.',
        verbose_name='groupes'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
        blank=True,
        help_text='Permissions spécifiques pour cet utilisateur.',
        verbose_name='permissions utilisateur'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.role == 'admin':
                self.is_superuser = True
                self.is_staff = True
            elif self.role in ['responsable_scolarite', 'enseignant']:
                self.is_staff = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class ResponsableScolarite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Enseignant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cours = models.ManyToManyField('Cours', through='Inscription')


class StructureAcademique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()


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
    participants = models.ManyToManyField(CustomUser)
    historique_message = models.TextField()


class Forum(models.Model):
    nom_du_forum = models.CharField(max_length=255)
    date_creation = models.DateField(auto_now_add=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)


# Paiements et Comptabilité
class Paiement(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    etudiant = models.ForeignKey("Etudiant", on_delete=models.CASCADE)
    accountant = models.ForeignKey("Comptable", on_delete=models.SET_NULL, null=True, blank=True)

    
    def __str__(self):
        return f"Paiement de {self.montant}$ pour {self.etudiant.user.username}"


class Comptabilite(models.Model):
    paiements = models.ManyToManyField(Paiement)


class Comptable(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comptable: {self.user.username}"


from django import forms
from .models import Paiement

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['etudiant', 'montant']


class OnlineSchoolChatParticipant(models.Model):
    customuser = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
