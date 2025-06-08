"""
Migration visant a supprimer le modele obsolete Categorie, 
et a ajuster les relations dans les modeles relies aux categories budgetaires.

Objectifs :
- Supprimer le modele Categorie devenu inutile.
- Supprimer la contrainte d'unicite liee a Categorie.
- Modifier les relations pour harmoniser les noms et les liens.
- Mettre a jour l'annee par defaut dans Budget (2025).
"""

from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0015_auto_20170701_1852'),
    ]

    operations = [
    
        migrations.AlterUniqueTogether(
            name='categorie',
            unique_together=set([]),
        ),

        migrations.RemoveField(
            model_name='categorie',
            name='proprietaire',
        ),

        migrations.AlterField(
            model_name='budget',
            name='annee',
            field=models.IntegerField(
                choices=[(i, i) for i in range(2000, 2031)],
                default=2025
            ),
        ),

        migrations.AlterField(
            model_name='categoriebudget',
            name='categorie',
            field=models.CharField(max_length=100),
        ),

        migrations.AlterField(
            model_name='categoriebudget',
            name='groupe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='categories_budgetaires',
                to='budgetapp.GroupeCategorieBudget'
            ),
        ),
        migrations.AlterField(
            model_name='categoriebudget',
            name='proprietaire',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='categories_budgetaires',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.AlterField(
            model_name='groupecategoriebudget',
            name='budget',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='groupes_categories_budgetaires',
                to='budgetapp.Budget'
            ),
        ),
        migrations.AlterField(
            model_name='groupecategoriebudget',
            name='proprietaire',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='groupes_categories_budgetaires',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.DeleteModel(
            name='Categorie',
        ),
    ]
