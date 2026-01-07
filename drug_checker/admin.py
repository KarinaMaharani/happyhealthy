from django.contrib import admin
from .models import DrugSearch, DrugInteractionCheck, SavedDrug

@admin.register(DrugSearch)
class DrugSearchAdmin(admin.ModelAdmin):
    list_display = ('drug_name', 'drugbank_id', 'user', 'searched_at')
    list_filter = ('searched_at',)
    search_fields = ('drug_name', 'drugbank_id', 'user__username')
    date_hierarchy = 'searched_at'
    ordering = ('-searched_at',)

@admin.register(DrugInteractionCheck)
class DrugInteractionCheckAdmin(admin.ModelAdmin):
    list_display = ('user', 'drug1_name', 'drug2_name', 'severity', 'checked_at')
    list_filter = ('severity', 'checked_at')
    search_fields = ('drug1_name', 'drug2_name', 'user__username')
    date_hierarchy = 'checked_at'
    ordering = ('-checked_at',)

@admin.register(SavedDrug)
class SavedDrugAdmin(admin.ModelAdmin):
    list_display = ('drug_name', 'drugbank_id', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('drug_name', 'drugbank_id', 'user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
