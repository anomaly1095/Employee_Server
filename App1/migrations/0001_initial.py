# Generated by Django 4.2.7 on 2023-12-14 12:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='affectation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='avantages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Indemnité_Transport', models.FloatField(default=0)),
                ('Indemnité_Panier', models.FloatField(default=0)),
                ('Indemnité_Présence', models.FloatField(default=0)),
                ('Jours_Supp', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='banque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(default='banque x', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='cnss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Affectation', models.DateField(null=True)),
                ('Numero', models.CharField(default='1827390-02', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='congés',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Congé_Annuel', models.FloatField(default=18)),
                ('Congé_Maladie', models.FloatField(default=15)),
                ('Congé_Non_Payé', models.FloatField(default=0)),
                ('Congé_Annuel_Ce_Mois', models.FloatField(default=0)),
                ('Congé_Maladie_Ce_Mois', models.FloatField(default=0)),
                ('Congé_Non_Payé_Ce_Mois', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='contrat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(choices=[('CONTRACTUEL', 'Contractuel'), ('OCCASIONNEL', 'Occasionnel'), ('SAISONNIER', 'Saisonnier'), ('STAGIAIRE', 'Stagiaire'), ('CTT', 'CTT'), ('CUI', 'CUI')], default=('CONTRACTUEL', 'Contractuel'), max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='fiche_paie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=20, null=True)),
                ('Prénom', models.CharField(max_length=20, null=True)),
                ('Num_Affiliation', models.CharField(max_length=30, null=True)),
                ('Qualification', models.CharField(max_length=50, null=True)),
                ('N_CNSS', models.TextField(null=True)),
                ('Date', models.CharField(max_length=30, null=True)),
                ('Matricule', models.CharField(max_length=30, null=True)),
                ('CIN', models.CharField(max_length=15, null=True)),
                ('Adresse', models.CharField(max_length=50, null=True)),
                ('Sit_Admin', models.CharField(max_length=20, null=True)),
                ('Cat', models.IntegerField(default=0)),
                ('Ech', models.IntegerField(default=0)),
                ('Enfants', models.IntegerField(default=0)),
                ('Chef_Famille', models.CharField(max_length=4, null=True)),
                ('Congé_Payé', models.IntegerField(default=0)),
                ('Congé_Non_Payé', models.IntegerField(default=0)),
                ('Net', models.CharField(max_length=4, null=True)),
                ('Salaire_Du_Mois', models.FloatField(default=0)),
                ('Indemnité_Transport', models.FloatField(default=0)),
                ('Indemnité_Panier', models.FloatField(default=0)),
                ('Indemnité_Présence', models.FloatField(default=0)),
                ('Jours_Supp', models.IntegerField(default=0)),
                ('Autres_Ind_Primes', models.FloatField(default=0)),
                ('SalaireBrut', models.FloatField(default=0)),
                ('cnss', models.FloatField(default=0)),
                ('Imposable', models.FloatField(default=0)),
                ('css', models.FloatField(default=0)),
                ('irpp', models.FloatField(default=0)),
                ('Salaire_Net', models.FloatField(default=0)),
                ('Net_a_Payer', models.FloatField(default=0)),
                ('Avance', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Adresse', models.CharField(default='2 rue ... Tunis', max_length=50)),
                ('Code_Postal', models.IntegerField(default=2035)),
                ('Designation', models.CharField(choices=[('SIEGE', 'Siege'), ('LA_MARSA1', 'Marsa_Korniche'), ('LA_MARSA2', 'Marsa_Saada'), ('TUNIS_CITY', 'Tunis_City'), ('AZUR_CITY', 'Azur_City'), ('SOUSSE', 'Mall_Of_Sousse'), ('SFAX', 'Mall_Of_Sfax'), ('TUNISIA_MALL', 'Tunisia_Mall')], default=('SIEGE', 'Siege'), max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(default='Vendeur', max_length=100)),
                ('Description', models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='situation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sexe', models.CharField(choices=[('HOMME', 'Homme'), ('FEMME', 'Femme')], default=('HOMME', 'Homme'), max_length=5)),
                ('Chef_Famille', models.CharField(default='off', max_length=4)),
                ('Nb_Enfants', models.SmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='employé',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Creation_Time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('Numero_Compte', models.BigIntegerField(editable=False, null=True)),
                ('Nom', models.CharField(default='NaN', max_length=255)),
                ('Prenom', models.CharField(default='NaN', max_length=255)),
                ('Cat', models.IntegerField(default=0)),
                ('Ech', models.IntegerField(default=0)),
                ('Matricule', models.CharField(default='000000', max_length=30)),
                ('CIN', models.CharField(default='12345678', max_length=15)),
                ('Adresse', models.CharField(max_length=50, null=True)),
                ('Salaire', models.FloatField(default=1000, null=0)),
                ('Avance', models.FloatField(default=0)),
                ('Lieu_De_Naissance', models.CharField(max_length=50, null=True)),
                ('Date_De_Naissance', models.DateField(null=True)),
                ('Id_Affectation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.affectation')),
                ('Id_Avantage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.avantages')),
                ('Id_Banque', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.banque')),
                ('Id_CNSS', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App1.cnss')),
                ('Id_Congé', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App1.congés')),
                ('Id_Fiche', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App1.fiche_paie')),
                ('Id_Situation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App1.situation')),
            ],
        ),
        migrations.AddField(
            model_name='affectation',
            name='Id_Contrat',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='App1.contrat'),
        ),
        migrations.AddField(
            model_name='affectation',
            name='Id_Local',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='App1.local'),
        ),
        migrations.AddField(
            model_name='affectation',
            name='Id_Poste',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='App1.poste'),
        ),
    ]
