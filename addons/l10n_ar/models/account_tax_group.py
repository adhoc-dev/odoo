# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class AccountTaxGroup(models.Model):

    _inherit = 'account.tax.group'

    l10n_ar_afip_code = fields.Integer(
        'AFIP Code',
    )
    type = fields.Selection([
        ('tax', 'TAX'),
        ('perception', 'Perception'),
        ('withholding', 'Withholding'),
        ('other', 'Other'),
    ],
        index=True,
    )
    tax = fields.Selection([
        ('vat', 'VAT'),
        ('profits', 'Profits'),
        ('gross_income', 'Gross Income'),
        ('other', 'Other')],
        index=True,
    )
    application = fields.Selection([
        ('national_taxes', 'National Taxes'),
        ('provincial_taxes', 'Provincial Taxes'),
        ('municipal_taxes', 'Municipal Taxes'),
        ('internal_taxes', 'Internal Taxes'),
        ('others', 'Others')],
        help='Other Taxes According AFIP',
        index=True,
    )
    application_code = fields.Char(
        'Application Code',
        compute='_compute_application_code',
    )

    @api.depends('application')
    def _compute_application_code(self):
        code = {
            'national_taxes': '01',
            'provincial_taxes': '02',
            'municipal_taxes': '03',
            'internal_taxes': '04',
        }
        for rec in self:
            rec.application_code = code.get(rec.application, '99')
