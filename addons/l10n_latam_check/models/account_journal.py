from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    l10n_latam_manual_checkbooks = fields.Boolean(
        string='Use electronic and deferred checks',
        help="* Printing is disabled\n* You're allowed to put numbers manually\n* New field for payment date (Check Cash-In Date)"
    )

    @api.constrains('l10n_latam_manual_checkbooks', 'check_manual_sequencing')
    def _check_l10n_latam_manual_checkbooks(self):
        """ Protect from setting check_manual_sequencing (Manual Numbering) + checkbooks for these reasons
        * Printing checks on checkbooks is not implemented and using a "check printing" option together with checkbooks is confusing
        * The next check number field shown when choosing "Manual Numbering" don't have any meaning when using checkbooks
        * Some methods of account_check_printing module behave differently if "Manual Numbering" is configured
        """
        recs = self.filtered(
            lambda x: x.check_manual_sequencing and x.l10n_latam_manual_checkbooks)
        if recs:
            raise UserError(_(
                "Checkbooks can't be used together with check manual sequencing (check printing functionality), "
                "please choose one or the other. Journal ids: %s", ",".join(recs.mapped("name"))))
