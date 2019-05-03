# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    l10n_ar_afip_code = fields.Char(
        'Afip Code',
    )
