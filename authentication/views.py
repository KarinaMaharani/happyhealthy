from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django import forms
from .models import UserProfile, CaregiverPatientRelationship, SymptomRecord


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


def register(request):
    """Simplified registration without email verification"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')
        
        # Debug: print what role we received
        print(f"DEBUG: Received role from POST: {role}")
        print(f"DEBUG: All POST data: {request.POST}")
        
        # Validate role
        if not role or role not in ['patient', 'caregiver']:
            form.add_error(None, 'Please select a role (Patient or Caregiver)')
        
        if form.is_valid():
            user = form.save()
            
            # Create user profile with the correct role IMMEDIATELY
            # Delete any profile that might have been auto-created
            UserProfile.objects.filter(user=user).delete()
            
            profile = UserProfile.objects.create(
                user=user,
                role=role
            )
            
            print(f"DEBUG: User created with role: {profile.role}")
            print(f"DEBUG: Profile role verification: {user.profile.role}")
            
            # Auto-login after registration
            login(request, user)
            
            # Refresh user from database to ensure profile is loaded
            request.user.refresh_from_db()
            messages.success(request, f'Welcome to Happy Healthy, {user.username}!')
            
            # Redirect to disclaimer if not accepted
            if not profile.disclaimer_accepted:
                return redirect('accept_disclaimer')
            
            return redirect('drug_home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def accept_disclaimer(request):
    """Disclaimer acceptance page for first-time users"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to continue.')
        return redirect('login')
    
    profile = request.user.profile
    
    # If already accepted, redirect to home
    if profile.disclaimer_accepted:
        return redirect('drug_home')
    
    if request.method == 'POST':
        if request.POST.get('accept_disclaimer'):
            profile.accept_disclaimer()
            messages.success(request, 'Thank you for accepting the terms. You can now use Happy Healthy!')
            return redirect('drug_home')
        else:
            context = {'error': 'You must accept the disclaimer to use Happy Healthy.'}
            return render(request, 'auth/disclaimer.html', context)
    
    return render(request, 'auth/disclaimer.html')


