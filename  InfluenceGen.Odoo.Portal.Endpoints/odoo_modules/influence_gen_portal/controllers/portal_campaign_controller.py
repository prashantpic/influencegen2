from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError, UserError
import werkzeug

# Max file size for content submissions (e.g., 50MB)
MAX_FILE_SIZE_CONTENT = 50 * 1024 * 1024
ALLOWED_MIME_TYPES_CONTENT = ['image/jpeg', 'image/png', 'image/gif', 'video/mp4', 'video/quicktime']


class InfluenceGenPortalCampaign(http.Controller):
    """
    Controller for influencer campaign interactions: discovery, details, application, content submission.
    """

    def _get_influencer_profile(self):
        """Helper to get the current user's influencer profile."""
        user = request.env.user
        influencer_profile = request.env['influence_gen.influencer_profile'].sudo().search([('user_id', '=', user.id)], limit=1)
        if not influencer_profile:
            raise werkzeug.exceptions.Forbidden(_("Access denied. Influencer profile not found."))
        if influencer_profile.kyc_status != 'approved' or influencer_profile.account_status != 'active':
            # Or redirect to a page explaining why access is limited
            raise werkzeug.exceptions.Forbidden(_("Access to campaigns requires a verified and active profile."))
        return influencer_profile


    @http.route(['/my/campaigns', '/my/campaigns/page/<int:page>'], type='http', auth="user", website=True)
    def campaign_discovery(self, page=1, search=None, sort_by=None, **kw):
        """
        Renders the campaign discovery page with listing, search, sort, and filters.
        """
        try:
            influencer = self._get_influencer_profile()
            
            # Prepare search domain and filters based on `search`, `sort_by`, `kw`
            # For example, filters = {'niche': kw.get('niche'), 'compensation_type': kw.get('compensation_type')}
            # campaigns, total_campaigns = request.env['influence_gen.campaign_service'].sudo().get_discoverable_campaigns(
            #     influencer_id=influencer.id,
            #     page=page,
            #     search_term=search,
            #     sort_order=sort_by,
            #     filters=kw # Pass all other kw as potential filters
            # )
            
            # Placeholder data
            campaigns = request.env['influence_gen.campaign'].sudo().search([('status','=','published')], limit=10) # Simplified
            total_campaigns = len(campaigns)

            # Pagination
            pager_url = "/my/campaigns"
            if search: pager_url += f"?search={search}" # Add other params
            
            pager = portal_pager(
                url=pager_url,
                total=total_campaigns,
                page=page,
                step=10 # Number of campaigns per page
            )

            qcontext = {
                'influencer': influencer,
                'campaigns': campaigns,
                'pager': pager,
                'search': search,
                'sort_by': sort_by,
                'page_name': 'campaign_discovery',
                # 'available_filters': request.env['influence_gen.campaign_service'].get_filter_options() # For dropdowns
            }
            return request.render("influence_gen_portal.portal_campaign_discovery_list", qcontext)
        except werkzeug.exceptions.Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'error_message': str(e)})
        except Exception as e:
            # Log error
            qcontext = {'error_message': _("An unexpected error occurred while loading campaigns.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign_id>'], type='http', auth="user", website=True)
    def campaign_details(self, campaign_id, **kw):
        """
        Renders the detailed view of a specific campaign.
        Checks if the influencer can apply.
        """
        try:
            influencer = self._get_influencer_profile()
            
            if not campaign_id.sudo().exists(): # Ensure campaign exists and is accessible
                raise werkzeug.exceptions.NotFound()

            # can_apply = request.env['influence_gen.campaign_service'].sudo().can_influencer_apply(influencer.id, campaign_id.id)
            can_apply = True # Placeholder

            qcontext = {
                'influencer': influencer,
                'campaign': campaign_id.sudo(), # Sudo if portal user might not have direct read
                'can_apply': can_apply,
                'page_name': 'campaign_details',
                'success_message': kw.get('success_message'),
                'error_message': kw.get('error_message'),
            }
            return request.render("influence_gen_portal.portal_campaign_detail_page", qcontext)
        except werkzeug.exceptions.Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'error_message': str(e)})
        except werkzeug.exceptions.NotFound:
            return request.redirect('/my/campaigns')
        except Exception as e:
            # Log error
            qcontext = {'error_message': _("An unexpected error occurred while loading campaign details.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)

    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign_id>/apply'], type='http', auth="user", website=True)
    def campaign_apply(self, campaign_id, **kw):
        """
        Renders the campaign application form.
        """
        try:
            influencer = self._get_influencer_profile()
            if not campaign_id.sudo().exists():
                raise werkzeug.exceptions.NotFound()

            # Check eligibility again before rendering form
            # if not request.env['influence_gen.campaign_service'].sudo().can_influencer_apply(influencer.id, campaign_id.id):
            #     return request.redirect(f'/my/campaigns/{campaign_id.id}?error_message=' + _("You are not eligible or have already applied."))

            qcontext = {
                'influencer': influencer,
                'campaign': campaign_id.sudo(),
                'page_name': 'campaign_apply',
                'error': kw.get('error')
            }
            return request.render("influence_gen_portal.portal_campaign_application_form", qcontext)
        except werkzeug.exceptions.Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'error_message': str(e)})
        except werkzeug.exceptions.NotFound:
            return request.redirect('/my/campaigns')
        except Exception as e:
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/campaigns/<model("influence_gen.campaign"):campaign_id>/apply/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_campaign_application(self, campaign_id, **post):
        """
        Processes the campaign application submission.
        """
        try:
            influencer = self._get_influencer_profile()
            if not campaign_id.sudo().exists():
                raise werkzeug.exceptions.NotFound()

            proposal = post.get('proposal', '')
            agreed_to_terms = post.get('agree_terms_checkbox')

            if not agreed_to_terms:
                return request.redirect(f'/my/campaigns/{campaign_id.id}/apply?error=' + _("You must agree to the campaign requirements."))

            # Call business service to create application
            # application_result = request.env['influence_gen.campaign_service'].sudo().create_campaign_application(
            #     influencer_id=influencer.id,
            #     campaign_id=campaign_id.id,
            #     proposal=proposal,
            #     # pass other application fields from post
            # )
            # if not application_result.get('success'):
            #     return request.redirect(f'/my/campaigns/{campaign_id.id}/apply?error=' + application_result.get('message', _("Application failed.")))
            
            # application_id = application_result.get('application_id')
            
            # Placeholder
            application_id = request.env['influence_gen.campaign_application'].sudo().create({
                'campaign_id': campaign_id.id,
                'influencer_profile_id': influencer.id,
                'proposal': proposal,
                'status': 'submitted',
            })


            # Redirect to application status page or campaign discovery with success
            return request.redirect(f'/my/campaigns?success_message=' + _("Successfully applied to campaign: ") + campaign_id.name)
        except werkzeug.exceptions.Forbidden as e:
            # Should be caught by _get_influencer_profile, but good practice
            return request.render("influence_gen_portal.portal_error_page", {'error_message': str(e)})
        except werkzeug.exceptions.NotFound:
            return request.redirect('/my/campaigns')
        except UserError as e: # Catch validation errors from business service
            return request.redirect(f'/my/campaigns/{campaign_id.id}/apply?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect(f'/my/campaigns/{campaign_id.id}/apply?error=' + _("An unexpected error occurred during application."))


    @http.route(['/my/campaigns/submit/<model("influence_gen.campaign_application"):campaign_application_id>'], type='http', auth="user", website=True)
    def campaign_content_submission_form(self, campaign_application_id, **kw):
        """
        Renders the content submission form for an active campaign application.
        """
        try:
            influencer = self._get_influencer_profile()
            
            # Security check: ensure campaign_application_id belongs to the current influencer
            if campaign_application_id.sudo().influencer_profile_id.id != influencer.id:
                raise werkzeug.exceptions.Forbidden(_("You do not have permission to access this submission form."))
            
            # Check if submission is allowed (e.g., application approved, not past deadline)
            # if not request.env['influence_gen.content_submission_service'].sudo().can_submit_content(campaign_application_id.id):
            #    return request.redirect(f'/my/campaigns/{campaign_application_id.campaign_id.id}?error_message=' + _("Content submission is not currently open for this campaign."))

            # Fetch eligible AI images for this campaign/influencer
            # eligible_ai_images = request.env['influence_gen.ai_image_service'].sudo().get_eligible_images_for_submission(influencer.id, campaign_application_id.campaign_id.id)
            eligible_ai_images = [] # Placeholder

            qcontext = {
                'influencer': influencer,
                'application': campaign_application_id.sudo(),
                'campaign': campaign_application_id.sudo().campaign_id,
                'eligible_ai_images': eligible_ai_images,
                'page_name': 'content_submission',
                'error': kw.get('error'),
                'success_message': kw.get('success_message'),
            }
            return request.render("influence_gen_portal.portal_content_submission_page", qcontext)
        except werkzeug.exceptions.Forbidden as e:
            return request.render("influence_gen_portal.portal_error_page", {'error_message': str(e)})
        except werkzeug.exceptions.NotFound: # If application_id is invalid
            return request.redirect('/my/campaigns')
        except Exception as e:
            # Log error
            qcontext = {'error_message': _("An unexpected error occurred.")}
            return request.render("influence_gen_portal.portal_error_page", qcontext)


    @http.route(['/my/campaigns/submit/<model("influence_gen.campaign_application"):campaign_application_id>/process'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def process_content_submission(self, campaign_application_id, **post):
        """
        Processes content submission: file uploads, links, AI image selections.
        """
        try:
            influencer = self._get_influencer_profile()

            if campaign_application_id.sudo().influencer_profile_id.id != influencer.id:
                raise werkzeug.exceptions.Forbidden()

            errors = {}
            submitted_content_file = request.httprequest.files.get('content_file')
            submitted_content_link = post.get('content_link')
            selected_ai_image_id = post.get('selected_ai_image_id') # If using a select for AI images
            caption = post.get('caption', '')

            if not (submitted_content_file or submitted_content_link or selected_ai_image_id):
                errors['general'] = _("You must submit a file, a link, or select an AI generated image.")

            if submitted_content_file:
                if submitted_content_file.content_length > MAX_FILE_SIZE_CONTENT:
                    errors['content_file'] = _("File is too large (max 50MB).")
                if submitted_content_file.mimetype not in ALLOWED_MIME_TYPES_CONTENT:
                    errors['content_file'] = _("Invalid file type.")

            if errors:
                error_str = "; ".join([f"{k}: {v}" for k,v in errors.items()])
                return request.redirect(f'/my/campaigns/submit/{campaign_application_id.id}?error=' + error_str)

            # Call business service to create content submission record
            # submission_data = {
            #     'caption': caption,
            #     'link': submitted_content_link,
            #     'ai_image_id': selected_ai_image_id,
            # }
            # result = request.env['influence_gen.content_submission_service'].sudo().create_content_submission(
            #     application_id=campaign_application_id.id,
            #     submission_data=submission_data,
            #     uploaded_file_data=submitted_content_file.read() if submitted_content_file else None,
            #     uploaded_file_name=submitted_content_file.filename if submitted_content_file else None,
            #     uploaded_file_mimetype=submitted_content_file.mimetype if submitted_content_file else None,
            # )
            # if not result.get('success'):
            #     return request.redirect(f'/my/campaigns/submit/{campaign_application_id.id}?error=' + result.get('message', _("Content submission failed.")))

            # Placeholder
            vals = {
                'campaign_application_id': campaign_application_id.id,
                'content_url': submitted_content_link or 'file_placeholder', # Service would handle actual storage
                'review_status': 'pending',
                'feedback': caption, # Using feedback as caption for simplicity here
            }
            if selected_ai_image_id:
                vals['generated_image_id'] = int(selected_ai_image_id) # Ensure it's int if from form

            request.env['influence_gen.content_submission'].sudo().create(vals)

            return request.redirect(f'/my/campaigns/{campaign_application_id.campaign_id.id}?success_message=' + _("Content submitted successfully!"))
        except werkzeug.exceptions.Forbidden:
            return request.render("influence_gen_portal.portal_error_page", {'error_message': _("Access Denied.")})
        except werkzeug.exceptions.NotFound:
            return request.redirect('/my/campaigns')
        except UserError as e: # Catch validation errors from business service
            return request.redirect(f'/my/campaigns/submit/{campaign_application_id.id}?error=' + str(e))
        except Exception as e:
            # Log error
            return request.redirect(f'/my/campaigns/submit/{campaign_application_id.id}?error=' + _("An unexpected error occurred during content submission."))