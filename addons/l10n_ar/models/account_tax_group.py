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
        for rec in self:
            if rec.application == 'national_taxes':
                application_code = '01'
            elif rec.application == 'provincial_taxes':
                application_code = '02'
            elif rec.application == 'municipal_taxes':
                application_code = '03'
            elif rec.application == 'internal_taxes':
                application_code = '04'
            else:
                application_code = '99'
            rec.application_code = application_code
