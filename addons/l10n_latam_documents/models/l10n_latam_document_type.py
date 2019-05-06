# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class L10nLatamAccountDocmentType(models.Model):

    _name = 'l10n_latam.document.type'
    _description = 'Latam Document Type'
    _order = 'sequence, id'

    sequence = fields.Integer(
        default=10,
        required=True,
        help='To set in which order show the documents type taking into'
        ' account the most commonly used first',
    )
    country_id = fields.Many2one(
        'res.country',
        required=True,
        index=True,
        help='Country in which this type of document is valid',
    )
    name = fields.Char(
        required=True,
        index=True,
        help='The document name',
    )
    doc_code_prefix = fields.Char(
        'Document Code Prefix',
        help="Prefix for Documents Codes on Invoices and Account Moves. "
        "For eg. 'FA ' will build 'FA 0001-0000001' Document Number"
    )
    code = fields.Char(
        help='Code used by different localizations',
    )
    report_name = fields.Char(
        'Name on Reports',
        help='Name that will be printed in reports, for example "CREDIT NOTE"'
    )
    internal_type = fields.Selection([],
        index=True,
        help='Analog to odoo account.invoice.type but with more options'
        ' allowing to identify the kind of document we are working with.'
        ' (not only related to account.invoice, could be for documents of'
        ' other models like stock.picking)'
    )
    validator_id = fields.Many2one(
        'base.validator',
        'Validator',
    )

    @api.multi
    def validate_document_number(self, document_number):
        self.ensure_one()
        if self.validator_id:
            return self.validator_id.validate_value(document_number)
        return False

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            if rec.code:
                name = '(%s) %s' % (rec.code, name)
            result.append((rec.id, name))
        return result

    @api.multi
    def _get_taxes_included(self):
        """ This method is to be inherited by different localizations and
        must return the recordset of the taxes to be included on reports of
        this document type.
        All taxes are going to be discriminated except the one returned by
        this method.
        """
        self.ensure_one()
        return self.env['account.tax']
