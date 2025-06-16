# -*- coding: utf-8 -*-
import logging
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import UserError, AccessError
from werkzeug.exceptions import Forbidden, NotFound

_logger = logging.getLogger(__name__)

class InfluenceGenPortalMain(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(InfluenceGenPortalMain, self)._prepare_portal_layout_values()
        user = request.env.user
        influencer_profile = user.influencer_profile_id if hasattr(user, 'influencer_profile_id') else False
        values['influencer_profile'] = influencer_profile
        values['page_name'] = values.get('page_name', 'home') # Default page_name
        return values

    def _get_influencer_profile_or_raise(self):
        user = request.env.user
        influencer_profile = user.influencer_profile_id if hasattr(user, 'influencer_profile_id') else False
        if not influencer_profile:
            raise Forbidden(_("Your influencer profile could not be loaded. Please contact support or complete onboarding."))
        return influencer_profile

    @http.route(['/my', '/my/dashboard'], type='http', auth='user', website=True)
    def influencer_dashboard(self, **kw):
        """
        Influencer Dashboard page.
        Fetches summary data for the logged-in influencer.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service'] # Main business service name
            dashboard_data = business_service.sudo(influencer_profile.user_id.id).get_influencer_dashboard_summary(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching dashboard data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Dashboard Load Error"), 'message': _("Could not load dashboard data. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'dashboard_data': dashboard_data,
            'page_name': 'dashboard',
        })
        return request.render("influence_gen_portal.portal_dashboard", values)

    @http.route(['/my/profile'], type='http', auth='user', website=True)
    def influencer_profile(self, **kw):
        """
        Influencer Profile page.
        Displays profile details, KYC status, social media, bank accounts.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            profile_details = business_service.sudo(influencer_profile.user_id.id).get_influencer_full_profile(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching profile data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Profile Load Error"), 'message': _("Could not load profile data. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'profile_details': profile_details,
            'page_name': 'profile',
        })
        return request.render("influence_gen_portal.portal_profile_main", values)

    @http.route(['/my/profile/update'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def update_influencer_profile(self, **post):
        """
        Handles POST request to update influencer profile details.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            business_service.sudo(influencer_profile.user_id.id).update_influencer_profile_details(influencer_profile.id, post)
            request.session['flash_message'] = {'type': 'success', 'message': _("Profile updated successfully.")}
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Forbidden as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error updating profile for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while updating your profile.")}
        return request.redirect("/my/profile")

    @http.route(['/my/payments'], type='http', auth='user', website=True)
    def influencer_payment_info(self, **kw):
        """
        Influencer Payments page.
        Displays bank account details, payment history.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            payment_data = business_service.sudo(influencer_profile.user_id.id).get_influencer_payment_data(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching payment data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Payment Info Load Error"), 'message': _("Could not load payment information. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'payment_data': payment_data,
            'page_name': 'payments',
        })
        return request.render("influence_gen_portal.portal_payment_info", values)

    @http.route(['/my/payments/update'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def update_influencer_payment_info(self, **post):
        """
        Handles POST request to update influencer payment details (bank accounts).
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            business_service.sudo(influencer_profile.user_id.id).update_influencer_bank_account(influencer_profile.id, post)
            request.session['flash_message'] = {'type': 'success', 'message': _("Payment information updated successfully.")}
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Forbidden as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error updating payment info for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while updating your payment information.")}
        return request.redirect("/my/payments")

    @http.route(['/my/ai-image-generator'], type='http', auth='user', website=True)
    def influencer_ai_image_generator(self, **kw):
        """
        AI Image Generator page.
        Displays the interface for generating images.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            ai_image_service = request.env['influence_gen.ai.image.service']
            ai_props = ai_image_service.sudo(influencer_profile.user_id.id).get_ai_image_generator_props(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching AI image generator data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("AI Tool Load Error"), 'message': _("Could not load AI image generator. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'ai_props': ai_props,
            'page_name': 'ai_image_generator',
        })
        return request.render("influence_gen_portal.portal_ai_image_generator_page", values)

    @http.route(['/my/performance'], type='http', auth='user', website=True)
    def influencer_performance_dashboard(self, **kw):
        """
        Influencer Performance Dashboard page.
        Displays performance metrics for completed campaigns.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            performance_data = business_service.sudo(influencer_profile.user_id.id).get_influencer_performance_data(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching performance data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Performance Load Error"), 'message': _("Could not load performance data. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'performance_data': performance_data,
            'page_name': 'performance',
        })
        return request.render("influence_gen_portal.portal_performance_dashboard", values)

    @http.route(['/my/consent'], type='http', auth='user', website=True)
    def influencer_consent_management(self, **kw):
        """
        Influencer Consent Management page.
        Displays consent history and allows accepting new terms.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            business_service = request.env['influence_gen.business.service']
            consent_data = business_service.sudo(influencer_profile.user_id.id).get_influencer_consent_data(influencer_profile.id)
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching consent data for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Consent Load Error"), 'message': _("Could not load consent information. Please try again later.")})

        values = self._prepare_portal_layout_values()
        values.update({
            'consent_data': consent_data,
            'page_name': 'consent',
        })
        return request.render("influence_gen_portal.portal_consent_management", values)

    @http.route(['/my/consent/accept'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def influencer_accept_terms(self, **post):
        """
        Handles POST request to record influencer's consent to terms/policy.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            if not post.get('accept_terms'):
                request.session['flash_message'] = {'type': 'warning', 'message': _("You must accept the terms to continue.")}
                return request.redirect("/my/consent")

            business_service = request.env['influence_gen.business.service']
            business_service.sudo(influencer_profile.user_id.id).record_influencer_consent(
                influencer_profile.id,
                post.get('tos_version'),
                post.get('privacy_policy_version')
            )
            request.session['flash_message'] = {'type': 'success', 'message': _("Terms accepted successfully.")}
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Forbidden as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
        except Exception as e:
            _logger.error("Error recording consent for user %s: %s", request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while recording your consent.")}

        redirect_url = post.get('redirect', '/my/dashboard')
        return request.redirect(redirect_url)