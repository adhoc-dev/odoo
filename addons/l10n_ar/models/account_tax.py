# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class AccountTax(models.Model):

    _inherit = 'account.tax'

    jurisdiction_code = fields.Char(
        compute='_compute_jurisdiction_code',
    )

    @api.multi
    def _compute_jurisdiction_code(self):
        for rec in self:
            tag = rec.tag_ids.filtered('jurisdiction_code')
            rec.jurisdiction_code = tag and tag[0].jurisdiction_code
