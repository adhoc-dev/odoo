# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_latam_journal_mapping_ids = fields.One2many(
        'l10n_latam.journal.mapping',
        'journal_id',
        'Documents Types',
        auto_join=True,
    )
    l10n_latam_use_documents = fields.Boolean(
        'Use Documents?',
    )

    @api.onchange('company_id', 'type')
    def change_company(self):
        self.l10n_latam_use_documents = self.type in ['sale', 'purchase'] and \
           self.company_id.l10n_latam_use_documents

    @api.multi
    @api.constrains(
        'code',
        'company_id',
        'l10n_latam_use_documents',
    )
    def update_journal_document_types(self):
        """
        Tricky constraint to create documents on journal.
        You should not inherit this function, inherit
        "_update_journal_document_types" instead
        """
        return self._update_journal_document_types()

    @api.multi
    def _update_journal_document_types(self):
        """
        Function to be inherited by different localizations
        """
        self.ensure_one()
        return True

    @api.constrains('l10n_latam_use_documents')
    def check_use_document(self):
        for rec in self:
            if rec.env['account.invoice'].search(
                    [('journal_id', '=', rec.id)]):
                raise ValidationError(_(
                    'You can not modify the field "Use Documents?"'
                    ' if invoices already exist in the journal!'))