def custom_login(request):
    """Login view with disclaimer check"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Refresh user from database to ensure profile is loaded
            request.user.refresh_from_db()
            
            print(f"DEBUG: Login - User {user.username} has role: {user.profile.role}")
            
            # Check if disclaimer accepted
            if not user.profile.disclaimer_accepted:
                return redirect('accept_disclaimer')
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('drug_home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def verify_email(request, token):
    """Legacy email verification - now disabled"""
    messages.info(request, 'Email verification is no longer required. Please login to continue.')
    return redirect('login')


@login_required
def resend_verification(request):
    """Resend verification email"""
    profile = request.user.profile
    
    if profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('home')
    
    token = profile.generate_verification_token()
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': token})
    )
    
    email_message = f'''Hello {request.user.username},

Please verify your email by clicking the link below:
{verification_url}

This link will expire in 24 hours.

Thank you,
Happy Healthy Team'''
    
    send_mail(
        'Verify Your Email - Happy Healthy',
        email_message,
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )
    
    messages.success(request, f'Verification email sent to {request.user.email}')
    return redirect('home')


@login_required
def add_patient(request):
    """Caregiver adds a patient by username and email confirmation"""
    if request.user.profile.role != 'caregiver':
        messages.error(request, 'Only caregivers can add patients.')
        return redirect('drug_home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        request_message = request.POST.get('request_message', '').strip()
        
        try:
            patient = User.objects.get(username=username, email=email)
            
            # Check if patient is actually a patient
            if patient.profile.role != 'patient':
                messages.error(request, f'{username} is not registered as a patient.')
                return redirect('add_patient')
            
            # Check if relationship already exists
            existing = CaregiverPatientRelationship.objects.filter(
                caregiver=request.user, 
                patient=patient
            ).first()
            
            if existing:
                if existing.status == 'pending':
                    messages.info(request, f'You already have a pending request for {username}.')
                elif existing.status == 'active':
                    messages.info(request, f'You are already monitoring {username}.')
                elif existing.status == 'rejected':
                    messages.error(request, f'{username} has rejected your monitoring request.')
                else:
                    messages.info(request, f'A relationship with {username} already exists.')
            else:
                # Create new relationship request
                relationship = CaregiverPatientRelationship.objects.create(
                    caregiver=request.user,
                    patient=patient,
                    request_message=request_message
                )
                
                # Send notification email to patient
                try:
                    send_mail(
                        'Caregiver Monitoring Request - Happy Healthy',
                        f'Hello {patient.username},\n\n'
                        f'{request.user.username} ({request.user.email}) has requested to monitor your health on Happy Healthy.\n\n'
                        f'{f"Message: {request_message}" if request_message else ""}\n\n'
                        f'Please log in to your account to approve or reject this request.\n\n'
                        f'Best regards,\nHappy Healthy Team',
                        settings.DEFAULT_FROM_EMAIL,
                        [patient.email],
                        fail_silently=True,
                    )
                    messages.success(request, f'Monitoring request sent to {username}. They will receive an email notification.')
                except Exception as e:
                    messages.success(request, f'Monitoring request sent to {username}. (Email notification may not have been sent)')
            
            return redirect('caregiver_dashboard')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with that username and email combination. Both must match exactly.')
            return redirect('add_patient')
    
    return render(request, 'auth/add_patient.html')


@login_required
def caregiver_dashboard(request):
    """Dashboard for caregivers to manage patients"""
    if request.user.profile.role != 'caregiver':
        messages.error(request, 'Access denied. Caregivers only.')
        return redirect('drug_home')
    
    relationships = CaregiverPatientRelationship.objects.filter(
        caregiver=request.user
    ).select_related('patient', 'patient__profile').order_by('-created_at')
    
    # Get concerning symptoms for all active patients
    from django.utils import timezone
    from datetime import timedelta
    
    active_patients = relationships.filter(status='active').values_list('patient_id', flat=True)
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    concerning_symptoms = SymptomRecord.objects.filter(
        patient_id__in=active_patients,
        is_concerning=True,
        recorded_at__gte=seven_days_ago
    ).select_related('patient').order_by('-recorded_at')[:20]
    
    context = {
        'relationships': relationships,
        'active_count': relationships.filter(status='active').count(),
        'pending_count': relationships.filter(status='pending').count(),
        'concerning_symptoms': concerning_symptoms,
    }
    return render(request, 'auth/caregiver_dashboard.html', context)


@login_required
def patient_requests(request):
    """View for patients to see and manage caregiver requests"""
    if request.user.profile.role != 'patient':
        messages.error(request, 'Access denied. Patients only.')
        return redirect('drug_home')
    
    requests = CaregiverPatientRelationship.objects.filter(
        patient=request.user
    ).select_related('caregiver', 'caregiver__profile').order_by('-created_at')
    
    context = {
        'requests': requests,
        'pending_count': requests.filter(status='pending').count(),
        'active_count': requests.filter(status='active').count(),
    }
    return render(request, 'auth/patient_requests.html', context)


@login_required
def approve_caregiver(request, relationship_id):
    """Patient approves a caregiver monitoring request"""
    relationship = get_object_or_404(
        CaregiverPatientRelationship, 
        id=relationship_id, 
        patient=request.user
    )
    
    relationship.approve()
    messages.success(request, f'{relationship.caregiver.username} can now monitor your medications.')
    return redirect('patient_requests')


@login_required
def reject_caregiver(request, relationship_id):
    """Patient rejects a caregiver monitoring request"""
    relationship = get_object_or_404(
        CaregiverPatientRelationship, 
        id=relationship_id, 
        patient=request.user
    )
    
    relationship.reject()
    messages.success(request, f'Monitoring request from {relationship.caregiver.username} rejected.')
    return redirect('patient_requests')


@login_required
def remove_patient(request, relationship_id):
    """Caregiver removes a patient from monitoring"""
    relationship = get_object_or_404(
        CaregiverPatientRelationship, 
        id=relationship_id, 
        caregiver=request.user
    )
    
    relationship.remove()
    messages.success(request, f'Stopped monitoring {relationship.patient.username}.')
    return redirect('caregiver_dashboard')


@login_required
def patient_activity(request, patient_id):
    """View patient's drug activity (for caregivers only)"""
    if request.user.profile.role != 'caregiver':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Verify caregiver has active relationship with patient
    relationship = get_object_or_404(
        CaregiverPatientRelationship,
        caregiver=request.user,
        patient_id=patient_id,
        status='active'
    )
    
    from drug_checker.models import DrugSearch, DrugInteractionCheck, SavedDrug
    
    patient = relationship.patient
    searches = DrugSearch.objects.filter(user=patient).order_by('-searched_at')[:20]
    interactions = DrugInteractionCheck.objects.filter(user=patient).order_by('-checked_at')[:20]
    saved_drugs = SavedDrug.objects.filter(user=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'relationship': relationship,
        'searches': searches,
        'interactions': interactions,
        'saved_drugs': saved_drugs,
    }
    return render(request, 'auth/patient_activity.html', context)


