from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='drug_home'),
    path('search/', views.search_drugs, name='search_drugs'),
    path('search/api/', views.search_drugs_api, name='search_drugs_api'),
    path('autocomplete/', views.autocomplete_drugs, name='autocomplete_drugs'),
    path('detail/<str:drugbank_id>/', views.drug_detail, name='drug_detail'),
    path('interaction/', views.interaction_checker, name='interaction_checker'),
    path('history/', views.history, name='history'),
    path('saved/', views.saved_drugs, name='saved_drugs'),
    path('save/', views.save_drug, name='save_drug'),
]
