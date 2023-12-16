from django.urls import path
from .views import *
urlpatterns = [
    path(route="Index", view=Index, name="Index"),
    path(route="Comptes/", view=Comptes, name="Comptes"),
    path(route="Congés/", view=Congés, name= 'Congés'),
    path(route="Congés/Add", view=Congés_Add, name='Congés_Add'),
    path(route="Congés/Détails", view=Congés_Détails, name='Congés_Détails'),
    path(route="search/", view=search_view, name='Search_view'),
    path(route="Fiche/", view=Fiche_Paie, name='Fiche_Paie'),
    path(route="Avances/", view=Avances, name='Avances'),
    path(route="Etats/", view=Etats, name='Etats'),
    path(route="Fin_De_Mois/", view=Fin_De_Mois, name='Fin_De_Mois'),
]
