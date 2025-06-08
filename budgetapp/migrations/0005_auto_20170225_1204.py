
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0004_postededepense_proprietaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupepostebudget',
            name='proprietaire',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='groupes_poste_budget', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='objectifbudget',
            name='plan_budgetaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectifs_budget', to='budgetapp.PlanBudgetaire'),
        ),
        migrations.AlterField(
            model_name='objectifbudget',
            name='objectif_long_terme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='objectifs_budget', to='budgetapp.ObjectifLongTerme'),
        ),
        migrations.AlterField(
            model_name='postebudget',
            name='poste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postes_budgets', to='budgetapp.PosteDeDepense'),
        ),
        migrations.AlterField(
            model_name='postebudget',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postes_budgets', to='budgetapp.GroupePosteBudget'),
        ),
        migrations.AlterField(
            model_name='groupepostebudget',
            name='plan_budgetaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupes_poste_budget', to='budgetapp.PlanBudgetaire'),
        ),
        migrations.AlterField(
            model_name='revenu',
            name='plan_budgetaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revenus', to='budgetapp.PlanBudgetaire'),
        ),
        migrations.AlterField(
            model_name='objectiflongterme',
            name='proprietaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objectifs_long_terme', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mouvement',
            name='poste_budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mouvements', to='budgetapp.PosteBudget'),
        ),
    ]