def guest_continue(request):
    """Allow users to continue as guest"""
    request.session['is_guest'] = True
    messages.info(request, 'Continuing as guest. Some features may be limited.')
    return redirect('home')


def logout_view(request):
    """Custom logout view"""
    logout(request)
    if 'is_guest' in request.session:
        del request.session['is_guest']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')


@login_required
def record_symptom(request):
    """Record a new symptom (patients only)"""
    if request.user.profile.role != 'patient':
        messages.error(request, 'Only patients can record symptoms.')
        return redirect('drug_home')
    
    if request.method == 'POST':
        symptom_type = request.POST.get('symptom_type')
        severity = request.POST.get('severity')
        notes = request.POST.get('notes', '').strip()
        
        if symptom_type and severity:
            symptom = SymptomRecord.objects.create(
                patient=request.user,
                symptom_type=symptom_type,
                severity=int(severity),
                notes=notes
            )
            
            # Check if concerning and notify caregivers
            if symptom.is_concerning:
                # Get all active caregivers
                relationships = CaregiverPatientRelationship.objects.filter(
                    patient=request.user,
                    status='active'
                )
                
                # Mark as notified (in real app, send actual notifications)
                symptom.caregiver_notified = True
                symptom.save()
                
                messages.warning(request, 
                    f'Symptom recorded. This is flagged as concerning - your caregivers have been notified.')
            else:
                messages.success(request, 'Symptom recorded successfully.')
            
            return redirect('my_symptoms')
    
    context = {
        'symptom_categories': SymptomRecord.SYMPTOM_CATEGORIES,
        'severity_levels': SymptomRecord.SEVERITY_LEVELS,
    }
    return render(request, 'auth/record_symptom.html', context)


@login_required
def my_symptoms(request):
    """View patient's symptom history"""
    if request.user.profile.role != 'patient':
        messages.error(request, 'Only patients can view symptom records.')
        return redirect('drug_home')
    
    symptoms = SymptomRecord.objects.filter(patient=request.user).order_by('-recorded_at')
    
    # Get statistics
    total_symptoms = symptoms.count()
    concerning_count = symptoms.filter(is_concerning=True).count()
    
    # Recent 30 days
    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_symptoms = symptoms.filter(recorded_at__gte=thirty_days_ago)
    
    context = {
        'symptoms': symptoms[:50],  # Last 50 symptoms
        'total_symptoms': total_symptoms,
        'concerning_count': concerning_count,
        'recent_count': recent_symptoms.count(),
    }
    return render(request, 'auth/my_symptoms.html', context)
