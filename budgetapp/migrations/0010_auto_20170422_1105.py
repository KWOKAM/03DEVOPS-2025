"""
Ajout d'une contrainte d'unicite sur le modele PlanBudgetaire.

Objectif :
- Garantir qu'un utilisateur ne puisse pas avoir deux plans budgetaires pour le meme mois et la meme annee.

Contrainte ajoutee :
- (proprietaire, mois,annee) doit etre unique.

"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0009_auto_custom_fbrain'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='planbudgetaire',
            unique_together={('proprietaire', 'mois', 'annee')},
        ),
    ]
