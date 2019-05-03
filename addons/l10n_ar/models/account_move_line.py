# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    afip_responsability_type = fields.Selection(
        related='move_id.afip_responsability_type',
    )
