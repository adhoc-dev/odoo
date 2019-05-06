# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class AccountFiscalPosition(models.Model):

    _inherit = 'account.fiscal.position'

    l10n_ar_afip_code = fields.Char(
        'AFIP Code',
        help='This code will be used on electronic invoice and citi '
        'reports',
    )

    def get_fiscal_position(self, partner_id, delivery_id=None):
        PartnerObj = self.env['res.partner']
        partner = PartnerObj.browse(partner_id)
        afip_responsability = (
            partner.commercial_partner_id.l10n_ar_afip_responsability_type)
        # para nosotros fp con vat_required o no es segun responsabilidad y no
        # segun si el partner tiene seteado vat

        # if it is exento, proveedor del exterior or monotributo, when we buy
        # there are no taxes so we choose a vat_required=False position
        # (IVA Compras no corresponde)
        if afip_responsability in ['6', '4', '8']:
            # if no delivery use invoicing
            if delivery_id:
                delivery = PartnerObj.browse(delivery_id)
            else:
                delivery = partner
            fp = self._get_fpos_by_region(
                delivery.country_id.id, delivery.state_id.id, delivery.zip,
                vat_required=False)
            return fp.id if fp else False
        return super().get_fiscal_position(partner_id, delivery_id=delivery_id)
