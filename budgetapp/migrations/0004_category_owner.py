"""
Migration numero 4 qui est l'ajout du proprietaire a chaque poste de depense.

Cette migration ajoute un champ de liaison vers l'utilisateur (`proprietaire`)
pour chaque instance de `PosteDeDepense`. Cela permet de filtrer les donnees
par utilisateur et de gerer les permissions sans framework DRF.
"""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0003_auto_20170130_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='postededepense',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='postes_depense',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
    ]
