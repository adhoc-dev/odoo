from odoo import models, fields, api


class ResCompany(models.Model):

    _inherit = 'res.company'

    l10n_ar_id_category_id = fields.Many2one(
        related='partner_id.l10n_ar_id_category_id',
    )
    l10n_ar_id_number = fields.Char(
        related='partner_id.l10n_ar_id_number',
    )
    l10n_ar_cuit = fields.Char(
        related='partner_id.l10n_ar_cuit'
    )

    @api.multi
    def cuit_required(self):
        return self.partner_id.cuit_required()

    @api.model
    def create(self, vals):
        """
        On create, we set id number to partner
        """
        company = super(ResCompany, self).create(vals)
        company.change_main_id_category()
        l10n_ar_id_number = vals.get('l10n_ar_id_number')
        if l10n_ar_id_number:
            company.partner_id.l10n_ar_id_number = l10n_ar_id_number
        return company

    @api.onchange('l10n_ar_id_category_id')
    def change_main_id_category(self):
        # we force change on partner to get updated number
        if self.partner_id:
            self.partner_id.l10n_ar_id_category_id = self.l10n_ar_id_category_id
            self.l10n_ar_id_number = self.partner_id.l10n_ar_id_number
