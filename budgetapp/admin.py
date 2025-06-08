from django.contrib import admin
from .models import Budget, CategorieBudget, GroupeCategorieBudget, Transaction


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('mois', 'annee', 'proprietaire')
    list_filter = ('mois', 'annee')
    search_fields = ('proprietaire__username',)

    def mois(self, obj):
        return obj.mois
    mois.short_description = 'Mois'

    def annee(self, obj):
        return obj.annee
    annee.short_description = 'Annee'

    def proprietaire(self, obj):
        return obj.proprietaire.username
    proprietaire.short_description = 'Proprietaire'


@admin.register(GroupeCategorieBudget)
class GroupeCategorieBudgetAdmin(admin.ModelAdmin):
    list_display = ('nom_du_groupe', 'budget_associe')
    search_fields = ('nom',)

    def nom_du_groupe(self, obj):
        return obj.nom
    nom_du_groupe.short_description = 'Nom du groupe'

    def budget_associe(self, obj):
        return f"{obj.budget.mois} {obj.budget.annee}"
    budget_associe.short_description = 'Budget associe'


@admin.register(CategorieBudget)
class CategorieBudgetAdmin(admin.ModelAdmin):
    list_display = ('categorie', 'groupe', 'plafond')
    list_filter = ('groupe',)
    search_fields = ('categorie',)

    def categorie(self, obj):
        return obj.categorie
    categorie.short_description = 'Categorie'

    def groupe(self, obj):
        return obj.groupe.nom
    groupe.short_description = 'Groupe'

    def plafond(self, obj):
        return obj.plafond
    plafond.short_description = 'Plafond (EUR)'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('montant', 'destinataire', 'categorie_budgetaire', 'date')
    list_filter = ('date', 'allocation_detail')
    search_fields = ('destinataire__nom',)

    def montant(self, obj):
        return obj.montant
    montant.short_description = 'Montant (EUR)'

    def destinataire(self, obj):
        return obj.destinataire.nom
    destinataire.short_description = 'Destinataire'

    def categorie_budgetaire(self, obj):
        return obj.allocation_detail.categorie
    categorie_budgetaire.short_description = 'Categorie budgetaire'
