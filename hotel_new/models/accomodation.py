import datetime
from odoo import models, fields, api, _, tools
from datetime import datetime, date, timedelta

from odoo.exceptions import ValidationError


class Accomodation(models.Model):
    _name = 'hotel.accomodation'
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = 'Accomodation Management'
    _order = "check_in desc"
    _rec_name = 'room_id'

    facility_id = fields.Many2many('hotel.facility', string="Facility")
    # bed_type = fields.Selection([('single', 'Single'), ('double', 'Double'),
    #                              ('dormitory', 'Dormitory')],
    #                             string="Bed Types")
    bed_id = fields.Many2one('hotel.bed', string="Bed type")
    room_id = fields.Many2one('hotel.room', string="Room Id")
    # unit_category_id = fields.Many2one(
    #     related='room_id.unit_category_id',
    #     string="UOM Category")
    # unit_id = fields.Many2one(
    #     related='room_id.unit_id',
    #     string="UOM Category")
    room_rent = fields.Monetary(related='room_id.rent', string="Room Rent",
                                currency_field="currency_id")

    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    no_of_days = fields.Integer(string="No of Days of Stay",
                                compute='_compute_days',
                                store=True)
    rent = fields.Monetary(string="Rent",
                           compute='_compute_rent',
                           store=True, currency_field="currency_id")

    @api.depends('no_of_days', 'room_rent')
    def _compute_rent(self):
        for rec in self:
            if rec.no_of_days:
                rec.rent = rec.no_of_days * rec.room_rent
                print(rec.rent)

            else:
                rec.rent = False

    def _compute_expected_date(self):
        for rec in self:
            if rec.expected_days and rec.check_in:
                rec.expected_date = fields.Datetime.from_string(rec.check_in) \
                                    + timedelta(days=rec.expected_days)
            else:
                self.expected_date = False

    @api.onchange('bed_id')
    def onchange_bed_id(self):
        return {'domain': {'room_id': [('bed_type', '=',
                                        self.bed_id.bed_type_id),
                                       ('state', '=', 'avaliable'),
                                       ('facility_ids', '=',
                                        self.facility_id.facility)
                                       ]}}

    check_in = fields.Datetime(string="Check In Time", readonly="True")
    check_out = fields.Datetime(string="Check Out Time", readonly="True")
    expected_days = fields.Integer(string="Expected No of Days")
    expected_date = fields.Datetime(string="Expected Date",
                                    compute='_compute_expected_date',
                                    store=True)

    current_date = fields.Datetime(string="current date",
                                   default=fields.Datetime.today())

    @api.depends('expected_days', 'check_in')
    def _compute_expected_date(self):
        for rec in self:
            if rec.expected_days and rec.check_in:
                rec.expected_date = fields.Datetime.from_string(rec.check_in) \
                                    + timedelta(days=rec.expected_days)
            else:
                self.expected_date = False

    state = fields.Selection([('draft', 'Draft'), ('check_in', 'Check In'),
                              ('check_out', 'Check Out'), ('cancel', 'Cancel')],
                             default='draft')
    no_of_guest = fields.Integer(string="No of Guests")

    guest_id = fields.Many2one('res.partner', string="Guest", required=True)
    guest_line = fields.One2many('hotel.guest.line', 'guest_id',
                                 string="Guest Line")
    payment_line = fields.One2many('hotel.payment.line', 'payment_id',
                                   string="Guest Line")
    guest_count = fields.Integer(string='Count', compute='get_guest_count',
                                 default=0)
    attachment_count = fields.Integer(compute='count_attachments')
    invoice_id = fields.Many2one('account.move')

    def get_guest_count(self):
        for rec in self:
            count = 0
            for line in rec.guest_line:
                count += 1
            rec.guest_count = count

    def count_attachments(self):
        obj_attachment = self.env['ir.attachment']
        for record in self:
            record.attachment_count = 0
            attachment_ids = obj_attachment.search(
                [('res_model', '=', 'hotel.accomodation'),
                 ('res_id', '=', record.id)])
            if attachment_ids:
                record.attachment_count = len(attachment_ids)

    payment_line_ids = fields.One2many('hotel.food', 'room_no',
                                       string="Payment Line")

    def action_check_in(self):
        self.state = 'check_in'
        self.check_in = fields.datetime.now()
        # for rec in self:
        #     if rec.state == 'check_in':
        self.room_id.state = 'not_avaliable'

        if self.attachment_count == 0:
            raise ValidationError(_("Please attach your documents"))
        if self.no_of_guest != self.guest_count:
            raise ValidationError(_("Please enter all guest details"))

    def action_check_out(self):
        self.state = 'check_out'
        self.check_out = fields.datetime.now()
        self.room_id.state = 'avaliable'

    @api.depends('check_in', 'check_out')
    def _compute_days(self):
        for rec in self:
            check_in = fields.Date.to_string(rec.check_in)
            check_out = fields.Date.to_string(rec.check_out)
            if check_in and check_out:
                check_in_day = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_day = datetime.strptime(check_out, '%Y-%m-%d').date()
                if check_out_day > check_in_day:
                    rec.no_of_days = (check_out_day - check_in_day).days
                    print(rec.no_of_days)
                else:
                    rec.no_of_days = 1
                    print(rec.no_of_days)

    def action_invoice(self):
        self.ensure_one()
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.guest_id.id,
            'invoice_origin': self.accomodation_id,
            'invoice_date': self.current_date,
            'date': self.current_date,
            'invoice_line_ids': [(0, 0, {
                'name': 'Rent',
                'quantity': self.no_of_days,
                'price_unit': self.rent,


            })],
        }
        for order in self.payment_line:
            invoice_line_vals = {
                'name': order.description_id,
                'quantity': order.quantity,
                'price_unit': order.price,

            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'target': 'current',
            'action': 'Invoice_action',
        }

    def action_cancel(self):
        self.state = 'cancel'
        self.room_id.state = 'avaliable'

    accomodation_id = fields.Char(string='Accomodation Order', required=True,
                                  copy=False, readonly=True,
                                  default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('accomodation_id', _('New')) == _('New'):
            vals['accomodation_id'] = self.env['ir.sequence'].next_by_code(
                'hotel.accomodation') or _('New')
        res = super(Accomodation, self).create(vals)
        return res


class Guest(models.Model):
    _name = 'hotel.guest.line'
    _description = 'Guest Line'
    guest_name = fields.Char(string="Guest Name")
    guest_gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                                    string="Gender")
    guest_age = fields.Integer(string="Age")
    guest_id = fields.Many2one('hotel.accomodation', string="Accomodation ID")


class Payment(models.Model):
    _name = 'hotel.payment.line'
    _description = 'Payment Line'

    product_id = fields.Many2one('hotel.food.item', string="product")
    description_id = fields.Char(related="product_id.description",
                                 string="Description")
    quantity = fields.Integer(string="Quantity")
    uom = fields.Char(string="UOM", default='unit')
    unit = fields.Char(string="Unit", default='unit')
    unit_category_id = fields.Many2one(
        related='product_id.unit_category_id',
        string="Unit of measure category")
    unit_id = fields.Many2one(
        related='product_id.unit_id',
        string="Unit of Measure")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    price = fields.Monetary(related='product_id.price',
                            currency_field="currency_id",
                            string="Price")
    sub_total = fields.Monetary(default="0", string="Sub Total",
                                currency_field="currency_id")
    food_id = fields.Many2one('hotel.food', string="Food ID")
    payment_id = fields.Many2one('hotel.accomodation', string="Accomodation ID")
