# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Cubic ERP - Teradata SAC. (http://cubicerp.com)

{
    'name': 'Argentina - Accounting',
    'version': '12.0.1.0.0',
    'description': """
Argentinian accounting chart and tax localization.
==================================================

Install Argentinian chart of accounts:

* Responsable Inscripto (RI)
    """,
    'author': ['ADHOC SA'],
    'category': 'Localization',
    'depends': [
        'l10n_latam_documents',
        'l10n_ar_base',
    ],
    # TODO review OLD dependencies from l10n_ar_chart
    # # for afip_code on fiscal position and other tax modifications
    # 'l10n_ar_account',
    # 'account_withholding',
    # 'account_check',
    'data':[
        'data/account_account_tag_data.xml',
        'data/account_chart_template.xml',
        'data/account_chart_base.xml',
        'data/account_chart_exento.xml',
        'data/account_chart_respinsc.xml',
        'data/account_tax_group.xml',
        'data/account_tax_withholding_template.xml',
        'data/account_tax_template.xml',
        'data/account_fiscal_template.xml',
        'data/uom_uom.xml',
        'data/base_validator_data.xml',
        'data/l10n_latam.document.type.csv',
        'data/res_partner_data.xml',
        'data/res_currency_data.xml',
        'data/afip_vat_f2002_category_data.xml',
        'data/res_country_afip_code.xml',
        'data/res_country_group_data.xml',
        'data/menuitem.xml',
        'data/product_data.xml',
        'data/afip_incoterm.xml',
        # los cargamos con csv pero los hacemos no actualizables con un hook
        'views/account_move_line_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/afip_menuitem.xml',
        'views/afip_incoterm_view.xml',
        'views/account_account_view.xml',
        'views/res_currency_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/uom_uom_view.xml',
        'views/account_journal_view.xml',
        'views/account_invoice_view.xml',
        'views/l10n_latam_document_type_view.xml',
        'views/afip_concept_view.xml',
        'views/afip_tax_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    'demo': [
        # 'demo/partner_demo.xml',
        # TODO this partners depends of the ones defined in l10n_ar_base that we delete so this ones will not work
        'demo/company_demo.xml',
        # 'demo/product_product_demo.xml',
        # 'demo/account_customer_invoice_demo.yml',
        # 'demo/account_customer_expo_invoice_demo.yml',
        # 'demo/account_customer_invoice_validate_demo.yml',
        # 'demo/account_customer_refund_demo.yml',
        # 'demo/account_supplier_invoice_demo.yml',
        # 'demo/account_supplier_refund_demo.yml',
        # 'demo/account_tax_template_demo.xml',
        # 'demo/account_other_docs_demo.yml',
    ],
    'application': True,
    'post_init_hook': 'post_init_hook',
}
