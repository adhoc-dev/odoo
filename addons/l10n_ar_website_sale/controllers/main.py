# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request, route
from odoo.exceptions import ValidationError


class L10nARWebsiteSale(WebsiteSale):

    def _get_mandatory_billing_fields(self):
        """Extend mandatory fields to add new identification and responsibility fields when company is argentina"""
        res = super()._get_mandatory_billing_fields()
        if request.website.sudo().company_id.country_id == request.env.ref('base.ar'):
            res += ["l10n_latam_identification_type_id", "l10n_ar_afip_responsibility_type_id", "vat"]
        return res

    @route()
    def address(self, **kw):
        """Extend to send information about the identification types and AFIP responsibility to show in the address form"""
        response = super().address(**kw)
        if request.website.sudo().company_id.country_id == request.env.ref('base.ar'):
            response.qcontext.update({'identification_types': request.env['l10n_latam.identification.type'].sudo().search([]),
                                      'responsibility_types': request.env['l10n_ar.afip.responsibility.type'].sudo().search([]),
                                      'identification': kw.get('l10n_latam_identification_type_id'),
                                      'responsibility': kw.get('l10n_ar_afip_responsibility_type_id')})
        return response

    def _get_vat_validation_fields(self, data):
        res = super()._get_vat_validation_fields(data)
        if request.website.sudo().company_id.country_id == request.env.ref('base.ar'):
            res.update({'l10n_latam_identification_type_id': int(data['l10n_latam_identification_type_id'])
                                                             if data.get('l10n_latam_identification_type_id') else False})
        return res
