from odoo import api, fields, models
from odoo.exceptions import ValidationError

class LegalDocumentVersion(models.Model):
    _name = 'influence_gen.legal_document_version'
    _description = 'InfluenceGen Legal Document Version'
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
        string="Document File",
        # Store as binary in db for simplicity unless large files are expected
        # attachment=True #This is for fields.Binary not Many2one
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
                    doc_type_label = dict(self._fields['document_type'].selection).get(record.document_type)
                    raise ValidationError(f"Only one version of {doc_type_label} can be active at a time.")