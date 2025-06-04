from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    deferred_checks_account_id = fields.Many2one(
       comodel_name="account.account",
       string="Deferred Checks Account",
    )
