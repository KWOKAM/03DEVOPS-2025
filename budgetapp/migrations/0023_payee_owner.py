"""
Ajout du champ proprietaire au modele Beneficiaire :
- Chaque beneficiaire est maintenant lie a un utilisateur (proprietaire)
"""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0022_auto_20190108_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiaire',
            name='proprietaire',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),
    ]
