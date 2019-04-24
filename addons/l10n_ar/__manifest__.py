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
    'author': ['Cubic ERP', 'ADHOC'],
    'category': 'Localization',
    'depends': ['base', 'account'],
    'data':[
        'data/l10n_ar_chart_data.xml',
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
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
}
