"""
Harmonisation du champ annee pour le modele PlanBudgetaire.

Objectif :
- Redefinir explicitement les annees autorisees dans les choix de selection de l'utilisateur.
- Garder la coherence avec les annees precedemment definies dans la migration 0007.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0007_auto_custom_fbrain'),  
    ]

    operations = [
        migrations.AlterField(
            model_name='planbudgetaire',
            name='annee',
            field=models.IntegerField(
                choices=[(y, y) for y in range(2000, 2031)],  
                default=2025  
            ),
        ),
    ]
