from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class TolerancePercentage(models.Model):
    _inherit = "res.partner"

    tolerance = fields.Float(string='Tolerance (%)', digits='Tolerance')


class SaleLineTolerance(models.Model):
    _inherit = "sale.order.line"

    tolerance_val = fields.Float(string='Tolerance (%)')

    @api.onchange('tolerance_val')
    @api.depends('tolerance_val')
    def _compute_tolerance(self):
        for rec in self:
            if rec.tolerance_val:
                customer = self.env['res.partner'].search(
                    [('id', '=', rec.order_partner_id.id)])
                for i in customer:
                    i.write({'tolerance': rec.tolerance_val})
            else:
                rec.tolerance_val = False


class SaleTolerance(models.Model):
    _inherit = "sale.order"

    @api.onchange('order_line')
    def onchange_order_line(self):
        for rec in self.order_line:
            rec.tolerance_val = self.partner_id.tolerance
            print(rec.tolerance_val)


class DeliveryValidate(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):

        picking_id = self.picking_type_id
        if picking_id.id == 2:
            tolerance_val = self.partner_id.tolerance
            print(self.partner_id)
            print(tolerance_val)
            for rec in self.move_line_ids_without_package:
                reserved_val = rec.product_uom_qty
                print(reserved_val)
                done_val = rec.qty_done
                print(done_val)
                start_val = reserved_val - tolerance_val
                if start_val < 0:
                    start_val = -1 * start_val
                end_val = reserved_val + tolerance_val
                if (done_val >= start_val) and (done_val <= end_val):
                    continue

                else:
                    print('else')
                    return {'type': 'ir.actions.act_window',
                            'res_model': 'validate.tolerance.wizard',
                            'view_mode': 'form',
                            'target': 'new'}
            res = super(DeliveryValidate, self).button_validate()
            return res

        elif picking_id.id == 1:
            origin_id = self.origin
            po_id = self.env['purchase.order'].search(
                [('name', '=', origin_id)])
            so_name = po_id.origin
            so_id = self.env['sale.order'].search(
                [('name', '=', so_name)])
            cust_id = so_id.partner_id
            tolerance_val = cust_id.tolerance
            print(tolerance_val)
            for rec in self.move_ids_without_package:
                reserved_val = rec.product_uom_qty
                print(reserved_val)
                done_val = rec.quantity_done
                print(done_val)
                start_val = reserved_val - tolerance_val
                if start_val < 0:
                    start_val = -1 * start_val
                end_val = reserved_val + tolerance_val
                if (done_val >= start_val) and (done_val <= end_val):
                    continue

                else:
                    print('else')
                    return {'type': 'ir.actions.act_window',
                            'res_model': 'validate.tolerance.wizard',
                            'view_mode': 'form',
                            'target': 'new'}
            res = super(DeliveryValidate, self).button_validate()
            return res
