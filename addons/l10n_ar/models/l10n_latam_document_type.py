from odoo import models, api, fields


class L10nLtamDocumentType(models.Model):

    _inherit = 'l10n_latam.document.type'

    l10n_ar_letter = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('E', 'E'),
        ('M', 'M'),
        ('T', 'T')],
        'Letters',
    )
    internal_type = fields.Selection(
        selection_add=[
            ('invoice', 'Invoices'),
            ('debit_note', 'Debit Notes'),
            ('credit_note', 'Credit Notes'),
            ('ticket', 'Ticket'),
            ('receipt_invoice', 'Receipt Invoice'),
            ('customer_payment', 'Customer Voucer'),
            ('supplier_payment', 'Supplier Invoice'),
            # ('inbound_payment_voucher', 'Inbound Payment Voucer'),
            # ('outbound_payment_voucher', 'Outbound Payment Voucer'),
            ('in_document', 'In Document')],
        help='It defines some behaviours on different places:'
        '* invoice: used on sale and purchase journals. Auto selected if not'
        'debit_note specified on context.'
        '* debit_note: used on sale and purchase journals but with lower'
        'priority than invoices.'
        '* credit_note: used on sale_refund and purchase_refund journals.'
        '* ticket: automatically loaded for purchase journals but only loaded'
        'on sales journals if point_of_sale is fiscal_printer'
        '* receipt_invoice: mean to be used as invoices but not automatically'
        'loaded because it is not usually used'
        '* in_document: automatically loaded for purchase journals but not '
        'loaded on sales journals. Also can be selected on partners, to be '
        'available it must be selected on partner.'
    )
    purchase_cuit_required = fields.Boolean(
        help='Verdadero si la declaración del CITI compras requiere informar '
        'CUIT'
    )
    purchase_alicuots = fields.Selection(
        [('not_zero', 'No Cero'), ('zero', 'Cero')],
        help='Cero o No cero según lo requiere la declaración del CITI compras'
    )

    @api.multi
    def get_document_sequence_vals(self, journal):
        vals = super(L10nLtamDocumentType, self).get_document_sequence_vals(
            journal)
        if self.country_id.code == 'AR':
            vals.update({
                'padding': 8,
                'implementation': 'no_gap',
                'prefix': "%04i-" % (journal.point_of_sale_number),
            })
        return vals

    @api.multi
    def get_taxes_included(self):
        """ In argentina we include taxes depending on document letter
        """
        self.ensure_one()
        if self.country_id.code == 'AR' and self.l10n_ar_letter in [
           'B', 'C', 'X', 'R']:
            return self.env['account.tax'].search(
                [('tax_group_id.tax', '=', 'vat'),
                    ('tax_group_id.type', '=', 'tax')])
        else:
            return super(L10nLtamDocumentType, self).get_taxes_included()
