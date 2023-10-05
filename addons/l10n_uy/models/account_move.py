# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):

    _inherit = 'account.move'

    def _check_uruguayan_invoices(self):
        """ Check that the UY invoices are vaid
        * the partner of the invoice should have a valid identification type
        * each invoice line should have one and only one vat tax
        * export invoices should not have any vat tax.
        """
        uy_invs = self.filtered(lambda x: (x.company_id.country_id.code == 'UY' and x.l10n_latam_use_documents))
        if not uy_invs:
            return True
        uy_invs.mapped('partner_id').check_vat()

        uruguayan_vat_taxes = self.env['account.tax.group'].search([('l10n_uy_tax_category', '=', 'vat')])

        # Check that we do not send any tax in export invoices
        expo_cfes = uy_invs.filtered(
            lambda x: int(x.l10n_latam_document_type_id.code) in [121, 122, 123])
        for inv_line in expo_cfes.mapped('invoice_line_ids'):
            vat_taxes = inv_line.tax_ids.filtered(lambda x: x.tax_group_id in uruguayan_vat_taxes)
            if len(vat_taxes) != 0:
                raise ValidationError(_('Should not be any VAT tax in the export cfe line "%s" (Id Invoice: %s)',
                                      inv_line.product_id.name, inv_line.move_id.id))

        # We check that there is one and only one vat tax per line
        for line in (uy_invs - expo_cfes).mapped('invoice_line_ids').filtered(
                lambda x: x.display_type not in ('line_section', 'line_note')):
            vat_taxes = line.tax_ids.filtered(lambda x: x.tax_group_id in uruguayan_vat_taxes)
            if len(vat_taxes) != 1:
                raise ValidationError(_('Should be one and only one VAT tax per line. Verify lines with product "%s" (Id Invoice: %s)',
                                      line.product_id.name, line.move_id.id))

    def _get_l10n_latam_documents_domain(self):
        """ We overwrite original domain to only show available active uruguayan document types
        """
        self.ensure_one()
        domain = super()._get_l10n_latam_documents_domain()
        if self.journal_id.company_id.account_fiscal_country_id.code == "UY":
            codes = self.journal_id._l10n_uy_get_journal_codes()
            if codes:
                domain.extend([('code', 'in', codes), ('active', '=', True)])
        return domain

    def unlink(self):
        """ When using documents on vendor bills the document_number is set manually by the number given from the vendor
        so the odoo sequence is not used. In this case we allow to delete vendor bills with document_number/name """
        self.filtered(lambda x: x.move_type in x.get_purchase_types() and x.state in ('draft', 'cancel') and
                      x.l10n_latam_use_documents).write({'name': '/'})
        return super().unlink()

    def _post(self, soft=True):
        """ We make validations here and not with a constraint because we want a validation before sending
        electronic data on l10n_uy_edi
        """
        uy_invoices = self.filtered(lambda x: x.company_id.country_id.code == 'UY' and x.l10n_latam_use_documents)
        uy_invoices._check_uruguayan_invoices()
        return super()._post(soft=soft)

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
