from budgetapp.urls import app_name
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

BUDGET = 'budget'
CATEGORIE_BUDGETAIRE = 'categoriebudget'
GROUPE_CATEGORIES = 'groupecategoriebudget'
TRANSACTION = 'transaction'
UTILISATEUR = 'user'

donnees_post = {
    BUDGET: {
        'month': 'JAN',
        'year': 2025,
    },
    CATEGORIE_BUDGETAIRE: {
        'budget_month': 'JAN',
        'budget_year': 2025,
        'group': 'test',
        'category': 'Courses',
    },
    GROUPE_CATEGORIES: {
        'name': 'test',
        'budget': '',
    },
    UTILISATEUR: {
        'username': 'test',
        'email': 'test@test.com',
        'password': 'test',
    }
}

utilisateurs_test = [
    {'username': 'test0', 'email': 'test0@test.com', 'password': 'test0'},
    {'username': 'test1', 'email': 'test1@test.com', 'password': 'test1'},
]

def test_lister(client, nom_modele, auth=False, index_utilisateur=0):
    url = obtenir_url(nom_modele, 'list')
    if auth:
        connexion_utilisateur_test(client, index_utilisateur)
    response = client.get(url)
    client.logout()
    return response

def test_creation(client, nom_modele, auth=False, index_utilisateur=0):
    url = obtenir_url(nom_modele, 'list')
    if auth:
        connexion_utilisateur_test(client, index_utilisateur)
    response = client.post(url, donnees_post[nom_modele])
    client.logout()
    return response

def test_detail(client, nom_modele, auth=False, index_utilisateur=0):
    response = creer_modele_test(client, nom_modele, index_utilisateur)
    if auth:
        connexion_utilisateur_test(client, index_utilisateur)
    response = client.get(response.data['url'])
    client.logout()
    return response

def test_detail_cross_user(client, nom_modele):

    response = creer_modele_test(client, nom_modele, 0)
    connexion_utilisateur_test(client, 1)
    response = client.get(response.data['url'])
    client.logout()
    return response

def test_modification(client, nom_modele, auth=False, index_utilisateur=0):
    response = creer_modele_test(client, nom_modele, index_utilisateur)
    if auth:
        connexion_utilisateur_test(client, index_utilisateur)
    response = client.put(response.data['url'], donnees_post[nom_modele])
    client.logout()
    return response

def test_modif_cross_user(client, nom_modele):
    response = creer_modele_test(client, nom_modele, 0)
    connexion_utilisateur_test(client, 1)
    response = client.put(response.data['url'], donnees_post[nom_modele])
    client.logout()
    return response

def test_suppression(client, nom_modele, auth=False, index_utilisateur=0):
    response = creer_modele_test(client, nom_modele, index_utilisateur)
    if auth:
        connexion_utilisateur_test(client, index_utilisateur)
    response = client.delete(response.data['url'])
    client.logout()
    return response

def test_suppression_cross_user(client, nom_modele):
    response = creer_modele_test(client, nom_modele, 0)
    connexion_utilisateur_test(client, 1)
    response = client.delete(response.data['url'])
    client.logout()
    return response

def creer_utilisateurs_test():
    for utilisateur in utilisateurs_test:
        User.objects.create_user(username=utilisateur['username'],
                                 email=utilisateur['email'],
                                 password=utilisateur['password'])

def connexion_utilisateur_test(client, index=0):
    utilisateur = User.objects.get(username=utilisateurs_test[index]['username'])
    if utilisateur is None:
        raise Exception('Utilisateur de test introuvable')
    client.force_login(utilisateur)

def creer_modele_test(client, nom_modele, index_utilisateur=0):
    connexion_utilisateur_test(client, index_utilisateur)
    url = obtenir_url(nom_modele, 'list')
    donnees = donnees_post[nom_modele]
    response = client.post(url, donnees)
    if response.status_code != status.HTTP_201_CREATED:
        raise Exception(f"Echec de creation de {nom_modele} : {response.data}")
    client.logout()
    return response

def obtenir_url(nom_modele, suffixe, args=[]):
    return reverse(f'{app_name}:{nom_modele}-{suffixe}', args=args)
