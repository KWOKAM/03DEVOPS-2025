"""
Migration initiale du modele de donnees de l'application BudgetApp.

Cette migration cree les tables suivantes :
- PosteDeDepense : represente une categorie de depenses.
- RevenuMensuel : represente un revenu recu durant un mois.
- SuiviMensuel : represente une periode mensuelle avec un objectif financier.
- Operation : represente une depense liee a un poste et une periode donnee.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PosteDeDepense',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RevenuMensuel',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_reception', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SuiviMensuel',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('mois', models.CharField(max_length=20)),
                ('annee', models.IntegerField()),
                ('objectif_financier', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10)),
                ('libelle', models.CharField(max_length=100)),
                ('date_operation', models.DateField()),
                ('poste', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='budgetapp.PosteDeDepense')),
                ('suivi', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='budgetapp.SuiviMensuel')),
            ],
        ),
    ]
