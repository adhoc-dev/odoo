##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, _, api
from odoo.exceptions import UserError, ValidationError
import logging
# import odoo.addons.decimal_precision as dp
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):

    _inherit = 'account.payment'

    check_id = fields.Many2one('account.check', string='Check', readonly=True, states={'draft': [('readonly', False)]}, copy=False,)
    # this fields is to help with code and view but if needed this field could be removed and check everywhere for the payment_method_code
    check_type = fields.Char(compute='_compute_check_type')
    available_check_ids = fields.Many2many('account.check', compute='_compute_check_data')
    amount = fields.Monetary(compute='_compute_amount', readonly=False, store=True)

    def _get_checks_operations(self):
        return self._get_checks_operations_model(self.payment_method_code, self.payment_type, self.is_internal_transfer, self.journal_id)

    @api.model
    def _get_checks_operations_model(self, payment_method_code, payment_type, is_internal_transfer, journal_id, destination_journal_id=None):
        """
        This method is called from:
        * cancellation of payment to execute delete the right operation and unlink check if needed
        * from post to add check operation and, if needded, change payment vals and/or create check and
        """
        if payment_method_code in ['new_third_checks', 'out_third_checks', 'in_third_checks']:
            # third checks
            domain = [('type', '=', 'third_check')]
            if is_internal_transfer:
                if payment_type == 'outbound':
                    if destination_journal_id and any(x.code == 'in_third_checks' for x in destination_journal_id.inbound_payment_method_ids):
                        # transferencia a otro diario de terceros
                        # TODO implementar el movimiento entre diarios de cheques de terceros con dos operations?
                        return (
                            'holding',
                            domain + [('journal_id', '=', journal_id.id), ('state', '=', 'holding')])
                    else:
                        # deposito o venta
                        return (
                            'deposited',
                            domain + [('journal_id', '=', journal_id.id), ('state', '=', 'holding')])
                elif payment_type == 'inbound':
                    # Deposit rejection
                    return (
                        'holding',
                        # we can get the rejected check in a diferent journal
                        # ('journal_id', '=', journal_id.id),
                        domain + [('state', '=', 'deposited')])
            elif payment_method_code == 'new_third_checks':
                return 'holding', domain + [('journal_id', '=', journal_id.id), ('state', '=', 'draft')]
            elif payment_method_code == 'out_third_checks':
                return 'delivered', domain + [('journal_id', '=', journal_id.id), ('state', '=', 'holding')]
            elif payment_method_code == 'in_third_checks':
                return 'holding', domain + [('state', '=', 'delivered')]
        elif payment_method_code in ['new_own_checks', 'in_own_checks']:
            # issue checks
            domain = [('type', '=', 'own_check')]
            if is_internal_transfer and payment_type == 'outbound':
                return 'withdrawed', domain + [('journal_id', '=', journal_id.id), ('state', '=', 'draft')]
            elif payment_method_code == 'new_own_checks':
                return 'handed', domain + [('journal_id', '=', journal_id.id), ('state', '=', 'draft')]
            elif payment_method_code == 'in_own_checks':
                return 'returned', domain + [('journal_id', '=', journal_id.id), ('state', '=', 'handed'), ('partner_id.commercial_partner_id', '=', self.partner_id.commercial_partner_id.id)]
        raise UserError(_(
            'This operatios is not implemented for checks:\n'
            '* Payment type: %s\n'
            '* Payment method: %s\n%s') % (
                payment_type,
                payment_method_code,
                '* Destination journal: %s\n' % destination_journal_id.name if is_internal_transfer else ''))

    @api.onchange('available_check_ids')
    def reset_check_ids(self):
        self.check_id = False

    @api.depends('payment_method_code', 'partner_id', 'check_type', 'is_internal_transfer', 'journal_id')
    def _compute_check_data(self):
        for rec in self:
            available_checks = rec.env['account.check']
            if not rec.check_type:
                rec.available_check_ids = available_checks
                continue
            operation, domain = rec._get_checks_operations()
            if domain:
                available_checks = available_checks.search(domain)
            rec.available_check_ids = available_checks

    @api.depends('payment_method_code')
    def _compute_check_type(self):
        """ Method to """
        for rec in self:
            if rec.payment_method_code in ['new_third_checks', 'out_third_checks', 'in_third_checks']:
                rec.check_type = 'third_check'
            elif rec.payment_method_code in ['new_own_checks', 'in_own_checks']:
                rec.check_type = 'own_check'
            else:
                rec.check_type = False

    @api.depends('check_id.amount', 'check_type')
    def _compute_amount(self):
        for rec in self.filtered('check_id'):
            rec.amount = rec.check_id.amount

    @api.constrains('check_id', 'select_check_ids')
    # @api.constrains('check_ids')
    def _check_checks(self):
        for rec in self:
            # we only overwrite if payment method is delivered
            if rec.payment_method_code == 'delivered_third_check':
                rec.amount = rec.check_id.amount
