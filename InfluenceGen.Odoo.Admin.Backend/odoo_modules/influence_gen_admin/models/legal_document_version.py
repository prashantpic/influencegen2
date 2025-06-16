from odoo import api, fields, models
from odoo.exceptions import ValidationError

class LegalDocumentVersion(models.Model):
    _name = 'influence_gen.legal_document_version'
    _description = "InfluenceGen Legal Document Version"
    _order = 'document_type, effective_date desc'

    document_type = fields.Selection(
        selection=[
            ('tos', 'Terms of Service'),
            ('privacy_policy', 'Privacy Policy')
        ],
        required=True,
        string='Document Type'
    )
    version = fields.Char(
        required=True,
        string='Version'
    )
    content = fields.Html(
        required=True,
        string='Content'
    )
    effective_date = fields.Date(
        required=True,
        string='Effective Date',
        default=fields.Date.today
    )
    is_active = fields.Boolean(
        string='Active',
        default=False,
        copy=False
    )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string="Document File"
    )

    @api.constrains('is_active', 'document_type')
    def _check_active_version_unicity(self):
        for record in self:
            if record.is_active:
                domain = [
                    ('id', '!=', record.id),
                    ('document_type', '=', record.document_type),
                    ('is_active', '=', True)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(f"Only one version of {record.display_name} for document type '{record.document_type}' can be active at a time.")