# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # useful to group by this field
    afip_responsability_type_id = fields.Many2one(
        related='move_id.afip_responsability_type_id',
        readonly=True,
        auto_join=True,
        # stored required to group by
        store=True,
    )
