# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import models
from . import wizards
from . import report
from .hooks import post_init_hook

from odoo import SUPERUSER_ID

# TODO review if we really need this (take from old l10n_ar_chart)
def load_translations(cr, registry):
    chart_template = registry['ir.model.data'].xmlid_to_object(
        cr, SUPERUSER_ID, 'l10n_be.l10nbe_chart_template')
    chart_template.process_coa_translations()
