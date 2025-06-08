"""
Restructuration des objectifs et transactions :
- Suppression des anciens modeles ObjectifBudgetaire, ObjectifLongTerme et Revenu
- Introduction du modele Beneficiaire
- Ajout d'un champ entree aux transactions
- Mise a jour des relations pour les transactions
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetapp', '0021_auto_20181115_1903'),
    ]

    operations = [

        migrations.CreateModel(
            name='Beneficiaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),

        migrations.AlterUniqueTogether(
            name='objectifbudgetaire',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='objectifbudgetaire',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='objectifbudgetaire',
            name='objectif_long_terme',
        ),

        migrations.RemoveField(
            model_name='objectiflongterme',
            name='proprietaire',
        ),

        migrations.RemoveField(
            model_name='revenu',
            name='budget',
        ),

        migrations.AddField(
            model_name='transaction',
            name='entree',
            field=models.BooleanField(default=False),
        ),

        migrations.AlterField(
            model_name='transaction',
            name='allocation_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.CategorieBudget'),
        ),

        migrations.AlterField(
            model_name='transaction',
            name='destinataire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgetapp.Beneficiaire'),
        ),

        migrations.AlterField(
            model_name='budget',
            name='annee',
            field=models.IntegerField(default=2025),
        ),

        migrations.DeleteModel(name='ObjectifBudgetaire'),
        migrations.DeleteModel(name='Revenu'),
        migrations.DeleteModel(name='ObjectifLongTerme'),
    ]
