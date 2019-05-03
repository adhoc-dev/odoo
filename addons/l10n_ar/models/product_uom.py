##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ProductUom(models.Model):
    _inherit = 'product.uom'

    l10n_ar_afip_code = fields.Char(
        'Afip Code',
    )
