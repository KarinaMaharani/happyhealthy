from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('disclaimer/', views.accept_disclaimer, name='accept_disclaimer'),
    path('guest/', views.guest_continue, name='guest_continue'),
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('caregiver-dashboard/', views.caregiver_dashboard, name='caregiver_dashboard'),
    path('patient-requests/', views.patient_requests, name='patient_requests'),
    path('approve-caregiver/<int:relationship_id>/', views.approve_caregiver, name='approve_caregiver'),
    path('reject-caregiver/<int:relationship_id>/', views.reject_caregiver, name='reject_caregiver'),
    path('remove-patient/<int:relationship_id>/', views.remove_patient, name='remove_patient'),
    path('patient-activity/<int:patient_id>/', views.patient_activity, name='patient_activity'),
    path('record-symptom/', views.record_symptom, name='record_symptom'),
    path('my-symptoms/', views.my_symptoms, name='my_symptoms'),
]
