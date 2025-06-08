
"""
Nous definissons les routes URL pour l'application BudgetApp.

Ce fichier configure les points d'entree de l'API REST a l'aide d'un routeur DRF (DefaultRouter),
et associe les vues bases sur les classes aux differentes operations :
- Gestion des budgets, categories et transactions
- Authentification et gestion des utilisateurs
- Copie de budget, consultation des informations utilisateur, etc.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'budgetapp'

routeur = DefaultRouter()
routeur.register(r'budgets', views.BudgetViewSet)
routeur.register(r'categories-budget', views.CategorieBudgetViewSet)
routeur.register(r'groupes-categories-budget', views.GroupeCategorieBudgetViewSet)
routeur.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('utilisateurs/', views.ListeUtilisateursView.as_view(), name='liste-utilisateurs'),
    path('utilisateurs/inscription/',
         views.CreationUtilisateurView.as_view(),
         name='creation-utilisateur'),
    path('utilisateurs/connexion/',
         views.ObtenirJetonAuthCookieView.as_view(),
         name='connexion-utilisateur'),
    path('utilisateurs/<int:pk>/',
         views.DetailUtilisateurView.as_view(),
         name='detail-utilisateur'),
    path('infos-utilisateur/', views.InfosUtilisateurView.as_view(), name='infos-utilisateur'),
    path('copier-budget/', views.CopieBudgetView.as_view(), name='copier-budget'),
    path('', include(routeur.urls)),
]
