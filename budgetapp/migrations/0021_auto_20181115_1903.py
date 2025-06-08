"""
Modification du champ annee dans le modele Budget.

Objectif :
- Fixer l'annee par defaut a 2025 pour les nouveaux budgets crees.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0020_auto_20181024_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='annee',
            field=models.IntegerField(default=2025),
        ),
    ]
