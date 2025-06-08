
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from rest_framework.test import force_authenticate

from budgetapp.models import Budget, BudgetCategory, BudgetCategoryGroup
from budgetapp.serializers import BudgetCategorySerializer


class TestSerializerCategorieBudgetaire(TestCase):
    """
    Serie de tests permettant de valider les regles de validation
    du serializer BudgetCategorySerializer.
    """

    def setUp(self):
        self.utilisateur_1 = User.objects.create(username='steve', password='!Rottou1234')
        self.utilisateur_2 = User.objects.create(username='ronald', password='!Rottou1234')

        self.budget = Budget.objects.create(month='JAN', year=2000, owner=self.utilisateur_1)
        self.groupe = BudgetCategoryGroup.objects.create(name='Groupe Principal', budget=self.budget)

        self.categorie_existante = BudgetCategory.objects.create(
            category='Courses',
            group=self.groupe,
            limit=100
        )
        self.requete_factory = RequestFactory()

    def test_categorie_budget_valide(self):
        requete = self.requete_factory.post('/budgetcategories/')
        requete.user = self.utilisateur_1

        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.groupe.budget.year,
                'budget_month': self.groupe.budget.month,
                'category': 'Transport',
                'group': self.groupe.name,
                'limit': 150,
            },
            context={'request': requete},
        )

        self.assertTrue(serializer.is_valid())

    def test_categorie_budget_dupliquee(self):
        requete = self.requete_factory.post('/budgetcategories/')
        requete.user = self.utilisateur_1

        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.groupe.budget.year,
                'budget_month': self.groupe.budget.month,
                'category': 'Courses',
                'group': self.groupe.name,
                'limit': 100,
            },
            context={'request': requete},
        )

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'non_field_errors': ['Category must be unique within this budget.']}
        )

    def test_categorie_identique_utilisateur_different(self):
        requete = self.requete_factory.post('/budgetcategories/')
        requete.user = self.utilisateur_2  

        serializer = BudgetCategorySerializer(
            data={
                'budget_year': self.groupe.budget.year,
                'budget_month': self.groupe.budget.month,
                'category': 'Courses', 
                'group': self.groupe.name,
                'limit': 120,
            },
            context={'request': requete},
        )

        self.assertTrue(serializer.is_valid())
