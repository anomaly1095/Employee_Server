# Generated by Django 4.2.7 on 2023-12-14 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0004_fiche_paie_val_congé_non_payé_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiche_paie',
            name='Val_Ind_Présence',
            field=models.FloatField(default=0),
        ),
    ]
