# -*- coding: utf-8 -*-
import logging
from odoo import http, _, SUPERUSER_ID
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import UserError, AccessError
from werkzeug.exceptions import Forbidden, NotFound

_logger = logging.getLogger(__name__)

class InfluenceGenPortalCampaign(http.Controller):

    _items_per_page = 10

    def _get_influencer_profile_or_raise(self):
        user = request.env.user
        influencer_profile = user.influencer_profile_id if hasattr(user, 'influencer_profile_id') else False
        if not influencer_profile:
            raise Forbidden(_("Your influencer profile could not be loaded. Please complete onboarding or contact support."))
        # Add additional checks, e.g., KYC approved for campaign participation
        if influencer_profile.kyc_status != 'approved':
             raise Forbidden(_("Your KYC must be approved to participate in campaigns."))
        return influencer_profile

    @http.route(['/my/campaigns', '/my/campaigns/page/<int:page>'], type='http', auth='user', website=True)
    def campaign_discovery(self, page=1, search=None, sort_by=None, **kw):
        """
        Campaign Discovery page. Lists campaigns available for the influencer.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            campaign_service = request.env['influence_gen.campaign.service'] # Specific campaign service

            domain_params = {
                'search': search,
                'sort_by': sort_by,
                'filters': kw # Pass all other query params as potential filters
            }
            
            campaign_count = campaign_service.sudo(influencer_profile.user_id.id).get_discoverable_campaign_count(influencer_profile.id, domain_params)
            
            pager = portal_pager(
                url="/my/campaigns",
                url_args={'search': search, 'sort_by': sort_by, **kw},
                total=campaign_count,
                page=page,
                step=self._items_per_page
            )

            campaigns = campaign_service.sudo(influencer_profile.user_id.id).get_discoverable_campaigns(
                influencer_profile.id,
                domain_params=domain_params,
                limit=self._items_per_page,
                offset=pager['offset']
            )
            # filter_options = campaign_service.get_campaign_filter_options() # For template
        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except Exception as e:
            _logger.error("Error fetching campaigns for user %s: %s", request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Campaigns Load Error"), 'message': _("Could not load campaign list. Please try again later.")})

        return request.render("influence_gen_portal.portal_campaign_discovery_list", {
            'campaigns': campaigns,
            'pager': pager,
            'search': search,
            'sort_by': sort_by,
            'filter_args': kw,
            # 'filter_options': filter_options,
            'page_name': 'campaigns',
            'influencer_profile': influencer_profile,
        })

    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign>'], type='http', auth='user', website=True)
    def campaign_details(self, campaign, **kw):
        """
        Campaign Details page. Displays detailed information about a specific campaign.
        Using Odoo's model converter for campaign_id.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            campaign_service = request.env['influence_gen.campaign.service']
            
            # Ensure campaign exists and is accessible
            if not campaign.exists():
                raise NotFound()

            campaign_detail_data = campaign_service.sudo(influencer_profile.user_id.id).get_campaign_details_for_influencer(campaign.id, influencer_profile.id)
            if not campaign_detail_data: # Service returns None if not accessible or found
                 raise NotFound() # Or AccessError depending on service logic

            influencer_can_apply = campaign_service.sudo(influencer_profile.user_id.id).can_influencer_apply_to_campaign(campaign.id, influencer_profile.id)

        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except NotFound:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Campaign Not Found"), 'message': _("The requested campaign could not be found.")})
        except Exception as e:
            _logger.error("Error fetching campaign details (ID %s) for user %s: %s", campaign.id, request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Campaign Details Load Error"), 'message': _("Could not load campaign details. Please try again later.")})

        return request.render("influence_gen_portal.portal_campaign_detail_page", {
            'campaign': campaign_detail_data, # This is the rich data object from the service
            'influencer_can_apply': influencer_can_apply,
            'page_name': 'campaign_details',
            'influencer_profile': influencer_profile,
        })

    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign>/apply'], type='http', auth='user', website=True, methods=['GET'])
    def campaign_apply_form(self, campaign, **kw):
        """
        Campaign Application page. Renders the form to apply for a campaign.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            campaign_service = request.env['influence_gen.campaign.service']

            if not campaign.exists():
                raise NotFound()

            if not campaign_service.sudo(influencer_profile.user_id.id).can_influencer_apply_to_campaign(campaign.id, influencer_profile.id):
                request.session['flash_message'] = {'type': 'warning', 'message': _("You are not currently eligible or have already applied for this campaign.")}
                return request.redirect(f"/my/campaigns/{campaign.id}")
            
            # Fetch campaign details again for the form context if needed, or rely on the 'campaign' object
            campaign_data_for_form = campaign_service.sudo(influencer_profile.user_id.id).get_campaign_details_for_application_form(campaign.id)

        except Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': str(e)})
        except NotFound:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Campaign Not Found"), 'message': _("The requested campaign could not be found.")})
        except Exception as e:
            _logger.error("Error preparing campaign application (ID %s) for user %s: %s", campaign.id, request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Application Load Error"), 'message': _("Could not load campaign application form. Please try again later.")})

        return request.render("influence_gen_portal.portal_campaign_application_form", {
            'campaign': campaign_data_for_form,
            'page_name': 'campaign_application',
            'influencer_profile': influencer_profile,
        })

    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign>/apply/process'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_campaign_application(self, campaign, **post):
        """
        Handles POST request for campaign application submission.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            campaign_service = request.env['influence_gen.campaign.service']

            if not campaign.exists():
                raise UserError(_("Campaign not found."))

            campaign_service.sudo(influencer_profile.user_id.id).process_campaign_application(campaign.id, influencer_profile.id, post)
            request.session['flash_message'] = {'type': 'success', 'message': _("Campaign application submitted successfully.")}
            return request.redirect("/my/dashboard") # Or to a specific "my applications" page
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
            return request.redirect(f"/my/campaigns/{campaign.id}/apply")
        except Forbidden as e: # Handle Forbidden from _get_influencer_profile_or_raise
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
            return request.redirect("/my/campaigns")
        except Exception as e:
            _logger.error("Error processing campaign application (ID %s) for user %s: %s", campaign.id, request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred while submitting your application.")}
            return request.redirect(f"/my/campaigns/{campaign.id}/apply")

    @http.route(['/my/campaigns/submit/<model("influence_gen.campaign_application"):application>'], type='http', auth='user', website=True, methods=['GET'])
    def campaign_content_submission_form(self, application, **kw):
        """
        Campaign Content Submission page. Renders the form to submit content.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            content_submission_service = request.env['influence_gen.content.submission.service'] # Specific service

            if not application.exists() or application.influencer_profile_id != influencer_profile:
                raise Forbidden()

            if not content_submission_service.sudo(influencer_profile.user_id.id).can_submit_content(application.id):
                request.session['flash_message'] = {'type': 'warning', 'message': _("Content submission is not currently open for this application.")}
                return request.redirect(f"/my/campaigns/{application.campaign_id.id}") # Redirect to campaign details

            submission_form_data = content_submission_service.sudo(influencer_profile.user_id.id).get_content_submission_form_data(application.id)

        except Forbidden:
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Access Denied"), 'message': _("You do not have permission to access this submission page.")})
        except Exception as e:
            _logger.error("Error fetching submission data for application %s (user %s): %s", application.id, request.env.user.login, e)
            return request.render("influence_gen_portal.portal_error_page", {'title': _("Submission Load Error"), 'message': _("Could not load content submission form. Please try again later.")})

        return request.render("influence_gen_portal.portal_content_submission_page", {
            'application': application,
            'campaign': application.campaign_id,
            'submission_form_data': submission_form_data, # Eligible AI images, previous submissions, etc.
            'page_name': 'content_submission',
            'influencer_profile': influencer_profile,
        })

    @http.route(['/my/campaigns/submit/<model("influence_gen.campaign_application"):application>/process'], type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def process_content_submission(self, application, **post):
        """
        Handles POST request for content submission.
        """
        try:
            influencer_profile = self._get_influencer_profile_or_raise()
            content_submission_service = request.env['influence_gen.content.submission.service']

            if not application.exists() or application.influencer_profile_id != influencer_profile:
                raise UserError(_("Invalid application."))
            
            uploaded_files = request.httprequest.files.getlist('content_files')
            
            # Prepare data including post and files for the service
            submission_data_payload = {
                'text_caption': post.get('text_caption'),
                'post_url': post.get('post_url'),
                'selected_ai_image_ids': request.httprequest.form.getlist('selected_ai_image_ids'), # From checkboxes
                # Add any other form fields from 'post'
            }

            content_submission_service.sudo(influencer_profile.user_id.id).process_content_submission(application.id, submission_data_payload, uploaded_files)
            request.session['flash_message'] = {'type': 'success', 'message': _("Content submitted successfully for review.")}
            return request.redirect(f"/my/campaigns/{application.campaign_id.id}") # Or to application status
        except UserError as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
            return request.redirect(f"/my/campaigns/submit/{application.id}")
        except Forbidden as e:
            request.session['flash_message'] = {'type': 'danger', 'message': str(e)}
            return request.redirect("/my/campaigns")
        except Exception as e:
            _logger.error("Error processing content submission for application %s (user %s): %s", application.id, request.env.user.login, e)
            request.session['flash_message'] = {'type': 'danger', 'message': _("An error occurred during content submission.")}
            return request.redirect(f"/my/campaigns/submit/{application.id}")