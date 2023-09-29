# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):

    _inherit = 'account.move'

    def _get_l10n_latam_documents_domain(self):
        """ We overwrite original domain to only show available active uruguayan document types
        """
        self.ensure_one()
        domain = super()._get_l10n_latam_documents_domain()
        if self.journal_id.company_id.account_fiscal_country_id.code == "UY":
            codes = self._l10n_uy_get_journal_codes()
            if codes:
                domain.extend([('code', 'in', codes)])
        return domain

    def _l10n_uy_get_journal_codes(self):
        """ Return list of the available document type codes for Uruguayan Sales Journals """
        self.ensure_one()
        if self.journal_id.type != 'sale':
            return []
        internal_types = ['invoice', 'debit_note', 'credit_note']
        doc_types = self.env['l10n_latam.document.type'].search([
            ('internal_type', 'in', internal_types),
            ('country_id.code', '=', 'UY')])
        available_types = doc_types.mapped('code')

        return available_types

    def _get_starting_sequence(self):
        """ If use documents then will create a new starting sequence using the document type code prefix and the
        journal document number with a 8 padding number """
        if self.journal_id.l10n_latam_use_documents and self.company_id.account_fiscal_country_id.code == "UY" and self.l10n_latam_document_type_id:
            return self._l10n_uy_get_formatted_sequence()
        return super()._get_starting_sequence()

    def _l10n_uy_get_formatted_sequence(self, number=0):
        return "%s A%07d" % (self.l10n_latam_document_type_id.doc_code_prefix, number)

    def _get_last_sequence_domain(self, relaxed=False):
        where_string, param = super(AccountMove, self)._get_last_sequence_domain(relaxed)
        if self.company_id.account_fiscal_country_id.code == "UY" and self.l10n_latam_use_documents:
            where_string += " AND l10n_latam_document_type_id = %(l10n_latam_document_type_id)s"
            param['l10n_latam_document_type_id'] = self.l10n_latam_document_type_id.id or 0
        return where_string, param
