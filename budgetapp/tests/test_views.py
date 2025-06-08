
import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from budgetapp.views import ObtainAuthTokenCookieView, logout


class TestVueAuthentification(TestCase):
    """
    Cette classe teste les vues liees a l'authentification :
    - Obtention du token avec cookie securise
    - Deconnexion avec suppression du cookie
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.utilisateur = User.objects.create_user(
            username='steve',
            password='!Rottou1234',
            email='ronald.tatouk97@gmail.com',
        )

    def test_obtention_du_token_cookie(self):
        requete = self.factory.post(reverse('budgetapp:obtain-auth-token'), {
            'username': 'steve',
            'password': '!Rottou1234',
        })
        reponse = ObtainAuthTokenCookieView.as_view()(requete)
        cookie = reponse.cookies.get('Token')

        self.assertIsNotNone(cookie)
        self.assertTrue(cookie['httponly'])
        self.assertEqual(json.loads(reponse.content), {
            'username': 'steve',
            'email': 'ronald.tatouk97@gmail.com',
        })

    def test_deconnexion_supprime_cookie(self):
        requete = self.factory.get(reverse('budgetapp:logout'))
        reponse = logout(requete)
        cookie = reponse.cookies.get('Token')

        self.assertEqual(cookie.value, 'logout')
        self.assertTrue(cookie['httponly'])
        self.assertEqual(cookie['expires'], 'Wed, 21 Oct 1900 07:28:00 GMT')
