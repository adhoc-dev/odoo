# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class ResCompany(models.Model):

    _inherit = "res.company"

    l10n_ar_country_code = fields.Char(related='country_id.code', string='Country Code')
    l10n_ar_gross_income_number = fields.Char(
        related='partner_id.l10n_ar_gross_income_number', string='Gross Income Number', readonly=False,
        help="This field is required in order to print the invoice report properly")
    l10n_ar_gross_income_type = fields.Selection(
        related='partner_id.l10n_ar_gross_income_type', string='Gross Income', readonly=False,
        help="This field is required in order to print the invoice report properly")
    l10n_ar_afip_responsability_type_id = fields.Many2one(
        domain="[('code', 'in', [1, 4, 6])]",
        related='partner_id.l10n_ar_afip_responsability_type_id', readonly=False)
    l10n_ar_company_requires_vat = fields.Boolean(
        compute='_compute_l10n_ar_company_requires_vat', string='Company Requires Vat?')
    l10n_ar_afip_start_date = fields.Date('Activities start')

    @api.onchange('country_id')
    def onchange_country(self):
        """ Argentinian companies use round_globally as tax_calculation_rounding_method """
        for rec in self.filtered(lambda x: x.country_id == self.env.ref('base.ar')):
            rec.tax_calculation_rounding_method = 'round_globally'

    @api.depends('l10n_ar_afip_responsability_type_id')
    def _compute_l10n_ar_company_requires_vat(self):
        for rec in self.filtered(lambda x: x.l10n_ar_afip_responsability_type_id.code == '1'):
            rec.l10n_ar_company_requires_vat = True

    def _localization_use_documents(self):
        """ Argentinian localization use documents """
        self.ensure_one()
        return True if self.country_id == self.env.ref('base.ar') else super()._localization_use_documents()

    def write(self, values):
        """ Set companies AFIP Responsability and Country from the if AR CoA installed """
        chart_template_id = values.get('chart_template_id', False)
        if chart_template_id:
            match = {
                self.env.ref('l10n_ar.l10nar_base_chart_template').id: self.env.ref('l10n_ar.res_RM').id,
                self.env.ref('l10n_ar.l10nar_ex_chart_template').id: self.env.ref('l10n_ar.res_IVAE').id,
                self.env.ref('l10n_ar.l10nar_ri_chart_template').id: self.env.ref('l10n_ar.res_IVARI').id,
            }
            ar_coa = match.get(chart_template_id, False)
            if ar_coa:
                values.update(l10n_ar_afip_responsability_type_id=ar_coa, country_id=self.env.ref('base.ar').id)
        return super().write(values)
