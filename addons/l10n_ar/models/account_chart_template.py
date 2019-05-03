# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields
import logging
_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    # MOVER A LOGICA DE def _get_fp_vals(self, company, position):
    @api.multi
    def generate_fiscal_position(
            self, tax_template_ref, acc_template_ref, company):
        """
        if chart is argentina localization, then we add l10n_ar_afip_code to
        fiscal positions.
        We also add other data to add fiscal positions automatically
        """
        res = super(AccountChartTemplate, self).generate_fiscal_position(
            tax_template_ref, acc_template_ref, company)
        if company.country_id.code != 'AR':
            return res
        positions = self.env['account.fiscal.position.template'].search(
            [('chart_template_id', '=', self.id)])
        for position in positions:
            created_position = self.env['account.fiscal.position'].search([
                ('company_id', '=', company.id),
                ('name', '=', position.name),
                ('note', '=', position.note)], limit=1)
            if created_position:
                created_position.update({
                    'l10n_ar_afip_code': position.l10n_ar_afip_code,
                    'afip_responsability_type': (
                        position.afip_responsability_type),
                })
        return res

    @api.multi
    def _prepare_all_journals(
            self, acc_template_ref, company, journals_dict=None):
        """
        Inherit this function in order to add use document and other
        configuration if company use argentinian localization
        """
        journal_data = super(
            AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict)

        # if argentinian chart, we dont create sales journal as we need more
        # data to create it properly
        if company.country_id.code == 'AR':
            # TODO iterar la lista journal_data y eliminar el diccionario que tiene key type == 'sale'
            pass
        return journal_data
