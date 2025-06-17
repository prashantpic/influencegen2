# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AreaOfInfluence(models.Model):
    """
    Area of Influence Model
    Represents a category or niche of influence (e.g., Fashion, Gaming).
    This model defines and manages distinct areas of influence or niches
    that influencers can be associated with.
    It inherits from BaseAuditMixin to log CRUD operations.
    REQ-DMG-002
    """
    _name = 'influence_gen.area_of_influence'
    _description = 'Area of Influence'
    _inherit = ['influence_gen.base_audit_mixin'] # Inherit audit mixin

    name = fields.Char(
        string='Name', 
        required=True, 
        index=True,
        help="The name of the area of influence (e.g., 'Fashion', 'Gaming')."
    )
    influencer_profile_ids = fields.Many2many(
        comodel_name='influence_gen.influencer_profile',
        relation='influencer_area_of_influence_rel',
        column1='area_id',
        column2='influencer_id',
        string='Influencer Profiles',
        help="Influencers associated with this area of influence."
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The area of influence name must be unique.')
    ]

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name