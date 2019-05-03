# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class AccountAccount(models.Model):

    _inherit = 'account.account'

    afip_activity_id = fields.Many2one(
        'afip.activity',
        'AFIP Activity',
        help='AFIP activity, used for IVA f2002 report',
        auto_join=True,
    )
    vat_f2002_category_id = fields.Many2one(
        'afip.vat.f2002_category',
        auto_join=True,
        string='Categoría IVA f2002',
    )
