from odoo import api, fields, models, _
from odoo.exceptions import UserError

class LegalHold(models.Model):
    _name = 'influence_gen.legal_hold'
    _description = 'InfluenceGen Legal Hold'
    _order = 'effective_date desc, name'

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
        index=True,
        tracking=True
    )
    target_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Target Model',
        help="The model containing the data to be held."
        # No specific domain, admin should choose carefully.
    )
    target_record_id = fields.Reference(
        selection=lambda self: [(model.model, model.name) for model in self.env['ir.model'].search([('transient', '=', False), ('abstract', '=', False)])],
        string="Target Record",
        help="Specific record to be held. Use if holding a single record. Select Target Model first.",
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
        string='Lifted Date',
        readonly=True
    )
    created_by_id = fields.Many2one(
        comodel_name='res.users',
        string='Created By',
        readonly=True,
        default=lambda self: self.env.user,
        copy=False
    )
    lifted_by_id = fields.Many2one(
        comodel_name='res.users',
        string='Lifted By',
        readonly=True,
        copy=False
    )

    @api.onchange('target_model_id')
    def _onchange_target_model_id(self):
        if not self.target_model_id:
            self.target_record_id = False


    def action_lift_hold(self):
        for record in self:
            if record.status != 'active':
                raise UserError(_("Legal hold '%s' is not active and cannot be lifted.") % record.name)
            
            record.write({
                'status': 'lifted',
                'lifted_date': fields.Date.today(),
                'lifted_by_id': self.env.user.id
            })
            record.message_post(body=_("Legal hold lifted by %s.") % self.env.user.name)
            
            # Placeholder: Audit log entry should be created by the audit log service
            # self.env['influence_gen.audit_log'].sudo().create_log_entry(
            #     actor_user_id=self.env.user.id,
            #     event_type='legal_hold_lifted',
            #     action='lift',
            #     target_entity=self._name,
            #     target_id=record.id,
            #     details={'hold_name': record.name}
            # )
        return True

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.status})"
            if record.target_model_id:
                name += f" - Model: {record.target_model_id.name}"
            if record.target_record_id:
                try:
                    # Attempt to get display name of the referenced record
                    record_display_name = record.target_record_id.display_name if record.target_record_id else "N/A"
                    name += f" - Record: {record_display_name}"
                except Exception: # Handle cases where display_name might not be accessible or record deleted
                    name += f" - Record ID: {record.target_record_id.id if record.target_record_id else 'N/A'}"

            elif record.target_influencer_id:
                name += f" - Influencer: {record.target_influencer_id.name or 'N/A'}"
            elif record.target_campaign_id:
                name += f" - Campaign: {record.target_campaign_id.name or 'N/A'}"
            result.append((record.id, name))
        return result