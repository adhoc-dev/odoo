from odoo import models, api, _
from odoo.exceptions import ValidationError


class AccountPaymentMethodLine(models.Model):
    _inherit = 'account.payment.method.line'

    @api.constrains('payment_method_id', 'payment_account_id')
    def _check_payment_outstanding_account(self):
        if self.payment_method_id.code in ['new_third_party_checks', 'in_third_party_checks', 'out_third_party_checks','own_checks'] and not self.payment_account_id:
            raise ValidationError(_('The payment check method require outstanding account'))
