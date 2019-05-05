# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class AccountAccount(models.Model):

    _inherit = 'account.account'

    vat_f2002_category_id = fields.Many2one(
        'afip.vat.f2002_category',
        auto_join=True,
        string='Categoría IVA f2002',
    )
