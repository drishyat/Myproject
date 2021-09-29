from odoo import models, fields, api


class ValidateToleranceWiz(models.TransientModel):
    _name = 'validate.tolerance.wizard'
    _description = "Validate Tolerance Wizard"

    # _inherit = "stock.picking"

    def accept(self):
        return True
