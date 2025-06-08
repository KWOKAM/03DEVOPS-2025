"""
Ce fichier contient la def des modeles de donnees utilises dans l'app BudgetApp.

L'objectif principal est de permettre la gestion des budgets personnels et familiaux par utilisateur,
avec la possibilite de :
- creer des budgets mensuels,
- organiser les depenses par groupes et categories,
- suivre les transactions par beneficiaire,
- calculer les plafonds et les montants depenses automatiquement.

Modeles definis :
- Budget : represente un budget mensuel appartenant a un utilisateur.
- GroupeCategorieBudget : groupe de categories de depenses liees a un budget.
- CategorieBudget : categorie de depense associee a un groupe, avec un plafond et les depenses calculees.
- Transaction : depense enregistree pour une categorie, associee a un beneficiaire.
- Beneficiaire : personne ou entite ayant recu un paiement.

Chaque modele inclut des methodes utilitaires pour simplifier la gestion des donnees,
comme la duplication de categories ou le calcul automatique des depenses.

Toutes les relations sont concues pour respecter l'integrite des donnees et assurer un suivi precis
des finances personnelles.
"""

from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Budget(models.Model):
    CHOIX_MOIS = (
        ('JAN', 'Janvier'),
        ('FEB', 'Fevrier'),
        ('MAR', 'Mars'),
        ('APR', 'Avril'),
        ('MAY', 'Mai'),
        ('JUN', 'Juin'),
        ('JUL', 'Juillet'),
        ('AUG', 'Aout'),
        ('SEP', 'Septembre'),
        ('OCT', 'Octobre'),
        ('NOV', 'Novembre'),
        ('DEC', 'Decembre'),
    )

    MOIS_INDEX = {
        choix[0]: index for index, choix in enumerate(CHOIX_MOIS)
    }

    mois = models.CharField(max_length=100, choices=CHOIX_MOIS, default='JAN')
    annee = models.IntegerField(default=datetime.now().year)
    proprietaire = models.ForeignKey(
        'auth.User', related_name='budgets', on_delete=models.CASCADE
    )

    def copier_categories(self, budget_source):
        self.supprimer_categories()
        for groupe in budget_source.groupes_categories.all():
            categories = groupe.categories.all()
            groupe.pk = None
            groupe.budget = self
            groupe.save()
            for categorie in categories:
                categorie.pk = None
                categorie.groupe = groupe
                categorie.save()

    def supprimer_categories(self):
        self.groupes_categories.all().delete()

    @property
    def precedent(self):
        annee = self.annee
        index_mois = self.MOIS_INDEX[self.mois] - 1
        if index_mois < 0:
            index_mois = 11
            annee -= 1
        try:
            return Budget.objects.get(
                proprietaire=self.proprietaire,
                annee=annee,
                mois=self.CHOIX_MOIS[index_mois][0],
            )
        except Budget.DoesNotExist:
            return None

    class Meta:
        unique_together = ('proprietaire', 'mois', 'annee')
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        ordering = ['-annee', 'mois']

    def __str__(self):
        return f"{self.proprietaire.username} - {self.get_mois_display()} {self.annee}"


class GroupeCategorieBudget(models.Model):
    nom = models.CharField(max_length=100)
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name='groupes_categories'
    )

    @property
    def proprietaire(self):
        return self.budget.proprietaire

    class Meta:
        unique_together = ('nom', 'budget')
        verbose_name = "Groupe de categories"
        verbose_name_plural = "Groupes de categories"

    def __str__(self):
        return f"{self.nom} [{self.proprietaire.username}]"


class CategorieBudget(models.Model):
    nom = models.CharField(max_length=100)
    groupe = models.ForeignKey(
        GroupeCategorieBudget,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    plafond = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    @property
    def depense(self):
        return Decimal(
            Transaction.objects
            .filter(categorie_budget_id=self.pk)
            .aggregate(depense=Coalesce(Sum('montant'), Decimal(0)))['depense']
        )

    @property
    def proprietaire(self):
        return self.groupe.budget.proprietaire

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.nom} ({self.groupe.budget.get_mois_display()} {self.groupe.budget.annee}) [{self.proprietaire.username}]"


class Transaction(models.Model):
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    beneficiaire = models.ForeignKey('Beneficiaire', on_delete=models.CASCADE)
    categorie_budget = models.ForeignKey('CategorieBudget', on_delete=models.CASCADE)
    date = models.DateField()

    @property
    def proprietaire(self):
        return self.categorie_budget.groupe.budget.proprietaire

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.montant} - {self.beneficiaire.nom} - {self.date}"


class Beneficiaire(models.Model):
    nom = models.CharField(max_length=30)
    proprietaire = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('nom', 'proprietaire')
        verbose_name = "Beneficiaire"
        verbose_name_plural = "Beneficiaires"

    def __str__(self):
        return self.nom
