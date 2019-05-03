# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError
try:
    from pysimplesoap.client import SoapFault
except ImportError:
    SoapFault = None
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _afip_responsabilities = [
        ('1', 'IVA Responsable Inscripto'),
        ('1FM', 'IVA Responsable Inscripto Factura M'),
        ('4', 'IVA Sujeto Exento'),
        ('5', 'Consumidor Final'),
        ('6', 'Responsable Monotributo'),
        ('8', 'Proveedor del Exterior'),
        ('9', 'Cliente del Exterior'),
        ('10', 'IVA Liberado – Ley Nº 19.640'),
    ]

    gross_income_number = fields.Char(
        'Gross Income Number',
        size=64,
    )
    gross_income_type = fields.Selection([
        ('multilateral', 'Multilateral'),
        ('local', 'Local'),
        ('no_liquida', 'No Liquida'),
    ],
        'Gross Income Type',
    )
    start_date = fields.Date(
        'Start-up Date',
    )
    afip_responsability_type = fields.Selection(
        _afip_responsabilities,
        'AFIP Responsability Type',
        index=True,
    )
