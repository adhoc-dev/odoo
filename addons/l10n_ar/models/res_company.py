# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.addons.account_document.models.res_company import ResCompany


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
    afip_responsability_type_id = fields.Many2one(
        related='partner_id.afip_responsability_type_id',
    )
    company_requires_vat = fields.Boolean(
        related='afip_responsability_type_id.company_requires_vat',
        readonly=True,
    )
    # use globally as default so that if child companies are created they
    # also use this as default
    # TODO cambiar a un onchange en vez de modificar default
    tax_calculation_rounding_method = fields.Selection(
        default='round_globally',
    )
