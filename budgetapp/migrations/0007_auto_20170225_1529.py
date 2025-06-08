"""
Renforcement de la lisibilite + du controle sur les champs mois et annee.

Objectifs :
- Etendre la taille maximale du champ mois pour plus de flexibilite.
- Restreindre le champ annee a une liste d'annees comprises entre 2000 et 2030 (inclus).

"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0006_auto_20250606_1532'),  
    ]

    operations = [
        
        migrations.AlterField(
            model_name='planbudgetaire',
            name='mois',
            field=models.CharField(
                max_length=100,
                choices=[
                    ('JAN', 'Janvier'),
                    ('FEB', 'Fevrier'),
                    ('MAR', 'Mars'),
                    ('APR', 'Avril'),
                    ('MAY', 'Mai'),
                    ('JUN', 'Juin'),
                    ('JUL', 'Juillet'),
                    ('AUG', 'Aout'),
                    ('SEP', 'Septembre'),
                    ('OCT', 'Octobre'),
                    ('NOV', 'Novembre'),
                    ('DEC', 'Decembre'),
                ],
                default='JAN',
            ),
        ),

        migrations.AlterField(
            model_name='planbudgetaire',
            name='annee',
            field=models.IntegerField(
                choices=[(y, y) for y in range(2000, 2031)],
                default=2025,
            ),
        ),
    ]
