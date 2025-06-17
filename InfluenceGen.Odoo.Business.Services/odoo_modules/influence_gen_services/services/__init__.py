from . import onboarding_service
from . import campaign_management_service
from . import payment_processing_service
from . import ai_integration_service
from . import data_management_service
from . import retention_and_legal_hold_service

# To make services easily accessible via self.env['influence_gen.services.service_name']
# we can instantiate them once or provide a mechanism to get an instance.
# A common pattern is to have a base service class or a registry if complex setup is needed.
# For simple cases, other parts of the code can instantiate them directly:
# SvcClass(self.env).method_name()
#
# If we want them to behave somewhat like Odoo models in terms of env access,
# we can register them in the environment or provide helpers.
# For now, relying on direct instantiation by callers.

# Example of how services might be 'registered' or made available if needed:
# (This is conceptual and not strictly necessary if services are plain Python classes
#  called with env passed to their constructor from models/controllers/wizards)

# def get_onboarding_service(env):
#     return onboarding_service.OnboardingService(env)

# def get_campaign_management_service(env):
#     return campaign_management_service.CampaignManagementService(env)

# ... and so on for other services.

# Or, if they were to be singletons per request/transaction (less common for plain classes):
# _onboarding_service_instance = None
# def get_onboarding_service(env):
# global _onboarding_service_instance
# if _onboarding_service_instance is None or _onboarding_service_instance.env != env:
# _onboarding_service_instance = onboarding_service.OnboardingService(env)
# return _onboarding_service_instance

# The simplest approach is direct instantiation by the caller:
# from odoo.addons.influence_gen_services.services.onboarding_service import OnboardingService
# onboarding_svc = OnboardingService(self.env)
# onboarding_svc.some_method()
# This __init__.py primarily ensures the service modules are partof the Python package.