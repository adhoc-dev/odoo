# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountJournal(models.Model):

    _inherit = "account.journal"

    def _l10n_uy_get_journal_codes(self):
        """ Return list of the available document type codes for Uruguayan Sales Journals
        """
        self.ensure_one()
        if self.type != 'sale':
            return []
        internal_types = ['invoice', 'debit_note', 'credit_note']
        doc_types = self.env['l10n_latam.document.type'].search([
            ('internal_type', 'in', internal_types),
            ('country_id', '=', self.env.ref('base.uy').id)])
        available_types = doc_types.mapped('code')

        return available_types
