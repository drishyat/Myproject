import time
import json
import datetime
import io
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ExcelWizard(models.TransientModel):
    _name = "xlsx.report.wizard"

    guest_id = fields.Many2one('res.partner', string="Guest")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")

    def print_xlsx(self):
        # if self.start_date > self.end_date:
        #     raise ValidationError('Start Date must be less than End Date')
        data = {
            'start_date': self.from_date,
            'end_date': self.to_date,
            'guest_id': self.guest_id
        }
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
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'xlsx.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    user_obj = self.env.user
    sheet = workbook.add_worksheet('Accomodation XLS')
    heading = workbook.add_format(
        {'font_size': 20, 'align': 'center', 'bold': True})
    format = workbook.add_format(
        {'font_size': 10, 'align': 'left'})
    format1 = workbook.add_format(
        {'font_size': 10, 'align': 'left', 'bold': True})
    sheet.merge_range('A1:C1', user_obj.company_id.name, format)
    sheet.merge_range('A2:C2', user_obj.company_id.street, format)
    sheet.merge_range('A3:C3', user_obj.company_id.city, format)
    sheet.write('B3', user_obj.company_id.zip, format)
    sheet.merge_range('A4:C4', user_obj.company_id.state_id.name,
                      format)
    sheet.merge_range('A5:C5', user_obj.company_id.country_id.name,
                      format)
    sheet.merge_range('C7:I8', 'SL No', heading)
    sheet.write('B9', 'From', format)
    sheet.merge_range('C9:D9', 'start_date', format)
    sheet.write('F11', 'To', format)
    sheet.merge_range('G11:H11', 'end_date', format)
    sheet.merge_range('B13:C13', 'Guest_id', format1)
    sheet.merge_range('D13:E13', "Room No", format1)
    row = 14
    for rec in data['data']:
        sheet.write('B' + str(row), rec[''])
        sheet.write('B' + str(row), rec['accomodation_id'])
        sheet.write('D' + str(row), rec['check_in'])
        sheet.write('F' + str(row), rec['check_out'])
        sheet.write('F' + str(row), rec['name'])
        sheet.write('F' + str(row), rec['room_no'])

        row += 1
    row += 1
    sheet.merge_range(row, 0, row, 1,
                      user_obj.company_id.phone, format)
    sheet.merge_range(row, 2, row, 4,
                      user_obj.company_id.email, format)
    sheet.merge_range(row, 5, row, 7,
                      user_obj.company_id.website, format)
    workbook.close()
    output.seek(0)
    response.stream.write(output.read())
    output.close()