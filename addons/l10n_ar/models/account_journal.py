# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):

    _inherit = "account.journal"

    _point_of_sale_types_selection = [
        ('manual', 'Manual'),
        ('preprinted', 'Preprinted'),
        ('online', 'Online'),
    ]

    point_of_sale_type = fields.Selection(
        _point_of_sale_types_selection,
        'Point Of Sale Type',
    )
    point_of_sale_number = fields.Integer(
        'Point Of Sale Number',
    )

    @api.multi
    def get_journal_letter(self, counterpart_partner=False):
        """Function to be inherited by others"""
        self.ensure_one()
        return self._get_journal_letter(
            journal_type=self.type,
            company=self.company_id,
            counterpart_partner=counterpart_partner)

    @api.model
    def _get_journal_letter(
            self, journal_type, company, counterpart_partner=False):
        """ Regarding the AFIP responsability of the company and the type of
        journal (sale/purchase), get the allowed letters.
        Optionally, receive the counterpart partner (customer/supplier) and
        get the allowed letters to work with him.
        This method is used to populate document types on journals and also
        to filter document types on specific invoices to/from customer/supplier
        """
        responsability = company.afip_responsability_type_id
        if journal_type == 'sale':
            resp_field = 'issuer_ids'
        elif journal_type == 'purchase':
            resp_field = 'receptor_ids'
        else:
            raise UserError(_(
                'Letters not implemented for journal type %s' % (
                    journal_type)))
        letters = self.env['account.document.letter'].search([
            '|', (resp_field, '=', responsability.id),
            (resp_field, '=', False)])

        if counterpart_partner:
            counterpart_resp = counterpart_partner.afip_responsability_type_id
            if journal_type == 'sale':
                letters = letters.filtered(
                    lambda x: not x.receptor_ids or
                    counterpart_resp in x.receptor_ids)
            else:
                letters = letters.filtered(
                    lambda x: not x.issuer_ids or
                    counterpart_resp in x.issuer_ids)
        return letters

    @api.multi
    def _update_journal_document_types(self):
        """
        It creates, for journal of type:
            * sale: documents of internal types 'invoice', 'debit_note',
                'credit_note' if there is a match for document letter
        TODO complete here
        """
        self.ensure_one()
        if self.company_id.country_id.code != 'AR':
            return super(
                AccountJournal, self)._update_journal_document_types()

        if not self.use_documents:
            return True

        letters = self.get_journal_letter()

        other_purchase_internal_types = ['in_document', 'ticket']

        if self.type in ['purchase', 'sale']:
            internal_types = ['invoice', 'debit_note', 'credit_note']
            # for purchase we add other documents with letter
            if self.type == 'purchase':
                internal_types += other_purchase_internal_types
        else:
            raise UserError(_('Type %s not implemented yet' % self.type))

        document_types = self.env['account.document.type'].search([
            ('internal_type', 'in', internal_types),
            ('localization', '=', self.localization),
            '|', ('document_letter_id', 'in', letters.ids),
            ('document_letter_id', '=', False)])

        # no queremos que todo lo que es factura de credito electronica se cree
        # por defecto ya que es poco usual
        # TODO mejorar este parche
        document_types = document_types.filtered(lambda x: int(x.code) not in [
            201, 202, 203, 206, 207, 208, 211, 212, 213])

        # TODO borrar, ya estamos agregando arriba porque buscamos letter false
        # for purchases we add in_documents and ticket whitout letters
        # TODO ver que no hace falta agregar los tickets aca porque ahora le
        # pusimos al tique generico la letra x entonces ya se agrega solo.
        # o tal vez, en vez de usar letra x, lo deberiamos motrar tambien como
        # factible por no tener letra y ser tique
        # if self.type == 'purchase':
        #     document_types += self.env['account.document.type'].search([
        #         ('internal_type', 'in', other_purchase_internal_types),
        #         ('document_letter_id', '=', False)])

        # take out documents that already exists
        document_types = document_types - self.mapped(
            'journal_document_type_ids.document_type_id')

        sequence = 10
        for document_type in document_types:
            sequence_id = False
            if self.type == 'sale':
                # Si es nota de debito nota de credito y same sequence,
                # no creamos la secuencia, buscamos una que exista
                if (
                        document_type.internal_type in [
                        'debit_note', 'credit_note'] and
                        self.document_sequence_type == 'same_sequence'
                ):
                    journal_document = self.journal_document_type_ids.search([
                        ('document_type_id.document_letter_id', '=',
                            document_type.document_letter_id.id),
                        ('journal_id', '=', self.id)], limit=1)
                    sequence_id = journal_document.sequence_id.id
                else:
                    sequence_id = self.env['ir.sequence'].create(
                        document_type.get_document_sequence_vals(self)).id
            self.journal_document_type_ids.create({
                'document_type_id': document_type.id,
                'sequence_id': sequence_id,
                'journal_id': self.id,
                'sequence': sequence,
            })
            sequence += 10
