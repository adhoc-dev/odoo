# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Uruguay - Accounting',
    'website': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['uy'],
    'version': '0.1',
    'author': 'Uruguay l10n Team, Guillem Barba, ADHOC',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
General Chart of Accounts.
==========================

This module adds accounting functionalities for the Uruguayan localization, representing the minimum required configuration for a company to operate in Uruguay under the regulations and guidelines provided by the DGI (Dirección General Impositiva).

Among the functionalities are:

* Uruguayan Generic Chart of Account
* Pre-configured VAT Taxes and Tax Groups.
* Legal document types in Uruguay.
* Valid contact identification types in Uruguay.
* Configuration and activation of Uruguayan Currencies  (UYU, UYI - Unidad Indexada Uruguaya).
* Frequently used default contacts already configured: DGI, Consumidor Final Uruguayo.

NOTE: This module adds both models and fields that will eventually be used for the electronic invoicing module.

Configuration
-------------

Follow the steps below to configure in production after installing the module:

1. Company Configuration. Go to the Company menu and create or configure the Uruguayan Company. set the RUT number (vat)
2. Install Chart of Accounts: Go to the Accounting / Configuration / Settings menu, under the Accounting / Fiscal Localization section, select the package "Uruguayan Generic Chart of Accounts" and then click Save.

    IMPORTANT:

    1. This option will only appear if the company where you are currently working does not yet have a chart of accounts installed. Once the chart of accounts is installed and invoices have been generated, it cannot be changed.
    2. This configuration is company-specific, so make sure you are in the correct company where you want the chart of accounts to be installed.

Demo data for testing:

* Uruguayan company named "UY Company" with the Uruguayan chart of accounts already installed, pre configured taxes, document types and identification types.
* Uruguayan contacts for testing:

   * IEB Internacional
   * Consumidor Final Anónimo.

""",
    'depends': [
        'account',
        'l10n_latam_invoice_document',
        'l10n_latam_base',
    ],
    'data': [
        'data/account_tax_report_data.xml',
        'data/l10n_latam.document.type.csv',
        'data/l10n_latam_identification_type_data.xml',
        'data/res_partner_data.xml',
        'views/l10n_latam_document_type_views.xml',
        'views/account_journal_view.xml',
        'data/res_currency_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/res_partner_demo.xml',
        'demo/res_currency_rate_data.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
