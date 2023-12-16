from django.db import models
from django.utils import timezone
from datetime import datetime

NUM_AFFILIATION = "48552668-52"
YEAR = datetime.now().year
MONTH = datetime.now().month
DAY = datetime.now().day

class contrat(models.Model):
    TYPES_CONTRATS = (
        ("CONTRACTUEL", "Contractuel"),
        ("OCCASIONNEL", "Occasionnel"),
        ("SAISONNIER", "Saisonnier"),
        ("STAGIAIRE", "Stagiaire"),
        ("CTT", "CTT"),
        ("CUI", "CUI"),
    )
    Designation = models.CharField(max_length=30, null=False, choices=TYPES_CONTRATS, default=TYPES_CONTRATS[0])

def default_contrat():
    return contrat.objects.create(Designation=contrat.TYPES_CONTRATS[0])

class local(models.Model):
    LOCAUX = (
        ("SIEGE", "Siege"),
        ("LA_MARSA1", "Marsa_Korniche"),
        ("LA_MARSA2", "Marsa_Saada"),
        ("TUNIS_CITY", "Tunis_City"),
        ("AZUR_CITY", "Azur_City"),
        ("SOUSSE", "Mall_Of_Sousse"),
        ("SFAX", "Mall_Of_Sfax"),
        ("TUNISIA_MALL", "Tunisia_Mall"),
    )
    Adresse = models.CharField(max_length=50, null=False, default="2 rue ... Tunis")
    Code_Postal = models.IntegerField(null=False, default=2035)
    Designation = models.CharField(max_length=30, null=False, choices=LOCAUX, default=LOCAUX[0])

def default_local():
    return local.objects.create(
        Adresse="2 rue ... Tunis",
        Code_Postal=2035,
        Designation=local.LOCAUX[0]
    )

class poste(models.Model):
    Designation = models.CharField(max_length=100, null=False, default="Vendeur")
    Description = models.TextField(null=True)
    
    def __str__(self):
        return self.Designation

def default_poste():
    return poste.objects.create(Designation="Vendeur")

class affectation(models.Model):
    Id_Contrat = models.ForeignKey(contrat, null=False, blank=True, on_delete=models.CASCADE)
    Id_Poste = models.ForeignKey(poste, null=False, blank=True, on_delete=models.CASCADE)
    Id_Local = models.ForeignKey(local, null=False, blank=True, on_delete=models.CASCADE)

def default_affectation():
    return affectation.objects.create(
        Id_Contrat=default_contrat(),
        Id_Poste=default_poste(),
        Id_Local=default_local()
        # ... other fields ...
    )

class cnss(models.Model):
    Date_Affectation = models.DateField(null=True)
    Numero = models.CharField(null=False, max_length=30, default="1827390-02")

def default_cnss():
    return cnss.objects.create(Date_Affectation=timezone.now(), Numero="1827390-02")

class situation(models.Model):
    SEXES = (
        ("HOMME", "Homme"),
        ("FEMME", "Femme"),
    )
    Sexe = models.CharField(max_length=5, null=False, default=SEXES[0], choices=SEXES)
    Chef_Famille = models.CharField(null=False, default="off", max_length=4)
    Nb_Enfants = models.SmallIntegerField(null=False, default=0)

def default_situation():
    return situation.objects.create(Sexe=situation.SEXES[0], Chef_Famille="off", Nb_Enfants=0)

class banque(models.Model):
    Designation = models.CharField(max_length=255, null=False, default="banque x")

def default_banque():
    return banque.objects.create(Designation="banque x")

class congés(models.Model):
    Congé_Annuel = models.IntegerField(null=False, default=18)
    Congé_Maladie = models.IntegerField(null=False, default=15)
    Congé_Non_Payé = models.IntegerField(null=False, default=0)
    Congé_Annuel_Ce_Mois = models.IntegerField(null=False, default=0)
    Congé_Maladie_Ce_Mois = models.IntegerField(null=False, default=0)
    Congé_Non_Payé_Ce_Mois = models.IntegerField(null=False, default=0)

def default_conges():
    return congés.objects.create(
        Congé_Annuel=18,
        Congé_Maladie=15,
        Congé_Non_Payé=0,
        Congé_Annuel_Ce_Mois=0,
        Congé_Maladie_Ce_Mois=0,
        Congé_Non_Payé_Ce_Mois=0
    )

class avantages(models.Model):
    Indemnité_Transport = models.FloatField(null=False, default=0)
    Indemnité_Panier = models.FloatField(null=False, default=0)
    Indemnité_Présence = models.FloatField(null=False, default=0)
    Jours_Supp = models.FloatField(null=False, default=0)
    Autres_Ind_Primes = models.FloatField(null=False, default=0)

