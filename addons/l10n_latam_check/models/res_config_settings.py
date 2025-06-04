from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    deferred_checks_account_id = fields.Many2one(
        comodel_name="account.account",
        related="company_id.deferred_checks_account_id",
        string="Deferred Checks Account",
        readonly=False,
        check_company=True,
    )
