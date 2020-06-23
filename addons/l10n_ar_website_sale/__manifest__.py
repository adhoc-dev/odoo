# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Argentinian Website',
    'version': '1.0',
    'category': 'Localization',
    'sequence': 14,
    'author': 'Odoo, ADHOC SA',
    'description': """

* Be able to see Identification Type and AFIP Responsibility in shop check address.
* Show shop taxes included/excluded with a new option that depends on the partner responsibility.

""",
    'depends': [
        'website_sale',
        'l10n_ar',
    ],
    'data': [
        'data/ir_model_fields.xml',
        'views/templates.xml',
        'views/res_config_settings_views.xml',
        'demo/res_users_demo.xml',
        'demo/website_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'post_init_hook': '_set_default_tax_group_for_public_portal_users',
}
