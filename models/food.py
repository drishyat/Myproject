import base64

from odoo import models, fields, api, _, tools
from datetime import datetime, date
from odoo.modules.module import get_module_resource


class Food(models.Model):
    _name = 'hotel.food'
    _description = 'Food Management'
    _rec_name = 'room_no'

    room_id = fields.Many2one('hotel.room', string="Room Number",
                              domain="[('state', '=', 'not_avaliable')]")


    @api.depends('room_id')
    def compute_room(self):
        lst = []
        acc = False
        for rec in self.room_id:
            print(lst)
            lst.append(rec.room_number_id.id)
            print('lst', lst)
            acc = self.env['hotel.accomodation'].search([('state',
                                                          '=', 'check_in'),
                                                         (
                                                             'room_id.room_number_id',
                                                             'in',
                                                             lst)
                                                         ])
            print(acc)
        self.acc_id = acc
        return acc

    acc_id = fields.Many2one("hotel.accomodation", string="Room Number",
                             compute=compute_room, store=True)
    print(acc_id)
    guest_name = fields.Many2one(related='acc_id.guest_id',
                                 string="Guest Name", store=True)
    print(guest_name)
    room_no = fields.Many2one(related='acc_id.room_id',
                              string="Guest Name", store=True)
    print(room_no)
    order_time = fields.Datetime(string="Order Time", readonly="True",
                                 default=fields.datetime.now())
    product_id = fields.Many2one("hotel.category", string="Food Category")
    food_line_ids = fields.One2many('hotel.order', 'food_list_id',
                                    string="Food Line")
    order_line_ids = fields.One2many('hotel.order.line', 'order_list_id',
                                     string="Order Line")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        print(self.acc_id)
        print(self.guest_name)
        print(self.room_no.id)
        for rec in self:
            lines = []
            for line in self.product_id.food_list_ids:
                vals = {
                    'product_id': line.id
                }
                lines.append((0, 0, vals))
            rec.food_line_ids = lines


class ProductCategory(models.Model):
    _name = 'hotel.category'
    _description = 'Food Management'
    _rec_name = 'category_name'

    category_name = fields.Char(string="Category Name")
    food_list_ids = fields.One2many('hotel.food.item', 'category_list_id')


class FoodProduct(models.Model):
    _name = 'hotel.food.item'
    _description = 'Food Item'
    _inherit = 'image.mixin'
    _rec_name = "food_name"

    food_name = fields.Char(string="Food Name", required=True)
    category_list_id = fields.Many2one("hotel.category", string="Food Category")
    description = fields.Char(string="Description")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    price = fields.Monetary(string="Price", currency_field='currency_id',
                            required=True)
    image = fields.Binary(string="Food Image", attachment=True)

    food_id = fields.Many2one('hotel.food', string="Food ID")
    unit_category_id = fields.Many2one('hotel.unit.category',
                                       string="UOM Category")
    unit_id = fields.Many2one('hotel.unit',
                              string="Unit of Measure")


class OrderLine(models.Model):
    _name = 'hotel.order'
    _description = 'Food Item'
    _rec_name = "product_id"

    product_id = fields.Many2one('hotel.food.item', string="product")
    description_id = fields.Char(related="product_id.description",
                                 string="Description")
    food_category = fields.Many2one(related='product_id.category_list_id',
                                    string="category")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    food_price = fields.Monetary(related='product_id.price',
                                 currency_field="currency_id", string="price")
    image = fields.Image(related='product_id.image', string="image")
    food_list_id = fields.Many2one('hotel.food', string="Food ID")
    room_id = fields.Many2one(related='food_list_id.room_no', string="Room")
    quantity = fields.Integer(string="Quantity")
    unit_category_id = fields.Many2one(
        related='product_id.unit_category_id',
        string="Unit of measure category")
    unit_id = fields.Many2one(
        related='product_id.unit_id',
        string="Unit of Measure")

    def action_add_product(self, line=None):
        # return True
        line = self.env['hotel.order.line'].create(
            {
                'order_product_id': self.product_id.id,
                'description_id': self.description_id,
                'order_quantity': self.quantity,
                'order_food_price': self.food_price,
                'sub_total': self.quantity * self.food_price,
                'order_unit_category_id': self.unit_category_id,
                'order_unit_id': self.unit_id,
                'order_list_id': self.food_list_id.id,

            }
        )
        rec = self.env['hotel.payment.line'].create(
            {
                'product_id': self.product_id.id,
                'description_id': self.description_id,
                'quantity': self.quantity,
                'price': self.food_price,
                'sub_total': self.quantity * self.food_price,
                'food_id': self.food_list_id.id,
                'unit_category_id': self.unit_category_id,
                'unit_id': self.unit_id,
                'payment_id': self.food_list_id.id,

            }
        )


class OrderList(models.Model):
    _name = 'hotel.order.line'
    _description = 'order line'

    order_product_id = fields.Many2one('hotel.food.item', string="Product")
    description_id = fields.Char(related="order_product_id.description",
                                 string="Description")
    order_unit_category_id = fields.Many2one(
        related='order_product_id.unit_category_id',
        string="Unit of measure category")
    order_unit_id = fields.Many2one(
        related='order_product_id.unit_id',
        string="Unit of Measure")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    order_food_price = fields.Monetary(related='order_product_id.price',
                                       currency_field="currency_id",
                                       string="Price")
    order_quantity = fields.Integer(string="Quantity")
    sub_total = fields.Monetary(default="0", string="Sub Total",
                                currency_field="currency_id")
    order_list_id = fields.Many2one('hotel.food', string="Order ID")


class Unit(models.Model):
    _name = 'hotel.unit'
    _description = 'unit of measure'
    _rec_name = 'unit'

    unit = fields.Char(string="Unit of Measure")
    unit_category_id = fields.Many2one('hotel.unit.category',
                                       string="Unit of Measure Category")


class UnitCategory(models.Model):
    _name = 'hotel.unit.category'
    _description = 'unit of measure category'
    _rec_name = 'unit_of_measure'

    unit_of_measure = fields.Char(string="Unit of Measure Category")
