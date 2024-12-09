# views.py
from django.shortcuts import render,get_object_or_404, redirect
from .forms import NaissanceForm  # Assurez-vous que vous avez créé un formulaire pour le modèle Naissance
from django.contrib import messages
from .forms import UserForm
from django.http import JsonResponse
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .models import Naissance,Utilisateur,Naissance


# views.py
def valider_acte(request, id_acte):
    acte = Naissance.objects.get(id=id_acte)
    if acte.statut_validation == 'En attente':
        acte.statut_validation = 'Validé'
        acte.save()
        messages.success(request, f"L'acte {id_acte} a été validé.")
    else:
        messages.warning(request, f"L'acte {id_acte} est déjà validé.")
    return redirect('liste_actes')

def gestion_naissances(request):
    # Récupérer toutes les naissances
    naissances = Naissance.objects.all()

    # Recherche (si un terme est soumis)
    search_term = request.GET.get('search', '')
    if search_term:
        naissances = naissances.filter(
            nom_enfant__icontains=search_term) | naissances.filter(
            nom_pere__icontains=search_term)
    
    return render(request, 'gestion_naissances.html', {'naissances': naissances})

def gestion_actes(request):
    naissance = Naissance.objects.all()
    return render(request, 'gestion_actes.html', {'naissance': naissance})

def dashboard(request):
    total_actes = Naissance.objects.count()
    en_attente = Naissance.objects.filter(statut_validation="en_attente").count()
    validés = Naissance.objects.filter(statut_validation="valide").count()
    rejetés = Naissance.objects.filter(statut_validation="rejete").count()
    
    actes = Naissance.objects.all()
    
    return render(request, 'dashboard.html', {
        'total_actes': total_actes,
        'en_attente': en_attente,
        'validés': validés,
        'rejetés': rejetés,
        'actes': actes
    })
# views.py

@csrf_exempt
def update_acte(request, acte_id):
    if request.method == "POST":
        try:
            acte = Naissance.objects.get(id=acte_id)
            statut = request.POST.get("statut")
            nom_enfant = request.POST.get("nom_enfant")
            date_naissance = request.POST.get("date_naissance")

            if statut:
                acte.statut_validation = statut
            if nom_enfant:
                acte.nom_enfant = nom_enfant
            if date_naissance:
                acte.date_naissance = date_naissance

            acte.save()
            return JsonResponse({"status": "success", "message": "Acte mis à jour!"})

        except Naissance.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Acte de naissance non trouvé!"})

def liste_actes(request):
    actes = Naissance.objects.all()
    return render(request, 'liste_actes.html', {'actes': actes})

# views.py

def ajouter_acte(request):
    if request.method == 'POST':
        nom_enfant = request.POST.get('nom_enfant')
        date_naissance = request.POST.get('date_naissance')
        statut = request.POST.get('statut')
        
        Naissance.objects.create(
            nom_enfant=nom_enfant,
            date_naissance=date_naissance,
            statut_validation=statut
        )
        
        return redirect('liste_actes')
    
    return render(request, 'ajouter_acte.html')
# views.py

def modifier_acte(request, acte_id):
    acte = get_object_or_404(Naissance, id=acte_id)
    
    if request.method == 'POST':
        acte.nom_enfant = request.POST.get('nom_enfant')
        acte.date_naissance = request.POST.get('date_naissance')
        acte.statut_validation = request.POST.get('etat')
        acte.save()
        
        return redirect('liste_actes')
    
    return render(request, 'modifier_acte.html', {'acte': acte})
# views.py

def details_acte(request, acte_id):
    acte = get_object_or_404(Naissance, id=acte_id)
    return render(request, 'details_acte.html', {'naissance': acte})



# Vue pour le rapport mensuel
def rapport_mensuel(request):
    # Calculer les données nécessaires
    total_naissances = Naissance.objects.filter(date_naissance__month=11).count()  # Exemple pour le mois de novembre
    actes_valides = Naissance.objects.filter(date_naissance__month=11, statut_validation="validé").count()
    dossiers_en_retard = Naissance.objects.filter(date_naissance__month=11, statut_validation="en attente").count()

    # Détails des naissances par localité (vous devez ajuster selon la structure de votre modèle)
    naissances_par_localite = Naissance.objects.filter(date_naissance__month=11) \
        .values('lieu_naissance') \
        .annotate(nombre_naissances=Count('id')) \
        .annotate(taux_natalite=Count('id') * 100.0 / total_naissances)

    # Récupérer les valeurs pour le graphique
    localites = [item['lieu_naissance'] for item in naissances_par_localite]
    taux_natalite = [item['taux_natalite'] for item in naissances_par_localite]

    context = {
        'total_naissances': total_naissances,
        'actes_valides': actes_valides,
        'dossiers_en_retard': dossiers_en_retard,
        'naissances_par_localite': naissances_par_localite,
        'localites': localites,
        'taux_natalite': taux_natalite,
    }

    return render(request, 'rapport_mensuel.html', context)

# Vue pour modifier un acte de naissance
def modifier_naissance(request, naissance_id):
    # Récupérer l'acte de naissance par ID
    naissance = get_object_or_404(Naissance, id=naissance_id)

    if request.method == 'POST':
        # Créer un formulaire avec les données envoyées
        form = NaissanceForm(request.POST, instance=naissance)
        if form.is_valid():
            # Sauvegarder les modifications
            form.save()
            # Rediriger vers une page de succès ou vers la liste des actes
            return redirect('gestion:liste_naissances')
    else:
        # Si c'est une requête GET, pré-remplir le formulaire avec les données de l'acte
        form = NaissanceForm(instance=naissance)

    return render(request, 'modifier_actes.html', {'form': form, 'naissance': naissance})





# Afficher la liste des utilisateurs
def gestion_utilisateurs(request):
    users = UserProfile.objects.all()
    return render(request, 'gestion_utilisateurs.html', {'users': users})

# Ajouter un nouvel utilisateur
def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gestion_utilisateurs')
    else:
        form = UserForm()
    return render(request, 'gestion_utilisateurs.html', {'form': form})

# Modifier un utilisateur
def modifier_utilisateur(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('gestion_utilisateurs')
    else:
        form = UserForm(instance=user)
    return render(request, 'modifier_utilisateur.html', {'form': form, 'user': user})
