# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class AccountFiscalPosition(models.Model):

    _inherit = 'account.fiscal.position'

    l10n_ar_afip_code = fields.Char(
        'AFIP Code',
        help='For eg. This code will be used on electronic invoice and citi '
        'reports',
    )
    # TODO tal vez podriamos usar funcionalidad nativa con "vat subjected"

    """
    # TODO borrar si no lo usamos, por ahora lo resolivmos de manera nativa
    # TODO ver que hacer con esto no va a funcionar
    afip_responsability_type_ids

    id='fiscal_position_template_iva_no_corresponde' [(6, False, [ref('l10n_ar.res_RM'), ref('l10n_ar.res_IVAE'), ref('l10n_ar.res_CLI_EXT'), ref('l10n_ar.res_EXT')])]

    id='fiscal_position_template_zona_franca' [(6, False, [ref('l10n_ar.res_IVA_LIB')])]"

    id='fiscal_position_template_exportaciones_al_exterior' [(6, False, [ref('l10n_ar.res_CLI_EXT')])]

    <field name="vat_required" position="replace">
        <field name="afip_responsability_type_ids" widget="many2many_tags" attrs="{'invisible': [('auto_apply', '!=', True)]}"/>
    </field>
    """

    @api.model
    def _get_fpos_by_region_and_responsability(
            self, country_id=False, state_id=False,
            zipcode=False, afip_responsability_type=False):
        """ We use similar code than _get_fpos_by_region but we use
        "afip_responsability_type" insted of vat_required
        """

        base_domain = [
            ('auto_apply', '=', True),
            ('afip_responsability_type', '=', afip_responsability_type)
        ]

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

    @api.model
    def get_fiscal_position(self, partner_id, delivery_id=None):
        """
        We overwrite original functionality and replace vat_required logic
        for afip_responsability_type_ids
        """
        # we need to overwrite code (between #####) from original function
        #####
        if not partner_id:
            return False
        # This can be easily overriden to apply more complex fiscal rules
        PartnerObj = self.env['res.partner']
        partner = PartnerObj.browse(partner_id)

        # if no delivery use invoicing
        if delivery_id:
            delivery = PartnerObj.browse(delivery_id)
        else:
            delivery = partner

        # partner manually set fiscal position always win
        if (
                delivery.property_account_position_id or
                partner.property_account_position_id):
            return (
                delivery.property_account_position_id.id or
                partner.property_account_position_id.id)
        #####

        afip_responsability = (
            partner.commercial_partner_id.afip_responsability_type)

        # First search only matching responsability positions
        fpos = self._get_fpos_by_region_and_responsability(
            delivery.country_id.id, delivery.state_id.id, delivery.zip,
            afip_responsability)
        if not fpos and afip_responsability:
            fpos = self._get_fpos_by_region_and_responsability(
                delivery.country_id.id, delivery.state_id.id, delivery.zip,
                False)

        return fpos.id if fpos else False
