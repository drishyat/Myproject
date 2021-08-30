from odoo import models, fields, api, _


class Room(models.Model):
    _name = 'hotel.room'
    _description = 'Room Management'
    _rec_name = 'room_number_id'

    room_number_id = fields.Many2one('hotel.number', string="Room Numbers")
    # bed_type = fields.Many2one('hotel.bed',string="Bed type")

    bed_type = fields.Selection([('single', 'Single'), ('double', 'Double'),
                                 ('dormitory', 'Dormitory')],
                                string="Bed Types")
    # trial= fields.Selection([('a','A'),('b','B')],string="trial")
    avaliable_bed = fields.Integer()
    facility_ids = fields.Many2many('hotel.facility', string="Facility")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda
                                     self: self.env.user.company_id.id, index=1)
    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id,
                                  required=True)

    rent = fields.Monetary(string="Room Rent", currency_field='currency_id')


class Facility(models.Model):
    _name = 'hotel.facility'
    _description = 'Facility Management'
    _rec_name = 'facility'

    facility = fields.Char()


class RoomNo(models.Model):
    _name = 'hotel.number'
    _description = 'Room Number Management'
    _rec_name = 'room_no'

    room_no = fields.Char("Enter room number")
    # bed_type = fields.Many2one('hotel.room', string="bed type")


class BedType(models.Model):
    _name = 'hotel.bed'
    _description = 'Bed Type Management'
    _rec_name = 'bed_type_id'

    bed_type_id = fields.Char("Enter bed_type")
