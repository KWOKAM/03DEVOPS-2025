
from django.contrib.auth.models import User
from django.test import TestCase
from budgetapp import models
from budgetapp.utils.permissions import is_owner_or_admin


class TestPermissionsUtilisateurs(TestCase):
    """
    Ce fichier teste la fonction utilitaire 'is_owner_or_admin' utilisee pour
    controler les autorisations d'acces aux objets Budget et Groupes associes.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.utilisateur_proprio = User.objects.create(
            username='steve', password='!Rottou1234'
        )
        cls.utilisateur_autre = User.objects.create(
            username='visiteur', password='!Rottou1234'
        )
        cls.utilisateur_admin = User.objects.create(
            username='admin', password='adminpass', is_staff=True
        )

        cls.budget = models.Budget.objects.create(
            month='JAN', year=2025, owner=cls.utilisateur_proprio
        )

        cls.groupe = models.BudgetCategoryGroup.objects.create(
            name='Groupe Depenses Fixes', budget=cls.budget
        )

    def test_est_proprietaire_direct(self):
        self.assertTrue(is_owner_or_admin(self.utilisateur_proprio, self.budget))

    def test_est_proprietaire_indirect(self):
        self.assertTrue(is_owner_or_admin(self.utilisateur_proprio, self.groupe))

    def test_n_est_pas_proprietaire_direct(self):
        self.assertFalse(is_owner_or_admin(self.utilisateur_autre, self.budget))

    def test_n_est_pas_proprietaire_indirect(self):
        self.assertFalse(is_owner_or_admin(self.utilisateur_autre, self.groupe))

    def test_est_admin_acces_ok(self):
        self.assertTrue(is_owner_or_admin(self.utilisateur_admin, self.budget))
        self.assertTrue(is_owner_or_admin(self.utilisateur_admin, self.groupe))

    def test_objet_sans_proprietaire(self):
        objet_sans_owner = object()
        self.assertTrue(is_owner_or_admin(self.utilisateur_admin, objet_sans_owner))
