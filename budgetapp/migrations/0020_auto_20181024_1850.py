"""
Suppression de la contrainte d'unicite sur le modele Categoriebudget.

Objectif :
- Retirer la contrainte unique_together sur les champs de Categoriebudget,
  afin d'autoriser des doublons pour une plus grande flexibilite de gestion.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0019_auto_20181022_2226'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='categoriebudget',
            unique_together=set(),
        ),
    ]
