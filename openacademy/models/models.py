# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'
#     _description = 'openacademy.openacademy'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from odoo import models, fields, api, _


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'openacademy courses'
    name = fields.Char(string="title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users',ondelete='cascade',
                                     string='Responsible',index=True)
    session_ids= fields.One2many('openacademy.session', 'course_id',
                                 string="sessions")


class Session(models.Model):
    _name = 'openacademy.session'
    _description = 'openacademy sessions'
    name = fields.Char(required=True)
    date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Enter duration of session")
    seats = fields.Integer(string="no of seats")
    instuctor_id = fields.Many2one('res.partner', string="Instructor", required=True)

    course_id = fields.Many2one('openacademy.course', required=True, ondelete='cascade')
    trial_field=fields.Char()
    attendee_id = fields.Many2many('res.partner', string="Attendance")
