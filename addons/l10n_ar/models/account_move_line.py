# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    afip_responsability_type = fields.Selection(
        related='move_id.afip_responsability_type',
    )
