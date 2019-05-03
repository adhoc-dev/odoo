# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class AfipIncoterm(models.Model):
    _name = 'afip.incoterm'
    _description = 'Afip Incoterm'

    afip_code = fields.Char(
        'Code',
        required=True
    )
    name = fields.Char(
        'Name',
        required=True
    )
