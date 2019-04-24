{
    "name": "Módulo base de Contabilidad Argentina",
    'version': '11.0.1.17.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA,Moldeo Interactive,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        # agregamos esta dependencia ya que el fix que hace ese modulo
        # es fundamental para que el importa base de los impuestos se calcule
        # bien en los reembolsos.
        'account_fix',
        # para padron de afip
        'l10n_ar_afipws',
        # para guardar el link entre facturas y NC
        # el modulo tiene errores en los test (probado solo con odoo y tmb)
        # 'account_invoice_refund_link',
        # no es una dependencia en si (salvo para datos demo) pero si es
        # necesario por como implemenamos la localizacion
        # 'account_invoice_tax_wizard',
    ],
    'external_dependencies': {
        'python': ['pyafipws', 'pysimplesoap.client'],
    },
    'data': [
        'data/menuitem.xml',
        'data/product_data.xml',
        'data/base_validator_data.xml',
        # los cargamos con csv pero los hacemos no actualizables con un hook
        'data/account.document.type.csv',
        'data/afip_incoterm.xml',
        'data/product_uom.xml',
        # TODO analizar y migrar
        # 'data/account_financial_report_data.xml',
        # 'data/account_payment_term.xml',
    ],
    'demo': [
        'demo/partner_demo.xml',
        'demo/company_demo.xml',
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': 'post_init_hook',
}
