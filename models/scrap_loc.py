from odoo import models, fields, api, _, tools



class ScrapLocationChange(models.Model):
    _inherit = "stock.scrap"

    @api.onchange('product_id')
    def _onchange_product_id(self):

        temp = self.env['stock.putaway.rule']. \
            search([('product_id.name', '=',
                     self.product_id.name)
                    ]).location_out_id
        if temp:
            loc_id = ''
            lst = []
            for i in temp:
                lst.append(i.id)
                loc_id = i

            if self.product_id:
                self.location_id = loc_id
        res = super(ScrapLocationChange, self)._onchange_product_id()
        return res

