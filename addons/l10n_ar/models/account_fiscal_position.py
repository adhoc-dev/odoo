# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class AccountFiscalPosition(models.Model):

    _inherit = 'account.fiscal.position'

    l10n_ar_afip_code = fields.Char(
        'AFIP Code',
        help='This code will be used on electronic invoice and citi '
        'reports',
    )

    @api.model
    def _get_fpos_by_region_and_responsability(
            self, country_id=False, state_id=False,
            zipcode=False, afip_responsability_type=False):
        """ We use similar code than _get_fpos_by_region but we use
        "afip_responsability_type" insted of vat_required
        """
        base_domain = [
            ('auto_apply', '=', True),
        ]
        resp_code = {
            '9': ['|', ('l10n_ar_afip_code', 'in', 'X'),
                ('l10n_ar_afip_code', '=', False)],
            '10': [('l10n_ar_afip_code', '=', 'Z')],
            '6': [('l10n_ar_afip_code', '=', False)],
            '4': [('l10n_ar_afip_code', '=', False)],
            '8': [('l10n_ar_afip_code', '=', False)],
        }
        code_domain = resp_code.get(afip_responsability_type, [])
        base_domain.extend(code_domain)

        if self.env.context.get('force_company'):
            base_domain.append(
                ('company_id', '=', self.env.context.get('force_company')))

        null_state_dom = state_domain = [('state_ids', '=', False)]
        null_zip_dom = zip_domain = [
            ('zip_from', '=', 0), ('zip_to', '=', 0)]
        null_country_dom = [
            ('country_id', '=', False), ('country_group_id', '=', False)]

        if zipcode and zipcode.isdigit():
            zipcode = int(zipcode)
            zip_domain = [
                ('zip_from', '<=', zipcode), ('zip_to', '>=', zipcode)]
        else:
            zipcode = 0

        if state_id:
            state_domain = [('state_ids', '=', state_id)]

        domain_country = base_domain + [('country_id', '=', country_id)]
        domain_group = base_domain + [
            ('country_group_id.country_ids', '=', country_id)]

        # Build domain to search records with exact matching criteria
        fpos = self.search(
            domain_country + state_domain + zip_domain, limit=1)

        # return records that fit the most the criteria, and fallback on less
        # specific fiscal positions if any can be found
        if not fpos and state_id:
            fpos = self.search(
                domain_country + null_state_dom + zip_domain, limit=1)
        if not fpos and zipcode:
            fpos = self.search(
                domain_country + state_domain + null_zip_dom, limit=1)
        if not fpos and state_id and zipcode:
            fpos = self.search(
                domain_country + null_state_dom + null_zip_dom, limit=1)

        # fallback: country group with no state/zip range
        if not fpos:
            fpos = self.search(
                domain_group + null_state_dom + null_zip_dom, limit=1)

        if not fpos:
            # Fallback on catchall (no country, no group)
            fpos = self.search(
                base_domain + null_country_dom, limit=1)
        return fpos or False

    # We overwrite original Odoo methods in order ro replace vat_required logic
    # for afip_responsability_type
    @api.model
    def get_fiscal_position(self, partner_id, delivery_id=None):
        if not partner_id:
            return False
        # This can be easily overridden to apply more complex fiscal rules
        PartnerObj = self.env['res.partner']
        partner = PartnerObj.browse(partner_id)

        # if no delivery use invoicing
        if delivery_id:
            delivery = PartnerObj.browse(delivery_id)
        else:
            delivery = partner

        # partner manually set fiscal position always win
        if delivery.property_account_position_id or  partner.property_account_position_id:
            return delivery.property_account_position_id.id or partner.property_account_position_id.id

        ##### COMMENTED ORIGINAL CODE
        """
        # First search only matching VAT positions
        vat_required = bool(partner.vat)

        fp = self._get_fpos_by_region(delivery.country_id.id, delivery.state_id.id, delivery.zip, vat_required)

        # Then if VAT required found no match, try positions that do not require it
        if not fp and vat_required:
            fp = self._get_fpos_by_region(delivery.country_id.id, delivery.state_id.id, delivery.zip, False)

        return fp.id if fp else False
        """
        ##### INIT NEW CODE
        afip_responsability = (
            partner.commercial_partner_id.l10n_ar_afip_responsability_type)

        # First search only matching responsability positions
        fpos = self._get_fpos_by_region_and_responsability(
            delivery.country_id.id, delivery.state_id.id, delivery.zip,
            afip_responsability)
        if not fpos and afip_responsability:
            fpos = self._get_fpos_by_region_and_responsability(
                delivery.country_id.id, delivery.state_id.id, delivery.zip,
                False)

        return fpos.id if fpos else False
        ##### END NEW CODE
