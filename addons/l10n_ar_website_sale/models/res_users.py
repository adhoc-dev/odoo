from odoo import models, api
from odoo.addons.base.models.res_users import name_selection_groups


class ResUsers(models.Model):

    _inherit = 'res.users'

    def _l10n_ar_is_portal_public(self):
        """ Return True of False if the user is a portal or public user and belongs to an Argentinian Company """
        self.ensure_one()
        if (self.has_group('base.group_portal') or self._is_public()) and \
           self.company_id.filtered(lambda x: x.country_id == self.env.ref('base.ar')):
            return True
        return False

    def is_user_type(self):
        """ Let us know the name of the sel_groups related to the modification of the user/type
        this is: internal / portal / public """
        internal = self.env.ref('base.group_user')
        portal = self.env.ref('base.group_portal')
        public = self.env.ref('base.group_public')
        return name_selection_groups([internal.id, portal.id, public.id])

    def write(self, values):
        """ If user type has been change then update the user tax group """
        res = super().write(values)
        if self.is_user_type() in values:
            self._l10n_ar_update_portal_public_user_tax_group()
        return res

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        """ When copy public and portal users from argentinian company avoid error of have both tax groups that is auto
        compute by odoo with the implied groups when duplicating the user """
        default = default or {}
        if self._l10n_ar_is_portal_public() or self.env.ref('base.public_user'):
            new_groups = self.groups_id
            new_groups -= self.env.ref('account.group_show_line_subtotals_tax_included')
            new_groups -= self.env.ref('account.group_show_line_subtotals_tax_excluded')
            if new_groups:
                default.update({'groups_id': [(6, 0, new_groups.ids)]})
        return super().copy(default=default)

    @api.model
    def create(self, values):
        """ when a user is created re compute the tax groups """
        res = super().create(values)
        res._l10n_ar_update_portal_public_user_tax_group()
        return res

    def _l10n_ar_update_portal_public_user_tax_group(self):
        """ Will move the user to the correspond tax group depending of the configuration defined in the global settings
        NOTE: This will only applies to portal and public users for argentinian companies """
        portal_and_public_users = self.filtered(lambda x: x._l10n_ar_is_portal_public())

        tax_included = self.env.ref('account.group_show_line_subtotals_tax_included')
        tax_excluded = self.env.ref('account.group_show_line_subtotals_tax_excluded')
        company_tax_config = self.env['ir.config_parameter'].sudo().get_param(
            'l10n_ar_website_sale.l10n_ar_tax_groups') or 'tax_included'

        for user in portal_and_public_users:
            b2c = user.l10n_ar_afip_responsibility_type_id == self.env.ref('l10n_ar.res_CF') \
                if user.l10n_ar_afip_responsibility_type_id else company_tax_config in ['responsibility_type_b2c', 'tax_included']

            # clean up all the groups for the user
            tax_included.users -= user
            tax_excluded.users -= user

            if company_tax_config == 'tax_included' or ('responsibility_type' in company_tax_config and b2c):
                tax_included.users |= user
            else:
                tax_excluded.users |= user
