from odoo import _, fields, models


class ResCurrency(models.Model):

    _inherit = "res.currency"

    l10n_uy_bcu_code = fields.Integer('Código BCU', help='Este codigo idenfica cada moneda y permite extraer el valor de la tasa del Banco Central Uruguayo')
