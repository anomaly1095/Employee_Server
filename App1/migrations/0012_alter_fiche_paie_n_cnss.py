# Generated by Django 4.2.4 on 2023-12-16 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0011_alter_période_fiche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiche_paie',
            name='N_CNSS',
            field=models.CharField(max_length=15, null=True),
        ),
    ]