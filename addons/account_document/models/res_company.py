##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_latam_use_documents = fields.Boolean(
        '_compute_l10n_latam_use_documents',
    )
    def _compute_l10n_latam_use_documents(self):
        for rec in self:
            rec.l10n_latam_use_documents = \
                rec.company_id._localization_use_documents()

    def _localization_use_documents(self):
        """ This method is to be inherited by localizations and return
        True if localization use documents
        """
        self.ensure_one()
        return False
