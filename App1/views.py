from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import *
from django.core.serializers import serialize
from .models import *
from django.template.loader import get_template 
from xhtml2pdf import pisa
import zipfile
from io import BytesIO

login_test = False

def Index(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    try:
        Emp_List = employé.objects.all()
    except:
        Emp_List = None

    return render(request=request, template_name="Index.html", context={'Emp_List':Emp_List, "month": MONTH, "year": YEAR})

def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_exists = CustomUser.objects.filter(username=username, password=password).exists()

        if user_exists:
            request.session['login_test'] = True
            return redirect('Index')  # Redirect to your index view
        else:
            error_message = "Username ou Mot de passe invalides"
            request.session['login_test'] = False
            return render(request, 'Login.html', {'error_message': error_message})

    return render(request, 'Login.html')

def Comptes(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    try:
        Emp_List = employé.objects.all()
    except:
        Emp_List = None
    return render(request=request, template_name="Comptes.html", context={'Emp_List':Emp_List, "month": MONTH, "year": YEAR})

def Congés(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    if request.method == 'POST':
        # Accessing the submitted values
        employee_id = request.POST['employee_id']   
        maladie_annee = request.POST['maladie_annee']
        annuel_annee = request.POST['annuel_annee']
        non_paye_annee = request.POST['non_paye_annee']
        maladie_mois = request.POST['maladie_mois']
        annuel_mois = request.POST['annuel_mois']
        non_paye_mois = request.POST['non_paye_mois']

        emp_to_change = employé.objects.get(id=int(employee_id))
        emp_to_change.Id_Congé.Congé_Maladie = int(maladie_annee)
        emp_to_change.Id_Congé.Congé_Annuel = int(annuel_annee)
        emp_to_change.Id_Congé.Congé_Non_Payé = int(non_paye_annee)
        emp_to_change.Id_Congé.Congé_Maladie_Ce_Mois = int(maladie_mois)
        emp_to_change.Id_Congé.Congé_Annuel_Ce_Mois = int(annuel_mois)
        emp_to_change.Id_Congé.Congé_Non_Payé_Ce_Mois = int(non_paye_mois)
        emp_to_change.Id_Congé.save()

        # Re-query the database to get the latest employee data
        Emp_List = employé.objects.all()
    else:
        try:
            Emp_List = employé.objects.all()
        except:
            Emp_List = None
    return render(
        request=request,
        template_name="Congés.html",
        context={'Emp_List': Emp_List, "month": MONTH, "year": YEAR}
    )
    
def Congés_Add(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    if request.method == "POST":
        Id = request.POST.get('Id_Emp')
        try:
            emp = employé.objects.get(id=int(Id))
            # Perform any additional actions or validations here

            return render(request=request,
                  template_name="Congés_Add.html",
                  context={'Emp': emp, "month": MONTH, "year": YEAR})
        except ObjectDoesNotExist:
            emp = None
        # Render the template with the employee details
        return render(request=request,
                    template_name="Congés_Add.html",
                    context={'Emp': emp, "month": MONTH, "year": YEAR})
    else:
        return redirect(Congés)
    
def Congés_Détails(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    if request.method == "POST":
        Id = request.POST.get('Id_Emp')
        try:
            emp = employé.objects.get(id=int(Id))#modifier le graph dans la template pour afficher les absences de toute l'année au lieu de the current leaves
            # Perform any additional actions or validations here
            return render(request=request,
                  template_name="Congés_Détails.html",
                  context={'Emp': emp, "month": MONTH, "year": YEAR})
        except ObjectDoesNotExist:
            # Handle the case where the employee does not exist
            emp = None

def search_view(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    if request.method == "POST":
        search_name = request.POST.get("Search_Name")
        results = employé.objects.filter(Nom__icontains=search_name) | employé.objects.filter(Prenom__icontains=search_name) | employé.objects.filter(id__icontains=search_name)
        return render(request=request,
                      template_name="Search.html",
                      context={"month": MONTH, "year": YEAR, "results": results})
    else:
        return redirect(to=Index)
   #________________________________________________

def Find_omega(Chef_Famille: str, Enfants: int) -> int: #calculer la somme que nous allons enlever lors du calcul de l'IRPP (Varie avec le nombre d'enfants et chef de famille)
    x = 0
    if Chef_Famille == 'on':
        x += 300
        for i in range(Enfants):
            x += 100
    return x

def Find_X(Imposable_Annuel: float, Chef_Famille: str, Enfants: int) -> float: #calculer la somme que nous allons enlever lors du calcul de l'IRPP (10% avec plafond de 2000dt)
    if Imposable_Annuel <= 5000: 
        return Imposable_Annuel
    elif 5000 < Imposable_Annuel <= 20000:
        x = Imposable_Annuel*0.9
        x -= Find_omega(Chef_Famille, Enfants)
    else:
        x = Imposable_Annuel-2000
        x -= Find_omega(Chef_Famille, Enfants)
    return x

def Brut_Find_From_Net(Fiche: fiche_paie):
    omega = Find_omega(Fiche.Chef_Famille, Fiche.Enfants)
    Fiche.Salaire_Net = Fiche.Avance+Fiche.Net_a_Payer
    if Fiche.Salaire_Net*12 <= 5000:
        Fiche.irpp = 0
        Fiche.css = 0
        Fiche.Imposable = Fiche.Salaire_Net
        Fiche.SalaireBrut = Fiche.Imposable/0.9082
        Fiche.cnss = Fiche.SalaireBrut - Fiche.Imposable
        
    elif 5000 < (12*Fiche.Salaire_Net-(0.2385*omega+1170))/0.7615 <= 20000:
        ((12*Fiche.Salaire_Net-(0.2385*omega+1170))/0.7615)
        if 5000 < ((12*Fiche.Salaire_Net-(0.2385*omega+1170))/0.7615)*0.9-omega <= 20000:
            
            Fiche.SalaireBrut = (10.8*Fiche.Salaire_Net-1170-0.2385*omega)/7.4692184
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.2385*omega+1170))/0.7615)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = ((Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-5000)*0.26)/12
            Fiche.css = (25+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-5000)*0.005)/12
        else:#Changement de tranche/categorie aprés la soustraction de omega et 10%
            Fiche.irpp = 0
            Fiche.css = 0
            Fiche.Imposable = Fiche.Salaire_Net
            Fiche.SalaireBrut = Fiche.Imposable/0.9082
            Fiche.cnss = Fiche.SalaireBrut - Fiche.Imposable
            
    elif 20000 < (12*Fiche.Salaire_Net-(0.285*omega+2270))/0.715 <= 30000:
        if 20000 < ((12*Fiche.Salaire_Net-(0.285*omega+2270))/0.715)-2000-omega <= 30000:
            
            Fiche.SalaireBrut = (12*Fiche.Salaire_Net-2270-0.285*omega)/7.792356
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.285*omega+2270))/0.715)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = (15000*0.26+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-20000)*0.28)/12
            Fiche.css = (25+75+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-20000)*0.005)/12
        else:#Changement de tranche/categorie aprés la soustraction de omega et 2000
            Fiche.SalaireBrut = (10.8*Fiche.Salaire_Net-1170-0.2385*omega)/7.4692184
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.2385*omega+1170))/0.7615)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = ((Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-5000)*0.26)/12
            Fiche.css = (25+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-5000)*0.005)/12
            
    elif 30000 < ((12*Fiche.Salaire_Net-(0.325*omega+3550))/0.675) <= 50000:
        if 30000 < ((12*Fiche.Salaire_Net-(0.325*omega+3550))/0.675)-2000-omega <= 50000:
            
            Fiche.SalaireBrut = (12*Fiche.Salaire_Net-3550-0.325*omega)/7.35642
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.325*omega+3550))/0.675)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = (15000*0.26+10000*0.28+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-30000)*0.32)/12
            Fiche.css = (25+75+50+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-30000)*0.005)/12
        else:#Changement de tranche/categorie aprés la soustraction de omega et 2000
            Fiche.SalaireBrut = (12*Fiche.Salaire_Net-2270-0.285*omega)/7.792356
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.285*omega+2270))/0.715)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = (15000*0.26+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-20000)*0.28)/12
            Fiche.css = (25+75+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-20000)*0.005)/12
            
    elif 50000 < ((12*Fiche.Salaire_Net-(0.355*omega+5110))/0.645):
        if 50000 < ((12*Fiche.Salaire_Net-(0.355*omega+5110))/0.645)-2000-omega:
            
            Fiche.SalaireBrut = (12*Fiche.Salaire_Net-5110-0.355*omega)/7.029458
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.355*omega+5110))/0.645)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = (15000*0.26+10000*0.28+20000*0.32+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-50000)*0.35)/12
            Fiche.css = (25+75+50+100+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-50000)*0.005)/12
        else:#Changement de tranche/categorie aprés la soustraction de omega et 2000
            Fiche.SalaireBrut = (12*Fiche.Salaire_Net-3550-0.325*omega)/7.35642
            Fiche.Imposable = ((12*Fiche.Salaire_Net-(0.325*omega+3550))/0.675)/12
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.irpp = (15000*0.26+10000*0.28+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-30000)*0.32)/12
            Fiche.css = (25+75+50+(Find_X(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants)-30000)*0.005)/12
    return Fiche

