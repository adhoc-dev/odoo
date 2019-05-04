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
        if self.localization == 'argentina':
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
