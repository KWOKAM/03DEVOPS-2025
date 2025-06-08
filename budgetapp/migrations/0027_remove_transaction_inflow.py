"""
Suppression du champ 'entree_fonds' du modele Transaction :
- Ce champ est supprime car il est redondant ou remplace par un champ plus pertinent.
"""

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0026_remove_budgetcategory_spent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='entree_fonds',
        ),
    ]
