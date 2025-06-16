# -*- coding: utf-8 -*-
import logging
from odoo import http, _, SUPERUSER_ID
from odoo.http import request
from odoo.exceptions import UserError, AccessError
from werkzeug.exceptions import Forbidden, NotFound

_logger = logging.getLogger(__name__)

class InfluenceGenPortalOnboarding(http.Controller):

    def _get_influencer_profile(self):
        user = request.env.user
        return user.influencer_profile_id if hasattr(user, 'influencer_profile_id') else False

    @http.route('/influencer/register', type='http', auth='public', website=True, sitemap=False)
    def influencer_register(self, **kw):
        """
        Influencer Registration page. Renders the registration form.
        """
        user = request.env.user
        # If user is logged in and already an influencer, redirect to dashboard
        if user.id != request.website.user_id.id and hasattr(user, 'influencer_profile_id') and user.influencer_profile_id:
            return request.redirect('/my/dashboard')

        qcontext = request.params.copy()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.process_registration(**kw) # Call process directly if POST and no explicit error
                 # If process_registration does not redirect on error, this might not be reached
            except UserError as e:
                qcontext['error'] = str(e)
            except Exception as e:
                _logger.error("Registration process error: %s", e)
                qcontext['error'] = _("An unexpected error occurred.")
        return request.render("influence_gen_portal.portal_registration_form", qcontext)

    @http.route('/influencer/register/process', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def process_registration(self, **post):
        """
        Handles POST request for influencer registration.
        """
        if post.get('password') != post.get('confirm_password'):
            return request.redirect("/influencer/register?error=" + _("Passwords do not match.") + "&login=" + post.get('login', ''))

        required_fields = ['name', 'login', 'password']
        missing_fields = [f for f in required_fields if not post.get(f)]
        if missing_fields:
            return request.redirect("/influencer/register?error=" + _("Please fill in all required fields: %s") % ", ".join(missing_fields) + "&login=" + post.get('login', ''))

        try:
            onboarding_service = request.env['influence_gen.onboarding.service'].sudo()
            new_user = onboarding_service.create_influencer_user_and_profile(post)
            request.session.authenticate(request.session.db, post.get('login'), post.get('password'))
            return request.redirect("/my/kyc/submit")
        except UserError as e:
            _logger.warning("Influencer registration failed UserError: %s", str(e))
            return request.redirect("/influencer/register?error=" + str(e) + "&login=" + post.get('login', ''))
        except Exception as e:
            _logger.error("Influencer registration failed: %s", e, exc_info=True)
            return request.redirect("/influencer/register?error=" + _("An unexpected error occurred during registration. Please try again or contact support.") + "&login=" + post.get('login', ''))

    @http.route('/my/kyc/submit', type='http', auth='user', website=True)
    def influencer_kyc_submission(self, **kw):
        """
        Influencer KYC Submission page. Allows users to upload KYC documents.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Not Found"), 'message': _("Your influencer profile could not be loaded.")})

        onboarding_service = request.env['influence_gen.onboarding.service'].sudo(influencer_profile.user_id.id)
        current_kyc_status = onboarding_service.get_influencer_kyc_status_simple(influencer_profile.id)

        if current_kyc_status in ['approved', 'pending_review', 'in_review']:
            return request.redirect("/my/kyc/status")

        values = {'influencer': influencer_profile, 'current_kyc_status': current_kyc_status, 'page_name': 'kyc'}
        values.update(kw)
        return request.render("influence_gen_portal.portal_kyc_submission_form", values)

    @http.route('/my/kyc/submit/process', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_kyc_documents(self, **post):
        """
        Handles POST request for KYC document submission.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            request.session['flash_message'] = {'type': 'danger', 'message': _("Your profile could not be found.")}
            return request.redirect("/my/kyc/submit")

        id_document_front = request.httprequest.files.get('id_document_front')
        id_document_back = request.httprequest.files.get('id_document_back')
        document_type = post.get('document_type')

        if not document_type or not id_document_front: # Back might be optional for some types
            request.session['flash_message'] = {'type': 'warning', 'message': _("Please provide document type and at least the front image.")}
            return request.redirect("/my/kyc/submit")

        try:
            onboarding_service = request.env['influence_gen.onboarding.service'].sudo(influencer_profile.user_id.id)
            onboarding_service.submit_influencer_kyc(influencer_profile.id, document_type, id_document_front, id_document_back)
            request.session['flash_message'] = {'type': 'success', 'message': _("KYC documents submitted successfully.")}
            return request.redirect("/my/kyc/status")
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error processing KYC for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred during KYC submission.")}
        return request.redirect("/my/kyc/submit")

    @http.route('/my/kyc/status', type='http', auth='user', website=True)
    def check_kyc_status(self, **kw):
        """
        Influencer KYC Status page. Displays the current status of KYC verification.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Not Found"), 'message': _("Your influencer profile could not be loaded.")})

        try:
            onboarding_service = request.env['influence_gen.onboarding.service'].sudo(influencer_profile.user_id.id)
            kyc_status_details = onboarding_service.get_influencer_kyc_status_details(influencer_profile.id)
        except Exception as e:
            _logger.error("Error fetching KYC status for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("KYC Status Load Error"), 'message': _("Could not load KYC status. Please try again later.")})

        return request.render("influence_gen_portal.portal_kyc_status_page", {
            'influencer': influencer_profile,
            'kyc_status_details': kyc_status_details,
            'page_name': 'kyc_status',
        })

    @http.route('/my/social/setup', type='http', auth='user', website=True)
    def influencer_social_media_setup(self, **kw):
        """
        Influencer Social Media Setup page. Allows users to add/manage social media profiles.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Not Found"), 'message': _("Your influencer profile could not be loaded.")})

        try:
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            social_profiles = business_service.get_influencer_social_profiles(influencer_profile.id)
        except Exception as e:
            _logger.error("Error fetching social profiles for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Social Media Load Error"), 'message': _("Could not load social media profiles. Please try again later.")})

        return request.render("influence_gen_portal.portal_social_media_form", {
            'influencer': influencer_profile,
            'social_profiles': social_profiles,
            'page_name': 'social_setup',
        })

    @http.route('/my/social/setup/process', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_social_media_links(self, **post):
        """
        Handles POST request for social media links submission.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            request.session['flash_message'] = {'type': 'danger', 'message': _("Your profile could not be found.")}
            return request.redirect("/my/social/setup")

        try:
            # Reconstruct social_media list from form data (e.g., social_media_platform_0, social_media_handle_0, etc.)
            social_media_data = []
            i = 0
            while True:
                platform = post.get(f'social_media[{i}][platform]')
                if platform is None: # No more entries
                    break
                social_media_data.append({
                    'id': post.get(f'social_media[{i}][id]'), # For existing profiles
                    'platform': platform,
                    'handle': post.get(f'social_media[{i}][handle]', ''),
                    'url': post.get(f'social_media[{i}][url]', ''),
                })
                i += 1
            
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            business_service.update_influencer_social_profiles(influencer_profile.id, social_media_data)
            request.session['flash_message'] = {'type': 'success', 'message': _("Social media profiles updated.")}
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error updating social media for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while updating social media profiles.")}
        return request.redirect("/my/profile#social")

    @http.route('/my/bank/setup', type='http', auth='user', website=True)
    def influencer_bank_account_setup(self, **kw):
        """
        Influencer Bank Account Setup page. Allows users to add/manage bank account details.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Not Found"), 'message': _("Your influencer profile could not be loaded.")})

        try:
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            bank_accounts = business_service.get_influencer_bank_accounts(influencer_profile.id)
        except Exception as e:
            _logger.error("Error fetching bank accounts for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Bank Account Load Error"), 'message': _("Could not load bank account details. Please try again later.")})

        return request.render("influence_gen_portal.portal_bank_account_form", {
            'influencer': influencer_profile,
            'bank_accounts': bank_accounts, # Expecting a list, form might handle one primary for simplicity
            'page_name': 'bank_setup',
        })

    @http.route('/my/bank/setup/process', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_bank_account_details(self, **post):
        """
        Handles POST request for bank account details submission.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            request.session['flash_message'] = {'type': 'danger', 'message': _("Your profile could not be found.")}
            return request.redirect("/my/bank/setup")

        try:
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            business_service.update_influencer_bank_account(influencer_profile.id, post)
            request.session['flash_message'] = {'type': 'success', 'message': _("Bank account details updated.")}
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error updating bank account for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while updating bank account details.")}
        return request.redirect("/my/payments") # Part of main profile/payments page

    @http.route('/my/tos/agree', type='http', auth='user', website=True)
    def influencer_tos_agreement(self, **kw):
        """
        Influencer ToS Agreement page. Displays current terms and allows agreement.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Not Found"), 'message': _("Your influencer profile could not be loaded.")})

        try:
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            terms_data = business_service.get_latest_terms_and_privacy_policy()
            consent_status = business_service.get_influencer_consent_status(influencer_profile.id, terms_data.get('tos_version'), terms_data.get('privacy_policy_version'))
        except Exception as e:
            _logger.error("Error fetching terms for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Terms Load Error"), 'message': _("Could not load terms and conditions. Please try again later.")})

        return request.render("influence_gen_portal.portal_tos_agreement_form", {
            'influencer': influencer_profile,
            'terms_data': terms_data,
            'consent_status': consent_status, # e.g. {'accepted_latest': True/False, 'history': [...]}
            'page_name': 'tos_agreement',
        })

    @http.route('/my/tos/agree/process', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_tos_agreement(self, **post):
        """
        Handles POST request for processing ToS agreement.
        """
        influencer_profile = self._get_influencer_profile()
        if not influencer_profile:
            request.session['flash_message'] = {'type': 'danger', 'message': _("Your profile could not be found.")}
            return request.redirect("/my/tos/agree")

        if not post.get('accept_terms'):
            request.session['flash_message'] = {'type': 'warning', 'message': _("You must accept the terms to continue.")}
            return request.redirect("/my/tos/agree")

        try:
            business_service = request.env['influence_gen.business.service'].sudo(influencer_profile.user_id.id)
            business_service.record_influencer_consent(influencer_profile.id, post.get('tos_version'), post.get('privacy_policy_version'))
            request.session['flash_message'] = {'type': 'success', 'message': _("Terms accepted successfully.")}
            # Check if all onboarding steps are complete
            if request.env['influence_gen.onboarding.service'].sudo(influencer_profile.user_id.id).is_onboarding_complete(influencer_profile.id):
                 return request.redirect("/my/dashboard")
            else:
                 # Redirect to the next pending onboarding step
                 next_step_url = request.env['influence_gen.onboarding.service'].sudo(influencer_profile.user_id.id).get_next_onboarding_step_url(influencer_profile.id)
                 return request.redirect(next_step_url or "/my/dashboard")

        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error recording consent for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while recording your consent.")}
        return request.redirect("/my/tos/agree")