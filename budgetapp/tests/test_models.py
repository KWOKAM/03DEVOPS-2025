

from datetime import datetime
from decimal import Decimal

from budgetapp import models
from django.contrib.auth.models import User
from django.test import TestCase


class TestBudget(TestCase):
    """
    Cette classe teste le fonctionnement des objets Budget :
    - la methode de copie des categories entre budgets,
    - la detection du budget precedent dans la chronologie.
    """

    def setUp(self):
        self.utilisateur = User.objects.create(username='test', password='test')

        self.budget_janvier = models.Budget.objects.create(
            month='JAN', year=2000, owner=self.utilisateur
        )
        groupe_janvier = models.BudgetCategoryGroup.objects.create(
            name='Groupe Janvier', budget=self.budget_janvier
        )
        models.BudgetCategory.objects.create(category='Categorie A', group=groupe_janvier, limit=100)
        models.BudgetCategory.objects.create(category='Categorie B', group=groupe_janvier, limit=200)

        self.budget_fevrier = models.Budget.objects.create(
            month='FEB', year=2000, owner=self.utilisateur
        )
        groupe_fevrier = models.BudgetCategoryGroup.objects.create(
            name='Groupe Fevrier', budget=self.budget_fevrier
        )
        models.BudgetCategory.objects.create(category='Categorie C', group=groupe_fevrier, limit=100)
        models.BudgetCategory.objects.create(category='Categorie D', group=groupe_fevrier, limit=200)

    def test_copie_categories(self):
        self.budget_janvier.copy_categories(self.budget_fevrier)

        groupes = list(
            self.budget_janvier.budget_category_groups.order_by('name').values_list('name', flat=True)
        )
        self.assertEqual(groupes, ['Groupe Fevrier'])

        categories = list(
            models.BudgetCategory.objects.filter(group__budget=self.budget_janvier)
            .order_by('category')
            .values_list('category', flat=True)
        )
        self.assertEqual(categories, ['Categorie C', 'Categorie D'])

    def test_budget_precedent(self):
        self.assertEqual(self.budget_fevrier.previous, self.budget_janvier)

    def test_aucun_budget_precedent(self):
        self.assertIsNone(self.budget_janvier.previous)

    def test_budget_precedent_annee_prec(self):
           budget_decembre = models.Budget.objects.create(
            month='DEC', year=1999, owner=self.utilisateur
        )
        self.assertEqual(self.budget_janvier.previous, budget_decembre)


class TestCategorieBudgetaire(TestCase):

    def setUp(self):
        self.utilisateur = User.objects.create(username='test', password='test')
        budget = models.Budget.objects.create(month='JAN', year=2000, owner=self.utilisateur)
        self.groupe = models.BudgetCategoryGroup.objects.create(name='Groupe Principal', budget=budget)
        self.destinataire = models.Payee.objects.create(name='Fournisseur A', owner=self.utilisateur)

    def test_depense_sans_transaction(self):
         categorie = models.BudgetCategory.objects.create(
            category='Sans mouvement', group=self.groupe, limit=100
        )
        self.assertEqual(categorie.spent, Decimal(0))

    def test_depense_positive(self):
        categorie = models.BudgetCategory.objects.create(
            category='Depenses courantes', group=self.groupe, limit=100
        )
        models.Transaction.objects.create(budget_category=categorie, payee=self.destinataire, amount=100, date=datetime.now())
        models.Transaction.objects.create(budget_category=categorie, payee=self.destinataire, amount=100, date=datetime.now())
        self.assertEqual(categorie.spent, Decimal(200))

    def test_depense_negative(self):
        categorie = models.BudgetCategory.objects.create(
            category='Correction', group=self.groupe, limit=100
        )
        models.Transaction.objects.create(budget_category=categorie, payee=self.destinataire, amount=100, date=datetime.now())
        models.Transaction.objects.create(budget_category=categorie, payee=self.destinataire, amount=-200, date=datetime.now())
        self.assertEqual(categorie.spent, Decimal(-100))
