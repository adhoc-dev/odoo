# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountAccountTag(models.Model):

    _inherit = 'account.account.tag'

    jurisdiction_code = fields.Char(
        size=3,
    )
