"""
Ce fichier contient les classes de serialisation pour :
- les budgets et leurs categories
- les transactions et beneficiaires
- l'inscription d'utilisateurs
"""


from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import (Budget, BudgetCategorie, GroupeCategorieBudget, Beneficiaire, Transaction)

champ_proprietaire = serializers.PrimaryKeyRelatedField(
    read_only=True, default=serializers.CurrentUserDefault())
champ_budget = serializers.HyperlinkedRelatedField(
    queryset=Budget.objects.all(),
    view_name='budgetapp:budget-detail'
)
champ_categorie_budget = serializers.HyperlinkedRelatedField(
    queryset=BudgetCategorie.objects.all(),
    view_name='budgetapp:budgetcategorie-detail'
)
champ_categories_budget = serializers.HyperlinkedRelatedField(
    view_name='budgetapp:budgetcategorie-detail',
    many=True,
    read_only=True
)


class ListeEnDictionnaire(serializers.ListSerializer):

    dict_key = 'pk'

    @property
    def data(self):
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        items = super().to_representation(data)
        return {item[self.dict_key]: item for item in items}


class CategorieBudgetSerialiseur(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='budgetapp:budgetcategorie-detail')
    groupe = serializers.CharField(source='group.name')
    mois_budget = serializers.CharField(write_only=True)
    annee_budget = serializers.IntegerField(write_only=True)
    depense = serializers.CharField(read_only=True)

    def validate(self, data):
        super().validate(data)
        mois = data.get('mois_budget')
        annee = data.get('annee_budget')
        categorie = data.get('category')

        if self.instance:
            mois = mois or self.instance.group.budget.month
            annee = annee or self.instance.group.budget.year
            categorie = categorie or self.instance.category

        existant = BudgetCategorie.objects.filter(
            group__budget__month=mois,
            group__budget__year=annee,
            group__budget__owner=self.context['request'].user,
            category=categorie,
        )
        if self.instance:
            existant = existant.exclude(id=self.instance.id)

        if existant.exists():
            raise serializers.ValidationError(
            )
        return data

    def create(self, validated_data):
        self.creer_ou_utiliser_groupes(validated_data)
        return BudgetCategorie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.creer_ou_utiliser_groupes(validated_data)
        return super().update(instance, validated_data)

    def creer_ou_utiliser_groupes(self, validated_data):
        mois = validated_data.get('mois_budget')
        annee = validated_data.get('annee_budget')
        categorie = validated_data.get('category')
        nom_groupe = validated_data.get('group', {}).get('name')

        if self.instance:
            mois = mois or self.instance.group.budget.month
            annee = annee or self.instance.group.budget.year
            categorie = categorie or self.instance.category
            nom_groupe = nom_groupe or self.instance.group.name

        budget, _ = Budget.objects.get_or_create(
            month=mois,
            year=annee,
            owner=self.context['request'].user,
        )

        groupe, _ = GroupeCategorieBudget.objects.get_or_create(
            budget=budget,
            name=nom_groupe,
        )

        validated_data.pop('mois_budget', None)
        validated_data.pop('annee_budget', None)
        validated_data.pop('group', None)

        validated_data['group'] = groupe

    class Meta:
        model = BudgetCategorie
        fields = ('url', 'pk', 'mois_budget', 'annee_budget', 'category', 'groupe', 'limit', 'depense')
        list_serializer_class = ListeEnDictionnaire


class TransactionSerialiseur(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='budgetapp:transaction-detail')
    categorie_budget = serializers.PrimaryKeyRelatedField(queryset=BudgetCategorie.objects.all())
    beneficiaire = serializers.CharField()

    def create(self, validated_data):
        self.creer_ou_utiliser_beneficiaire(validated_data)
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.creer_ou_utiliser_beneficiaire(validated_data)
        return super().update(instance, validated_data)

    def creer_ou_utiliser_beneficiaire(self, validated_data):
        beneficiaire = validated_data.get('beneficiaire')
        if not self.instance or beneficiaire is not None:
            beneficiaire, _ = Beneficiaire.objects.get_or_create(
                name=beneficiaire,
                owner=self.context['request'].user,
            )
            validated_data['payee'] = beneficiaire

    class Meta:
        model = Transaction
        fields = ('url', 'pk', 'amount', 'categorie_budget', 'date', 'beneficiaire')
        list_serializer_class = ListeEnDictionnaire


class BeneficiaireSerialiseur(serializers.ModelSerializer):
    class Meta:
        model = Beneficiaire
        fields = ('pk', 'name')
        list_serializer_class = ListeEnDictionnaire


class GroupeCategorieBudgetListeSerialiseur(ListeEnDictionnaire):
    dict_key = 'name'


class GroupeCategorieBudgetSerialiseur(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='budgetapp:budgetcategorygroup-detail')
    budget = champ_budget
    categories_budget = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = GroupeCategorieBudget
        fields = ('url', 'pk', 'name', 'budget', 'categories_budget')
        list_serializer_class = GroupeCategorieBudgetListeSerialiseur


class BudgetSerialiseur(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='budgetapp:budget-detail')
    proprietaire = champ_proprietaire
    groupes_categories = GroupeCategorieBudgetSerialiseur(many=True, read_only=True)
    categories_budget = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    beneficiaires = serializers.SerializerMethodField()

    def get_categories_budget(self, budget):
        objets = BudgetCategorie.objects.filter(group__budget__pk=budget.pk)
        serializer = CategorieBudgetSerialiseur(objets, many=True, context=self.context)
        return serializer.data

    def get_transactions(self, budget):
        objets = Transaction.objects.filter(categorie_budget__group__budget__pk=budget.pk)
        serializer = TransactionSerialiseur(objets, many=True, context=self.context)
        return serializer.data

    def get_beneficiaires(self, budget):
        objets = Beneficiaire.objects.filter(owner=self.context['request'].user)
        serializer = BeneficiaireSerialiseur(objets, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Budget
        fields = (
            'url', 'pk', 'proprietaire', 'month', 'year',
            'groupes_categories', 'categories_budget', 'transactions', 'beneficiaires'
        )


class UtilisateurSerialiseur(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        utilisateur = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        utilisateur.set_password(validated_data['password'])
        utilisateur.save()
        return utilisateur
