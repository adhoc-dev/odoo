# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models


class AccountChartTemplate(models.AbstractModel):

    _inherit = "account.chart.template"

    @api.model
    def _get_demo_data(self, company=False):
        demo_data = super()._get_demo_data(company)
        if company == self.env.ref('l10n_uy.demo_company_uy', raise_if_not_found=False):
            # Do not load generic demo data on these companies
            return {}
        return demo_data

    def _post_load_demo_data(self, company=False):
        if company != self.env.ref('l10n_uy.demo_company_uy', raise_if_not_found=False):
            # Do not load generic demo data on these companies
            return super()._post_load_demo_data(company)
