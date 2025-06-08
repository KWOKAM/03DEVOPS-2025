"""
Renommage des modeles et champs pour clarifier leur signification.

Objectifs :
- Renommer CategoryBudgetGroup en ThemeDepense pour plus de clarte semantique.
- Renommer CategoryBudget en AffectationDepense.
- Renommer le champ category_budget de la classe Transaction en detail_affectation.
"""

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budgetapp', '0014_auto_20170422_2039'),
    ]

    operations = [
        migrations.RenameModel('CategoryBudgetGroup', 'ThemeDepense'),
        migrations.RenameModel('CategoryBudget', 'AffectationDepense'),
        migrations.RenameField('Transaction', 'category_budget', 'detail_affectation'),
    ]
