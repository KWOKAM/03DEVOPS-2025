"""
Ajout d'une contrainte d'unicite sur le modele CategorieBudget.

Objectif :
- Eviter la duplication d'une meme categorie dans un meme groupe pour un utilisateur specifique.
"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0012_options_et_contrainte_groupecategoriebudget'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoriebudget',
            unique_together={('proprietaire', 'categorie', 'groupe')},
        ),
    ]
