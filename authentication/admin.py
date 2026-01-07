from django.contrib import admin
from .models import UserProfile, CaregiverPatientRelationship, SymptomRecord

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'disclaimer_accepted', 'phone_number', 'created_at')
    list_filter = ('role', 'disclaimer_accepted', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(CaregiverPatientRelationship)
class CaregiverPatientRelationshipAdmin(admin.ModelAdmin):
    list_display = ('caregiver', 'patient', 'status', 'created_at', 'approved_date')
    list_filter = ('status', 'created_at')
    search_fields = ('caregiver__username', 'patient__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = ['approve_relationships', 'reject_relationships']
    
    def approve_relationships(self, request, queryset):
        for relationship in queryset:
            relationship.approve()
        self.message_user(request, f'{queryset.count()} relationships approved.')
    approve_relationships.short_description = 'Approve selected relationships'
    
    def reject_relationships(self, request, queryset):
        for relationship in queryset:
            relationship.reject()
        self.message_user(request, f'{queryset.count()} relationships rejected.')
    reject_relationships.short_description = 'Reject selected relationships'


@admin.register(SymptomRecord)
class SymptomRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'symptom_type', 'severity', 'is_concerning', 'caregiver_notified', 'recorded_at')
    list_filter = ('symptom_type', 'severity', 'is_concerning', 'caregiver_notified', 'recorded_at')
    search_fields = ('patient__username', 'notes')
    date_hierarchy = 'recorded_at'
    ordering = ('-recorded_at',)
    readonly_fields = ('recorded_at', 'is_concerning')

