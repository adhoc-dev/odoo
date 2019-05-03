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
    afip_responsability_type_id = fields.Many2one(
        'afip.responsability.type',
        'AFIP Responsability Type',
        auto_join=True,
        index=True,
    )