# +                    'El importe del pago no coincide con el importe del cheque seleccionado. Por favor intente '
# +                    'eliminar y volver a agregar el cheque.'))

                # TODO chequear esto
                # # si es una entrega de cheques de terceros y es en otra moneda
                # # a la de la cia, forzamos el importe en moneda de cia de los
                # # cheques originales
                # # escribimos force_amount_company_currency directamente en vez
                # # de amount_company_currency por lo explicado en
                # # _inverse_amount_company_currency
                # if rec.currency_id != rec.company_currency_id:
                #     rec.force_amount_company_currency = sum(
                #         rec.check_ids.mapped('amount_company_currency'))

    # def _create_paired_internal_transfer_payment(self):
    #     for rec in self:
    #         super(AccountPayment, rec.with_context(default_check_ids=rec.check_ids))._create_paired_internal_transfer_payment()

    def action_post(self):
        """ this method is called when posting an account_move of a payment or the payment directly and do two things:
        1. Do check operations (handed, delivered, etc)
        2. Split liquidity lines so that statements reconciliation and accounting analysis is suitable for checks management.
        When spliting the lines we also:
        a) modify name to be more representative
        b) add date_maturity from the check

        This split is done for now on this easy way but could be doable directly on draft states by modifying the way
        the lines are synchronized between move and payment.
        """
        res = super(AccountPayment, self).action_post()
        for rec in self.filtered('check_id'):
            if not rec.currency_id.is_zero(rec.check_id.amount - rec.amount):
                raise UserError(_(
                    'El importe del pago no coincide con el importe del cheque seleccionado. Por favor intente '
                    'eliminar y volver a agregar el cheque.'))
            # TODO check if needed
            # if rec.payment_method_code == 'own_check' and (
            #         not rec.check_number or not rec.check_name):
            #     raise UserError(_(
            #         'Para mandar a proceso de firma debe definir número '
            #         'de cheque en cada línea de pago.\n'
            #         '* ID del pago: %s') % rec.id)
            rec._do_checks_operations()
            # TODO change journal item name and fields?
            # liquidity_lines, counterpart_lines, writeoff_lines = rec._seek_for_lines()
            # rec._split_aml_line_per_check(liquidity_lines, operation)

        return res
    #         new_name % check.name
    #         document_name = _('Check %s %s') % (check.name, operation)
    #         check_vals = {
    #             'name': liquidity_lines._get_default_line_name(
    #                 document_name, check.amount, self.currency_id, self.date, partner=self.partner_id),
    #             amount_field: check.amount_company_currency,
    #             'date_maturity': check.payment_date,
    #             'amount_currency': currency and currency_sign * check.amount,
    #         }
    def _do_checks_operations(self, cancel=False):
        operation, domain = self._get_checks_operations()
        if cancel:
            self.check_id._del_operation(self.move_id)
        else:
            self.check_id._add_operation(operation, self.move_id, date=self.date)
