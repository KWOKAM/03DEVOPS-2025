"""
Ajout de deux ajustements au modele :
- Modification de l'option verbose_name_plural pour Categorie.
- Ajout d'une contrainte d'unicite sur GroupeCategorieBudget.

Objectifs :
- Ameliorer l'affichage dans l'administration pour le modele Categorie.
- Eviter les doublons de groupes de categories portant le meme nom dans un meme plan budgetaire pour un utilisateur donne.
"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0011_alter_unique_together_categorie'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorie',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterUniqueTogether(
            name='groupecategoriebudget',
            unique_together={('proprietaire', 'nom', 'plan_budgetaire')},
        ),
    ]
