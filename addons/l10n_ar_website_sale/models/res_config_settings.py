# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    l10n_ar_tax_groups = fields.Selection([
        ('responsibility_type', 'Regarding Responsibility Type'),
        ('tax_excluded', 'Tax-Excluded (B2B)'),
        ('tax_included', 'Tax-Included (B2C)')],
        string="Portal and Public Users Default Tax Display", default='responsibility_type',
        config_parameter='l10n_ar_website_sale.l10n_ar_tax_groups')

    def set_values(self):
        """ When changing setting for how to display the prices in Argentinian company we also update all the related
        portal and public users """
        res = super().set_values()

        if self.env.company.country_id == self.env.ref('base.ar'):
            company_tax_config = self.env['ir.config_parameter'].sudo().get_param('l10n_ar_website_sale.l10n_ar_tax_groups')
            if company_tax_config != self.l10n_ar_tax_groups:
                self.env['res.users'].search([])._l10n_ar_update_user_tax_group()
        return res

    def _onchange_sale_tax(self):
        """ Only run onchange when we are not in Argentinian Company """
        if self.env.company.country_id != self.env.ref('base.ar'):
            super()._onchange_sale_tax()
