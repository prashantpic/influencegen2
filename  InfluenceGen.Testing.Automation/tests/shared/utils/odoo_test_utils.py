# This module is intended for utility functions that interact with an Odoo environment.
# These functions are most effective when tests are run within Odoo's test runner context
# (e.g., using odoo.tests.common.HttpCase or similar for integration tests),
# where the 'env' object is readily available.
#
# If testing Odoo externally (e.g., API tests not running inside Odoo),
# these utilities would need to be adapted to use an Odoo client library
# (like odoorpc, odoo-client-lib, or direct XML-RPC/JSON-RPC calls)
# to interact with the Odoo instance. The current implementation assumes
# an 'env' object (Odoo Environment) is passed, typical of internal Odoo tests.

# from odoo.exceptions import UserError, ValidationError # Example imports if needed

def create_test_influencer(env, name: str, email: str, **extra_profile_vals):
    """
    Creates or retrieves a test influencer (res.users and associated influence_gen.influencer_profile).
    This function assumes it's run within an Odoo test environment where 'env' is available.

    Args:
        env: Odoo Environment object.
        name (str): Full name of the influencer.
        email (str): Email for the influencer (used as login).
        **extra_profile_vals: Additional values for the influencer profile.

    Returns:
        odoo.model.browse_record: The influencer_profile record.
    """
    UserModel = env['res.users']
    ProfileModel = env['influence_gen.influencer_profile'] # Replace with actual model name from your Odoo module

    # Find or create the res.users record
    user = UserModel.search([('login', '=', email)], limit=1)
    if not user:
        portal_group_id = env.ref('base.group_portal').id
        user_vals = {
            'name': name,
            'login': email,
            'password': 'testpassword123',  # Default password for test users
            'groups_id': [(6, 0, [portal_group_id])], # Assign to portal group
            'company_id': env.company.id, # Ensure a company is set
            'company_ids': [(6, 0, [env.company.id])], # Ensure company_ids is set
        }
        user = UserModel.create(user_vals)
        env.cr.commit() # Commit to make user available for foreign key in profile if created in same transaction

    # Find or create the influence_gen.influencer_profile record
    profile = ProfileModel.search([('user_id', '=', user.id)], limit=1)
    if not profile:
        profile_vals = {
            'user_id': user.id,
            'full_name': name,
            'email': email, # Often email is on the profile too
        }
        profile_vals.update(extra_profile_vals)
        profile = ProfileModel.create(profile_vals)
        env.cr.commit() # Commit if creating profile in the same transaction
    
    return profile

def get_campaign_by_name(env, campaign_name: str):
    """
    Fetches a campaign by its name.
    This function assumes it's run within an Odoo test environment.

    Args:
        env: Odoo Environment object.
        campaign_name (str): The name of the campaign to find.

    Returns:
        odoo.model.browse_record or odoo.model.browse_null: The campaign record or empty recordset.
    """
    CampaignModel = env['influence_gen.campaign'] # Replace with actual campaign model name
    return CampaignModel.search([('name', '=', campaign_name)], limit=1)

def set_kyc_status_for_influencer(env, influencer_profile_id: int, new_status: str, reviewer_user_id: int = None):
    """
    Updates the KYC status for a given influencer profile.
    This function assumes it's run within an Odoo test environment.
    Note: The exact field names ('kyc_status', 'kyc_reviewer_id', etc.) and model
    structure for KYC might vary. Adjust as per your Odoo module's design.

    Args:
        env: Odoo Environment object.
        influencer_profile_id (int): The ID of the influence_gen.influencer_profile record.
        new_status (str): The new KYC status (e.g., 'approved', 'rejected').
        reviewer_user_id (int, optional): The ID of the res.users (admin) who reviewed.

    Returns:
        odoo.model.browse_record: The updated influencer_profile record.

    Raises:
        ValueError: If the influencer profile is not found.
    """
    ProfileModel = env['influence_gen.influencer_profile'] # Replace with actual model name
    profile = ProfileModel.browse(influencer_profile_id)

    if not profile.exists():
        raise ValueError(f"Influencer profile with ID {influencer_profile_id} not found.")

    write_vals = {}
    
    # This assumes KYC status is directly on the influencer_profile model.
    # If KYC data is on a separate model (e.g., 'influence_gen.kyc_data' linked via one2many or many2one):
    # kyc_record = env['influence_gen.kyc_data'].search([('influencer_profile_id', '=', influencer_profile_id)], limit=1, order='create_date desc')
    # if kyc_record:
    #     kyc_write_vals = {'verification_status': new_status}
    #     if reviewer_user_id:
    #         kyc_write_vals['reviewer_user_id'] = reviewer_user_id # Adjust field name
    #     kyc_record.write(kyc_write_vals)
    # else:
    #     # Or create one if the test context implies it should exist or handle error
    #     raise ValueError(f"No KYC record found for influencer profile ID {influencer_profile_id} to update status.")
    #
    # For this example, let's assume 'kyc_status' is a field on 'influence_gen.influencer_profile'
    
    # Check if 'kyc_status' field exists on the model
    if 'kyc_status' in ProfileModel._fields:
        write_vals['kyc_status'] = new_status
    else:
        # Log or handle missing field. For now, we'll assume it exists based on SDS.
        # This could also point to a related model that needs updating.
        # Example: profile.kyc_data_id.write({'status': new_status})
        pass # Placeholder for more complex KYC model interaction if kyc_status is not direct

    # Example: If there's a reviewer field on the profile model for KYC
    # if reviewer_user_id and 'kyc_reviewer_id' in ProfileModel._fields:
    #    write_vals['kyc_reviewer_id'] = reviewer_user_id

    if write_vals:
        profile.write(write_vals)
        env.cr.commit() # Commit changes if necessary within the test flow
    
    return profile

# Add more Odoo-specific helper functions as needed, for example:
# - create_test_campaign(env, name, **details)
# - create_content_submission(env, application_id, content_url, **details)
# - get_n8n_callback_payload(success=True, image_url=None, error_message=None)
# - etc.