"""
Vue principale de l'application de gestion budgetaire (BudgetApp).
Ce fichier definit les controleurs responsables :
- de la gestion des utilisateurs (creation, authentification),
- de l'affichage et manipulation des budgets, categories et transactions,
- de l'application des permissions (proprietaire ou administrateur).
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django import forms

from .models import Budget, BudgetCategory, BudgetCategoryGroup, Transaction


def est_admin(user):
    return user.is_staff


### Gestion des utilisateurs ###

@require_http_methods(["POST"])
@csrf_exempt
def connexion_utilisateur(request):
 
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse({'message': 'Connexion reussie'})
    return JsonResponse({'erreur': 'Identifiants invalides'}, status=401)


@login_required
def deconnexion_utilisateur(request):

    logout(request)
    return JsonResponse({'message': 'Deconnexion reussie'})


@require_http_methods(["POST"])
@csrf_exempt
def inscription_utilisateur(request):
   
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if User.objects.filter(username=username).exists():
        return JsonResponse({"erreur': 'Nom d'utilisateur deja pris"}, status=400)

    utilisateur = User.objects.create_user(username=username, password=password, email=email)
    return JsonResponse({'message': 'Utilisateur cree avec succes'})


### Gestion des budgets ###

@login_required
def lister_budgets(request):

    budgets = Budget.objects.filter(owner=request.user)
    data = [{"id": b.id, "mois": b.month, "annee": b.year} for b in budgets]
    return JsonResponse(data, safe=False)


@login_required
def voir_budget(request, budget_id):

    budget = get_object_or_404(Budget, id=budget_id, owner=request.user)
    data = {"id": budget.id, "mois": budget.month, "annee": budget.year}
    return JsonResponse(data)

@login_required
def lister_transactions(request, budget_id):

    budget = get_object_or_404(Budget, id=budget_id, owner=request.user)
    transactions = Transaction.objects.filter(budget_category__group__budget=budget)
    data = [
        {
            "id": t.id,
            "nom": t.name,
            "montant": float(t.amount),
            "categorie": t.budget_category.name
        }
        for t in transactions
    ]
    return JsonResponse(data, safe=False)

class FormulaireCopieBudget(forms.Form):
    source = forms.ModelChoiceField(queryset=Budget.objects.all(), required=False)
    annee_cible = forms.IntegerField()
    mois_cible = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.utilisateur = kwargs.pop('utilisateur')
        super().__init__(*args, **kwargs)

    def clean_source(self):
        source = self.cleaned_data.get('source')
        if source and source.owner != self.utilisateur:
            raise forms.ValidationError("Impossible de copier le budget d'un autre utilisateur.")
        return source


@login_required
@require_http_methods(["POST"])
def copier_budget(request):

    formulaire = FormulaireCopieBudget(data=request.POST, utilisateur=request.user)
    if formulaire.is_valid():
        data = formulaire.cleaned_data
        cible, _ = Budget.objects.get_or_create(
            year=data['annee_cible'],
            month=data['mois_cible'],
            owner=request.user
        )

        source = data['source'] or cible.previous
        if source:
            cible.copy_categories(source)
        else:
            cible.delete_categories()
        return JsonResponse({'message': 'Budget copie avec succes'})

    return JsonResponse({'erreurs': formulaire.errors}, status=400)
