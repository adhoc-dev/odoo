# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Base Validator',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': '',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'depends': [
    ],
    'data': [
        'views/base_validator_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/base_validator.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
