# Generated by Django 4.2.7 on 2023-12-14 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0006_alter_congés_congé_annuel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiche_paie',
            name='Salaire_de_base',
            field=models.FloatField(default=0),
        ),
    ]
