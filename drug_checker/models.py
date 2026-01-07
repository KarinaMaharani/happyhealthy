from django.db import models
from django.contrib.auth.models import User


class DrugSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    drug_name = models.CharField(max_length=255)
    drugbank_id = models.CharField(max_length=20, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
    
    def __str__(self):
        return f"{self.drug_name} - {self.searched_at.strftime('%Y-%m-%d %H:%M')}"


class DrugInteractionCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    drug1_name = models.CharField(max_length=255)
    drug1_id = models.CharField(max_length=20)
    drug2_name = models.CharField(max_length=255)
    drug2_id = models.CharField(max_length=20)
    severity = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-checked_at']
    
    def __str__(self):
        return f"{self.drug1_name} + {self.drug2_name}"


class SavedDrug(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=255)
    drugbank_id = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'drugbank_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.drug_name}"
