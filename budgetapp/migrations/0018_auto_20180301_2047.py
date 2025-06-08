"""
Migration visant a uniformiser la precision des champs monetaires.

Objectifs :
- Harmoniser les champs numeriques lies aux montants (plafond, depense, montant_objectif, progres, montant) avec une precision uniforme : Decimal(10, 2).
- Appliquer des valeurs par defaut logiques la ou necessaire (ex : 0 pour les progres ou depenses).

Modifications :
- Tous les champs de type montant utilisent decimal_places=2 et max_digits=10.
"""

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0017_auto_20180227_2055'),
    ]

    operations = [
        # CategorieBudget
        migrations.AlterField(
            model_name='categoriebudget',
            name='plafond',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='categoriebudget',
            name='depense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),

        # ObjectifBudget
        migrations.AlterField(
            model_name='objectifbudget',
            name='montant_objectif',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='objectifbudget',
            name='progres',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),

        # ObjectifLongTerme
        migrations.AlterField(
            model_name='objectiflongterme',
            name='montant_objectif',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='objectiflongterme',
            name='progres',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),

        # Revenu
        migrations.AlterField(
            model_name='revenu',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),

        # Transaction
        migrations.AlterField(
            model_name='transaction',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