def default_avantages():
    return avantages.objects.create(
        Indemnité_Transport=0,
        Indemnité_Panier=0,
        Indemnité_Présence=0,
        Jours_Supp=0,
        Autres_Ind_Primes= 0
    )

class fiche_paie(models.Model):
    Nom = models.CharField(max_length=20, null=True)
    Prénom = models.CharField(max_length=20, null=True)
    Num_Affiliation = models.CharField(max_length=30, null=True)
    Qualification = models.CharField(max_length=50, null=True)
    N_CNSS = models.CharField(max_length=15,null=True)
    Date = models.CharField(null=True, max_length=30)
    Matricule = models.CharField(max_length=30, null=True)
    CIN = models.CharField(max_length=15, null=True)
    Adresse = models.CharField(max_length=50, null=True)
    Sit_Admin = models.CharField(null=True, max_length=20)
    Cat = models.IntegerField(null=False, default=0)
    Ech = models.IntegerField(null=False, default=0)
    Enfants = models.IntegerField(null=False, default=0)
    Chef_Famille = models.CharField(null=True, max_length=4)
    Congé_Payé = models.IntegerField(null=False, default=0)
    Congé_Non_Payé = models.IntegerField(null=False, default=0)
    val_congé_payé = models.FloatField(null=False, default=0)
    val_congé_non_payé = models.FloatField(null=False, default=0)
    val_jours_supp = models.FloatField(null=False, default=0)
    Val_Ind_Présence = models.FloatField(null=False, default=0)
    Net = models.CharField(null=True, max_length=4)
    Salaire_Du_Mois = models.FloatField(null=False, default=0)
    Indemnité_Transport = models.FloatField(null=False, default=0)
    Indemnité_Panier = models.FloatField(null=False, default=0)
    Indemnité_Présence = models.FloatField(null=False, default=0)
    Jours_Supp = models.IntegerField(null=False, default=0)
    Autres_Ind_Primes = models.FloatField(null=False, default=0)
    SalaireBrut = models.FloatField(null=False, default=0)
    cnss = models.FloatField(null=False, default=0)
    Imposable = models.FloatField(null=False, default=0)
    css = models.FloatField(null=False, default=0)
    irpp = models.FloatField(null=False, default=0)
    Salaire_Net = models.FloatField(null=False, default=0)
    Net_a_Payer = models.FloatField(null=False, default=0)
    jours_travaillés = models.IntegerField(null=False, default=0)
    Avance = models.FloatField(null=False, default=0)
    Salaire_de_base = models.FloatField(null=False, default=0)
    
class employé(models.Model):
    Creation_Time = models.DateTimeField(editable=False, null=False, default=timezone.now)
    Numero_Compte = models.BigIntegerField(editable=False, null=True)
    Nom = models.CharField(max_length=255, null=False, default="NaN")
    Prenom = models.CharField(max_length=255, null=False, default="NaN")
    Cat = models.IntegerField(null=False, default=0)
    Ech = models.IntegerField(null=False, default=0)
    Matricule = models.CharField(max_length=30, null=False, default="000000")
    CIN = models.CharField(null=False, default="12345678", max_length=15)
    Adresse = models.CharField(max_length=50, null=True)
    Salaire = models.FloatField(null=0, default=1000)
    Avance = models.FloatField(null=False, default=0)  # avance resets to 0 every month
    Lieu_De_Naissance = models.CharField(max_length=50, null=True)
    Date_De_Naissance = models.DateField(null=True)
    Id_Affectation = models.ForeignKey(to=affectation, on_delete=models.CASCADE, null=False)
    Id_CNSS = models.OneToOneField(to=cnss, on_delete=models.CASCADE, null=False)
    Id_Banque = models.ForeignKey(to=banque, on_delete=models.CASCADE, null=True)
    Id_Situation = models.ForeignKey(to=situation, on_delete=models.CASCADE, null=False)
    Id_Congé = models.OneToOneField(to=congés, on_delete=models.CASCADE, null=False)
    Id_Avantage = models.ForeignKey(to=avantages, on_delete=models.CASCADE, null=False)
    Id_Fiche = models.ForeignKey(to=fiche_paie, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return "{0} {1}".format(self.Prenom, self.Nom)

class période(models.Model):
    Année = models.CharField(max_length=4, null=False, default= str(timezone.now().year))
    Mois = models.CharField(max_length=25, null=False, default=str(timezone.now().month))
    Fiche = models.ManyToManyField(to=fiche_paie, editable=True)