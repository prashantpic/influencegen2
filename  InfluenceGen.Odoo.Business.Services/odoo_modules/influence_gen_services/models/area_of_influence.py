from odoo import models, fields, api, _

class InfluenceGenAreaOfInfluence(models.Model):
    _name = 'influence_gen.area_of_influence'
    _description = "Area of Influence / Niche"
    _order = 'name'

    name = fields.Char(string="Name", required=True, index=True, unique=True)
    description = fields.Text(string="Description")
    
    # M2M defined on influencer_profile side for the relation table name
    # influencer_profile_ids = fields.Many2many(
    #     'influence_gen.influencer_profile',
    #     'influencer_area_of_influence_rel',  # Relation table name
    #     'area_id',                           # Column for this model's ID in rel table
    #     'influencer_id',                     # Column for other model's ID in rel table
    #     string="Influencers"
    # )

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Area of Influence name must be unique!')
    ]