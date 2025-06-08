"""
Migration visant a simplifier certains modeles et a redefinir les contraintes d'unicite.

Objectifs :
- Redefinir les contraintes d'unicite sur les modeles clefs pour renforcer la coherence des donnees.
- Supprimer les champs `proprietaire` devenus redondants ou inutiles sur plusieurs modeles.

Modifications :
- Contrainte unique (categorie, groupe) sur CategorieBudget.
- Contrainte unique (nom, budget) sur GroupeCategorieBudget.
- Contrainte unique (budget, objectif_long_terme) sur ObjectifBudget.
- Suppression du champ proprietaire sur : Revenu, Transaction, CategorieBudget, GroupeCategorieBudget, ObjectifBudget.
"""

from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0016_auto_20180226_1944'),
    ]

    operations = [
       
        migrations.AlterUniqueTogether(
            name='categoriebudget',
            unique_together=set([('categorie', 'groupe')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupecategoriebudget',
            unique_together=set([('nom', 'budget')]),
        ),
        migrations.AlterUniqueTogether(
            name='objectifbudget',
            unique_together=set([('budget', 'objectif_long_terme')]),
        ),

        migrations.RemoveField(
            model_name='revenu',
            name='proprietaire',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='proprietaire',
        ),
        migrations.RemoveField(
            model_name='categoriebudget',
            name='proprietaire',
        ),
        migrations.RemoveField(
            model_name='groupecategoriebudget',
            name='proprietaire',
        ),
        migrations.RemoveField(
            model_name='objectifbudget',
            name='proprietaire',
        ),
    ]
