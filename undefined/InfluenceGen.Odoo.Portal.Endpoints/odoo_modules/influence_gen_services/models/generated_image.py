# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class GeneratedImage(models.Model):
    _name = 'influence_gen.generated_image'
    _description = 'AI Generated Image Metadata'
    _inherit = ['influence_gen.base_audit_mixin']
    _order = 'create_date desc, id desc'

    request_id = fields.Many2one(
        'influence_gen.ai_image_generation_request', string='Generation Request',
        required=True, ondelete='cascade', index=True, tracking=True) # REQ-AIGS-006

    image_attachment_id = fields.Many2one(
        'ir.attachment', string='Image Attachment',
        ondelete='restrict', help="Reference to the ir.attachment record storing the image file.", tracking=True)
    storage_url = fields.Char(
        string='External Storage URL',
        help="URL if the image is stored externally (e.g., S3).", tracking=True)

    file_format = fields.Char(string='File Format', help="e.g., PNG, JPEG.", tracking=True)
    file_size = fields.Integer(string='File Size (Bytes)', help="Size of the image file in bytes.", tracking=True)
    width = fields.Integer(string='Width (px)', help="Image width in pixels.", tracking=True)
    height = fields.Integer(string='Height (px)', help="Image height in pixels.", tracking=True)

    hash_value = fields.Char(
        string='Image Hash (SHA-256)', index=True,
        help="SHA-256 hash of the image file for integrity and deduplication.", tracking=True) # REQ-AIGS-010

    retention_category = fields.Selection([
        ('personal_generation', 'Personal Generation'),
        ('campaign_asset_standard', 'Campaign Asset - Standard Rights'),
        ('campaign_asset_extended', 'Campaign Asset - Extended Rights'),
        ('system_temp', 'System Temporary'),
        ('marked_for_deletion', 'Marked for Deletion'),
    ], string='Retention Category', required=True, default='personal_generation', tracking=True, index=True,
       help="Category determining the data retention policy for this image.") # REQ-AIGS-011, REQ-DMG-020

    usage_rights = fields.Text(
        string='Usage Rights',
        help="Specific usage rights applicable to this image, derived from campaign or platform policy.", tracking=True)

    is_campaign_asset = fields.Boolean(
        string='Is Campaign Asset', compute='_compute_is_campaign_asset', store=True,
        help="Indicates if this image is intended as an asset for a campaign.", tracking=True)

    legal_hold_status = fields.Boolean(
        string='Legal Hold Active', default=False, tracking=True,
        help="Indicates if this image is under a legal hold, preventing automated deletion/archival.") # REQ-DMG-020

    # REQ-DMG-008: Generated Image Metadata Storage

    @api.depends('request_id.campaign_id', 'request_id.intended_use')
    def _compute_is_campaign_asset(self):
        for record in self:
            record.is_campaign_asset = bool(record.request_id.campaign_id) or \
                                       record.request_id.intended_use == 'campaign'


    def name_get(self):
        """Custom display name for generated images."""
        result = []
        for img in self:
            name = _("Image for Request %s") % (img.request_id.name or img.request_id.id)
            if img.file_format:
                name += f" ({img.file_format})"
            result.append((img.id, name))
        return result

    def action_mark_for_deletion(self):
        """Marks the image for deletion according to retention policies."""
        # REQ-AIGS-011: This could be part of a broader retention service action.
        # This method is a placeholder for a more complex deletion/anonymization process
        # which should be handled by RetentionAndLegalHoldService.
        self.ensure_one()
        _logger.info(f"Marking image ID {self.id} (request ID {self.request_id.id}) for deletion.")
        self.write({'retention_category': 'marked_for_deletion'})
        self.message_post(body=_("Image marked for deletion."))
        # The actual deletion would be handled by a cron job running RetentionAndLegalHoldService
        return True

    def action_view_image(self):
        """Action to view the image attachment or URL."""
        self.ensure_one()
        if self.image_attachment_id:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self.image_attachment_id.id}?download=true',
                'target': 'self',
            }
        elif self.storage_url:
            return {
                'type': 'ir.actions.act_url',
                'url': self.storage_url,
                'target': 'new',
            }
        else:
            raise models.UserError(_("No image attachment or URL found for this record."))