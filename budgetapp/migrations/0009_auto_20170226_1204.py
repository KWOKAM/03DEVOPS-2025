"""
Ajout du champ proprietaire sur plusieurs modeles,
et redefinition du champ annee dans le modele PlanBudgetaire.

Objectifs :
- Permettre l'attribution explicite des objets ObjectifBudget, CategorieBudget, Revenu et Transaction a un utilisateur proprietaire.
- Clarifier le champ annee de PlanBudgetaire avec une liste limitee de valeurs (2000 a 2030).
"""

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0008_auto_custom_fbrain'),  
    ]

    operations = [

        migrations.AddField(
            model_name='objectifbudget',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='objectifs_budget',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='categoriebudget',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='categories_budget',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='revenu',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='revenus',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='transaction',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='transactions',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.AlterField(
            model_name='planbudgetaire',
            name='annee',
            field=models.IntegerField(
                choices=[(y, y) for y in range(2000, 2031)],
                default=2025
            ),
        ),
    ]
