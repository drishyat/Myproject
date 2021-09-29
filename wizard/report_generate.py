# -*- coding: utf-8 -*-

from odoo import api, fields, models


class GenerateReport(models.TransientModel):
    _name = 'hotel.generate.report.wizard'
    _description = 'Generate Report'

    guest_id = fields.Many2one('res.partner', string="Guest")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    # accomodation_seq = fields.Char(string="Accomddation seq")

    def generate(self):
        domain = []
        guest_id = self.guest_id
        from_date = self.from_date
        to_date = self.to_date
        print(to_date)
        query = 'SELECT acc.accomodation_id,acc.check_in,acc.check_out,' \
                'res.name,num.room_no  FROM hotel_accomodation acc INNER JOIN ' \
                'res_partner res ON (acc.guest_id = res.id) ' \
                'INNER JOIN hotel_number num ON acc.room_id = num.id'
        if guest_id and from_date and to_date:
            query = query + "where guest_id = '%d'and check_in>'%s' and " \
                            "check_out <'%s'" % (guest_id, from_date, to_date)
        elif guest_id and from_date:
            query = query + " where guest_id = '%d' and check_in>'%s'" % (
                guest_id, from_date)
        elif guest_id and to_date:
            query = query + " where guest_id = '%s' and check_out<'%s'" % (
                to_date)
        elif from_date and to_date:
            query = query + " where check_in >'%s' and check_out<'%s'" % (
                from_date, to_date)
        elif from_date:
            query = query + " where check_in>'%s'" % (from_date)
        elif to_date:
            query = query + " where check_out<'%s'" % (to_date)
        elif guest_id:
            query = query + " where guest_id ='%d'" % (guest_id)

        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()
        print(record)
        data = {
            'form_data': self.read()[0],
            'data': record
        }
        return self.env.ref('hotel_demo.generate_report').report_action(
            self, data=data)
