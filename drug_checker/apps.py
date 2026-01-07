from django.apps import AppConfig


class DrugCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drug_checker'
    
    def ready(self):
        """Preload DrugBank database when Django starts"""
        import os
        # Only preload in the main process (not in reloader)
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                print("\n" + "="*60)
                print("🔄 Preloading DrugBank database...")
                print("This will take 30-60 seconds but speeds up first search!")
                print("="*60 + "\n")
                
                from .services import DrugBankService
                service = DrugBankService()
                # Access root to trigger loading
                _ = service.root
                
                print("\n" + "="*60)
                print("✅ DrugBank database preloaded successfully!")
                print("All drug searches will now be instant.")
                print("="*60 + "\n")
            except Exception as e:
                print(f"\n⚠️  Warning: Could not preload DrugBank database: {e}\n")
