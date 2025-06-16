# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class InfluenceGenAreaOfInfluence(models.Model):
    _name = 'influence_gen.area_of_influence'
    _description = "Area of Influence / Niche"
    _order = 'name'

    name = fields.Char(string="Name", required=True, index=True)
    description = fields.Text(string="Description")
    
    # Reverse relation to influencer_profile_ids is defined on influence_gen.influencer_profile
    # If needed here for specific views or logic:
    influencer_profile_ids = fields.Many2many(
        'influence_gen.influencer_profile',
        'influencer_area_of_influence_rel', # Same relation table name
        'area_id', 'influencer_id', # Correct column names for this side
        string="Influencers"
    )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Area of Influence name must be unique!')
    ]