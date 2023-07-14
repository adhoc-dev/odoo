from odoo import models
from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):

    _inherit = 'account.chart.template'

    # ar base
    @template('ar_base', 'account.account')
    def _get_ar_base_withholding_account_account(self):
        return self._parse_csv('ar_base', 'account.account', module='l10n_ar_withholding')
    
    @template(model='ir.sequence')
    def _get_ir_sequence(self, template_code):
        return self._parse_csv(template_code, 'ir.sequence')

    # ri chart
    @template('ar_ri', 'account.tax.group')
    def _get_ar_ri_withholding_account_tax_group(self):
        return self._parse_csv('ar_ri', 'account.tax.group', module='l10n_ar_withholding')

    @template('ar_ri', 'ir.sequence')
    def _get_ar_ri_withholding_ir_sequence(self):
        return self._parse_csv('ar_ri', 'ir.sequence', module='l10n_ar_withholding')

    @template('ar_ri', 'account.tax')
    def _get_ar_ri_withholding_account_tax(self):
        additionnal = self._parse_csv('ar_ri', 'account.tax', module='l10n_ar_withholding')
        self._deref_account_tags('ar_ri', additionnal)
        self._deref_account_tags('ar_ex', additionnal)
        return additionnal

    # ex chart
    @template('ar_ex', 'account.tax.group')
    def _get_ar_ex_withholding_account_tax_group(self):
        return self._parse_csv('ar_ex', 'account.tax.group', module='l10n_ar_withholding')

    @template('ar_ex', 'account.tax')
    def _get_ar_ex_withholding_account_tax(self):
        additionnal = self._parse_csv('ar_ex', 'account.tax', module='l10n_ar_withholding')
        self._deref_account_tags('ar_ex', additionnal)

    def _post_load_data(self, template_code, company, template_data):
        result = super()._post_load_data(template_code, company, template_data)
        if template_code in ['ar_base', 'ar_ri', 'ar_ex']:
            company.l10n_ar_tax_base_account_id = self.ref('base_tax_account')
        return result
