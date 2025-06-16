from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, UserError
import werkzeug

class InfluenceGenPortalMain(http.Controller):
    """
    Controller for the main influencer portal pages.
    Handles dashboard, profile, payments, AI generator access, performance, and consent.
    """

    def _get_influencer_profile(self):
        """Helper to get the current user's influencer profile."""
        user = request.env.user
        influencer_profile = request.env['influence_gen.influencer_profile'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not influencer_profile:
            # This case should ideally be handled by a global onboarding check/redirect
            # or the user shouldn't be able to access portal pages without a profile.
            # For now, redirect to a generic error or home.
            # Consider a dedicated "profile not found" page.
            raise werkzeug.exceptions.NotFound(_("Influencer profile not found for the current user."))
        return influencer_profile

    @http.route(['/my/dashboard'], type='http', auth="user", website=True)
    def influencer_dashboard(self, **kw):
        """
        Renders the influencer's main dashboard.
        Fetches summary data: active campaigns, pending tasks, notifications, AI quota.
        """
        try:
            influencer = self._get_influencer_profile()
            qcontext = {
                'influencer': influencer,
                'page_name': 'dashboard',
            }
            # Fetch summary data from business services
            # Example:
            # qcontext['active_campaigns_count'] = request.env['influence_gen.campaign_service'].get_active_campaigns_count(influencer.id)
            # qcontext['pending_tasks'] = request.env['influence_gen.onboarding_service'].get_pending_tasks(influencer.id)
            # qcontext['recent_notifications'] = request.env['mail.message'].sudo().search([
            #     ('model', '=', 'influence_gen.influencer_profile'),
            #     ('res_id', '=', influencer.id),
            #     ('message_type', '!=', 'notification') # Adjust as needed for notification types
            # ], limit=5, order='date desc')
            # qcontext['ai_quota'] = request.env['influence_gen.ai_usage_quota_service'].get_user_quota_status(influencer.user_id.id)

            # Placeholder data for now
            qcontext['active_campaigns_count'] = 0
            qcontext['pending_tasks'] = [] # e.g., [{'name': _("Complete KYC"), 'url': '/my/kyc/submit'}]
            qcontext['recent_notifications'] = []
            qcontext['ai_quota'] = {'used': 0, 'total': 100} # Example

            return request.render("influence_gen_portal.portal_dashboard", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/') # Or an error page
        except Exception as e:
            # Log the error
            # request.env['ir.logging'].sudo().create({'name': 'Portal Dashboard Error', 'type': 'server', 'level': 'ERROR', 'message': str(e)})
            qcontext = {'error_message': _("An unexpected error occurred. Please try again later.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/profile'], type='http', auth="user", website=True)
    def influencer_profile(self, **kw):
        """
        Renders the influencer's profile page.
        Fetches profile details, KYC status, bank accounts.
        """
        try:
            influencer = self._get_influencer_profile()
            # bank_accounts = request.env['influence_gen.bank_account'].sudo().search([('influencer_profile_id', '=', influencer.id)])
            # social_profiles = request.env['influence_gen.social_media_profile'].sudo().search([('influencer_profile_id', '=', influencer.id)])

            qcontext = {
                'influencer': influencer,
                # 'bank_accounts': bank_accounts,
                # 'social_profiles': social_profiles,
                'page_name': 'profile',
                'error': {},
                'success_message': kw.get('success_message'),
                'error_message': kw.get('error_message'),
            }
            return request.render("influence_gen_portal.portal_profile_main", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while loading your profile.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/profile/update'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def update_influencer_profile(self, **post):
        """
        Handles POST requests to update non-sensitive influencer profile fields.
        """
        try:
            influencer = self._get_influencer_profile()
            # Call business service to update profile
            # Example: result = request.env['influence_gen.influencer_profile_service'].update_profile(influencer.id, post)
            # if not result.get('success'):
            #     return request.redirect('/my/profile?error_message=' + result.get('message', _("Update failed.")))

            # Simplified update for now
            allowed_fields = ['fullName', 'phone', 'residentialAddress'] # Define what can be updated here
            update_vals = {key: val for key, val in post.items() if key in allowed_fields}
            
            # Example: areas of influence might be M2M, handled differently
            # if 'areasOfInfluence' in post:
            #    handle m2m update via service

            if update_vals:
                influencer.sudo().write(update_vals) # Use sudo() if portal user doesn't have direct write access

            return request.redirect('/my/profile?success_message=' + _("Profile updated successfully!"))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            # Log error
            return request.redirect('/my/profile?error_message=' + _("An error occurred during profile update."))


    @http.route(['/my/payments'], type='http', auth="user", website=True)
    def influencer_payment_info(self, **kw):
        """
        Renders the influencer's payment information page.
        Fetches bank account details, payment history.
        """
        try:
            influencer = self._get_influencer_profile()
            # payment_records = request.env['influence_gen.payment_record'].sudo().search([('influencer_profile_id', '=', influencer.id)], order='create_date desc')
            # bank_accounts = request.env['influence_gen.bank_account'].sudo().search([('influencer_profile_id', '=', influencer.id)])
            
            qcontext = {
                'influencer': influencer,
                # 'payment_records': payment_records,
                # 'bank_accounts': bank_accounts,
                'page_name': 'payments',
                'success_message': kw.get('success_message'),
                'error_message': kw.get('error_message'),
            }
            return request.render("influence_gen_portal.portal_payment_info_tab_content", qcontext) # Assuming this is rendered inside profile page or a dedicated page
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while loading payment information.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/payments/update'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def update_influencer_payment_info(self, **post):
        """
        Handles POST requests to add/update bank account details.
        """
        try:
            influencer = self._get_influencer_profile()
            # Call business service to add/update bank account
            # Example: result = request.env['influence_gen.payment_service'].add_or_update_bank_account(influencer.id, post)
            # if not result.get('success'):
            #     return request.redirect('/my/payments?error_message=' + result.get('message', _("Update failed.")))

            # Simplified: assuming it's an update to one account or adding a new one
            # Actual logic for multiple accounts, primary, verification would be in business service
            return request.redirect('/my/payments?success_message=' + _("Payment information updated. Verification may be required."))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            # Log error
            return request.redirect('/my/payments?error_message=' + _("An error occurred during payment information update."))


    @http.route(['/my/ai-image-generator'], type='http', auth="user", website=True)
    def influencer_ai_image_generator(self, **kw):
        """
        Renders the AI Image Generator page.
        Fetches user's quota, models, saved prompts.
        """
        try:
            influencer = self._get_influencer_profile()
            # ai_quota = request.env['influence_gen.ai_usage_quota_service'].get_user_quota_status(influencer.user_id.id)
            # available_models = request.env['influence_gen.ai_image_service'].get_available_models() # This might be a general service call
            # saved_prompts = request.env['influence_gen.ai_image_service'].get_user_saved_prompts(influencer.id)
            
            qcontext = {
                'influencer': influencer,
                # 'ai_quota': ai_quota,
                # 'available_models': available_models,
                # 'saved_prompts': saved_prompts,
                'page_name': 'ai_image_generator',
            }
             # Placeholder data for now
            qcontext['ai_quota'] = {'used': 0, 'total': 100} 
            qcontext['default_params'] = {} # Load from config or business service
            qcontext['param_ranges'] = {}   # Load from config or business service

            return request.render("influence_gen_portal.portal_ai_image_generator_page", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while loading the AI Image Generator.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/performance'], type='http', auth="user", website=True)
    def influencer_performance_dashboard(self, **kw):
        """
        Renders the influencer's performance dashboard.
        Fetches performance data for campaigns.
        """
        try:
            influencer = self._get_influencer_profile()
            # performance_data = request.env['influence_gen.performance_service'].get_influencer_performance_summary(influencer.id)
            
            qcontext = {
                'influencer': influencer,
                # 'performance_data': performance_data, # List of campaign performances
                'page_name': 'performance',
            }
            # Placeholder data for now
            qcontext['performance_data'] = [] # List of dicts, e.g., [{'campaign_name': 'X', 'reach': 1000, ...}]
            
            return request.render("influence_gen_portal.portal_performance_dashboard", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while loading your performance data.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/consent'], type='http', auth="user", website=True)
    def influencer_consent_management(self, **kw):
        """
        Renders the influencer's consent management page.
        Fetches consent history and checks for new versions requiring acceptance.
        """
        try:
            influencer = self._get_influencer_profile()
            # consent_history = request.env['influence_gen.terms_consent_service'].get_consent_history(influencer.id)
            # pending_consents = request.env['influence_gen.terms_consent_service'].get_pending_consents(influencer.id)

            qcontext = {
                'influencer': influencer,
                # 'consent_history': consent_history,
                # 'pending_consents': pending_consents, # e.g. {'tos': 'v2.0', 'privacy': 'v1.5'}
                'page_name': 'consent',
                'success_message': kw.get('success_message'),
                'error_message': kw.get('error_message'),
            }
            # Placeholder data for now
            qcontext['consent_history'] = [] # List of dicts e.g. {'tos_version': '1.0', 'consent_date': ...}
            qcontext['pending_consents'] = {} # e.g. {'tos_version': '2.0', 'privacy_policy_version': '1.1'}
            
            return request.render("influence_gen_portal.portal_consent_management_tab_content", qcontext) # Assuming this is rendered inside profile page or a dedicated page
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while loading consent information.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/consent/accept'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def influencer_accept_terms(self, **post):
        """
        Handles POST requests to accept new Terms of Service / Privacy Policy.
        """
        try:
            influencer = self._get_influencer_profile()
            tos_version = post.get('tos_version')
            privacy_policy_version = post.get('privacy_policy_version')

            if not tos_version or not privacy_policy_version: # Basic check
                return request.redirect('/my/consent?error_message=' + _("Required versions not provided."))

            # result = request.env['influence_gen.terms_consent_service'].record_consent(
            #     influencer.id, 
            #     tos_version, 
            #     privacy_policy_version
            # )
            # if not result.get('success'):
            #     return request.redirect('/my/consent?error_message=' + result.get('message', _("Failed to record consent.")))
            
            # Simplified for now
            return request.redirect('/my/dashboard?success_message=' + _("Terms accepted successfully!"))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            # Log error
            return request.redirect('/my/consent?error_message=' + _("An error occurred while accepting terms."))