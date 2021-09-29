from odoo import models, fields, api, _, tools


class ScrapLocationChange(models.Model):
    _inherit = "stock.scrap"

    def _onchange_product_id(self):
        print("test")
        res = super(ScrapLocationChange, self)._onchange_product_id()
        return res

