"""
Suppression du champ 'depense' du modele CategorieBudget :
- Le champ est retire car redondant ou calcule dynamiquement dans les vues ou les gabarits.
"""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0025_rename_recipient_payee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoriebudget',
            name='depense',
        ),
    ]
