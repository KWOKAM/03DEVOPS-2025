"""
Renommage du champ 'beneficiaire' en 'destinataire' dans le modele Transaction :
- Le champ devient plus explicite pour designer la personne recevant la transaction.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0024_payee_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='beneficiaire',
            new_name='destinataire',
        ),
    ]
