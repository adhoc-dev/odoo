# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountTaxGroup(models.Model):

    _inherit = "account.tax.group"

    l10n_uy_tax_category = fields.Selection([
        ('vat', 'VAT'),
    ], string="Tax Category")
