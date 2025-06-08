"""
champ annee + clarification des mois du plan budgetaire.

Objectifs :
- Ajouter le champ annee par defaut a 2025 dans le modele PlanBudgetaire.
- Definir explicitement les noms de mois en francais pour une meilleure lisibilite dans l'interface Django.

"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0005_auto_20250606_1534'),  
    ]

    operations = [

        migrations.AddField(
            model_name='planbudgetaire',
            name='annee',
            field=models.IntegerField(default=2025),
        ),

        migrations.AlterField(
            model_name='planbudgetaire',
            name='mois',
            field=models.CharField(
                max_length=3,
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
    ]