def IRPP_CSS_Net_Find(Imposable_Annuel: float, Chef_Famille: str, Enfants: int, Fiche: fiche_paie): # calculer l'irpp la css et le net à partir de l'imposable annuel
    x = Find_X(Imposable_Annuel, Chef_Famille, Enfants)
    if 5000 < x <= 20000:
        Fiche.irpp = ((x-5000)*0.26)/12
        Fiche.css = (25+(x-5000)*0.005)/12
    elif 20000 < x <= 30000:
        Fiche.irpp = (15000*0.26+(x-20000)*0.28)/12
        Fiche.css = (25+75+(x-20000)*0.005)/12
    elif 30000 < x <= 50000:
        Fiche.irpp = (15000*0.26+10000*0.28+(x-30000)*0.32)/12
        Fiche.css = (25+75+50+(x-30000)*0.005)/12
    elif 50000 < x:
        Fiche.irpp = (15000*0.26+10000*0.28+20000*0.32+(x-50000)*0.35)/12
        Fiche.css = (25+75+50+100+(x-50000)*0.005)/12
    else:
        Fiche.irpp = 0
        Fiche.css = 0
    Fiche.Salaire_Net = Fiche.Imposable-Fiche.irpp-Fiche.css
    return Fiche

def get_request_primary_content(request) -> fiche_paie: #obtenir les donnes primaires nom, prenom, cin...
    Fiche = fiche_paie()
    Fiche.Nom =request.POST.get("Nom", None)
    Fiche.Prénom =request.POST.get("Prénom", None)
    Fiche.Num_Affiliation = NUM_AFFILIATION
    Fiche.Qualification =request.POST.get("Qualification", None)
    Fiche.N_CNSS =request.POST.get("N_CNSS", None)
    Fiche.Date =request.POST.get("Date")
    Fiche.Sit_Admin =request.POST.get("Sit_Admin", None)
    Fiche.Cat =int(request.POST.get("Cat"))
    Fiche.Ech =int(request.POST.get("Ech"))
    Fiche.Matricule = request.POST.get("Matricule")
    Fiche.Avance = float(request.POST.get("Avance"))
    Fiche.CIN = request.POST.get("CIN")
    Fiche.Adresse = request.POST.get("Adresse")
    Fiche.Enfants =int(request.POST.get("Enfants"))
    Fiche.Chef_Famille =request.POST.get("Chef_Famille")#on or none
    Fiche.Congé_Payé =int(request.POST.get("Congé_Payé"))
    Fiche.Congé_Non_Payé =int(request.POST.get("Congé_Non_Payé"))
    Fiche.Net =request.POST.get("Net")
    Fiche.Indemnité_Transport = float(request.POST. get("Indemnité_Transport"))
    Fiche.Indemnité_Présence= float(request.POST.get("Indemnité_Présence"))
    Fiche.Jours_Supp= int(request.POST.get("Jours_Supp"))
    Fiche.Autres_Ind_Primes= float(request.POST.get("Autres_Ind_Primes"))
    Fiche.Indemnité_Panier= float(request.POST.get("Indemnité_Panier"))
    return Fiche

