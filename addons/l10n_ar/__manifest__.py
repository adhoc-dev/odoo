# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Argentinian Accounting',
    'version': '13.0.1.0.0',
    'description': """
Argentinian Accounting
======================

* Activate ARS currency.
* Create new model AFIP Responsibility to identifiy the partners fiscal responsibility.
* Add the Identification Types valid in Argentina.
* Define Argentinian chart of accounts:

  * Responsable Inscripto (RI)
  * Exento (EX)
  * Monotributo (Mono)

* Define Argentinian Taxes
* Define Fiscal Positions
* Define AFIP Legal Documents
* Add AFIP Codes for models:

    * Identification Type
    * Currency
    * Country (used to identify legal entities and natural persons of foreign countries)
    * Product Unit of Measure
    * Tax Group

Follow the next configuration steps

1. Go to your company and configure your CUIT number and AFIP Responsibility
2. Go to Invoicing / Configuration and set the Chart of Account you will like
   to use.
3. Create your sale journals taking into account AFIP info if needed.
""",
    'author': 'ADHOC SA',
    'category': 'Localization',
    'depends': [
        'l10n_latam_document',
        'l10n_latam_base',
        'base_vat',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/l10n_latam_identification_type_data.xml',
        'data/l10n_ar_afip_responsibility_type_data.xml',
        'data/account_group_data.xml',
        'data/account_chart_template_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_data2.xml',
        'data/account_tax_group.xml',
        'data/account_tax_template_data.xml',
        'data/account_fiscal_template.xml',
        'data/uom_uom_data.xml',
        'data/l10n_latam.document.type.csv',
        # NOTE: we load as csv but we made them not update True with a hook
        'data/res_partner_data.xml',
        'data/res_currency_data.xml',
        'data/res.country.csv',
        'data/res_country_data.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/res_country_view.xml',
        'views/afip_menuitem.xml',
        'views/l10n_ar_afip_responsibility_type_view.xml',
        'views/res_currency_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/uom_uom_view.xml',
        'views/account_journal_view.xml',
        'views/l10n_latam_document_type_view.xml',
        'views/ir_sequence_view.xml',
        'views/report_invoice.xml',
    ],
    'demo': [
        # we create demo data on different companies (not main_company) to
        # allow different setups and also to allow multi-localization demo data
        'demo/exento_demo.xml',
        'demo/mono_demo.xml',
        'demo/respinsc_demo.xml',
        'demo/res_partner_demo.xml',
        'demo/account_tax_template_demo.xml',
        'demo/product_product_demo.xml',
        'demo/account_customer_invoice_demo.xml',
        'demo/account_customer_expo_invoice_demo.xml',
        'demo/account_customer_invoice_validate_demo.xml',
        'demo/account_customer_refund_demo.xml',
        'demo/account_supplier_invoice_demo.xml',
        'demo/account_supplier_invoice_validate_demo.xml',
        'demo/account_supplier_refund_demo.xml',
        # restore
        'demo/res_users_demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'application': False,
}

