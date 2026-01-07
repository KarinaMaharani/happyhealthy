from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('caregiver', 'Caregiver'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Disclaimer consent
    disclaimer_accepted = models.BooleanField(default=False)
    disclaimer_accepted_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def accept_disclaimer(self):
        """Mark disclaimer as accepted"""
        self.disclaimer_accepted = True
        self.disclaimer_accepted_at = timezone.now()
        self.save()


class CaregiverPatientRelationship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed'),
    ]
    
    caregiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients_monitoring')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caregivers_assigned')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    request_message = models.TextField(blank=True, help_text="Message from caregiver explaining relationship")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('caregiver', 'patient')
        verbose_name = 'Caregiver-Patient Relationship'
        verbose_name_plural = 'Caregiver-Patient Relationships'
    
    def __str__(self):
        return f"{self.caregiver.username} → {self.patient.username} ({self.status})"
    
    def approve(self):
        """Approve the relationship"""
        self.status = 'active'
        self.approved_date = timezone.now()
        self.save()
    
    def reject(self):
        """Reject the relationship"""
        self.status = 'rejected'
        self.save()
    
    def remove(self):
        """Remove the relationship"""
        self.status = 'removed'
        self.save()


class SymptomRecord(models.Model):
    """WHO ICD-10 based symptom tracking for mental health"""
    
    # ICD-10 Mental Health Symptom Categories (F00-F99)
    SYMPTOM_CATEGORIES = [
        # Mood/Depression Symptoms (F32-F33)
        ('depressed_mood', 'Depressed Mood'),
        ('loss_of_interest', 'Loss of Interest or Pleasure'),
        ('fatigue', 'Fatigue or Loss of Energy'),
        ('sleep_disturbance', 'Sleep Disturbance (Insomnia/Hypersomnia)'),
        ('appetite_change', 'Appetite or Weight Change'),
        ('concentration_difficulty', 'Difficulty Concentrating'),
        ('feelings_worthlessness', 'Feelings of Worthlessness or Guilt'),
        ('psychomotor_agitation', 'Psychomotor Agitation or Retardation'),
        ('suicidal_thoughts', 'Suicidal Thoughts'),
        
        # Anxiety Symptoms (F40-F41)
        ('excessive_worry', 'Excessive Worry'),
        ('restlessness', 'Restlessness or Feeling On Edge'),
        ('irritability', 'Irritability'),
        ('muscle_tension', 'Muscle Tension'),
        ('panic_attacks', 'Panic Attacks'),
        ('social_anxiety', 'Social Anxiety'),
        
        # Behavioral Symptoms
        ('social_withdrawal', 'Social Withdrawal'),
        ('self_harm', 'Self-Harm Behavior'),
        ('substance_use', 'Substance Use'),
        ('mood_swings', 'Mood Swings'),
        
        # Physical Symptoms
        ('headaches', 'Headaches'),
        ('body_aches', 'Body Aches'),
        ('digestive_issues', 'Digestive Issues'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Severe'),
        (4, 'Critical'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_records')
    symptom_type = models.CharField(max_length=50, choices=SYMPTOM_CATEGORIES)
    severity = models.IntegerField(choices=SEVERITY_LEVELS)
    notes = models.TextField(blank=True, help_text="Additional details about the symptom")
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    # Flag for concerning symptoms that need caregiver notification
    is_concerning = models.BooleanField(default=False)
    caregiver_notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Symptom Record'
        verbose_name_plural = 'Symptom Records'
    
    def __str__(self):
        return f"{self.patient.username} - {self.get_symptom_type_display()} ({self.get_severity_display()})"
    
    def save(self, *args, **kwargs):
        """Auto-flag concerning symptoms"""
        # Critical severity or suicidal thoughts/self-harm are always concerning
        if (self.severity >= 3 or 
            self.symptom_type in ['suicidal_thoughts', 'self_harm', 'panic_attacks']):
            self.is_concerning = True
        super().save(*args, **kwargs)


# Signal removed - profile creation now handled in views to set correct role
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Auto-create UserProfile when User is created"""
#     if created:
#         UserProfile.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     """Save UserProfile when User is saved"""
#     if hasattr(instance, 'profile'):
#         instance.profile.save()