def Round_Values(Fiche: fiche_paie):
    Fiche.val_congé_payé = round(Fiche.val_congé_payé, 4)
    Fiche.val_congé_non_payé = round(Fiche.val_congé_non_payé, 4)
    Fiche.val_jours_supp = round(Fiche.val_jours_supp, 4)
    Fiche.Val_Ind_Présence = round(Fiche.Val_Ind_Présence, 4)
    Fiche.Salaire_Du_Mois = round(Fiche.Salaire_Du_Mois, 4)
    Fiche.Indemnité_Transport = round(Fiche.Indemnité_Transport, 4)
    Fiche.Indemnité_Panier = round(Fiche.Indemnité_Panier, 4)
    Fiche.Indemnité_Présence = round(Fiche.Indemnité_Présence, 4)
    Fiche.Jours_Supp = round(Fiche.Jours_Supp, 4)
    Fiche.Autres_Ind_Primes = round(Fiche.Autres_Ind_Primes, 4)
    Fiche.SalaireBrut = round(Fiche.SalaireBrut, 4)
    Fiche.cnss = round(Fiche.cnss, 4)
    Fiche.Imposable = round(Fiche.Imposable, 4)
    Fiche.css = round(Fiche.css, 4)
    Fiche.irpp = round(Fiche.irpp, 4)
    Fiche.Salaire_Net = round(Fiche.Salaire_Net, 4)
    Fiche.Net_a_Payer = round(Fiche.Net_a_Payer, 4)
    Fiche.Avance = round(Fiche.Avance, 4)
    Fiche.Salaire_de_base = round(Fiche.Salaire_de_base, 4)
    return Fiche

