# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class L10nAccountDocumentType(models.Model):

    _inherit = 'l10n_latam.document.type'

    internal_type = fields.Selection(selection_add=[('stock_picking', 'Delivery Guide')])

    def _format_document_number(self, document_number):
        """ As of now, format the document_number only, in the future, validate the document_number """
        self.ensure_one()
        if self.country_id.code != "UY":
            return super()._format_document_number(document_number)

        if not document_number:
            return

        return document_number.zfill(8)
