import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class CampaignKpi(models.Model):
    """
    Represents a specific Key Performance Indicator for a campaign.
    REQ-DMG-004, REQ-2-001
    """
    _name = 'influence_gen.campaign_kpi'
    _description = 'Campaign Key Performance Indicator'
    _inherit = ['influence_gen.base_audit_mixin'] # Audit for CRUD on KPIs

    campaign_id = fields.Many2one(
        'influence_gen.campaign', string='Campaign',
        required=True, ondelete='cascade', index=True
    )
    name = fields.Char(string='KPI Name', required=True, tracking=True,
                       help="e.g., 'Reach', 'Engagement Rate', 'Click-Through Rate', 'Conversions'")
    target_value = fields.Float(string='Target Value', tracking=True,
                                help="The desired value for this KPI.")
    actual_value = fields.Float(string='Actual Value', tracking=True,
                                help="The achieved value for this KPI. Can be updated manually or by automation.")
    unit_of_measure = fields.Char(string='Unit of Measure', tracking=True,
                                  help="e.g., '%', 'Impressions', 'Clicks', 'Number'")
    
    description = fields.Text(string='Description', help="More details about how this KPI is measured or its importance.")
    is_primary_kpi = fields.Boolean(string='Is Primary KPI?', default=False, tracking=True,
                                   help="Mark if this is a key determining factor for campaign success.")

    company_id = fields.Many2one(related='campaign_id.company_id', store=True)

    _sql_constraints = [
        ('campaign_kpi_name_unique',
         'UNIQUE(campaign_id, name)',
         'A KPI name must be unique per campaign.')
    ]

    @api.onchange('actual_value')
    def _onchange_actual_value(self):
        """ Potentially trigger campaign performance recalculation or notifications. """
        if self.actual_value and self.campaign_id:
            _logger.info(f"KPI '{self.name}' for campaign '{self.campaign_id.name}' updated to actual value: {self.actual_value}")
            # self.campaign_id.recalculate_overall_performance() # Example method on campaign model