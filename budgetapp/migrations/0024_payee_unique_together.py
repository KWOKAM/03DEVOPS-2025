"""
Ajout d'une contrainte d'unicite sur le modele Beneficiaire :
- Un meme utilisateur ne peut pas enregistrer deux beneficiaires avec le meme nom
"""

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0023_payee_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='beneficiaire',
            unique_together={('nom', 'proprietaire')},
        ),
    ]
