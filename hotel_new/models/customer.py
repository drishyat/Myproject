from odoo import models, fields, api


class TolerancePercentage(models.Model):
    _inherit = "res.partner"

    # customer_tolerance = fields.Integer(string="Tolerance Percentage")


# class SaleOrderTolerance(models.Model):
#     _inherit = "sale.order"
#
#     tolerance = fields.Integer()
