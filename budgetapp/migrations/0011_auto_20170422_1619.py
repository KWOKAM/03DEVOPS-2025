"""
Ajout d'une contrainte d'unicite sur le modele Categorie.

Objectif :
- S'assurer qu'un utilisateur ne puisse pas creer deux categories avec le meme nom.

Contrainte ajoutee :
- (proprietaire, nom) doit etre unique.
"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0010_alter_unique_together_planbudgetaire'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categorie',
            unique_together={('proprietaire', 'nom')},
        ),
    ]
