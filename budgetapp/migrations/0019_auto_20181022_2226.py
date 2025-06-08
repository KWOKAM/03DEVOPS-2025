"""
Migration visant a augmenter la precision des champs monetaires.

Objectifs :
- Passer tous les champs de montant de max_digits=10 a max_digits=20 pour permettre la saisie de valeurs plus grandes.
- Conserver decimal_places=2 pour les centimes.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0018_auto_20180301_2047'),
    ]

    operations = [

        migrations.AlterField(
            model_name='categoriebudget',
            name='plafond',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='categoriebudget',
            name='depense',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),

        migrations.AlterField(
            model_name='objectifbudget',
            name='montant_objectif',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='objectifbudget',
            name='progres',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),

        migrations.AlterField(
            model_name='revenu',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),

        migrations.AlterField(
            model_name='objectiflongterme',
            name='montant_objectif',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='objectiflongterme',
            name='progres',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),

        migrations.AlterField(
            model_name='transaction',
            name='montant',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
