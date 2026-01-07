from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .services import DrugBankService
from .models import DrugSearch, DrugInteractionCheck, SavedDrug


def home(request):
    return redirect('search_drugs')


def autocomplete_drugs(request):
    """API endpoint for drug name autocomplete"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    service = DrugBankService()
    result = service.search_drugs(query)
    
    if result['success']:
        suggestions = [{
            'name': drug['name'],
            'drugbank_id': drug['drugbank_id'],
            'type': drug.get('type', 'small molecule')
        } for drug in result['data'][:10]]
        return JsonResponse({'results': suggestions})
    else:
        return JsonResponse({'results': [], 'error': result.get('error')})


def search_drugs_api(request):
    """API endpoint for searching drugs (returns filtered results as JSON)"""
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': [], 'total': 0})
    
    service = DrugBankService()
    all_drugs = service.get_all_drugs()
    
    # Filter drugs by query (search in name, synonyms, ID)
    query_lower = query.lower()
    filtered = []
    for drug in all_drugs:
        if (query_lower in drug['name'].lower() or
            query_lower in drug['drugbank_id'].lower() or
            any(query_lower in syn.lower() for syn in drug.get('synonyms', []))):
            filtered.append(drug)
            if len(filtered) >= 100:  # Limit to 100 results
                break
    
    return JsonResponse({
        'results': filtered,
        'total': len(filtered),
        'total_in_db': len(all_drugs)
    })


def search_drugs(request):
    context = {'page_title': 'Search Drugs'}
    
    # Get all drugs for display and filtering
    service = DrugBankService()
    all_drugs = service.get_all_drugs()
    
    # Only send first 100 drugs initially to reduce page size
    # JavaScript will handle filtering on client-side
    context['all_drugs'] = all_drugs[:100]
    context['total_drugs'] = len(all_drugs)
    context['showing_partial'] = len(all_drugs) > 100
    
    return render(request, 'drug_checker/search.html', context)


def drug_detail(request, drugbank_id):
    service = DrugBankService()
    result = service.get_drug_details(drugbank_id)
    
    context = {'page_title': 'Drug Details', 'drugbank_id': drugbank_id}
    
    if result['success']:
        context['drug'] = result['data']
    else:
        context['error'] = result.get('error', 'Failed to load drug details')
    
    return render(request, 'drug_checker/drug_detail.html', context)


def interaction_checker(request):
    context = {'page_title': 'Check Drug Interactions'}
    
    if request.method == 'POST':
        drug1 = request.POST.get('drug1', '').strip()
        drug2 = request.POST.get('drug2', '').strip()
        
        if drug1 and drug2:
            service = DrugBankService()
            result = service.check_drug_interactions(drug1, drug2)
            
            if result['success']:
                # Transform data to match template expectations
                formatted_interactions = []
                for interaction in result['data']:
                    formatted_interactions.append({
                        'ingredient': {'name': interaction['drug1']},
                        'affected_ingredient': {'name': interaction['drug2']},
                        'description': interaction['description'],
                        'severity': interaction['severity'],
                        'extended_description': ''  # Not available in XML
                    })
                
                context['interactions'] = formatted_interactions
                context['total'] = result['total']
                context['drug1'] = drug1
                context['drug2'] = drug2
                
                if request.user.is_authenticated and result['data']:
                    for interaction in result['data'][:1]:
                        DrugInteractionCheck.objects.create(
                            user=request.user,
                            drug1_name=interaction.get('drug1', drug1),
                            drug1_id=drug1,
                            drug2_name=interaction.get('drug2', drug2),
                            drug2_id=drug2,
                            severity=interaction.get('severity', 'minor'),
                            description=interaction.get('description', '')
                        )
            else:
                context['error'] = result.get('error', 'Check failed. Please verify drug IDs.')
    
    return render(request, 'drug_checker/interaction_checker.html', context)


@login_required
def history(request):
    searches = DrugSearch.objects.filter(user=request.user)[:20]
    interactions = DrugInteractionCheck.objects.filter(user=request.user)[:20]
    
    context = {
        'page_title': 'My History',
        'searches': searches,
        'interactions': interactions
    }
    
    return render(request, 'drug_checker/history.html', context)


@login_required
def saved_drugs(request):
    saved = SavedDrug.objects.filter(user=request.user)
    
    context = {
        'page_title': 'Saved Drugs',
        'saved_drugs': saved
    }
    
    return render(request, 'drug_checker/saved_drugs.html', context)


@login_required
def save_drug(request):
    if request.method == 'POST':
        drugbank_id = request.POST.get('drugbank_id')
        drug_name = request.POST.get('drug_name')
        notes = request.POST.get('notes', '')
        
        if drugbank_id and drug_name:
            SavedDrug.objects.get_or_create(
                user=request.user,
                drugbank_id=drugbank_id,
                defaults={'drug_name': drug_name, 'notes': notes}
            )
            messages.success(request, f'{drug_name} saved successfully!')
        
    return redirect('saved_drugs')