def Fiche_Paie(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    if request.method == "POST":
        Fiche = get_request_primary_content(request) #obtenir les données primaires de la fiche de paie
        template_path = "Fiche_Template.html"
        template = get_template(template_path)
        #(1)calcul à partir du salaire de base
        if Fiche.Net == None:
            try:
                Fiche.Salaire_de_base = float(request.POST.get("SalaireBase")) #S'assurer que l'utilisateur a saisit une valeur pour Salaire de base
            except:
                Fiche.Salaire_de_base = None
                return redirect(Fiche_Paie)
            Fiche.val_congé_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Payé
            Fiche.val_congé_non_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Non_Payé
            Fiche.val_jours_supp = (Fiche.Jours_Supp*(Fiche.Salaire_de_base/26))
            Fiche.jours_travaillés = 26-Fiche.Congé_Non_Payé-Fiche.Congé_Payé
            Fiche.Val_Ind_Présence = Fiche.Indemnité_Présence*(Fiche.jours_travaillés+Fiche.Jours_Supp)
            Fiche.Salaire_Du_Mois = Fiche.Salaire_de_base-Fiche.val_congé_non_payé-Fiche.val_congé_payé
            Fiche.SalaireBrut = Fiche.Salaire_Du_Mois+Fiche.Indemnité_Transport+Fiche.Indemnité_Panier+Fiche.val_jours_supp+Fiche.Val_Ind_Présence+Fiche.Autres_Ind_Primes+Fiche.val_congé_payé
            Fiche.cnss = Fiche.SalaireBrut*0.0918
            Fiche.Imposable = Fiche.SalaireBrut-Fiche.cnss
            Fiche = IRPP_CSS_Net_Find(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants, Fiche)
            Fiche.Net_a_Payer = Fiche.Salaire_Net-Fiche.Avance
            #Fiche.Salaire_de_base = Fiche.Salaire_Du_Mois+Fiche.val_congé_non_payé+Fiche.val_congé_payé
            Fiche = Round_Values(Fiche)
            if request.POST.get("Save") == "on":
                
                Fiche.save()
                context = {"Fiche": Fiche, "year": datetime.now().year, "month": datetime.now().month, "day": datetime.now().day}
                html = template.render(context=context)
                response = HttpResponse(content_type='application/pdf')
                name = Fiche.Nom + ' ' + Fiche.Prénom + '_' + str(datetime.now().day) + '_' + str(datetime.now().month) + '_' + str(datetime.now().year) + ".pdf"
                response['Content-Disposition'] = 'attachment; filename='+name
                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
                
            return render(
                request=request,
                template_name="Fiche_Paie.html",
                context={
                    "Fiche": Fiche,
                    "NUM_AFFILIATION": NUM_AFFILIATION,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
        else:
            try:
                Fiche.Net_a_Payer = float(request.POST.get("Net_a_Payer"))
            except:
                Fiche.Net_a_Payer = None
                return redirect(Fiche_Paie)

            Fiche = Brut_Find_From_Net(Fiche)
            Fiche.jours_travaillés = 26 - Fiche.Congé_Non_Payé - Fiche.Congé_Payé
            Fiche.Val_Ind_Présence = Fiche.Indemnité_Présence*(Fiche.jours_travaillés+Fiche.Jours_Supp)
            # Calculate jours_travaillés and val_jours_supp
            Fiche.Salaire_Du_Mois = (Fiche.jours_travaillés*(Fiche.SalaireBrut - Fiche.Autres_Ind_Primes - Fiche.Indemnité_Panier - Fiche.Indemnité_Transport - Fiche.Val_Ind_Présence))/(Fiche.jours_travaillés+Fiche.Congé_Payé+Fiche.Jours_Supp)

            # Calculate val_congé_non_payé
            Fiche.val_jours_supp = Fiche.Jours_Supp * (Fiche.Salaire_Du_Mois / Fiche.jours_travaillés)
            Fiche.val_congé_payé = (Fiche.Salaire_Du_Mois / Fiche.jours_travaillés) *Fiche.Congé_Payé
            Fiche.val_congé_non_payé = (Fiche.Salaire_Du_Mois / Fiche.jours_travaillés)*Fiche.Congé_Non_Payé
            Fiche.Salaire_de_base = Fiche.Salaire_Du_Mois+Fiche.val_congé_non_payé+Fiche.val_congé_payé
            Fiche = Round_Values(Fiche)
            if request.POST.get("Save") == "on":
                Fiche.save()
                context = {"Fiche": Fiche, "year": datetime.now().year, "month": datetime.now().month, "day": datetime.now().day}
                html = template.render(context=context)
                response = HttpResponse(content_type='application/pdf')
                name = Fiche.Nom + ' ' + Fiche.Prénom + '_' + str(datetime.now().day) + '_' + str(datetime.now().month) + '_' + str(datetime.now().year) + ".pdf"
                response['Content-Disposition'] = 'attachment; filename='+name
                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response

            return render(
                request=request,
                template_name="Fiche_Paie.html",
                context={
                    "Fiche": Fiche,
                    "NUM_AFFILIATION":  NUM_AFFILIATION,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
    return render(
        request=request, 
        template_name="Fiche_Paie.html",
        context={
            "NUM_AFFILIATION": NUM_AFFILIATION,
            "year": YEAR,
            "month": MONTH,
            "day": DAY
        },
    )

def Avances(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    emp_list = employé.objects.all()
    serialized_data = serialize('json', emp_list)

    return render(request=request,
                  template_name="Avances.html",
                  context={"Emp_List": serialized_data})
    
def Etats(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    fiche_list = fiche_paie.objects.all()
    serialized_data = serialize('json', fiche_list)#remember to remove période and fiche paie from admin page editable
    
    return render(request=request,
                  template_name="Etats_Maneken.html",
                  context={"Fiche_List": serialized_data, "fiche_list": fiche_list})

def New_Fiche(emp:employé) -> fiche_paie:
    fiche = fiche_paie()
    fiche.Nom = emp.Nom
    fiche.Prénom = emp.Prenom
    fiche.Num_Affiliation = NUM_AFFILIATION
    fiche.Qualification = emp.Id_Affectation.Id_Poste.Designation
    fiche.N_CNSS = emp.Id_CNSS.Numero
    fiche.Date = f"{DAY}/{MONTH}/{YEAR}"
    fiche.Matricule = emp.Matricule
    fiche.CIN = emp.CIN
    try:
        fiche.Adresse = emp.Adresse
    except ValueError:
        fiche.Adresse = ""
    fiche.Sit_Admin = emp.Id_Affectation.Id_Contrat.Designation
    fiche.Cat = emp.Cat
    fiche.Ech = emp.Ech
    fiche.Enfants = emp.Id_Situation.Nb_Enfants
    fiche.Chef_Famille = emp.Id_Situation.Chef_Famille
    fiche.Congé_Payé = emp.Id_Congé.Congé_Maladie_Ce_Mois + emp.Id_Congé.Congé_Annuel_Ce_Mois
    fiche.Congé_Non_Payé = emp.Id_Congé.Congé_Non_Payé_Ce_Mois
    fiche.Net = None
    fiche.Salaire_de_base = emp.Salaire
    fiche.Indemnité_Transport = emp.Id_Avantage.Indemnité_Transport
    fiche.Indemnité_Panier = emp.Id_Avantage.Indemnité_Panier
    fiche.Indemnité_Présence = emp.Id_Avantage.Indemnité_Présence
    fiche.Jours_Supp = emp.Id_Avantage.Jours_Supp
    fiche.Autres_Ind_Primes = emp.Id_Avantage.Autres_Ind_Primes
    fiche.Avance = emp.Avance
    #resetting values to 0:
    emp.Avance = 0
    emp.Id_Congé.Congé_Annuel_Ce_Mois = 0
    emp.Id_Congé.Congé_Non_Payé_Ce_Mois = 0
    emp.Id_Congé.Congé_Maladie_Ce_Mois = 0
    emp.Id_Congé.save()
    emp.save()
    return fiche

def Fin_De_Mois(request):
    if not request.session.get('login_test', False):
        return redirect('login')
    Fiche_List = list()
    Emp_List = employé.objects.all() 
    if request.method == 'POST':
        try:
            emp_id = request.POST.get("Id_Emp")
        except:
            emp_id = None
        
        if emp_id is not None:
            emp = employé.objects.get(id=emp_id)
            Fiche = New_Fiche(emp)
            Fiche.val_congé_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Payé
            Fiche.val_congé_non_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Non_Payé
            Fiche.val_jours_supp = (Fiche.Jours_Supp*(Fiche.Salaire_de_base/26))
            Fiche.jours_travaillés = 26-Fiche.Congé_Non_Payé-Fiche.Congé_Payé
            Fiche.Val_Ind_Présence = Fiche.Indemnité_Présence*(Fiche.jours_travaillés+Fiche.Jours_Supp)
            Fiche.Salaire_Du_Mois = Fiche.Salaire_de_base-Fiche.val_congé_non_payé-Fiche.val_congé_payé
            Fiche.SalaireBrut = Fiche.Salaire_Du_Mois+Fiche.Indemnité_Transport+Fiche.Indemnité_Panier+Fiche.val_jours_supp+Fiche.Val_Ind_Présence+Fiche.Autres_Ind_Primes+Fiche.val_congé_payé
            Fiche.cnss = float(Fiche.SalaireBrut)*0.0918
            Fiche.Imposable = float(Fiche.SalaireBrut)-Fiche.cnss
            Fiche = IRPP_CSS_Net_Find(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants, Fiche)
            Fiche.Net_a_Payer = Fiche.Salaire_Net-float(Fiche.Avance)
            Fiche = Round_Values(Fiche)
            Fiche.save()
            print(Fiche.val_congé_payé)
            emp.Id_Fiche = Fiche
            Fiche_List.append(Fiche)
        else:
            for emp in Emp_List:
                Fiche = New_Fiche(emp)
                Fiche.val_congé_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Payé
                Fiche.val_congé_non_payé = (Fiche.Salaire_de_base/26)*Fiche.Congé_Non_Payé
                Fiche.val_jours_supp = (Fiche.Jours_Supp*(Fiche.Salaire_de_base/26))
                Fiche.jours_travaillés = 26-Fiche.Congé_Non_Payé-Fiche.Congé_Payé
                Fiche.Val_Ind_Présence = Fiche.Indemnité_Présence*(Fiche.jours_travaillés+Fiche.Jours_Supp)
                Fiche.Salaire_Du_Mois = Fiche.Salaire_de_base-Fiche.val_congé_non_payé-Fiche.val_congé_payé
                Fiche.SalaireBrut = Fiche.Salaire_Du_Mois+Fiche.Indemnité_Transport+Fiche.Indemnité_Panier+Fiche.val_jours_supp+Fiche.Val_Ind_Présence+Fiche.Autres_Ind_Primes+Fiche.val_congé_payé
                Fiche.cnss = float(Fiche.SalaireBrut)*0.0918
                Fiche.Imposable = float(Fiche.SalaireBrut)-Fiche.cnss
                Fiche = IRPP_CSS_Net_Find(Fiche.Imposable*12, Fiche.Chef_Famille, Fiche.Enfants, Fiche)
                Fiche.Net_a_Payer = Fiche.Salaire_Net-Fiche.Avance
                Fiche = Round_Values(Fiche)
                Fiche.save()
                emp.Id_Fiche = Fiche
                Fiche_List.append(Fiche)
                
        template_path = "Fiche_Template.html"
        template = get_template(template_path)
        zip_buffer = BytesIO()  # Create a buffer to hold the ZIP file
        with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
            for Fiche in Fiche_List:
                context = {"Fiche": Fiche, "year": YEAR, "month": MONTH, "day": DAY}
                html = template.render(context=context)
                response = HttpResponse(content_type='application/pdf')
                name = Fiche.Nom + ' ' + Fiche.Prénom + '_' + str(DAY) + '_' + str(MONTH) + '_' + str(YEAR) + ".pdf"
                response['Content-Disposition'] = 'attachment; filename=' + name
                pisa_status = pisa.CreatePDF(html, dest=response)
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')

                # Add the PDF content to the ZIP file
                zip_file.writestr(name, response.content)

        # Close the buffer for writing
        zip_buffer.seek(0)

        # Create a response with the ZIP file
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=Fiches_De_Paie.zip'

        return response
    return render(request=request,
                  template_name="Fin_De_Mois.html",
                  context={"Emp_List": Emp_List,
                           "year": YEAR,
                           "month": MONTH,
                           "day": DAY,
                           })