# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.addons.l10n_latam_document.models.res_company import ResCompany
from odoo.addons.l10n_ar.models.res_partner import ResPartner


class ResCompany(models.Model):

    _inherit = "res.company"

    gross_income_number = fields.Char(
        related='partner_id.gross_income_number',
        string='Gross Income'
    )
    gross_income_type = fields.Selection(
        related='partner_id.gross_income_type',
        string='Gross Income'
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
    # use globally as default so that if child companies are created they
    # also use this as default
    # TODO cambiar a un onchange en vez de modificar default
    tax_calculation_rounding_method = fields.Selection(
        default='round_globally',
    )

    @api.depends('afip_responsability_type')
    def _compute_company_requires_vat(self):
        for rec in self.filtered(
                lambda x: x.afip_responsability_type in ['1', '1FM']):
            rec.company_requires_vat = True