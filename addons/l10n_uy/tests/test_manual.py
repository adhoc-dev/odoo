# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tests.common import Form, tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged('post_install_l10n', '-at_install', 'post_install')
class TestManual(AccountTestInvoicingCommon):

    @classmethod
    def setUpClass(cls, chart_template_ref='uy'):
        super(TestManual, cls).setUpClass(chart_template_ref=chart_template_ref)

        cls.company_data['company'].write({
            'currency_id': cls.env.ref('base.UYU').id,
            'name': '(UY) Uruguay Company (Unit Tests)',
        })
        cls.company_uy = cls.company_data['company']

        cls.company_uy.partner_id.write({
            'name': '(UY) Uruguay Company (Unit Tests)',
            'vat': '215521750017',
            "street": 'Calle Falsa 254',
            "city": 'Montevideo',
            "country_id": cls.env.ref("base.uy").id,
            "state_id": cls.env.ref("base.state_uy_10").id,
            "zip": '2000',
            "phone": '+1 555 123 8069',
            "email": 'info@example.com',
            "website": 'www.example.com',
        })

        cls.partner_uy = cls.company_uy.partner_id
        cls.tax_22 = cls.env['account.tax'].with_context(active_test=False).search(
            [('country_code', '=', 'UY'), ('amount', '=', 22.0), ('type_tax_use', '=', 'sale'),
             ('tax_group_id', '=', cls._find_company_tax(cls, 'tax_group_iva_22').id),
             ('company_id', '=', cls.company_uy.id)], limit=1)
        cls.service_vat_22 = cls.env['product.product'].create({
            'name': 'Virtual Home Staging (VAT 22)',
            'list_price': 38.25,
            'standard_price': 45.5,
            'type': 'service',
            'default_code': 'VAT 22',
            'taxes_id': [(6, 0, cls.tax_22.ids)],
        })

    def _find_company_tax(self, tax_id):
        data_records = self.env['ir.model.data'].search([
            ('module', '=', 'account'),
            ('model', '=', 'account.tax.group'),
            ('name', 'ilike', tax_id),
        ])
        tax_group = self.env['account.tax.group'].search([
            ('id', 'in', data_records.mapped('res_id')),
            ('company_id', '=', self.company_uy.id)])
        return tax_group

    def _create_invoice(self, data=None, invoice_type='out_invoice'):
        data = {}
        with Form(self.env['account.move'].with_context(default_move_type=invoice_type)) as invoice_form:
            invoice_form.partner_id = self.partner_uy
            for line in data.get('lines', [{}]):
                with invoice_form.invoice_line_ids.new() as invoice_line_form:
                    invoice_line_form.display_type = line.get('display_type', 'product')
                    if line.get('display_type') in ('line_note', 'line_section'):
                        invoice_line_form.name = line.get('name', 'not invoice line')
                    else:
                        invoice_line_form.product_id = line.get('product', self.service_vat_22)
                        invoice_line_form.quantity = line.get('quantity', 1)
                        invoice_line_form.price_unit = line.get('price_unit', 100)
            invoice_form.invoice_date = invoice_form.date
        invoice = invoice_form.save()
        return invoice

    def _post(self, invoice):
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')

    def test_01_create_invoice(self):
        """ Create and validate an invoice for Uruguay

        * Invoice generated in the UY Company
        * Properly set the default sale taxes
        * Invoice can be validated without error
        """
        invoice = self._create_invoice()
        self.assertEqual(invoice.company_id, self.company_uy, 'created with wrong company')
        self.assertEqual(invoice.amount_tax, 22, 'invoice taxes are not properly set')
        self.assertEqual(invoice.amount_total, 122.0, 'invoice taxes has not been applied to the total')
        self._post(invoice)
        self.assertEqual(invoice.state, 'posted', 'invoice has not been validate in Odoo')
