from django.apps import AppConfig
import logging


logger = logging.getLogger(__name__)


class DrugCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drug_checker'
    
    def ready(self):
        """Preload DrugBank database when Django starts"""
        import os
        # Only preload in the main process (not in reloader)
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                from .services import DrugBankService
                service = DrugBankService()
                # Access root to trigger loading
                _ = service.root
            except Exception as e:
                logger.warning('Could not preload DrugBank database: %s', e)
