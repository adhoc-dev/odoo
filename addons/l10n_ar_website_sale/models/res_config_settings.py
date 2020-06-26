# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResConfigSettings(models.Model):
    _inherit = 'res.config.settings'

    group_show_line_subtotals_tax_excluded = fields.Boolean(group='base.group_portal,base.group_public')
    group_show_line_subtotals_tax_included = fields.Boolean(group='base.group_portal,base.group_public')
