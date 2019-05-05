# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class ResCompany(models.Model):

    _inherit = "res.company"

    l10n_ar_country_code = fields.Char(
        related='country_id.code',
        string='Country Code',
    )
    gross_income_number = fields.Char(
        related='partner_id.gross_income_number',
        string='Gross Income Number',
    )
    gross_income_type = fields.Selection(
        related='partner_id.gross_income_type',
        string='Gross Income',
    )
    start_date = fields.Date(
        related='partner_id.start_date',
    )
    afip_responsability_type = fields.Selection(
        related='partner_id.afip_responsability_type',
    )
    company_requires_vat = fields.Boolean(
        compute='_compute_company_requires_vat',
        readonly=True,
    )

    @api.onchange('country_id')
    def onchange_country(self):
        """ Argentinian companies use round_globally as
        tax_calculation_rounding_method
        """
        for rec in self.filtered(lambda x: x.country_id.code == 'AR'):
            rec.tax_calculation_rounding_method = 'round_globally'

    @api.depends('afip_responsability_type')
    def _compute_company_requires_vat(self):
        for rec in self.filtered(
                lambda x: x.afip_responsability_type in ['1', '1FM']):
            rec.company_requires_vat = True
