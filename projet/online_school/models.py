from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Utilisateur générique
class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
<<<<<<< HEAD
        ('responsable_scolarite', 'Responsable Scolarité'),
    )
    role = models.CharField(max_length=25, choices=ROLES, default='etudiant')
=======
        ('etudiant', 'Étudiant'),
        ('comptable', 'Comptable'),
    ]
    role = models.CharField(max_length=25, choices=role_choices, default='etudiant')
>>>>>>> a22106b4e75243569d8303c282204ed625154228

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

    def _str_(self):
        return f"{self.username} ({self.get_role_display()})"
<<<<<<< HEAD

# Profils spécifiques
=======
# Admin
>>>>>>> a22106b4e75243569d8303c282204ed625154228
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} (Admin)"

class ResponsableScolarite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} (Responsable Scolarité)"

class Enseignant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} (Enseignant)"

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    score_etudiant = models.IntegerField(default=0)
    cours = models.ManyToManyField('Cours', through='Inscription')
    def __str__(self):
        return f"{self.user.username} (Étudiant)"

# Structure Académique
class StructureAcademique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
<<<<<<< HEAD
    def __str__(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    enseignant = models.ForeignKey('Enseignant', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return self.nom

class Cours(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)  # Référence différée
=======

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)

class Cours(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)

>>>>>>> a22106b4e75243569d8303c282204ed625154228
    def __str__(self):
        return self.titre

class FormatCours(models.Model):
    type_choices = [('texte', 'Texte'), ('image', 'Image'), ('pdf', 'PDF'), ('video', 'Vidéo')]
    type = models.CharField(max_length=10, choices=type_choices)
<<<<<<< HEAD
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return f"{self.type} - {self.cours}"
=======
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
>>>>>>> a22106b4e75243569d8303c282204ed625154228

class Lecon(models.Model):
    titre_lecon = models.CharField(max_length=255)
    num_lecon = models.IntegerField()
<<<<<<< HEAD
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return self.titre_lecon

class Chapitre(models.Model):
    nom_chapitre = models.CharField(max_length=255)
    lecons = models.ManyToManyField('Lecon')  # Référence différée
    def __str__(self):
        return self.nom_chapitre

class Inscription(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)  # Référence différée
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return f"{self.etudiant} - {self.cours}"
=======
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)

class Chapitre(models.Model):
    nom_chapitre = models.CharField(max_length=255)
    lecons = models.ManyToManyField(Lecon)

class Inscription(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
>>>>>>> a22106b4e75243569d8303c282204ed625154228

# Évaluation et Résultats
class Evaluation(models.Model):
    type_choices = [('quiz', 'Quiz'), ('devoir', 'Devoir')]
    type = models.CharField(max_length=10, choices=type_choices)
    date_limite = models.DateField()
    nombre_tentatives = models.IntegerField()
<<<<<<< HEAD
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return f"{self.type} - {self.cours}"
=======
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
>>>>>>> a22106b4e75243569d8303c282204ed625154228

class Resultat(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)  # Référence différée
    evaluation = models.ForeignKey('Evaluation', on_delete=models.CASCADE)  # Référence différée
    note = models.FloatField()
    def __str__(self):
        return f"{self.etudiant} - {self.evaluation}: {self.note}"

<<<<<<< HEAD
=======
# Notes
>>>>>>> a22106b4e75243569d8303c282204ed625154228
class Notes(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)  # Référence différée
    points = models.FloatField()
<<<<<<< HEAD
    def __str__(self):
        return f"{self.etudiant} - {self.points}"
=======
>>>>>>> a22106b4e75243569d8303c282204ed625154228

# Chat et Forum
class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser)
    historique_message = models.TextField()
<<<<<<< HEAD
    def __str__(self):
        return f"Chat avec {len(self.participants.all())} participants"
=======
>>>>>>> a22106b4e75243569d8303c282204ed625154228

class Forum(models.Model):
    nom_du_forum = models.CharField(max_length=255)
    date_creation = models.DateField(auto_now_add=True)
<<<<<<< HEAD
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return self.nom_du_forum
=======
    cours = models.ForeignKey('Cours', on_delete=models.CASCADE)
>>>>>>> a22106b4e75243569d8303c282204ed625154228

# Paiements et Comptabilité
class Paiement(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
<<<<<<< HEAD
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)  # Référence différée
    def __str__(self):
        return f"{self.montant} - {self.etudiant}"

class Comptabilite(models.Model):
    paiements = models.ManyToManyField('Paiement')  # Référence différée
    def __str__(self):
        return f"Comptabilité avec {len(self.paiements.all())} paiements"
=======
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

class Comptabilite(models.Model):
    paiements = models.ManyToManyField(Paiement)


    
>>>>>>> a22106b4e75243569d8303c282204ed625154228
