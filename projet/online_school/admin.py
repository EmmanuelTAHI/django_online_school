from django.contrib import admin
from .models import (
    CustomUser, Admin, ResponsableScolarite, StructureAcademique, Enseignant,
    Matiere, Cours, FormatCours, Lecon, Chapitre, Etudiant, Inscription,
    Evaluation, Resultat, Notes, Chat, Forum, Paiement, Comptabilite, Comptable
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(ResponsableScolarite)
class ResponsableScolariteAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(StructureAcademique)
class StructureAcademiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'enseignant')
    search_fields = ('nom',)
    list_filter = ('enseignant',)


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere')
    search_fields = ('titre',)
    list_filter = ('matiere',)


@admin.register(FormatCours)
class FormatCoursAdmin(admin.ModelAdmin):
    list_display = ('type', 'cours')
    list_filter = ('type',)


@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre_lecon', 'num_lecon', 'cours')
    search_fields = ('titre_lecon',)


@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('nom_chapitre',)
    search_fields = ('nom_chapitre',)


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours')
    list_filter = ('cours',)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('type', 'date_limite', 'nombre_tentatives', 'cours')
    list_filter = ('type', 'cours')


@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'evaluation', 'note')
    list_filter = ('evaluation',)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'points')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'historique_message')


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('nom_du_forum', 'date_creation', 'cours')
    list_filter = ('cours',)


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('montant', 'date_paiement', 'etudiant')
    list_filter = ('date_paiement', 'etudiant')


@admin.register(Comptabilite)
class ComptabiliteAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Comptable)
class ComptableAdmin(admin.ModelAdmin):
    list_display = ('user',)
