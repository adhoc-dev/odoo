# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Cubic ERP - Teradata SAC. (http://cubicerp.com)

{
    'name': 'Argentina - Accounting',
    'version': '12.0.1.0.0',
    'description': """
Argentinian accounting chart and tax localization.
==================================================

Plan contable argentino e impuestos de acuerdo a disposiciones vigentes

    """,
    'author': ['ADHOC SA'],
    'category': 'Localization',
    'depends': [
        'account_document',
        'l10n_ar_base',
        ],
    'data':[
        'data/account.account.template.csv',
        'data/l10n_ar_chart_post_data.xml',
        'data/account_tax_group.xml',
        'data/account_account_tag_data.xml',
        'data/account_tax_template.xml',
        'data/account_chart_template_data.xml',
        'data/product_uom.xml',
        'data/res_partner_data.xml',
        'data/res_currency_data.xml',
        'data/afip_vat_f2002_category_data.xml',
        'data/res_country_afip_code.xml',
        'data/res_country_cuit.xml',
        'data/res_country_group_data.xml',
        'data/menuitem.xml',
        'data/product_data.xml',
        'data/base_validator_data.xml',
        'data/afip_incoterm.xml',
        'data/product_uom.xml',
        # los cargamos con csv pero los hacemos no actualizables con un hook
        'data/account.document.type.csv',
        'views/account_move_line_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/afip_menuitem.xml',
        'views/afip_incoterm_view.xml',
        'views/account_account_view.xml',
        'views/res_country_view.xml',
        'views/res_currency_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/product_uom_view.xml',
        'views/account_journal_view.xml',
        'views/account_invoice_view.xml',
        'views/afip_responsability_type_view.xml',
        'views/account_document_letter_view.xml',
        'views/account_document_type_view.xml',
        'views/product_template_view.xml',
        'views/afip_activity_view.xml',
        'views/afip_concept_view.xml',
        'views/afip_tax_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/account_ar_vat_line_view.xml',
        'report/invoice_analysis.xml',
    ],
    'demo': [
        'demo/partner_demo.xml',
        'demo/company_demo.xml',
    ],
}
