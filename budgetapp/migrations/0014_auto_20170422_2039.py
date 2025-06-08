"""
Ajout d'une contrainte d'unicite sur le modele ObjectifBudget.

Objectif :
- Empecher la redondance d'un meme objectif long terme associe plusieurs fois au meme budget pour un utilisateur donne.
"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0013_contrainte_unique_categoriebudget'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='objectifbudget',
            unique_together={('proprietaire', 'budget', 'objectif_long_terme')},
        ),
    ]
