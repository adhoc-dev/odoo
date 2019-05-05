# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class ResCompany(models.Model):

    _inherit = "res.company"

    l10n_ar_country_code = fields.Char(
        related='country_id.code',
        string='Country Code',
    )
    l10n_ar_gross_income_number = fields.Char(
        related='partner_id.l10n_ar_gross_income_number',
        string='Gross Income Number',
    )
    l10n_ar_gross_income_type = fields.Selection(
        related='partner_id.l10n_ar_gross_income_type',
        string='Gross Income',
    )
    l10n_ar_start_date = fields.Date(
        related='partner_id.l10n_ar_start_date',
    )
    l10n_ar_afip_responsability_type = fields.Selection(
        related='partner_id.l10n_ar_afip_responsability_type',
    )
    l10n_ar_company_requires_vat = fields.Boolean(
        compute='_compute_l10n_ar_company_requires_vat',
        readonly=True,
    )

    @api.onchange('country_id')
    def onchange_country(self):
        """ Argentinian companies use round_globally as
        tax_calculation_rounding_method
        """
        for rec in self.filtered(lambda x: x.country_id.code == 'AR'):
            rec.tax_calculation_rounding_method = 'round_globally'

    @api.depends('l10n_ar_afip_responsability_type')
    def _compute_l10n_ar_company_requires_vat(self):
        for rec in self.filtered(
                lambda x: x.l10n_ar_afip_responsability_type in ['1', '1FM']):
            rec.l10n_ar_company_requires_vat = True
