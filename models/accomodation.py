import datetime
from odoo import models, fields, api, _, tools
from datetime import datetime, date, timedelta

from odoo.exceptions import ValidationError


class Accomodation(models.Model):
    _name = 'hotel.accomodation'
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = 'Accomodation Management'
    _rec_name = 'accomodation_id'

    bed_id = fields.Many2one('hotel.bed', string="Bed type")
    room_id = fields.Many2one('hotel.room', string="Room Id")

    @api.onchange('bed_id')
    def onchange_bed_id(self):
        return {'domain': {'room_id': [('bed_type', '=',
                                        self.bed_id.bed_type_id)]}}

    facility_id = fields.Many2many('hotel.facility', string="Facility")

    # @api.onchange('facility_id')
    # def onchange_facility_id(self):
    #     return {'domain': {'room_id': [('bed_type', '=',
    #                                     self.bed_id.bed_type_id)]}}
    check_in = fields.Datetime(string="Check In Time", readonly="True",
                               default=fields.datetime.now())
    check_out = fields.Datetime(string="Check Out Time", readonly="True")
    expected_days = fields.Integer(string="Expected No of Days", default=0)
    expected_date = fields.Datetime(string="Expected Date",
                                    compute='_compute_expected_date')

    @api.depends('expected_days', 'check_in')
    def _compute_expected_date(self):
        self.expected_date = fields.Datetime.from_string(
            self.check_in) + timedelta(days=self.expected_days)

    state = fields.Selection([('draft', 'Draft'), ('check_in', 'Check In'),
                              ('check_out', 'Check Out'), ('cancel', 'Cancel')],
                             default='draft')
    no_of_guest = fields.Integer(string="No of Guests")

    guest_id = fields.Many2one('res.partner', string="Guest", required=True)
    guest_line = fields.One2many('hotel.guest.line', 'guest_id',
                                 string="Guest Line")
    guest_count = fields.Integer(string='Count', compute='get_guest_count',
                                 default=0)
    attachment_count = fields.Integer(compute='count_attachments')

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

    def action_check_in(self):
        self.state = 'check_in'
        self.check_in = fields.datetime.now()

        if self.attachment_count == 0:
            raise ValidationError(_("Please attach your documents"))
        if self.no_of_guest != self.guest_count:
            raise ValidationError(_("Please enter all guest details"))

    def action_check_out(self):
        self.state = 'check_out'
        self.check_out = fields.datetime.now()

    def action_cancel(self):
        self.state = 'cancel'

    accomodation_id = fields.Char(string='Accomodation Order', required=True,
                                  copy=False, readonly=True,
                                  default=lambda self: _('New'))
    note = fields.Text(string="description")

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New Accomodation'
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
