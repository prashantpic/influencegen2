from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)

class LegalHold(models.Model):
    _name = 'influence_gen.legal_hold'
    _description = "InfluenceGen Legal Hold"

    name = fields.Char(
        required=True,
        string='Hold Name/Case ID',
        index=True
    )
    description = fields.Text(
        string='Reason for Hold',
        required=True
    )
    status = fields.Selection(
        selection=[
            ('active', 'Active'),
            ('lifted', 'Lifted')
        ],
        required=True,
        default='active',
        string='Status',
        index=True
    )
    target_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Target Model',
        help="The model containing the data to be held."
    )
    target_record_id = fields.Reference(
        selection=lambda self: [(model.model, model.name) for model in self.env['ir.model'].search([])],
        string="Target Record",
        help="Specific record to be held. Use if holding a single record."
    )
    target_influencer_id = fields.Many2one(
        comodel_name='influence_gen.influencer_profile', # Assuming this model exists in influence_gen_services
        string='Target Influencer',
        help="If holding all data related to a specific influencer."
    )
    target_campaign_id = fields.Many2one(
        comodel_name='influence_gen.campaign', # Assuming this model exists in influence_gen_services
        string='Target Campaign',
        help="If holding all data related to a specific campaign."
    )
    effective_date = fields.Date(
        required=True,
        string='Effective Date',
        default=fields.Date.today
    )
    lifted_date = fields.Date(
        string='Lifted Date'
    )
    created_by_id = fields.Many2one(
        comodel_name='res.users',
        string='Created By',
        readonly=True,
        default=lambda self: self.env.user
    )
    lifted_by_id = fields.Many2one(
        comodel_name='res.users',
        string='Lifted By',
        readonly=True
    )

    def action_lift_hold(self):
        for record in self:
            if record.status == 'active':
                record.write({
                    'status': 'lifted',
                    'lifted_date': fields.Date.today(),
                    'lifted_by_id': self.env.user.id
                })
                _logger.info(
                    "Legal hold '%s' (ID: %s) lifted by user %s (ID: %s).",
                    record.name, record.id, self.env.user.name, self.env.user.id
                )
                # Potentially trigger audit log entry here via a service if not handled by write override
            else:
                _logger.warning(
                    "Attempted to lift legal hold '%s' (ID: %s) which is already in status '%s'.",
                    record.name, record.id, record.status
                )
        return True