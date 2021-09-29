from odoo import models, fields, api, _, tools


class ScrapLocationChange(models.Model):
    _inherit = "stock.scrap"

    @api.onchange('product_id')
    def change_location_id(self):
        temp = self.env['stock.quant'].\
            search([('product_id.name','=',
                     self.product_id.name),('quantity','>',0)]).location_id
        loc_id = ''
        list = []
        for i in temp:
            list.append(i.id)
            loc_id = i
        # print(list)
            if self.product_id:
                self.location_id = loc_id
        #
        # return {
        #     'domain': {
        #         'location_id':[('id', 'in', list)]
        #     }
        # }
