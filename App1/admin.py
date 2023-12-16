from django.contrib import admin

from .models import *


admin.site.site_header = "Maneken Manage"
admin.site.register(employé)
admin.site.register(banque)
admin.site.register(cnss)
admin.site.register(affectation)
admin.site.register(local)
admin.site.register(poste)
admin.site.register(situation)
admin.site.register(contrat)
admin.site.register(congés)
admin.site.register(avantages)