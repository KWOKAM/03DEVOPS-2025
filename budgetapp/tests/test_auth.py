
from budgetapp.tests.utils import auth_util
from budgetapp.urls import app_name
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BaseTestMixin:
    """
    Mixin general pour tester les principales operations CRUD
    avec et sans authentification sur un modele donne.
    """

    def setUp(self):
        auth_util.create_test_users()
        self.setup_test_models(self.client)

    @staticmethod
    def setup_test_models(client):
        pass

    def test_liste_sans_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_sans_auth(self):
        response = auth_util.detail_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creation_sans_auth(self):
        response = auth_util.post_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modif_sans_auth(self):
        response = auth_util.put_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_suppression_sans_auth(self):
        response = auth_util.delete_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        def test_liste_avec_auth(self):
        response = auth_util.list_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_avec_auth(self):
        response = auth_util.detail_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_avec_auth(self):
        response = auth_util.post_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modif_avec_auth(self):
        response = auth_util.put_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_suppression_avec_auth(self):
        response = auth_util.delete_test(self.client, self.model_name, auth=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_detail_autre_utilisateur(self):
        response = auth_util.detail_cross_user_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_modif_autre_utilisateur(self):
        response = auth_util.put_cross_user_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_suppression_autre_utilisateur(self):
        response = auth_util.delete_cross_user_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BudgetTests(BaseTestMixin, APITestCase):
    model_name = auth_util.BUDGET_NAME


class CategoryTests(BaseTestMixin, APITestCase):
    model_name = auth_util.CATEGORY_NAME


class CategoryBudgetGroupTests(BaseTestMixin, APITestCase):
    model_name = auth_util.CATEGORYBUDGETGROUP_NAME

    @staticmethod
    def setup_test_models(client):
        BudgetTests.setup_test_models(client)
        response = auth_util.create_test_model(client, auth_util.BUDGET_NAME)
        auth_util.post_data[auth_util.CATEGORYBUDGETGROUP_NAME]['budget'] = response.data['url']


class UserTests(BaseTestMixin, APITestCase):
    model_name = auth_util.USER_NAME

    def setUp(self):
        super(UserTests, self).setUp()
        user1 = User.objects.get(username=auth_util.test_users[0]['username'])
        user2 = User.objects.get(username=auth_util.test_users[1]['username'])
        self.detail_url = auth_util.get_url(self.model_name, 'detail', args=[user1.pk])
        self.detail_url2 = auth_util.get_url(self.model_name, 'detail', args=[user2.pk])

    def test_liste_users_non_auth(self):
        response = auth_util.list_test(self.client, self.model_name)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail_user_non_auth(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creation_user_non_auth(self):
        url = auth_util.get_url(self.model_name, 'create')
        response = self.client.post(url, auth_util.post_data[self.model_name])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modif_user_non_auth(self):
        response = self.client.put(self.detail_url, auth_util.post_data[self.model_name])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_suppression_user_non_auth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_liste_users_auth_non_admin(self):
        response = auth_util.list_test(self.client, self.model_name, True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_user_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.get(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creation_user_auth(self):
        auth_util.login_test_user(self.client)
        url = app_name + ':' + self.model_name + '-create'
        response = self.client.post(reverse(url), auth_util.post_data[self.model_name])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modif_user_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.put(self.detail_url, auth_util.post_data[self.model_name])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_suppression_user_auth(self):
        auth_util.login_test_user(self.client)
        response = self.client.delete(self.detail_url)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

     def test_detail_autre_user_interdit(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.get(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modif_autre_user_interdit(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.put(self.detail_url2, auth_util.post_data[self.model_name])
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_suppression_autre_user_interdit(self):
        auth_util.login_test_user(self.client, index=0)
        response = self.client.delete(self.detail_url2)
        self.client.logout()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
