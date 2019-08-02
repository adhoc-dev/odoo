# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from lxml import etree
import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):

    _inherit = 'account.move'

    @staticmethod
    def _l10n_ar_get_document_number_parts(document_number, document_type_code):
        # import shipments
        if document_type_code in ['66', '67']:
            pos = invoice_number = '0'
        else:
            pos, invoice_number = document_number.split('-')
        return {'invoice_number': int(invoice_number), 'point_of_sale': int(pos)}

    l10n_ar_afip_responsibility_type_id = fields.Many2one(
        'l10n_ar.afip.responsibility.type', string='AFIP Responsibility Type', help='Defined by AFIP to'
        ' identify the type of responsibilities that a person or a legal entity could have and that impacts in the'
        ' type of operations and requirements they need.')

    # TODO make it editable, we have to change move creation method
    l10n_ar_currency_rate = fields.Float(copy=False, digits=(16, 4), readonly=True, string="Currency Rate")

    # Mostly used on reports
    l10n_ar_afip_concept = fields.Selection(
        compute='_compute_l10n_ar_afip_concept', selection='get_afip_invoice_concepts', string="AFIP Concept",
        help="A concept is suggested regarding the type of the products on the invoice but it is allowed to force a"
        " different type if required.", readonly=True, states={'draft': [('readonly', False)]})
    l10n_ar_afip_service_start = fields.Date(string='AFIP Service Start Date', readonly=True, states={'draft': [('readonly', False)]})
    l10n_ar_afip_service_end = fields.Date(string='AFIP Service End Date', readonly=True, states={'draft': [('readonly', False)]})

    def get_afip_invoice_concepts(self):
        """ Return the list of values of the selection field. """
        return [('1', 'Products / Definitive export of goods'), ('2', 'Services'), ('3', 'Products and Services'),
                ('4', '4-Other (export)')]

    @api.depends('invoice_line_ids', 'invoice_line_ids.product_id', 'invoice_line_ids.product_id.type', 'journal_id')
    def _compute_l10n_ar_afip_concept(self):
        for rec in self.filtered(lambda x: x.company_id.country_id == self.env.ref('base.ar') and x.l10n_latam_use_documents):
            rec.l10n_ar_afip_concept = rec._get_concept()

    def _get_concept(self):
        """ Method to get the concept of the invoice considering the type of the products on the invoice """
        self.ensure_one()
        invoice_lines = self.invoice_line_ids
        product_types = set([x.product_id.type for x in invoice_lines if x.product_id])
        consumable = set(['consu', 'product'])
        service = set(['service'])
        mixed = set(['consu', 'service', 'product'])
        # Default value "product"
        afip_concept = '1'
        if product_types.issubset(mixed):
            afip_concept = '3'
        if product_types.issubset(service):
            afip_concept = '2'
        if product_types.issubset(consumable):
            afip_concept = '1'
        # on expo invoice you can mix services and products
        if self.l10n_latam_document_type_id.code in ['19', '20', '21'] and afip_concept == '3':
            afip_concept = '1'
        return afip_concept

    def _get_argentina_amounts(self):
        self.ensure_one()
        tax_lines = self.line_ids.filtered('tax_line_id')
        vat_taxes = tax_lines.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_vat_afip_code)

        # we add and "r.base" because only if a there is a base amount it is considered taxable, this is used for
        # eg to validate invoices on afif. Does not include afip_code [0, 1, 2] because their are not taxes
        # themselves: VAT Exempt, VAT Untaxed and VAT Not applicable
        vat_taxables = vat_taxes.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_vat_afip_code not in ['0', '1', '2'] and r.tax_base_amount)

        # vat exempt values (are the ones with code 2)
        vat_exempt_taxes = vat_taxes.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_vat_afip_code == '2')

        # vat untaxed values / no gravado (are the ones with code 1)
        vat_untaxed_taxes = vat_taxes.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_vat_afip_code == '1')

        # other taxes values
        not_vat_taxes = tax_lines - vat_taxes

        iibb_perc = tax_lines.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_tribute_afip_code == '07')
        mun_perc = tax_lines.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_tribute_afip_code == '08')
        intern_tax = tax_lines.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_tribute_afip_code == '04')
        other_perc = tax_lines.filtered(lambda r: r.tax_line_id.tax_group_id.l10n_ar_tribute_afip_code == '09')

        return dict(
            vat_tax_ids=vat_taxes,
            vat_taxable_ids=vat_taxables,
            vat_amount=sum(vat_taxes.mapped('price_unit')),
            vat_taxable_amount=sum(vat_taxables.mapped('tax_base_amount')),
            vat_exempt_base_amount=sum(vat_exempt_taxes.mapped('tax_base_amount')),
            vat_untaxed_base_amount=sum(vat_untaxed_taxes.mapped('tax_base_amount')),
            not_vat_tax_ids=not_vat_taxes,
            other_taxes_amount=sum(not_vat_taxes.mapped('price_unit')),
            iibb_perc_amount=sum(iibb_perc.mapped('price_unit')),
            mun_perc_amount=sum(mun_perc.mapped('price_unit')),
            intern_tax_amount=sum(intern_tax.mapped('price_unit')),
            other_perc_amount=sum(other_perc.mapped('price_unit')),
        )

    def _get_l10n_latam_documents_domain(self):
        self.ensure_one()
        domain = super()._get_l10n_latam_documents_domain()
        if self.journal_id.company_id.country_id == self.env.ref('base.ar'):
            letters = self.journal_id.get_journal_letter(counterpart_partner=self.partner_id.commercial_partner_id)
            domain += ['|', ('l10n_ar_letter', '=', False), ('l10n_ar_letter', 'in', letters)]
            codes = self.journal_id.get_journal_codes()
            if codes:
                domain.append(('code', 'in', codes))
        return domain

    def check_argentinian_invoice_taxes(self):
        """ We consider argentinian invoices the ones from companies with localization AR that belongs to a journal
        with use_documents """
        _logger.info('Running checks related to argentinian documents')

        # check that there is one and only one vat tax per invoice line
        for inv_line in self.filtered(lambda x: x.company_id.l10n_ar_company_requires_vat).mapped('invoice_line_ids'):
            vat_taxes = inv_line.tax_ids.filtered(
                lambda x: x.tax_group_id.l10n_ar_vat_afip_code)
            if len(vat_taxes) != 1:
                raise UserError(_(
                    'There must be one and only one VAT tax per line. Verify lines with product') + ' "%s"' % (
                        inv_line.product_id.name))

        # check partner has responsibility so it will be assigned on invoice validate
        without_responsibility = self.filtered(
            lambda x: not x.partner_id.l10n_ar_afip_responsibility_type_id)
        if without_responsibility:
            raise UserError(_(
                'The following invoices has a partner without AFIP responsibility') + ':<br/>%s' % ('<br/>'.join(
                    ['[%i] %s' % (i.id, i.display_name) for i in without_responsibility])))

        # We verify Vendor Bills that must report CUIT and do not have it configured
        without_vat = self.filtered(
            lambda x: x.type in ['in_invoice', 'in_refund'] and not x.commercial_partner_id.l10n_ar_vat)
        if without_vat:
            raise UserError(_('The following partners do not have VAT configured') + ': %s' % (', '.join(
                without_vat.mapped('commercial_partner_id.name'))))

        # Invoices that should not have any VAT and have
        not_zero_aliquot = self.filtered(
            lambda x: x.type in ['in_invoice', 'in_refund'] and x.l10n_latam_document_type_id.purchase_aliquots == 'zero'
            and any([t.tax_line_id.tax_group_id.l10n_ar_vat_afip_code != '0'
                     for t in x._get_argentina_amounts()['vat_tax_ids']]))
        if not_zero_aliquot:
            raise UserError(_(
                'The following invoices have incorrect VAT configured. You must use VAT Not Applicable.<br/>'
                ' * Invoices: %s') % (', '.join(not_zero_aliquot.mapped('l10n_latam_document_number'))))

        # Invoices that should have VAT but instead have VAT not correspond
        zero_aliquot = self.filtered(
            lambda x: x.type in ['in_invoice', 'in_refund']
            and x.l10n_latam_document_type_id.purchase_aliquots == 'not_zero' and
            any([t.tax_line_id.tax_group_id.l10n_ar_vat_afip_code == '0'
                 for t in x._get_argentina_amounts()['vat_tax_ids']]))
        if zero_aliquot:
            raise UserError(_(
                'The following invoices have VAT not applicable but you must select a correct rate (Not Taxed, Exempt,'
                ' Zero, 10.5, etc.)') + '. <br/> * ' + _('Invoices') + ': %s' % (', '.join(
                    zero_aliquot.mapped('l10n_latam_document_number'))))

    # TODO make it with create/write or with https://github.com/odoo/odoo/pull/31059
    @api.constrains('invoice_date')
    def set_afip_date(self):
        for rec in self.filtered('invoice_date'):
            invoice_date = fields.Datetime.from_string(rec.invoice_date)
            vals = {}
            if not rec.l10n_ar_afip_service_start:
                vals['l10n_ar_afip_service_start'] = invoice_date + relativedelta(day=1)
            if not rec.l10n_ar_afip_service_end:
                vals['l10n_ar_afip_service_end'] = invoice_date + relativedelta(day=1, days=-1, months=+1)
            if vals:
                rec.write(vals)

    @api.onchange('partner_id')
    def check_afip_responsibility(self):
        if self.company_id.country_id == self.env.ref('base.ar') and self.l10n_latam_use_documents and self.partner_id \
           and not self.partner_id.l10n_ar_afip_responsibility_type_id:
            return {'warning': {
                'title': 'Missing Partner Configuration',
                'message': 'Please configure the AFIP Responsibility for "%s" in order to continue' % (
                    self.partner_id.name)}}

    def get_document_type_sequence(self):
        """ Return the match sequences for the given journal and invoice """
        self.ensure_one()
        if self.journal_id.l10n_latam_use_documents and self.l10n_latam_country_code == 'AR':
            if self.journal_id.l10n_ar_share_sequences:
                return self.journal_id.l10n_ar_sequence_ids.filtered(
                    lambda x: x.l10n_ar_letter == self.l10n_latam_document_type_id.l10n_ar_letter)
            res = self.journal_id.l10n_ar_sequence_ids.filtered(
                lambda x: x.l10n_latam_document_type_id == self.l10n_latam_document_type_id)
            return res
        return super().get_document_type_sequence()

    # TODO make it with create/write or with https://github.com/odoo/odoo/pull/31059
    @api.constrains('partner_id')
    @api.onchange('partner_id')
    def _onchange_partner_journal(self):
        """ This method is used when the invoice is created from the sale or subscription """
        expo_journals = ['FEERCEL', 'FEEWS', 'FEERCELP']
        for rec in self.filtered(lambda x: x.company_id.country_id == self.env.ref('base.ar') and x.journal_id.type == 'sale'
                                 and x.l10n_latam_use_documents and x.partner_id.l10n_ar_afip_responsibility_type_id):
            res_code = rec.partner_id.l10n_ar_afip_responsibility_type_id.code
            domain = [('company_id', '=', rec.company_id.id), ('l10n_latam_use_documents', '=', True), ('type', '=', 'sale')]
            journal = self.env['account.journal']
            if res_code in ['8', '9', '10'] and rec.journal_id.l10n_ar_afip_pos_system not in expo_journals:
                # if partner is foregin and journal is not of expo, we try to change to expo journal
                journal = journal.search(domain + [('l10n_ar_afip_pos_system', 'in', expo_journals)], limit=1)
            elif res_code not in ['8', '9', '10'] and rec.journal_id.l10n_ar_afip_pos_system in expo_journals:
                # if partner is NOT foregin and journal is for expo, we try to change to local journal
                journal = journal.search(domain + [('l10n_ar_afip_pos_system', 'not in', expo_journals)], limit=1)
            if journal:
                rec.journal_id = journal.id

    def post(self):
        ar_invoices = self.filtered(lambda x: x.company_id.country_id == self.env.ref('base.ar') and x.l10n_latam_use_documents)
        for rec in ar_invoices:
            rec.l10n_ar_afip_responsibility_type_id = rec.commercial_partner_id.l10n_ar_afip_responsibility_type_id.id
            if rec.company_id.currency_id == rec.currency_id:
                l10n_ar_currency_rate = 1.0
            else:
                l10n_ar_currency_rate = rec.currency_id._convert(
                    1.0, rec.company_id.currency_id, rec.company_id, rec.invoice_date or fields.Date.today(), round=False)
            rec.l10n_ar_currency_rate = l10n_ar_currency_rate

        # We make validations here and not with a constraint because we want validaiton before sending electronic
        # data on l10n_ar_edi
        ar_invoices.check_argentinian_invoice_taxes()
        return super().post()

    def _reverse_moves(self, default_values_list=None, cancel=False):
        if not default_values_list:
            default_values_list = [{} for move in self]
        for move, default_values in zip(self, default_values_list):
            default_values.update({
                # TODO enable when we make l10n_ar_currency_rate editable
                # 'l10n_ar_currency_rate': move.l10n_ar_currency_rate,
                'l10n_ar_afip_service_start': move.l10n_ar_afip_service_start,
                'l10n_ar_afip_service_end': move.l10n_ar_afip_service_end,
            })
        return super()._reverse_moves(default_values_list=default_values_list, cancel=cancel)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """ Overwrite in order to filter the journals visible in the account move taking into account the type of
        the move
            * invoices and refunds: Show only journals that use documents
            * receipts: Show journals that NOT use documents
            * entry: Show all journals
        """
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='journal_id']"):
                domain = node.get('domain', '')
                if domain:
                    default_type = self._context.get('default_type')
                    if default_type and default_type != 'entry':
                        company_use_doc = True
                        use_doc = False if default_type in ('out_receipt', 'in_receipt') else company_use_doc
                        domain = domain[:-1] + ", ('l10n_latam_use_documents', '=', " + str(use_doc) + ")" + domain[-1]
                        node.set('domain', domain)
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res
