##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, _
import logging
_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _create_bank_journals(self, company, acc_template_ref):
        """
        Creates third checks journal and enable own checks on banks
        """

        res = super(AccountChartTemplate, self)._create_bank_journals(company, acc_template_ref)

        # creamos diario para cheques de terceros
        self.env['account.journal'].create({
            'name': _('Third Checks'),
            'type': 'cash',
            'company_id': company.id,
            'inbound_payment_method_ids': [
                (4, self.env.ref('account_check.account_payment_method_new_third_checks').id, None),
                (4, self.env.ref('account_check.account_payment_method_in_third_checks').id, None),
            ],
            'outbound_payment_method_ids': [
                (4, self.env.ref('account_check.account_payment_method_out_third_checks').id, None),
            ],
        })
        # creamos diario para cheques de terceros rechazados
        self.env['account.journal'].create({
            'name': _('Rejected Third Checks'),
            'type': 'cash',
            'company_id': company.id,
            'inbound_payment_method_ids': [
                (4, self.env.ref('account_check.account_payment_method_in_third_checks').id, None),
            ],
            'outbound_payment_method_ids': [
                (4, self.env.ref('account_check.account_payment_method_out_third_checks').id, None),
            ],
        })

        return res
