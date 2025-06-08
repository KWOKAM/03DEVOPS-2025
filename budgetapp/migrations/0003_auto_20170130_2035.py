"""
Migration de structure pour l'application BudgetApp (Etape 2).

Cette migration :
- Ajoute la notion de groupe de postes de depense.
- Supprime d'anciens champs devenus obsoletes.
- Relie les suivis mensuels et les objectifs long terme a un proprietaire (utilisateur).
"""

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupeDePoste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),

        migrations.RemoveField(
            model_name='postededepense',
            name='group',  
        ),

        migrations.RemoveField(
            model_name='suivimensuel',
            name='budget',  
        ),

        migrations.AddField(
            model_name='suivimensuel',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='suivis',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.AddField(
            model_name='objectiflongterme',
            name='proprietaire',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='objectifs',
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=False,
        ),

        migrations.DeleteModel(
            name='CategoryGroup',  
        ),

        migrations.AddField(
            model_name='groupedeposte',
            name='suivi',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='budgetapp.SuiviMensuel'
            ),
        ),

        migrations.AddField(
            model_name='postededepense',
            name='groupe',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to='budgetapp.GroupeDePoste'
            ),
            preserve_default=False,
        ),
    ]
