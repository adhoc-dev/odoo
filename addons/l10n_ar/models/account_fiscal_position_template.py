# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountFiscalPositionTemplate(models.Model):
    _inherit = 'account.fiscal.position.template'

    l10n_ar_afip_code = fields.Char(
        'AFIP Code',
        help='For eg. This code will be used on electronic invoice and citi '
        'reports',
    )

    # TODO this fields should be added on odoo core
    auto_apply = fields.Boolean(
        string='Detect Automatically',
        help="Apply automatically this fiscal position.")
    country_id = fields.Many2one(
        'res.country', string='Country',
        help="Apply only if delivery or invoicing country match.")
    country_group_id = fields.Many2one(
        'res.country.group', string='Country Group',
        help="Apply only if delivery or invocing country match the group.")
    state_ids = fields.Many2many(
        'res.country.state', string='Federal States')
    zip_from = fields.Integer(
        string='Zip Range From', default=0)
    zip_to = fields.Integer(
        string='Zip Range To', default=0)
