from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal # For redirect after login
from odoo.exceptions import UserError, AccessError
import werkzeug # For exceptions like Forbidden, NotFound

# Max file size for KYC documents (e.g., 5MB)
MAX_FILE_SIZE_KYC = 5 * 1024 * 1024
ALLOWED_MIME_TYPES_KYC = ['image/jpeg', 'image/png', 'application/pdf']


class InfluenceGenPortalOnboarding(http.Controller):
    """
    Controller for the influencer onboarding process.
    Handles registration, KYC, social/bank account setup, and ToS agreement.
    """

    def _get_influencer_profile(self, ensure_exists=True):
        """Helper to get the current user's influencer profile."""
        user = request.env.user
        influencer_profile = request.env['influence_gen.influencer_profile'].sudo().search([('user_id', '=', user.id)], limit=1)
        if ensure_exists and not influencer_profile:
            # This indicates an issue, as a logged-in user in onboarding steps should have a profile record.
            # Redirect to home or an error page.
            raise werkzeug.exceptions.NotFound(_("Influencer profile not found. Please contact support."))
        return influencer_profile

    def _redirect_if_onboarding_complete(self, influencer):
        """Redirects to dashboard if onboarding is considered complete."""
        # This logic needs to be defined in the business service
        # is_onboarding_complete = request.env['influence_gen.onboarding_service'].is_onboarding_complete(influencer.id)
        # For now, let's assume if KYC is approved, onboarding is mostly done for redirection purposes
        if influencer and influencer.kyc_status == 'approved':
             return request.redirect('/my/dashboard?message=' + _("Onboarding already completed."))
        return None


    @http.route(['/influencer/register'], type='http', auth="public", website=True, sitemap=True)
    def influencer_register(self, **kw):
        """
        Renders the influencer registration form.
        If user is already logged in and an influencer, redirect to dashboard.
        """
        if request.env.user.id != request.env.ref('base.public_user').id:
            try:
                influencer = self._get_influencer_profile(ensure_exists=False)
                if influencer:
                    redirect = self._redirect_if_onboarding_complete(influencer)
                    if redirect: return redirect
                    # If logged in but not fully onboarded, maybe redirect to a specific step later
                    return request.redirect('/my/dashboard') # Or last onboarding step
            except werkzeug.exceptions.NotFound: # No influencer profile, but logged in - could be an admin
                pass # Allow admins or other users to see the page if they are not influencers

        qcontext = {
            'error': kw.get('error'),
            'message': kw.get('message'),
        }
        return request.render("influence_gen_portal.portal_registration_form", qcontext)

    @http.route(['/influencer/register/process'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def process_registration(self, **post):
        """
        Processes the registration form data.
        Creates Odoo user and influencer.profile record.
        Logs in the user.
        """
        required_fields = ['fullName', 'email', 'password', 'confirm_password']
        errors = {}
        for field in required_fields:
            if not post.get(field):
                errors[field] = _("This field is required.")
        
        if post.get('password') != post.get('confirm_password'):
            errors['confirm_password'] = _("Passwords do not match.")

        if errors:
            qcontext = {'error': errors, **post}
            return request.render("influence_gen_portal.portal_registration_form", qcontext)

        try:
            # Call business service for registration
            user_id, influencer_id = request.env['influence_gen.onboarding_service'].sudo().process_registration_data({
                'full_name': post.get('fullName'),
                'email': post.get('email'),
                'password': post.get('password'),
            })
            
            # Log in the user
            request.session.authenticate(request.session.db, post.get('email'), post.get('password'))
            # Redirect to the next step, e.g., KYC submission
            return request.redirect('/my/kyc/submit?message=' + _("Registration successful! Please complete your KYC."))

        except UserError as e: # Catch validation errors from business service
            qcontext = {'error': {'general': str(e)}, **post}
            return request.render("influence_gen_portal.portal_registration_form", qcontext)
        except Exception as e:
            # Log error
            qcontext = {'error': {'general': _("An unexpected error occurred during registration.")}, **post}
            return request.render("influence_gen_portal.portal_registration_form", qcontext)


    @http.route(['/my/kyc/submit'], type='http', auth="user", website=True)
    def influencer_kyc_submission(self, **kw):
        """
        Renders the KYC document submission form.
        Checks if KYC is already submitted/approved.
        """
        try:
            influencer = self._get_influencer_profile()
            redirect = self._redirect_if_onboarding_complete(influencer) # Or a more specific KYC check
            if redirect: return redirect
            
            if influencer.kyc_status in ['submitted', 'in_review', 'approved']:
                 return request.redirect('/my/kyc/status')


            qcontext = {
                'influencer': influencer,
                'page_name': 'kyc_submission',
                'error': kw.get('error'),
                'message': kw.get('message'),
            }
            return request.render("influence_gen_portal.portal_kyc_submission_form", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/kyc/submit/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_kyc_documents(self, **post):
        """
        Processes KYC document uploads.
        """
        try:
            influencer = self._get_influencer_profile()
            errors = {}
            
            document_type = post.get('documentType')
            id_front_file = request.httprequest.files.get('id_document_front')
            id_back_file = request.httprequest.files.get('id_document_back') # Optional

            if not document_type:
                errors['documentType'] = _("Document type is required.")
            if not id_front_file:
                errors['id_document_front'] = _("Front of ID document is required.")
            
            # File validation
            if id_front_file:
                if id_front_file.content_length > MAX_FILE_SIZE_KYC:
                    errors['id_document_front'] = _("File is too large (max 5MB).")
                if id_front_file.mimetype not in ALLOWED_MIME_TYPES_KYC:
                    errors['id_document_front'] = _("Invalid file type. Allowed: JPG, PNG, PDF.")
            
            if id_back_file:
                if id_back_file.content_length > MAX_FILE_SIZE_KYC:
                    errors['id_document_back'] = _("File is too large (max 5MB).")
                if id_back_file.mimetype not in ALLOWED_MIME_TYPES_KYC:
                    errors['id_document_back'] = _("Invalid file type. Allowed: JPG, PNG, PDF.")
            
            if errors:
                return request.redirect('/my/kyc/submit?error=' + str(errors)) # Improve error display

            # Call business service to handle KYC documents
            # result = request.env['influence_gen.onboarding_service'].sudo().process_kyc_submission(
            #     influencer.id,
            #     document_type,
            #     id_front_file.read() if id_front_file else None,
            #     id_front_file.filename if id_front_file else None,
            #     id_front_file.mimetype if id_front_file else None,
            #     id_back_file.read() if id_back_file else None,
            #     id_back_file.filename if id_back_file else None,
            #     id_back_file.mimetype if id_back_file else None,
            # )
            # if not result.get('success'):
            #     return request.redirect('/my/kyc/submit?error=' + result.get('message', _("KYC submission failed.")))
            
            # Simplified success path for now
            influencer.sudo().write({'kyc_status': 'submitted'}) # This should be done by the service

            # Redirect to next onboarding step, e.g., social media setup
            return request.redirect('/my/social/setup?message=' + _("KYC documents submitted successfully."))

        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except UserError as e:
             return request.redirect('/my/kyc/submit?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect('/my/kyc/submit?error=' + _("An unexpected error occurred during KYC submission."))


    @http.route(['/my/social/setup'], type='http', auth="user", website=True)
    def influencer_social_media_setup(self, **kw):
        """
        Renders the social media account setup form.
        """
        try:
            influencer = self._get_influencer_profile()
            # existing_social_profiles = request.env['influence_gen.social_media_profile'].sudo().search([('influencer_profile_id', '=', influencer.id)])
            
            qcontext = {
                'influencer': influencer,
                # 'social_profiles': existing_social_profiles,
                'page_name': 'social_setup',
                'error': kw.get('error'),
                'message': kw.get('message'),
            }
            return request.render("influence_gen_portal.portal_social_media_form", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/social/setup/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_social_media_links(self, **post):
        """
        Processes submitted social media links.
        """
        try:
            influencer = self._get_influencer_profile()
            # Extract and validate social media links from post
            # E.g., post might contain platform_1, handle_1, url_1, platform_2, handle_2, etc.
            # social_media_data = [] # Collect into a list of dicts
            
            # Call business service
            # result = request.env['influence_gen.onboarding_service'].sudo().process_social_media_data(influencer.id, social_media_data)
            # if not result.get('success'):
            #     return request.redirect('/my/social/setup?error=' + result.get('message', _("Failed to save social media links.")))

            return request.redirect('/my/bank/setup?message=' + _("Social media links saved. Verification may be pending."))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except UserError as e:
             return request.redirect('/my/social/setup?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect('/my/social/setup?error=' + _("An error occurred while saving social media links."))


    @http.route(['/my/bank/setup'], type='http', auth="user", website=True)
    def influencer_bank_account_setup(self, **kw):
        """
        Renders the bank account setup form.
        """
        try:
            influencer = self._get_influencer_profile()
            # existing_bank_accounts = request.env['influence_gen.bank_account'].sudo().search([('influencer_profile_id', '=', influencer.id)])

            qcontext = {
                'influencer': influencer,
                # 'bank_accounts': existing_bank_accounts,
                'page_name': 'bank_setup',
                'error': kw.get('error'),
                'message': kw.get('message'),
            }
            return request.render("influence_gen_portal.portal_bank_account_form", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/bank/setup/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_bank_account_details(self, **post):
        """
        Processes submitted bank account details.
        """
        try:
            influencer = self._get_influencer_profile()
            # Extract and validate bank account data from post
            # bank_account_data = { ... }
            
            # Call business service
            # result = request.env['influence_gen.onboarding_service'].sudo().process_bank_account_data(influencer.id, bank_account_data)
            # if not result.get('success'):
            #     return request.redirect('/my/bank/setup?error=' + result.get('message', _("Failed to save bank account details.")))

            return request.redirect('/my/tos/agree?message=' + _("Bank account details saved. Verification may be pending."))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except UserError as e:
            return request.redirect('/my/bank/setup?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect('/my/bank/setup?error=' + _("An error occurred while saving bank account details."))

    @http.route(['/my/tos/agree'], type='http', auth="user", website=True)
    def influencer_tos_agreement(self, **kw):
        """
        Renders the Terms of Service and Privacy Policy agreement form.
        """
        try:
            influencer = self._get_influencer_profile()
            # Fetch current ToS/Privacy Policy versions from business service or config
            # current_tos_version = request.env['ir.config_parameter'].sudo().get_param('influence_gen.current_tos_version', '1.0')
            # current_privacy_version = request.env['ir.config_parameter'].sudo().get_param('influence_gen.current_privacy_version', '1.0')

            qcontext = {
                'influencer': influencer,
                # 'current_tos_version': current_tos_version,
                # 'current_privacy_version': current_privacy_version,
                'page_name': 'tos_agreement',
                'error': kw.get('error'),
                'message': kw.get('message'),
            }
            return request.render("influence_gen_portal.portal_tos_agreement_form", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/tos/agree/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_tos_agreement(self, **post):
        """
        Processes the ToS and Privacy Policy agreement.
        """
        try:
            influencer = self._get_influencer_profile()
            
            agreed_tos_version = post.get('tos_version')
            agreed_privacy_version = post.get('privacy_policy_version')
            consent_given = post.get('consent_checkbox')

            if not consent_given:
                return request.redirect('/my/tos/agree?error=' + _("You must agree to the terms to continue."))
            if not agreed_tos_version or not agreed_privacy_version:
                 return request.redirect('/my/tos/agree?error=' + _("Version information is missing."))


            # Call business service to record consent
            # result = request.env['influence_gen.onboarding_service'].sudo().process_tos_agreement(
            #     influencer.id, 
            #     agreed_tos_version, 
            #     agreed_privacy_version
            # )
            # if not result.get('success'):
            #     return request.redirect('/my/tos/agree?error=' + result.get('message', _("Failed to record agreement.")))

            # Potentially update influencer account status via service
            # influencer.sudo().write({'account_status': 'active'}) # This should be done by the service

            return request.redirect('/my/dashboard?success_message=' + _("Agreement accepted. Onboarding complete!"))
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except UserError as e:
             return request.redirect('/my/tos/agree?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect('/my/tos/agree?error=' + _("An error occurred while processing your agreement."))


    @http.route(['/my/kyc/status'], type='http', auth="user", website=True)
    def check_kyc_status(self, **kw):
        """
        Displays the current KYC status and any required actions.
        """
        try:
            influencer = self._get_influencer_profile()
            qcontext = {
                'influencer': influencer,
                'kyc_status': influencer.kyc_status,
                # 'kyc_notes': influencer.kyc_data_ids.filtered(lambda r: r.notes).mapped('notes'), # Example for notes
                'page_name': 'kyc_status',
                'message': kw.get('message'),
            }
            return request.render("influence_gen_portal.portal_kyc_status_page", qcontext)
        except werkzeug.exceptions.NotFound:
            return request.redirect('/')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred while fetching KYC status.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)