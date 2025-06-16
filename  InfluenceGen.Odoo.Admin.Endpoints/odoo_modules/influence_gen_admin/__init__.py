# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# REQ-ModuleInitialization: Initializes the Python package for the InfluenceGen Admin Odoo module.
# Namespace: odoo.addons.influence_gen_admin

from . import controllers
from . import models # For res.config.settings extension
from . import wizard